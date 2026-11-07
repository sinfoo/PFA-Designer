# Repo analysis playbook — fact → report location

Run `python scripts/analyze_repo.py <dir>` first; then read the flagged files. Use Grep/Glob, not guesses. Never read `.env` values (note only that config exists).

| Fact to extract | Where to look | Goes into |
|---|---|---|
| Project name, purpose, audience | README, package.json/pyproject/pubspec/pom description, docs/ | Cover, résumé, ch.1 |
| Stack & versions | package.json, requirements/pyproject, pom/gradle, pubspec, go.mod, Dockerfile | Ch.3 tech choices, ch.4 environment table |
| Architecture | top-level dirs, docker-compose services, monorepo packages, routers/controllers layering | Ch.3 architecture + deployment diagram |
| Data model | ORM models, prisma/schema, migrations, SQL, Mongoose schemas, Firestore rules | Ch.3 class/ER diagram, DB schema table |
| API surface | route files, controllers, OpenAPI/swagger, GraphQL schema | Ch.3 endpoint table, sequence diagrams |
| Actors & roles | auth/roles/permissions code, guards, middleware | Ch.2 actors, use cases |
| Features | route/page/screen names, i18n keys, feature folders, tests names | Ch.2 functional needs, backlog; ch.4 sections |
| Non-functional | auth (JWT/OAuth), rate limit, validation, caching, logging, i18n, a11y, perf configs | Ch.2 NFRs, ch.3 security choices |
| Tests | test dirs, coverage config, CI test step; run them if safe → real numbers | Ch.5 results |
| CI/CD, infra | .github/workflows, Dockerfile, k8s, vercel/wrangler config | Ch.4 DevOps section |
| Chronology & effort | `git log --date=short --pretty=format:'%ad %an %s'` , first/last commit, commits per week/author | Planning, Gantt, sprint reconstruction, contribution split |
| Size | LOC by language (script), file count, number of routes/models/components | Ch.4 "en chiffres" box |
| Third-party services | env var names, SDK imports (Stripe, Firebase, Supabase, S3…) | Ch.3 integrations |
| UI | components dir, design tokens, screenshots in repo | Ch.3 mock-ups, ch.4 screenshots |
| Known gaps | TODO/FIXME, open issues, skipped tests | Conclusion limits, perspectives |

## Sprint reconstruction (if Scrum claimed but no records)
Group commits by 2-week windows → derive sprint goals from commit themes. **Ask the user to confirm** the sprints are real before writing them as such; if the team did not use Scrum, say "développement itératif par modules" instead of inventing ceremonies.

## Screenshots
Ask the user for real captures. If the app can run locally (README run steps, dev server), use the `run` skill or Playwright to capture; never mock them up as real. Else placeholder `[CAPTURE À INSÉRER : écran X]`.

## Numbers you may state only if measured
Tests passing, coverage %, build time, Lighthouse score, API latency, dataset size, accuracy — run it or ask. Otherwise omit.

## Monorepo / multiple projects in cwd
Ask which one is the PFA subject. If the cwd is a workspace of many unrelated projects, do not guess.
