#!/usr/bin/env python3
"""Give each claim of a removed block to the carrier unit whose added lines hold most of its words.

  python3 repair/s173/claims_to_carrier.py <FOLDER>...     (folders under repair/migration/pharm)
"""
import json, re, sys
from bs4 import BeautifulSoup

def words(t):
    return {w for w in re.findall(r'[a-z0-9]+', t.lower()) if len(w) > 3}

def plain(h):
    return ' '.join(BeautifulSoup(h, 'html.parser').get_text(' ').split())

for f in sys.argv[1:]:
    d = 'repair/migration/pharm/%s/spine/' % f
    j = json.load(open(d + 'rewrite_s173/rewrite_s173.json'))
    base = {u['uid']: u for u in json.load(open(d + 'rewrite_s173/units.json'))['units']}
    cb = json.load(open(d + 'claims_before_s173.json'))
    cl = cb if isinstance(cb, list) else cb.get('claims', cb)
    text = {c['id']: c.get('new_text') or c.get('text') or '' for c in (cl if isinstance(cl, list) else cl.values())}
    U = {u['uid']: u for u in j['units']}
    for r in j['raw']:
        car = [c for c in r.get('carried_by', []) if c in U]
        if len(car) < 2:
            continue
        added = {c: words(plain(U[c]['new'])) - words(base[c]['text']) for c in car}
        keep = []
        for cid in r.get('claims', []):
            w = words(text.get(cid, ''))
            score = {c: len(w & added[c]) for c in car}
            best = max(car, key=lambda c: score[c])
            if len(w) < 2 or score[best] == 0:
                keep.append(cid); continue
            u = U[best]
            u['claims'] = sorted(set(u.get('claims') or base[best].get('claims_in', [])) | {cid})
            for c in car:
                if c != best and U[c].get('claims'):
                    U[c]['claims'] = [x for x in U[c]['claims'] if x != cid]
            print(f, cid, '->', best, score)
        r['claims'] = keep
        print(f, 'left on the raw:', keep)
    json.dump(j, open(d + 'rewrite_s173/rewrite_s173.json', 'w'), ensure_ascii=False, indent=1)
