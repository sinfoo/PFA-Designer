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

## 4. AI-tell patterns to avoid (French)
Adapted from the `humanizer` skill (blader/humanizer, MIT; itself based on Wikipedia's "Signs of AI writing") and translated to French report prose. Principle: every sentence kept must add something the reader does not already have. A tell counts in proportion to how rarely a careful writer would do it on purpose; patterns marked *faible seul* need company in the same passage before you act. The lint flags most of these (`scripts/lint_report.py`). Rewrite = state the fact; never swap one tic for another.

**A. Staging instead of stating (act on one sighting)**
- *Pas X mais Y* : « non seulement… mais aussi », « ne se limite pas à », « n'est pas seulement X, c'est Y », « il ne s'agit pas de X mais de Y », same contrast split over two sentences (« Cela ne signifie pas X. Cela signifie Y. »). Keep a contrast only if the negative half corrects a belief the reader really holds.
  - Avant : « Ce module n'est pas seulement un outil de saisie, c'est le cœur du système. » → Après : « Le module de saisie alimente directement les tables `commande` et `stock`. »
- *Fermetures d'une ligne* : a one-sentence paragraph that repeats the previous one (« C'est là tout l'enjeu. », « Cette distinction est essentielle. »), a sentence naming the lesson of an example (« Cela montre l'importance de… »), a row of fragments (« Pas de cache. Pas de file. Pas de reprise. »). Cut, or merge into one sentence with a claim. The same closer after several sections is a tell by itself.
- *Formules qui sonnent profond* : « la véritable question est », « au cœur de », « fondamentalement », « le nerf de la guerre », « X est le langage de Y ». Replace with the specific claim.
- *Mise en scène avant le propos* : « Voyons maintenant comment… », « Plongeons dans… », « Sans plus attendre », « Voici ce qu'il faut savoir ». Delete the run-up, start with the fact.
- *Discuter avec personne* : « Il serait tentant de… mais », « On pourrait penser que… », « Ne nous méprenons pas », « Il ne s'agit pas ici de… » when no objection appears elsewhere. Keep an alternative only if it was really considered (a rejected alternative + its reason is a concrete detail, see §1).

**B. Rhythm by rule**
- *Triplets forcés* : « rapide, fiable et sécurisé ». Keep three items only when there are three distinct ideas; otherwise merge or develop the strongest.
- *Débuts de phrase répétés* : 3+ consecutive sentences with the same first word; merge them, change the subject, or open with the action.
- *Tiret cadratin partout* : `---` or ` -- ` as a connector. Use a full stop, comma, colon or parentheses. Keep `--` for number ranges (pp. 12--15). *Faible seul.*
- *Réserves empilées* : « pourrait potentiellement », « il est possible que dans certains cas ». Keep one hedge only if the evidence needs it. *Faible seul.*
- *Passif sans sujet* : « les résultats sont automatiquement conservés » → « le serveur conserve les résultats ». Prefer the actor, especially « nous / je ». *Faible seul.*

**C. Inflation and borrowed authority**
- *Mots à surveiller* (tells in groups): crucial, pivot, incontournable, robuste (figurative), innovant, révolutionnaire, holistique, paysage (abstract), témoigne de, met en lumière / en exergue, s'inscrit dans une dynamique, foisonnant, florissant, véritable, un atout majeur, tirer parti de, s'avère être.
- *Importance gonflée* : « marque un tournant », « joue un rôle clé », « laisse une empreinte durable », « l'avenir s'annonce prometteur », a « Défis et perspectives » section that praises. Keep the fact, drop the significance; end a section on its last concrete fact.
- *Liens vagues* : « associé à », « en lien avec », « lié à » when the relationship is known (who did what). Name it.
- *Participes présents décoratifs* : « …, soulignant l'importance de », « …, reflétant », « …, garantissant ». Keep the fact; keep the rider only if the source supports it.
- *Langage publicitaire* : « riche », « exceptionnel », « une solution complète », « au service de ». Say what the thing is and does.
- *Autorité empruntée* : « selon les experts », « de nombreuses études montrent » with no source. Cite [n] or cut.
- *Éviter « est / a »* : « constitue », « représente », « sert de », « se positionne comme » for plain « est ». Use the simple verb. *Faible seul.*

