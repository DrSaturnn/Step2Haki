#!/usr/bin/env python3
import json, re, sys
d = json.load(sys.stdin)
if not d.get('agent_id'):
    sys.exit(0)                       # the lead is not lane-limited
ti = d.get('tool_input', {})
LANE = '/tmp/claude-0/-home-claude/a21f8c3f-20f3-50ee-8a14-7775eb37231d/scratchpad/lane/'
if d.get('tool_name') in ('Write', 'Edit', 'NotebookEdit'):
    p = ti.get('file_path', '')
    if not p.startswith(LANE):
        print('PROBE LANE: %s may not write %s' % (d.get('agent_type'), p), file=sys.stderr); sys.exit(2)
if d.get('tool_name') == 'Bash':
    c = ti.get('command', '')
    if re.search(r'git\s+(commit|push)|ship\.sh|mac_sync|/\.config/|tools/|index\.html', c):
        print('PROBE LANE: command refused for a subagent', file=sys.stderr); sys.exit(2)
sys.exit(0)
