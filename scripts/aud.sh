#!/bin/sh
# usage: scripts/aud.sh NN   (draft audit of manuscripts/NN-*; hides expected draft-only noise)
ROOT=$(cd "$(dirname "$0")/.." && pwd); cd "$ROOT/dsa-skills"; SP="$ROOT/.scratch"; mkdir -p "$SP"
D=$(ls -d manuscripts/$1-* | head -1)
python3 dsa-curriculum-auditor/scripts/audit_manuscripts.py "$D" --spec chapter-specs/$(basename "$D").md --draft --workdir "$SP/jw" 2>&1 | grep -v "spec-lesson-missing\|has no manuscript lesson\|missing-section\|chapter has no '\|no-human-review\|review-log.md"
