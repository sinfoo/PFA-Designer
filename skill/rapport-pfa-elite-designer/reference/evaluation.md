# Jury grid, QA, defense prep

## What Tunisian juries score (SupCom charter, ESIP/ESSECT guides; synthesis)
Jury: président + rapporteur + examinateur (+ supervisors attending). Defense 30–60 min incl. questions. Criteria: (1) written report — structure, clarity, scientific rigour; (2) oral presentation — clarity, mastery, synthesis; (3) relevance of results, methodology, prototype; (4) answers to questions; plus coherence objectives ↔ results. Ask the school for its exact grid.

## Report QA checklist (the lint script covers the starred)
- [ ] Problem statement clear & measurable; objectives in intro are checked in conclusion
- [ ] State of the art / benchmark with justified choice
- [ ] Methodology justified *and* evidenced (backlog, sprints, dates)
- [ ] Requirements traceable need → use case → feature → test
- [ ] Diagrams match the code
- [ ] Personal contribution separated from reused work
- [ ] Tech choices justified (alternatives named)
- [ ] Tests with measured results, not claims
- [ ] Limits and perspectives honest and specific
- [ ] ★ No `[À COMPLÉTER]`/placeholder left (or listed in handoff)
- [ ] ★ Every figure/table referenced in text; captions + sources
- [ ] ★ Every citation [n] exists in the bibliography and vice-versa
- [ ] ★ No stock AI/cliché phrases; varied paragraph openers
- [ ] ★ French typography (no `"` quotes, no space-before-`:` issues outside babel)
- [ ] ★ Page count within budget; annexes ≤ 1/3
- [ ] Visual check of rendered pages (cover, TOC, chapter opener, figure, table, bibliography): no overfull boxes, no orphan headings, no blank pages

## Defense prep (append to handoff)
Generate 10–15 likely questions from the actual project: why this stack vs alternative X; how is auth/security handled; what breaks at 10× load; what would you do differently; what part did *you* write; how did you test; data model choice; deployment; biggest bug; what's missing. Plus slide outline 15–25 slides for 20–30 min: context, problem, solution, architecture, 2 demos, results, limits, perspectives. Live demo + recorded fallback.
