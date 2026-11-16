#!/usr/bin/env python3
"""Find claims whose old text sat in several units (hover kickers such as "Label") and now carry the text of a unit
that does not state their facts; propose the unit whose new text shares most words with the claim's source quotes.

  python3 repair/s173/claims_detect.py <brief id>...   writes local/s173/auto_moves.json
"""
import json, re, subprocess, sys
from bs4 import BeautifulSoup
STOP = set('with from that this have been were which their there about after before should patients patient treatment used also than more most when into other these those such only does drug drugs dose doses risk'.split())

def words(t):
    return {w for w in re.findall(r'[a-z]{4,}', t.lower())} - STOP

def plain(h):
    return ' '.join(BeautifulSoup(h, 'html.parser').get_text(' ').split())

out = {}
for b in sys.argv[1:]:
    f = subprocess.run(['python3', 'tools/spine/folder_of.py', b], capture_output=True, text=True).stdout.split('\t')[1].strip()
    units = json.load(open(f + '/rewrite_s173/units.json'))['units']
    rw = {u['uid']: u for u in json.load(open(f + '/rewrite_s173/rewrite_s173.json'))['units']}
    cb = json.load(open(f + '/claims_before_s173.json')); cl = cb if isinstance(cb, list) else cb['claims']
    C = {c['id']: c for c in cl}
    d = json.load(open(f + '/delta_s173.json'))
    now = {}
    for ch in d['changes']:
        for u in ch.get('claim_updates', []):
            now[u['id']] = ch['uid']
    holders = {}
    for u in units:
        for cid in u.get('claims_in', []):
            holders.setdefault(cid, []).append(u['uid'])
    newtext = {u['uid']: plain(rw[u['uid']]['new']) if u['uid'] in rw and rw[u['uid']]['new'] else u['text'] for u in units}
    mv = {}
    for cid, uid in now.items():
        if uid.startswith('R') or len(holders.get(cid, [])) < 2:
            continue
        q = set()
        for s in C[cid].get('sources', []):
            q |= words(s.get('source_says', ''))
        if len(q) < 3:
            continue
        score = {h: len(q & words(newtext[h])) for h in holders[cid]}
        best = max(score, key=score.get)
        if best != uid and score[best] >= score.get(uid, 0) + 2:
            mv[cid] = best
            print('%s %s: %s (%d) -> %s (%d) "%s"' % (b, cid, uid, score.get(uid, 0), best, score[best], C[cid].get('new_text', '')[:30]))
    out[b] = mv
    print(b, 'moves', len(mv), 'of', sum(1 for c, u in now.items() if len(holders.get(c, [])) > 1), 'shared claims on changed units')
json.dump(out, open('local/s173/auto_moves.json', 'w'), indent=1)
