#!/usr/bin/env python3
"""List the agents the call gate holds for a wave: role, lane, calls used of budget.  python3 repair/s175/holds.py <wave>"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools', 'hooks'))
import common as C
d = os.path.dirname(C.state('agents', 'x')); tot = 0
for f in sorted(os.listdir(d)):
    if f.endswith('.json'):
        j = json.load(open(os.path.join(d, f)))
        if j.get('wave') == sys.argv[1]:
            tot += j['count']
            print('%-18s %-22s %3d of %s' % (j['role'], j['lane'].split('/migration/')[-1].replace('/spine', '').split('/lanes/')[-1], j['count'], j['budget']))
print('launches %d, calls %d' % (len(C.launches(sys.argv[1])), tot))
