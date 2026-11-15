#!/usr/bin/env python3
"""Wait until the call gate holds every launch of the wave (each launch bound to an agent), up to 90 s; print one line.
python3 repair/s176/wait_hold.py <wave>   (run from workspace/; exit 1 when a launch stays unheld)"""
import json, os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools', 'hooks'))
import common as C
d = os.path.dirname(C.state('agents', 'x'))
for _ in range(45):
    held = set()
    for f in os.listdir(d):
        if f.endswith('.json'):
            try: held.add(json.load(open(os.path.join(d, f))).get('launch'))
            except ValueError: pass
    L = C.launches(sys.argv[1]); free = [l for l in L if l.get('tool_use_id') not in held]
    if not free: break
    time.sleep(2)
print('launches %d, unheld %d%s' % (len(L), len(free), ''.join(' ' + l['lane'].split('/migration/')[-1] for l in free)))
sys.exit(1 if free else 0)
