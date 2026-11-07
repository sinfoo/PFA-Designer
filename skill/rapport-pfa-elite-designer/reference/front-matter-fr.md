# Front matter & framing texts (French) — patterns, not text to copy

Patterns observed in ESPRIT / ISI / ENET'Com / ITBS templates and real reports. Use as skeleton; fill with the student's real facts. **Do not reuse the stock phrases verbatim** — every Tunisian report starts "Je tiens à exprimer mes sincères remerciements…" and that sameness is exactly what reads as generic. Keep the order, change the content.

## Cover (page de garde)
Top → bottom: République Tunisienne / Ministère de l'Enseignement Supérieur et de la Recherche Scientifique / (Université) / École · logos left+right · nature ("Rapport de Projet de Fin d'Année" or "…d'Études") · diploma line ("Cycle d'ingénieur en …, spécialité …, Xe année") · **Titre** (+ sous-titre) · "Réalisé par" · "Encadré par" (académique, + professionnel if company) · host company/logo if any · (jury block at PFE: Président, Rapporteur, Encadrants) · "Année universitaire 20xx–20yy". One accent colour, lots of white space. Implemented in `template/cover.tex`; fields in `meta.tex`.

## Dédicace (optional, 2–5 lines, right-aligned italic)
Pattern: who (parents → siblings → one friend/teacher/other) + *one concrete reason each*. Short beats long.
- Weak: "À mes chers parents, source de tendresse et d'amour, qui m'ont soutenu tout au long de mon parcours."
- Better (structure): "À [prénom/lien], [fait précis : qui m'a attendu chaque soir de révision / qui m'a prêté son PC quand le mien est tombé]."
Ask the student for the real people and one real detail; if refused, keep it 2 lines, sincere, no superlatives pile-up.

## Remerciements (150–250 words, one paragraph per group)
Order (all sources agree): 1) encadrant académique → 2) encadrant professionnel / host team (if any) → 3) jury members → 4) teachers / department / team-mates who really helped → 5) family & friends.
Rules: thank only people who really helped; say **what** they did (a review, a meeting, a tool access), not "pour sa disponibilité" alone; first-person singular ("je") unless a team ("nous"); no religious/formulaic lines unless the student wants them; no longer than one page.

## Résumé (FR) + Abstract (EN) (150–250 words each, keywords 3–5)
Pattern, 5 beats: **contexte** (1 sentence) → **problème** → **ce qui a été fait** (real stack, 1–2 sentences) → **résultat** (one real number if the project has one: latency, accuracy, users, coverage, time saved) → **portée** (what it enables next).
Abstract = faithful English version, not a word-by-word translation. Keywords = the real techs/domains (e.g. "NestJS, microservices, e-commerce, JWT, CI/CD"). No "Ce travail s'inscrit dans le cadre de…" opener unless it is true and short — prefer starting on the problem.

## Introduction générale (1–2 p, 4 paragraphs, written last)
1. **Contexte large** — domain trend with ≥1 sourced fact (cited [n]).
2. **Problème précis** — who suffers, how, evidence (from the repo's README/issues/interviews). Avoid "à l'ère du numérique".
3. **Objectif et démarche** — what the project delivers, constraints, method (Scrum, UML…), tech chosen in one sentence.
4. **Plan** — future tense, one clause per chapter, ending with the conclusion: "Le premier chapitre situe le projet et compare les solutions existantes. Le deuxième…"
Does not contain results.

## Chapter intro / conclusion (each 0.3–0.5 p)
Intro: what question the chapter answers + what the reader will have by the end. Conclusion: one-sentence verdict + hand-off ("Ces besoins étant fixés, le chapitre suivant en dérive l'architecture.").

## Conclusion générale et perspectives (1–2 p)
1. Recap vs. the objectives stated in the introduction (tick each, honestly: done / partly / not done).
2. Difficulties actually met and what they taught (technical, then organisational/personal) — from the interview.
3. Limits (be specific: no load test beyond N users, no mobile build…).
4. Perspectives: 2–3 concrete, ranked, feasible next steps. No new results, no sales pitch.

## Glossary / abbreviations
Every acronym used ≥2 times; define at first use in text too. Table in `00-acronymes.tex` (`\acro{API}{…}`).
