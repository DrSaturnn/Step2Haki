#!/usr/bin/env python3
"""Lead fix (s175, bs-umbilical): the head CT line no longer runs ten source words in a row (vendor_scan). Run once from workspace/."""
import json, subprocess
f = subprocess.run(['python3', 'tools/spine/folder_of.py', 'bs-umbilical'], capture_output=True, text=True).stdout.split('\t')[1].strip() + '/rewrite_s175/rewrite_s175.json'
d = json.load(open(f)); a = 'abnormalities such as intracranial hemorrhage or congenital'; b = 'abnormalities (intracranial hemorrhage, congenital'
n = 0
for r in d['raw']:
    if a in r['new']:
        r['new'] = r['new'].replace(a + ' malformations;', b + ' malformations);'); n += 1
for c in d['new_claims']:
    if a in c['text']:
        c['text'] = c['text'].replace(a + ' malformations;', b + ' malformations);'); n += 1
assert n == 2, n
json.dump(d, open(f, 'w'), indent=1, ensure_ascii=False)
