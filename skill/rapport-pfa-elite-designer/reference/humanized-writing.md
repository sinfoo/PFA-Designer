# Humanized, original writing

Goal: a report that reads like a competent student who built the thing and can talk about it — because it is built from the project's real facts and the student's real experience. This is a *quality* standard (specific, varied, honest). It is not a detector-evasion technique, and the skill never uses one (no homoglyphs/invisible characters, no paraphrase spinners, no "make it score human" loops). Schools may restrict AI assistance: tell the user to check their rule and be able to defend every page orally.

## 1. Concrete-detail rule (the main lever)
Every paragraph of analysis must contain at least one thing only *this* project has: a file/module name, an endpoint, a table, a number, a commit-date range, a bug and its fix, a rejected alternative and why, a screenshot reference. A paragraph that could be pasted into any other report is deleted or rewritten.
- Generic: "L'application utilise une architecture moderne et scalable."
- Specific: "Le back-end est découpé en trois services (auth, catalogue, commandes) qui communiquent par RabbitMQ ; ce choix nous a évité de bloquer le paiement quand le catalogue était en maintenance."

## 2. Source of voice
- Use the interview answers: motives, real difficulties, decisions with trade-offs, what was dropped for lack of time.
- Use git history for honest chronology ("la première version du panier date du 12 mars ; elle a été réécrite en avril après…").
- Person: "nous" for team work, "je" for personal contribution; stay consistent per section. Past tense for what was done, present for how the system works, future only in the plan.
- One real limitation or mistake per major chapter. Perfection reads as invented.

## 3. Rhythm & register
- Mix sentence lengths (5 to 35 words). Max ~20 words average in technical passages. Paragraphs 3–7 sentences, not all the same shape.
- Academic but plain French. Prefer the verb over the nominalisation ("nous avons choisi" > "le choix a été porté sur").
- Vary paragraph openers; no three consecutive paragraphs starting with the same word (lint checks this).
- Prose first (≥80 %): bullets only for true lists (requirements, endpoints). Tables for comparisons, with a sentence before and after interpreting them.

## 4. AI-tell patterns to avoid (FR/EN)
Remove or rewrite on sight (lint flags them):
- Filler openers: "À l'ère du numérique", "Dans un monde en constante évolution", "Il est important de noter que", "Il convient de souligner", "Force est de constater", "Dans le cadre de ce chapitre, nous allons".
- Inflated vocab: "robuste", "puissant", "innovant", "révolutionnaire", "cutting-edge", "seamless", "holistique", "tirer parti de", "témoigne de", "joue un rôle crucial/clé".
- Structural tics: triplets everywhere ("rapide, fiable et sécurisé"), "non seulement … mais aussi" repeated, "En résumé / En conclusion" at the end of every section, every section ending with a moral, rhetorical questions, em-dash overload, bold on random words, uniform bullet lists with bold lead-ins.
- Empty claims without evidence: "améliore significativement", "très performant" → give the number or drop it.
- Symmetry: every chapter intro/outro identical in shape; every sprint section identical in length.
Do not replace with a different tic. Replace with a fact.

## 5. Originality & citations
- Definitions/state-of-the-art: paraphrase *from a source you read*, then cite [n]. Never paste. Quote (« … » + [n] + page) only for short exact wording.
- Every figure not drawn by the student: "Source : [n]" or "Source : capture d'écran de l'auteur" / "Réalisé par l'auteur".
- Reused code/libs/templates named explicitly in Réalisation ("composant X issu de la lib Y"). Personal contribution separated from reused.
- Bibliography only real, checked sources (open the URL / confirm the book). Unknown ⇒ `[SOURCE À TROUVER]`, never a plausible-looking fake.
- Plagiarism checkers compare against published text: original wording from project facts passes naturally; stock template sentences (dédicace/remerciements clichés, definitions of "Scrum", "UML", "MVC") are the usual false-positive sources → write them in your own words with citation.

## 6. Self-check before handoff
Read 3 random paragraphs aloud. Could the student explain each? Is there a project-specific fact in each? Any sentence that would be true of every project? Cut it.
