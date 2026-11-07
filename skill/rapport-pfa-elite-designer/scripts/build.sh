#!/usr/bin/env bash
# Usage: bash build.sh [report_dir]   (default: ./rapport). XeLaTeX via latexmk, falls back to tectonic.
set -u
cd "${1:-rapport}" || { echo "report dir not found"; exit 2; }
if command -v latexmk >/dev/null 2>&1; then
  latexmk -xelatex -interaction=nonstopmode -file-line-error main.tex >build.log 2>&1
else
  tectonic main.tex >build.log 2>&1
fi
rc=$?
grep -E "^(\./)?[^ ]+\.tex:[0-9]+:|^! " build.log | head -20
grep -cE "Overfull \\\\hbox" main.log 2>/dev/null | sed 's/^/overfull hboxes: /'
[ -f main.pdf ] && echo "OK -> $(pwd)/main.pdf" || echo "BUILD FAILED (see build.log)"
exit $rc
