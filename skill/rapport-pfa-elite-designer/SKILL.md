---
name: rapport-pfa-elite-designer
description: Use when the user asks for a rapport PFA, rapport de projet de fin d'année, rapport PFE, mémoire or report of a software/engineering project (Tunisian engineering schools like ESPRIT, INSAT, ENIT, SupCom, ISI, ENSI, ENETCom, FST), or says /rapport-pfa-elite-designer, "write my PFA report", "rapport du projet", "dédicace/remerciements/introduction générale" for the project in the current folder.
---

# Rapport PFA Elite Designer

Builds a complete, beautifully typeset French PFA/PFE report **from the project in the current working directory**, in the shape Tunisian juries expect. Output: XeLaTeX source + PDF. Research base: real Tunisian PFE/PFA reports and templates (INSAT, ISI, EPMPT, ISIMed, ISET, ENSIT, ESPRIT, ISI El Manar, ENET'Com, ENIT TIC, FSGF guide); see `reference/`.

**Principle: the report is only as good as its evidence.** Every claim comes from the repo, git history, or the student. Anything the repo cannot tell you is *asked*, never invented.

## Hard rules
1. **School template wins.** Ask once: "Ton école/encadrant impose-t-il un modèle (marges, police, page de garde, nombre de pages) ?" If yes, adapt `template/` to it. Otherwise use defaults in `reference/design-system.md`.
2. **Never fabricate**: no invented metrics, users, company names, supervisors, dates, test results, citations, or URLs. Unknown → `[À COMPLÉTER : …]` marker + list in final handoff. Personal sections (dédicace, remerciements, vécu, difficultés réelles) are drafted *from the student's answers*, not from imagination.
3. **Originality**: write from the project's facts; every borrowed idea/figure/definition gets a numbered citation and a source under the figure. No copy-paste from other reports, templates' example text, or papers. See `reference/humanized-writing.md`.
4. **Disclosure**: tell the user once that many schools restrict AI help and that they must follow their school's rule and be able to explain every page at the defense. Do not add detector-evasion tricks (character swaps, hidden text, paraphrase spinners) — they are misconduct and make the text worse.

## Workflow
1. **Recon (read-only)** — `python scripts/analyze_repo.py <project_dir> > facts.json` (stack, modules, routes, models, tests, git timeline, README, deps, size). Then read what it flags: README, entrypoints, schema/models, route files, tests, CI, docker files. Details: `reference/analysis-playbook.md`.
2. **Interview (one batch, ≤8 questions)** via AskUserQuestion/plain list: school + year + class, authors, supervisors (academic/pro), host company or none, problem/motivation in the student's words, 2–3 real difficulties and how solved, what was personally built vs reused, methodology really used (Scrum/Kanban/none), jury/defense date, language of résumé (FR/EN/AR), any imposed template. Skip what the repo already answers.
3. **Pick the chapter plan** by project type from `reference/structure.md` (web, mobile, ML/data, IoT/embedded, network/devops, other). Set page budget (PFA default 35–60 body pages; school limit wins).
4. **Scaffold**: copy `template/` to `<project>/rapport/` (never inside source dirs that ship), fill `meta.tex`, replace `sections/*.tex` placeholders. Template compiles as-is (`bash scripts/build.sh`).
5. **Diagrams** from real code (`reference/diagrams.md`): use-case, architecture, class/ER from actual models, sequence for 2–3 key flows, deployment, Gantt from git/sprints. Screenshots: ask the user for them or run the app if feasible (`run` skill); otherwise leave a captioned `[CAPTURE À INSÉRER]` placeholder.
6. **Write** chapter by chapter, intro + conclusion of each chapter, using `reference/humanized-writing.md` (voice, rhythm, humanizer-based French AI-tell patterns, concrete-detail rule) — run its 4-step method (mark tells, rewrite without adding facts, read aloud, re-scan) on each chapter before the lint and `reference/front-matter-fr.md` (dédicace, remerciements, résumé/abstract, introduction, conclusion patterns).
7. **Build + QA**: `bash scripts/build.sh` → `python scripts/lint_report.py rapport/` (placeholders left, empty sections, figures never referenced, French typography, AI-tell phrases, repeated openings, citation coverage, page count vs budget). Render 6–8 pages to PNG and look at them (cover, TOC, a chapter opener, a figure page, a table page, bibliography). Fix, rebuild.
8. **Handoff**: path to PDF + `.tex`, list of `[À COMPLÉTER]` items, list of claims to double-check, defense-prep questions (`reference/evaluation.md`). Commit only if the user asks.

## Quick reference (defaults when school gives nothing)
| Item | Value |
|---|---|
| Engine | XeLaTeX via `latexmk -xelatex` (MiKTeX/Tectonic OK) |
| Page | A4, margins 2.5 cm, header/footer 10 pt |
| Body | Times-like 12 pt (TeX Gyre Termes), spacing 1.5, justified, no hyphen abuse |
| Titles | sans (TeX Gyre Heros), 1 accent colour, max 3 numbered levels |
| Front matter | cover → dédicace → remerciements → résumé/abstract → TOC → figures → tables → abréviations (roman numerals) |
| Body | Introduction générale (1–2 p) → 4–5 chapters (each: intro box, sections, conclusion) → Conclusion générale + perspectives (≤1–2 p) → Bibliographie/Webographie → Annexes (≤ 1/3 of total) |
| Numbering | Arabic starts at Introduction; chapters 1…n; figures/tables numbered per document or chapter, captions: figure below, table above, source line |
| Résumé | FR 150–250 words + EN abstract, 3–5 keywords each |

## Files
- `reference/structure.md` — real-report structure, chapter plans per project type, page budgets, per-chapter contents
- `reference/front-matter-fr.md` — wording patterns and templates for cover, dédicace, remerciements, résumé, intro, conclusion
- `reference/humanized-writing.md` — authentic-voice rules, humanizer-derived French AI-tell patterns, concrete-detail rule, originality & citations
- `reference/analysis-playbook.md` — what to extract per stack and where each fact goes in the report
- `reference/design-system.md` — layout numbers, palettes, typography, cover, callouts, French typography rules
- `reference/diagrams.md` — TikZ/matplotlib recipes, code→diagram mapping, figure rules
- `reference/evaluation.md` — jury grid, QA checklist, defense Q&A prep
- `template/` — compiling XeLaTeX skeleton (`main.tex`, `meta.tex`, `preamble.tex`, `cover.tex`, `sections/`)
- `scripts/analyze_repo.py`, `scripts/build.sh`, `scripts/lint_report.py`

Invoke scripts via interpreter (`python …`, `bash …`).
