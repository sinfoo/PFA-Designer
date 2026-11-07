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
PLACE = re.compile(r"\[(À COMPLÉTER|A COMPLETER|CAPTURE À INSÉRER|SOURCE À TROUVER|TODO|personnel)[^\]]*\]|\[Texte personnel|\[titre\]|\[texte\]|\[ce que le lecteur|\[bilan", re.I)

def main(d, max_pages=None):
    d = Path(d); err, warn = [], []
    tex = {p: p.read_text(errors="ignore") for p in d.rglob("*.tex") if p.name not in ("preamble.tex", "cover.tex")}
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
    bib = "".join(p.read_text(errors="ignore") for p in d.rglob("*.bib"))
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
