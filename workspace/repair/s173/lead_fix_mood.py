#!/usr/bin/env python3
"""mood-anticonv rewrite file: name the removed question block's claims on its raw, the label claims included."""
import json

D = 'repair/migration/pharm/MOOD/spine/'
P = D + 'rewrite_s173/rewrite_s173.json'
j = json.load(open(P, encoding='utf-8'))
u = json.load(open(D + 'rewrite_s173/units.json', encoding='utf-8'))
units = u['units'] if isinstance(u, dict) else u
base = open(D + 'baseline_s173.html', encoding='utf-8').read()
LABELS = ['S315', 'S317', 'S319', 'S323', 'S325', 'S327', 'S331', 'S333', 'S335', 'S339', 'S341', 'S343']
for r in j['raw']:
    if 'pc-nbq' in r['old']:
        s = base.index(r['old']); e = s + len(r['old'])
        inside = sorted({c for x in units if s <= x['start'] and x['end'] <= e for c in (x.get('claims_in') or [])})
        r['claims'] = sorted(set(inside) | set(LABELS))
        print('claims', len(r['claims']))
json.dump(j, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