**D. Formatting by rule**
- *Gras décoratif* : bold on random words; `\item \textbf{Label} : phrase` lists where labels carry no information. Turn into prose. Bold only for a term at its first definition.
- *Titres décoratifs* : title-case headings (French uses sentence case: « Choix de l'architecture »), emojis, arrows, headings written for effect (« L'architecture en un clin d'œil »). A heading names what the section holds.
- *Guillemets* : « … » with non-breaking spaces; never straight `"` or curly “ ”.

**E. Leftovers from the chat**
- Remove outright: « J'espère que cela vous aide », « Bien sûr ! », « Excellente question », « N'hésitez pas à… », « Voici un aperçu de… », « En tant que modèle de langage ».
- *Limites de connaissance et devinettes* : « à la date de », « d'après les informations disponibles », « il est probable que… » used to fill a gap. If the repo or the student did not say it, ask (`[À COMPLÉTER : …]`); never fill with a plausible guess.
- *Titre répété* : a section whose first sentence restates its heading (« Sécurité. La sécurité est importante. »). Delete it.
- *Écrire sur le document* : no « ce chapitre est organisé en… » boilerplate beyond the one chapter-intro paragraph, no « le tableau ci-dessous compare… » when an interpreting sentence already introduces it, no account of how the text was produced.

**F. Structural tics (original list)**
- Filler openers: « À l'ère du numérique », « Dans un monde en constante évolution », « Il est important de noter que », « Il convient de souligner », « Force est de constater », « Dans le cadre de ce chapitre, nous allons ».
- « En résumé / En conclusion » at the end of every section; every section ending with a moral; rhetorical questions; uniform bullet lists.
- Empty claims without evidence: « améliore significativement », « très performant » → give the number or drop it.
- Symmetry: every chapter intro/outro identical in shape; every sprint section identical in length.

**When not to act.** Leave a watched phrase inside a quotation, a title, a proper name, or a passage that discusses the phrase. Keep what carries the student's voice: a specific odd detail, mixed feelings (« je pense que c'était le bon choix, mais… »), a first-person choice they can explain, a genuine aside.

**Method (per chapter, before the lint).** 1) Mark the tells, strongest first, looking at paragraph shape as well as sentences. 2) Rewrite keeping every supported claim; add no fact, number, date, name or citation the repo or the student did not give. 3) Read aloud, then search again for the tells that survive a rewrite: *pas X mais Y*, one-line closers, triplets, dashes, bold labels. 4) Write the final version in plain, varied French; if a sentence stays awkward, rewrite the paragraph around its point.

## 5. Originality & citations
- Definitions/state-of-the-art: paraphrase *from a source you read*, then cite [n]. Never paste. Quote (« … » + [n] + page) only for short exact wording.
- Every figure not drawn by the student: "Source : [n]" or "Source : capture d'écran de l'auteur" / "Réalisé par l'auteur".
- Reused code/libs/templates named explicitly in Réalisation ("composant X issu de la lib Y"). Personal contribution separated from reused.
- Bibliography only real, checked sources (open the URL / confirm the book). Unknown ⇒ `[SOURCE À TROUVER]`, never a plausible-looking fake.
- Plagiarism checkers compare against published text: original wording from project facts passes naturally; stock template sentences (dédicace/remerciements clichés, definitions of "Scrum", "UML", "MVC") are the usual false-positive sources → write them in your own words with citation.

## 6. Self-check before handoff
Read 3 random paragraphs aloud. Could the student explain each? Is there a project-specific fact in each? Any sentence that would be true of every project? Cut it.
