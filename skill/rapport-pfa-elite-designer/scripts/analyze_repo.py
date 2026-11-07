"""Read-only repo fact extractor for the PFA report. Usage: python analyze_repo.py <dir> > facts.json
Never reads .env values. Heuristic (ponytail: regex route/model sniffing; upgrade to AST/graph tools if a repo needs depth)."""
import json, os, re, subprocess, sys
from collections import Counter
from pathlib import Path

SKIP = {".git", "node_modules", "dist", "build", ".next", "venv", ".venv", "__pycache__", "target", ".gradle", ".idea", "vendor", "coverage", "rapport"}
LANG = {".py": "Python", ".js": "JavaScript", ".jsx": "JavaScript", ".ts": "TypeScript", ".tsx": "TypeScript", ".java": "Java", ".kt": "Kotlin",
        ".dart": "Dart", ".go": "Go", ".rs": "Rust", ".php": "PHP", ".cs": "C#", ".c": "C", ".cpp": "C++", ".swift": "Swift", ".rb": "Ruby",
        ".sql": "SQL", ".html": "HTML", ".css": "CSS", ".scss": "CSS", ".vue": "Vue", ".ino": "Arduino C++", ".ipynb": "Notebook"}
MANIFESTS = ["package.json", "requirements.txt", "pyproject.toml", "pom.xml", "build.gradle", "build.gradle.kts", "pubspec.yaml", "go.mod",
             "Cargo.toml", "composer.json", "Gemfile", "Dockerfile", "docker-compose.yml", "docker-compose.yaml", "platformio.ini"]
ROUTE = re.compile(r"""(?:@(?:Get|Post|Put|Patch|Delete)Mapping|@(?:Get|Post|Put|Patch|Delete)\(|\.(?:get|post|put|patch|delete)\(\s*['"`]|@(?:app|router|bp)\.(?:get|post|put|patch|delete|route)\(|path\(\s*['"]|Route::(?:get|post|put|delete)\()[^\n]{0,80}""")
MODEL = re.compile(r"^\s*(?:class\s+(\w+)\((?:[\w.]*Model|Base|db\.Model)\)|model\s+(\w+)\s*\{|@Entity|interface\s+(\w+Schema)|const\s+(\w+)Schema\s*=)", re.M)

def walk(root):
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in SKIP]
        for f in fn:
            yield Path(dp) / f

def git(root, *a):
    try:
        return subprocess.run(["git", "-C", str(root), *a], capture_output=True, text=True, timeout=30).stdout.strip()
    except Exception:
        return ""

def main(root):
    root = Path(root).resolve()
    langs, loc, files, tests, routes, models, manifests, ci = Counter(), Counter(), 0, [], [], [], {}, []
    for p in walk(root):
        files += 1
        rel = p.relative_to(root).as_posix()
        if p.name in MANIFESTS and len(manifests) < 12:
            manifests[rel] = p.read_text(errors="ignore")[:1500]
        if ".github/workflows" in rel or p.name in (".gitlab-ci.yml", "Jenkinsfile"):
            ci.append(rel)
        lang = LANG.get(p.suffix.lower())
        if not lang:
            continue
        try:
            txt = p.read_text(errors="ignore")
        except Exception:
            continue
        langs[lang] += 1
        loc[lang] += txt.count("\n") + 1
        if re.search(r"(^|/)(tests?|__tests__|spec)(/|$)|\.(test|spec)\.|_test\.", rel):
            tests.append(rel)
        if len(routes) < 80:
            for m in ROUTE.finditer(txt):
                routes.append({"file": rel, "hit": m.group(0).strip()[:90]})
                if len(routes) >= 80: break
        if len(models) < 60:
            for m in MODEL.finditer(txt):
                models.append({"file": rel, "name": next((g for g in m.groups() if g), "Entity")})
    readme = next((p for p in (root / n for n in ("README.md", "readme.md", "README.rst", "README")) if p.exists()), None)
    log = git(root, "log", "--date=short", "--pretty=format:%ad|%an|%s")
    commits = [l.split("|", 2) for l in log.splitlines()] if log else []
    by_month = Counter(c[0][:7] for c in commits)
    todos = git(root, "grep", "-nE", "TODO|FIXME", "--", ".")[:2000] if commits else ""
    out = {
        "root": str(root), "files": files, "languages_files": langs, "languages_loc": loc,
        "manifests": manifests, "ci": ci, "tests": {"count": len(tests), "samples": tests[:15]},
        "routes_sample": routes, "models_sample": models,
        "top_dirs": sorted(d.name for d in root.iterdir() if d.is_dir() and d.name not in SKIP)[:30],
        "env_files_present": [p.name for p in root.iterdir() if p.name.startswith(".env")],
        "readme_head": readme.read_text(errors="ignore")[:2500] if readme else None,
        "git": {"commits": len(commits), "first": commits[-1][0] if commits else None, "last": commits[0][0] if commits else None,
                "authors": Counter(c[1] for c in commits).most_common(8), "commits_per_month": dict(sorted(by_month.items())),
                "recent_subjects": [c[2] for c in commits[:25]]},
        "todo_fixme": todos,
    }
    json.dump(out, sys.stdout, ensure_ascii=False, indent=1, default=dict)

if __name__ == "__main__":
    if len(sys.argv) != 2 or not os.path.isdir(sys.argv[1]):
        sys.exit("usage: python analyze_repo.py <project_dir>")
    main(sys.argv[1])
