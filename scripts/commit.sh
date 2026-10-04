#!/bin/sh
# usage: scripts/commit.sh "message" -> add, commit with attribution, rebase, push
cd "$(dirname "$0")/.." && git add -A dsa-skills scripts output PROGRESS.md 2>/dev/null
git commit -q -m "$1

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01TN8bZJJSHyKNZF9kUc3HNp" && git pull -q --rebase origin main && git push -q origin HEAD:main; git log --oneline | head -1
