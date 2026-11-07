# Structure of a Tunisian PFA/PFE report (from real reports)

## Evidence base (read for this skill)
INSAT GL 2014/15 (ERP module, 92 pp, 6 chapters, 8 sprints) · ISI El Manar bank app (85 pp, 4 ch., Scrum) · EPMPT Tunisie Télécom BI (69 pp, 4 ch.) · ISIMed towing web app (64 pp, 4 ch., UML) · ISET Charguia OpenShift/CI-CD (65 pp, 4 ch.) · ISTLS Lean "Projet Fin d'Année" (82 pp) · ENSIT industrial (3 ch.) · FST Fès mechanical (3 ch.) · templates: ESPRIT PFE, ISI El Manar, ENIT TIC, ENET'Com, IT Business School; guides: FSGF (TNR 12, 1.5, margins 2.5, ≤60 pp), ISEAHM 2025/26, SupCom PFE charter. ENET'Com PFA is a 2nd-year project; PFA reports reuse the PFE skeleton, shorter.
**Not found publicly:** ESPRIT PFA/PIDEV official grid, INSAT/ENIT margin rules. Ask the school.

## Shape (consistent across all)
Cover → (signature page, some schools) → Dédicace (optional) → Remerciements → Résumé+mots-clés (FR) → Abstract+keywords (EN) [+ Arabic at some schools] → Table des matières → Liste des figures → Liste des tableaux → Liste des abréviations → **Introduction générale** → chapters → **Conclusion générale et perspectives** → Bibliographie / Webographie → Annexes → (Glossaire).
Roman numerals for front matter; Arabic starts at Introduction générale and ends at Conclusion.

## Page budgets
| Report | Body pages | Notes |
|---|---|---|
| PFA (default) | 35–60 | ENET'Com PFA is 2nd-year; shorter than PFE; often academic supervisor only |
| PFE | 55–90 (+annexes) | FSGF cap 60; ESPRIT ≈ 20–25 pp per chapter, annexes ≤ 1/3 |
Typical counts: 20–70 figures, 3–18 tables, 6–27 references (mostly web). Introduction 1–2 p; conclusion ≈1 p; chapter intro/conclusion ≈ 0.3–0.5 p each.

## Chapter plans by project type
Common spine: **Context → Analysis → Design → Realisation** (+ Tests). Each chapter opens with a short intro ("Dans ce chapitre…") and closes with a conclusion that points to the next.

### Web / SaaS (majority)
1. **Contexte général et étude préalable** — organisation/context, existing solutions + critique, benchmark table (criteria × solutions), problem, proposed solution, methodology choice (Scrum: roles/events/artefacts, sprint length; or 2TUP/Kanban), planning (Gantt).
2. **Analyse et spécification des besoins** — actors, functional needs, non-functional needs (performance, security, usability, maintainability), global use-case diagram + 4–8 textual use cases (pre/post-condition, nominal + alternative scenario), product backlog table (ID, user story, priority, estimate), sprint plan.
3. **Conception** — logical + physical architecture (layers, MVC/microservices, justified), deployment diagram, class diagram / ER (from real models), 2–4 sequence diagrams, DB schema, API endpoint table, UI mock-ups/design system, technology choices with justification.
4. **Réalisation** — environment (hardware/software table), stack with logos, one section per sprint/module: goal → what was built → screenshots → one short code excerpt (≤15 lines) → sprint review/retro. CI/CD, containers.
5. **Tests et validation** (may merge into 4) — test plan (unit/integration/E2E/perf/security), results table with real numbers, coverage, bugs found/fixed.

### Mobile
Same, plus: ch.3 navigation map + UI flows + offline/sync strategy; ch.4 SDK/framework, API, permissions, emulator + real-device tests, store build.

### ML / data (CRISP-DM)
1. Étude préalable (context, business problem, existing approaches) 2. État de l'art 3. Compréhension et préparation des données (sources, EDA, cleaning, features, leakage guard) 4. Modélisation et évaluation (baseline → models, metrics: accuracy/F1/ROC/confusion matrix, error analysis, ablation) 5. Déploiement (API, monitoring, limits).

### IoT / embedded
1. Contexte + état de l'art 2. Cahier des charges + architecture matérielle (block diagram, component table, power budget) 3. Architecture logicielle (firmware layers, protocols MQTT/BLE, state machines) 4. Réalisation + mesures (schematics, PCB, photos, measured vs expected) 5. Tests.

### Network / telecom / DevOps / cloud
1. Étude préalable 2. État de l'art (virtualisation, conteneurs, protocols) 3. Architecture + environnement (topology, addressing plan, tools) 4. Réalisation et test (configs in annex, pipeline stages, load/failover tests).

### Industrial / logistics (Lean/DMAIC) and civil/mech
Industrial: revue de littérature → cadrage + problem (QQOQCP, SIPOC) → diagnostic (VSM, Ishikawa, Pareto) → actions + control. Civil/mech: organisme/contexte → cahier des charges + analyse fonctionnelle + choix → conception/calcul/simulation → résultats.

## What the jury expects in each block (see `evaluation.md` for the full grid)
- **Introduction générale**: broad context (1 sourced fact) → problem → objective/approach → plan in future tense ("Le premier chapitre présentera…"). Written *last*.
- **Chapter 1** must end with a clear problem statement and a justified solution choice, not a catalogue.
- **Chapter 2** must be traceable: every functional need → a use case → a backlog item → a test.
- **Chapter 3** diagrams must match the code (class names, endpoints, tables real).
- **Chapter 4** shows personal contribution; reused parts are named as reused.
- **Conclusion**: mirrors the objectives of the introduction, honest limits, 2 concrete perspectives, no new results.
- Every annex cited in the body; sources under every figure not drawn by the student.

## References style
Numbered IEEE `[1]` via biblatex (template default) split or not into Bibliographie / Webographie. Web entries: author/site, title, URL, date consulted. Books: author, title, edition, year. Ask which style the school wants (IEEE / author-year).
