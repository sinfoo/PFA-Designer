# Design system (implemented in template/preamble.tex)

## Page
A4 · margins 2.5 cm (FSGF guide; 3 cm inner/2 cm outer only for bound twoside) · header/footer 10 pt, 1 cm · body Times-like 12 pt (TeX Gyre Termes) · spacing 1.5 (`\BodySpacing`; 1.25 only if school allows) · justified, microtype on, widows/orphans forbidden · no underlining, avoid ALL CAPS in titles.

## Hierarchy
| Level | Style |
|---|---|
| Chapter | big accent number (54 pt) + 24 pt sans title + accent rule, new page; unnumbered variant for intro/conclusion/résumé |
| Section | Large bold sans, accent |
| Subsection | large bold sans, ink |
| Subsubsection | bold sans, grey; max depth 3 (TOC depth 2) |
| Header | "n. Chapter title" (≤40 chars) left, year right; footer author left, page right (accent) |

## Colour
One accent + ink + muted grey + paper tint. Default `1F4E79` (navy). Alternatives: `0F6B5C` teal (data/ML), `7A1F3D` bordeaux (law/management), `B45309` amber (industrial), `2B2D8F` indigo (telecom). Pick by domain or school logo; never > 1 accent. Diagrams reuse the accent + its tints so figures feel part of the page.

## Components
- `cadre` / `definition` callouts (left rule, tinted bg) — use ≤1 per page; `\chapterintro{}` box at each chapter start.
- Figures: vector PDF/TikZ preferred; width 0.7–0.9 `\linewidth`; caption below, sentence-style, + `\source{}` when not original; referenced in text with `\cref{fig:x}` ("Figure 3.2") before it appears.
- Tables: booktabs only (no vertical rules), caption above, header row bold, ≤ 6 columns, numbers right-aligned.
- Code: `lstlisting` ≤15 lines, 8.5 pt mono, only to illustrate a design decision; full code goes to annex or repo link.
- Gantt: `pgfgantt`, accent bars.

## French typography (babel-french handles most)
Non-breaking space before `: ; ! ?` and inside « » (babel does it — do not hand-insert; in Word insert U+00A0/U+202F). Numbers "1 000", decimal comma, "12 %". "1^{er}", "2^{e}". Capital only on first word of titles. Use ’ apostrophes and « » not "". `Figure 2.3` in captions, "la figure 2.3" in running text. Acronyms defined at first use.

## Cover
See `template/cover.tex`: ministry line, logos, school, nature, diploma, title block (tinted box), "Réalisé par / Encadré par", academic year. Missing logo files are skipped automatically (`figures/logo-school.png`, `logo-right.png`).

## Variants
- Word required by school: generate `.docx` with the `docx` skill from the same content; keep the same hierarchy values above.
- School supplies a cover/template: keep its cover; keep this body styling only where it doesn't conflict.
- twoside printing: `\documentclass[...,twoside]`, `\cleardoublepage`, inner margin 3 cm.
