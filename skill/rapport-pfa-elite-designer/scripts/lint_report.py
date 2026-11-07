"""Report linter. Usage: python lint_report.py <report_dir> [--max-pages N]
Checks: placeholders, empty sections, unreferenced figures/tables, citations vs bib, cliché/AI-tell phrases, repeated paragraph openers,
French typography slips, page count. Exit 1 if any ERROR."""
import re, sys
from collections import Counter
from pathlib import Path

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

def main(d, max_pages=None):
    d = Path(d); err, warn = [], []
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
    plain = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?", " ", clean).lower().replace("’", "'")
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
    for para in re.split(r"\n\s*\n", plain):  # 3 sentences in a row with the same first word
        fw = [x.split()[0] for x in re.split(r"(?<=[.!?])\s+", para.strip()) if x.split()]
        for i in range(len(fw) - 2):
            if fw[i] == fw[i + 1] == fw[i + 2] and len(fw[i]) > 1:
                warn.append(f"3 phrases de suite commencent par '{fw[i]}'"); break
    # repeated openers
    paras = [p.strip() for p in re.split(r"\n\s*\n", plain) if len(p.split()) > 25]
    op = Counter(" ".join(p.split()[:2]) for p in paras)
    for k, v in op.items():
        if v >= 4: warn.append(f"{v} paragraphs open with '{k}'")
    # sentence-length variance
    sents = [len(s.split()) for s in re.split(r"[.!?]\s", plain) if len(s.split()) > 3]
    if len(sents) > 30:
        mean = sum(sents) / len(sents); sd = (sum((x - mean) ** 2 for x in sents) / len(sents)) ** .5
        if sd < 6: warn.append(f"flat rhythm: sentence length sd={sd:.1f} (mean {mean:.1f}); vary it")
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
            print(f"pages: {n}")
            if max_pages and n > max_pages: err.append(f"{n} pages > budget {max_pages}")
        except ImportError:
            warn.append("pymupdf missing: page count skipped")
    for w in warn: print("WARN ", w)
    for e in err: print("ERROR", e)
    print(f"{len(err)} errors, {len(warn)} warnings")
    return 1 if err else 0

if __name__ == "__main__":
    a = sys.argv[1:]
    if not a: sys.exit("usage: python lint_report.py <report_dir> [--max-pages N]")
    mp = int(a[a.index("--max-pages") + 1]) if "--max-pages" in a else None
    sys.exit(main(a[0], mp))
