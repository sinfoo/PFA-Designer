"""Report linter. Usage: python lint_report.py <report_dir> [--max-pages N] [--json] [--facts-diff <before_dir>]
Checks: placeholders, empty sections, unreferenced figures/tables, citations vs bib, cliché/AI-tell phrases, repeated openers and flat rhythm
(per file), decorative/title-case headings, French typography slips, page count. Exit 1 if any ERROR.
--facts-diff: compare against a pre-humanizing snapshot; numbers/URLs/citations added by the rewrite are ERRORs, new names and lost facts WARN.
--json: machine-readable output (pages, errors, warnings, tells_by_file)."""
import json, re, sys
from pathlib import Path

def plain_of(clean):
    return re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?", " ", clean).lower().replace("’", "'")

def read_tex(d):
    """{path: text without comments} for the report's own .tex files (no preamble/cover/meta)."""
    return {p: re.sub(r"(?m)(?<!\\)%.*$", "", p.read_text(encoding="utf-8", errors="ignore"))
            for p in Path(d).rglob("*.tex") if p.name not in ("preamble.tex", "cover.tex", "meta.tex")}

def facts(d):
    t = "\n".join(read_tex(d).values())
    cites = {k.strip() for g in re.findall(r"\\(?:auto|text|paren)?cite\w*\{([^}]+)\}", t) for k in g.split(",")}
    urls = set(re.findall(r"https?://[^\s}]+", t))
    t = re.sub(r"\\(?:label|[cC]?ref|includegraphics|input|include|cite\w*|url|href)(\[[^\]]*\])?\{[^}]*\}", " ", t)
    nums = {re.sub(r"\s", "", n) for n in re.findall(r"\d+(?:[.,]\d+)*\s?%?", t)}
    names = set(re.findall(r"(?<=[a-zà-ÿ,;(]\s)[A-ZÉÈ][\wéèêàç]{2,}", t))
    return {"nombre": nums, "citation": cites, "URL": urls, "nom propre": names}

def facts_diff(before, after, err, warn):
    b, a = facts(before), facts(after)
    for kind in b:
        for x in sorted(a[kind] - b[kind]):
            (warn if kind == "nom propre" else err).append(f"fait ajouté par la réécriture ({kind}) : {x}")
        for x in sorted(b[kind] - a[kind]):
            warn.append(f"fait perdu par la réécriture ({kind}) : {x}")

CLICHES = [r"à l'ère d(u|e)", r"monde en constante", r"il est important de (noter|souligner)", r"il convient de souligner", r"force est de constater",
           r"dans le cadre de ce chapitre", r"joue un rôle (crucial|clé|essentiel)", r"tirer parti", r"cutting[- ]edge", r"seamless", r"holistique",
           r"révolutionn", r"innovant", r"robuste et", r"sincères remerciements", r"se démarque", r"témoigne de", r"en constante évolution",
           r"plongeons|dévoilons|explorons ensemble", r"\bdelve\b", r"\btapestry\b"]
# humanizer-derived French tells (see reference/humanized-writing.md §4); warnings only, never errors
STRUCT = [
    (r"non seulement .{0,80}mais (aussi|également|encore)|ne (se )?(limite|résume) pas (seulement |simplement )?à|n'est pas (seulement|simplement|uniquement) [^.]{3,60}, (c'est|mais)|il ne s'agit pas (seulement |simplement )?d[eu']", "pas X mais Y"),
    (r"cela ne signifie pas [^.]{3,80}\. cela (signifie|veut dire)", "pas X mais Y (deux phrases)"),
    (r"voyons (maintenant |ensemble )?comment|sans plus attendre|allons-y|voici ce qu'il faut savoir|plongeons", "mise en scène avant le propos"),
    (r"la (véritable|vraie) question|au c(œ|oe)ur de|fondamentalement|le nerf de la guerre", "formule qui sonne profond"),
    (r"il serait tentant de|on pourrait penser que|ne nous méprenons pas|il ne s'agit pas ici", "discuter avec personne"),
    (r"c'est là (toute )?(la|l')|cela (montre|souligne|illustre) (bien )?l'importance", "fermeture d'une ligne"),
    (r"\bcrucial|\bpivot|incontournable|met(tre|tant)? en (lumière|exergue)|s'inscrit dans une (dynamique|démarche)|paysage (numérique|technologique)|foisonn|florissant|\bvéritable\b|un atout majeur|s'avère (être )?(un|une)|l'avenir s'annonce|marque un tournant|empreinte durable", "mot gonflé / importance gonflée"),
    (r"(,|\.) (soulignant|reflétant|illustrant|garantissant|témoignant|favorisant) ", "participe présent décoratif"),
    (r"j'espère que (cela|ça)|n'hésitez pas à|excellente question|voici (un|une) (aperçu|résumé)|en tant que (modèle|ia)\b", "résidu de chatbot"),
    (r"à la date de|d'après les informations disponibles|selon les informations disponibles|à ma connaissance", "limite de connaissance"),
    (r"selon (les|de nombreux) (experts|spécialistes|études)|de nombreuses études (montrent|prouvent)", "autorité empruntée sans source"),
    (r"pourrait potentiellement|il est possible que dans certains cas", "réserves empilées"),
]
PLACE = re.compile(r"\[(À COMPLÉTER|A COMPLETER|CAPTURE À INSÉRER|SOURCE À TROUVER|TODO|personnel)[^\]]*\]|\[Texte personnel|\[titre\]|\[texte\]|\[ce que le lecteur|\[bilan", re.I)

