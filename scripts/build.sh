#!/bin/sh
# usage: scripts/build.sh NN "Title" -> full audit, stamp, build, HTML audit, smoke, render. Output: output/<chapter>.html
set -e
ROOT=$(cd "$(dirname "$0")/.." && pwd); cd "$ROOT/dsa-skills"; SP="$ROOT/.scratch"
D=$(ls -d manuscripts/$1-* | head -1); B=$(basename "$D"); OUT="$ROOT/output"
mkdir -p "$OUT" "$SP/stamps" "$SP/shots/$1"
python3 dsa-curriculum-auditor/scripts/audit_manuscripts.py "$D" --spec chapter-specs/$B.md --workdir "$SP/jw" --update-ids --stamp "$SP/stamps/$1.json" > "$SP/stamps/$1.audit.txt" 2>&1 || true
tail -4 "$SP/stamps/$1.audit.txt"
python3 markdown-textbook-html/scripts/build_html.py "$D" -o "$OUT/$B.html" --chapter $1 --title "$2" --validation "$SP/stamps/$1.json"
python3 dsa-curriculum-auditor/scripts/audit_html.py "$OUT/$B.html" --manuscripts "$D" --smoke --stamp "$SP/stamps/$1.json"
node dsa-curriculum-auditor/scripts/render_check.mjs "$OUT/$B.html" "$SP/shots/$1" 2>&1 | grep -E "FAIL|all checks|SKIPPED"
