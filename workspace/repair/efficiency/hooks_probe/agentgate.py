#!/usr/bin/env python3
import json, sys
d = json.load(sys.stdin)
if d.get('tool_name') in ('Agent', 'Task'):
    ti = d.get('tool_input', {})
    if not ti.get('model'):
        print('PROBE GATE: launch refused: no model named', file=sys.stderr)
        sys.exit(2)
sys.exit(0)
