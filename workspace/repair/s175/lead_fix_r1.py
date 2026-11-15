#!/usr/bin/env python3
"""Round 1 lead fix (s175, bs-umbilical): the age in the Pearls answer line gets its stem fact (flags MED). Run once from workspace/."""
import json, subprocess
f = subprocess.run(['python3', 'tools/spine/folder_of.py', 'bs-umbilical'], capture_output=True, text=True).stdout.split('\t')[1].strip() + '/rewrite_s175/rewrite_s175.json'
d = json.load(open(f)); loc = d['facts_local']['local']
assert not any(r[0] == 'n9' for r in loc)
loc.append(['n9', loc[0][1], loc[0][2], 'A 2-month-old boy is brought to the physician'])
c = [c for c in d['new_claims'] if 'n1' in c['ids'] and 'n2' in c['ids']]; assert len(c) == 1
c[0]['ids'].append('n9')
json.dump(d, open(f, 'w'), indent=1, ensure_ascii=False)
