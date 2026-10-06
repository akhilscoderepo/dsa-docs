#!/bin/sh
# usage: scripts/c20.sh "message" -> add, commit, rebase, push (chapter 20 session)
cd "$(dirname "$0")/.." && git add -A dsa-skills scripts output PROGRESS.md 2>/dev/null
git commit -q -m "$1

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01LTfUKves1uE7MggvjMkL7f" && git pull -q --rebase origin main && git push -q origin HEAD:main; git log --oneline | head -1