def main(d, max_pages=None, as_json=False, before=None):
    d = Path(d); err, warn = [], []; pages = 0
    tex = {p: p.read_text(encoding="utf-8", errors="ignore") for p in d.rglob("*.tex") if p.name not in ("preamble.tex", "cover.tex")}
    body = "\n".join(t for p, t in tex.items() if p.name != "meta.tex")
    clean = re.sub(r"(?m)(?<!\\)%.*$", "", body)
    # placeholders
    for p, t in tex.items():
        for m in PLACE.finditer(re.sub(r"(?m)(?<!\\)%.*$", "", t)):
            warn.append(f"placeholder {p.name}: {m.group(0)[:60]}")
    # figures/tables referenced
    labels = re.findall(r"\\label\{((?:fig|tab):[^}]+)\}", clean)
    refs = set(re.findall(r"\\(?:c|C|auto)?ref\{([^}]+)\}", clean)) | set(x for g in re.findall(r"\\[cC]ref\{([^}]+)\}", clean) for x in g.split(","))
    for l in labels:
        if l not in refs: err.append(f"never referenced: {l}")
    if re.search(r"\\begin\{figure\}", clean) and not re.search(r"\\label\{fig:", clean): warn.append("figures without \\label{fig:...}")
    # citations
    bib = "".join(p.read_text(encoding="utf-8", errors="ignore") for p in d.rglob("*.bib"))
    keys = set(re.findall(r"@\w+\{([^,\s]+),", bib))
    cited = set(k.strip() for g in re.findall(r"\\(?:auto|text|paren)?cite\w*\{([^}]+)\}", clean) for k in g.split(","))
    for k in cited - keys: err.append(f"citation without bib entry: {k}")
    if not cited: warn.append("no citations in text")
    elif len(keys) < 6: warn.append(f"only {len(keys)} bib entries (typical 6-27)")
    # cliches
    plain = plain_of(clean)
    for pat in CLICHES:
        for m in re.finditer(pat, plain):
            warn.append(f"cliché/AI-tell: '{m.group(0)}' … {plain[max(0,m.start()-30):m.end()+30].strip()!r}")
    # humanizer-derived structural tells
    for pat, name in STRUCT:
        for m in re.finditer(pat, plain):
            warn.append(f"{name}: '{m.group(0)}' … {plain[max(0,m.start()-30):m.end()+30].strip()!r}")
    words = max(1, len(plain.split()))
    W = r"[\wàâçéèêëîïôûù-]+"
    for pat, name, n in [(r"\ben (résumé|conclusion|somme)\b", "'En résumé/En conclusion' répété", 3),
                         (r"\b(constitue|constituent|représente|représentent|sert de|servent de|se positionne comme)\b", "copule évitée (est/a)", 5),
                         (rf"\b{W}, {W} et {W}\b", "triplets forcés (a, b et c)", max(6, words // 400))]:
        c = len(re.findall(pat, plain))
        if c >= n: warn.append(f"{name}: {c} occurrences ({n}+ = tic ; garder seulement les vrais triplets)")
    dashes = len(re.findall(r"---|(?<=\s)--(?=\s)", clean))
    if dashes >= max(4, words // 800): warn.append(f"{dashes} tirets cadratins comme connecteur ; préférer point, virgule, deux-points")
    if len(re.findall(r"\\textbf\{", clean)) > max(8, words // 150): warn.append("gras décoratif : trop de \\textbf ; gras seulement à la première définition d'un terme")
    if len(re.findall(r"\\item\s*\\textbf\{[^}]*\}\s*:", clean)) >= 4: warn.append("listes « \\item \\textbf{Label} : … » ; passer en prose si les étiquettes n'apportent rien")
    # per-file checks, so each warning names the chapter that needs the rewrite
    tells = {}
    for p, c in read_tex(d).items():
        n, pl = p.name, plain_of(c)
        tells[n] = sum(len(re.findall(x, pl)) for x in CLICHES + [s for s, _ in STRUCT])
        paras = [x.strip() for x in re.split(r"\n\s*\n", pl) if x.split()]
        for para in paras:  # 3 sentences in a row with the same first word
            fw = [x.split()[0] for x in re.split(r"(?<=[.!?])\s+", para) if x.split()]
            for i in range(len(fw) - 2):
                if fw[i] == fw[i + 1] == fw[i + 2] and len(fw[i]) > 1:
                    warn.append(f"{n}: 3 phrases de suite commencent par '{fw[i]}'"); break
        op = [" ".join(x.split()[:2]) for x in paras if len(x.split()) > 25]
        for i in range(len(op) - 2):  # 3 consecutive long paragraphs with the same opener
            if op[i] == op[i + 1] == op[i + 2]:
                warn.append(f"{n}: 3 paragraphes de suite s'ouvrent par '{op[i]}'"); break
        sents = [len(s.split()) for s in re.split(r"[.!?]\s", pl) if len(s.split()) > 3]
        if len(sents) > 30:
            mean = sum(sents) / len(sents); sd = (sum((x - mean) ** 2 for x in sents) / len(sents)) ** .5
            if sd < 6: warn.append(f"{n}: rythme plat, écart-type des phrases {sd:.1f} (moyenne {mean:.1f}) ; varier")
        for m in re.finditer(r"\\(?:chapter|(?:sub)*section)\*?\{([^}]*)\}", c):
            title = m.group(1)
            caps = [w for w in re.findall(r"[A-Za-zÀ-ÿ]+", title)[1:] if len(w) > 3 and w[0].isupper() and not w.isupper()]
            if len(caps) >= 2: warn.append(f"{n}: titre en casse de titre « {title[:50]} » ; casse de phrase en français (ignorer les noms propres)")
            rest = re.sub(r"^(\s*\\(label|index)\{[^}]*\})*\s*", "", c[m.end():])
            if rest.startswith("\\"): continue
            first = plain_of(re.split(r"(?<=[.!?])\s", rest.split("\n\n")[0].strip())[0])
            hw = {w.lower() for w in re.findall(r"\w{4,}", title)}
            if hw and len(first.split()) <= 12 and hw <= set(re.findall(r"\w{4,}", first)):
                warn.append(f"{n}: la première phrase répète le titre « {title[:50]} » ; la supprimer")
    # French typography
    if re.search(r'(?<![\\`])"[^"\n]{2,}"', clean): warn.append('straight quotes "…" found; use « … » (\\og \\fg or «»)')
    if re.search(r"\w\s{2,}\w", clean) and False: pass
    if re.search(r"[“”]", clean): warn.append("guillemets anglais “ ” ; utiliser « … »")
    if re.search(r"\.\.\.", clean): warn.append("use … (\\ldots) not '...'")
    # empty sections
    for p, t in tex.items():
        for m in re.finditer(r"\\(sub)*section\*?\{[^}]*\}\s*(?=\\(sub)*section|\\chapter|\Z)", t):
            warn.append(f"empty section in {p.name}: {m.group(0).strip()[:50]}")
    # pages
    pdf = d / "main.pdf"
    if pdf.exists():
        try:
            import pymupdf
            n = len(pymupdf.open(str(pdf)))
            pages = n
            if max_pages and n > max_pages: err.append(f"{n} pages > budget {max_pages}")
        except ImportError:
            warn.append("pymupdf missing: page count skipped")
    if before: facts_diff(before, d, err, warn)
    if as_json:
        print(json.dumps({"pages": pages, "errors": err, "warnings": warn, "tells_by_file": tells}, ensure_ascii=False, indent=1))
        return 1 if err else 0
    if pages: print(f"pages: {pages}")
    for w in warn: print("WARN ", w)
    for e in err: print("ERROR", e)
    print("tics par fichier : " + (", ".join(f"{k} {v}" for k, v in sorted(tells.items(), key=lambda kv: -kv[1]) if v) or "aucun"))
    print(f"{len(err)} errors, {len(warn)} warnings")
    return 1 if err else 0

if __name__ == "__main__":
    a = sys.argv[1:]
    if not a: sys.exit("usage: python lint_report.py <report_dir> [--max-pages N] [--json] [--facts-diff <before_dir>]")
    mp = int(a[a.index("--max-pages") + 1]) if "--max-pages" in a else None
    bf = a[a.index("--facts-diff") + 1] if "--facts-diff" in a else None
    sys.exit(main(a[0], mp, "--json" in a, bf))
