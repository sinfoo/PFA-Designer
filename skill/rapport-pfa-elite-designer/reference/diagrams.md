# Diagrams from the real code

Rule: a diagram must be derivable from the repo. Class/ER names, endpoints, services, tables = the real ones. Keep ≤ 12 nodes per diagram; split otherwise. Vector output (TikZ → inline, or matplotlib/graphviz → PDF in `figures/`).

| Diagram | Source in repo | Where | Tool |
|---|---|---|---|
| Use-case (global + per actor) | roles, routes/pages | ch.2 | TikZ (actors left, system box, ellipses) |
| Architecture (logical) | dirs, services, compose | ch.3 | TikZ blocks, arrows labelled with protocol |
| Deployment | Dockerfile, compose, CI, hosting config | ch.3 | TikZ nodes (client, server, DB, third parties) |
| Class / ER | ORM models, schema | ch.3 | TikZ matrix of 3-section boxes, or Graphviz if installed |
| Sequence (2–4 key flows: login, main business flow, payment/sync) | controllers → services → repos | ch.3 | TikZ (lifelines + arrows) |
| Gantt | git log + sprint reconstruction (confirm with user) | ch.1/2 | pgfgantt |
| Pipeline / ML flow | training scripts | ch.3/4 | TikZ flow |
| Data charts (metrics, benchmarks) | measured results | ch.5 | matplotlib → PDF, accent palette, labelled axes with units, no chart junk (see `dataviz` skill) |

## TikZ starter (architecture block)
Define once in the chapter or preamble: `\tikzset{blk/.style={draw=accent,fill=accent!8,rounded corners=2pt,minimum height=9mm,minimum width=26mm,font=\sffamily\small,align=center}, flow/.style={-{Stealth},thick,color=ink!70}}`. Place nodes with `positioning` (`right=of`), group layers with `fit` + dashed accent box labelled in small caps. Arrow labels = protocol/data (REST/JSON, SQL, WebSocket).

## Tool availability on this machine
MiKTeX (xelatex, latexmk, biber, tikz, pgfgantt, tcolorbox) and Tectonic present; Graphviz/Mermaid/Pandoc/Typst absent → default to TikZ + matplotlib (`python -c "import matplotlib"` to check). Do not install tools without asking.

## Figure checklist
Numbered caption below · referenced in text before it appears · legible at print size (≥8 pt text) · source line when not original · alt-style sentence in text saying what to notice · same accent palette · exported at vector or ≥200 dpi.
