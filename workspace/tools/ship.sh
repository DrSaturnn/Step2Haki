#!/usr/bin/env bash
# One call per batch: build ledger, apply, gate, render, commit, copy deliverables. Prints a short summary.
# Usage: tools/ship.sh <pass> "<commit message>"   (expects repair/build_<pass>.py)
set -e; cd "$(dirname "$0")/.."
P=$1; MSG=$2
python3 repair/build_$P.py | tail -1
timeout 590 python3 repair/apply_ledger.py repair/LEDGER-$P.json 2>&1 | tail -1
python3 tools/gate.py index.html --base 092f98b > /tmp/gate.txt 2>&1 || { cat /tmp/gate.txt | grep -E 'FAIL' ; echo "GATE FAILED: git checkout index.html"; exit 1; }
grep -o 'item ids: [0-9]*\|brief ids: [0-9]*\|blueprint tags: [0-9/]*\|nbme links: [^|]*' /tmp/gate.txt | tr '\n' ' '; echo
node tools/render.js index.html | tail -1 | python3 -c "import json,sys;d=json.loads(sys.stdin.read());print('render mcq',d['mcq'],'malformed',d['malformedMcq'],'errs',len(d['errs']),'dead',len(d['dead']))"
git add -A && git commit -qm "$MSG

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01WVLLhgfkTJRaj2TrMiutSG" && git log --oneline -1
cp index.html OPEN_WORK.md PENDING_DECISIONS.md CURRENT_STATE.md /mnt/user-data/outputs/ 2>/dev/null || true
echo "copied to outputs"
