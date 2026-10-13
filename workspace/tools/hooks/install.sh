#!/bin/bash
# Install the Step2Haki hooks into /home/claude/.claude/settings.json (SPINE_SCALE_PLAN.md section 4; a new container
# has none, T10). Then re-run the tests in plan section A: T1 to T4, T8, T9 (tools/hooks/test_hooks.py covers the
# scripts offline; the live tests need real launches).
set -euo pipefail
H="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
mkdir -p /home/claude/.claude /home/claude/.config/axbx/hooks
chmod 700 /home/claude/.config/axbx /home/claude/.config/axbx/hooks
python3 - "$H" <<'PY'
import json, os, sys
h = sys.argv[1]
p = '/home/claude/.claude/settings.json'
s = json.load(open(p)) if os.path.exists(p) else {}
s['hooks'] = {
  'PreToolUse': [
    {'matcher': 'Agent|Task', 'hooks': [{'type': 'command', 'command': 'python3 %s/agentgate.py' % h}]},
    {'matcher': '', 'hooks': [{'type': 'command', 'command': 'python3 %s/callgate.py' % h}]}],
  'UserPromptSubmit': [{'hooks': [{'type': 'command', 'command': 'python3 %s/approval.py hook' % h}]}]}
json.dump(s, open(p, 'w'), indent=1)
print('hooks installed: %s (H1 agentgate, H2-H4 callgate, G-APPROVE approval hook)' % p)
PY
mkdir -p /home/claude/.claude/agents
cp "$H"/agents/*.md /home/claude/.claude/agents/
echo "agent types installed: $(ls "$H"/agents | tr '\n' ' ')(/home/claude/.claude/agents)"
