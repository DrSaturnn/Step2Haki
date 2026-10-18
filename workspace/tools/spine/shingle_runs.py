#!/usr/bin/env python3
"""shingle_runs (lead tool, s147): every 10-word run the built brief (above the Practice header) shares with any claim
source quote, all at once (verify shows a few per run).
  python3 tools/spine/shingle_runs.py <brief folder>"""
import sys,re,json,html,os
d=sys.argv[1]
b=open(os.path.join(d,'brief.html')).read()
b=b[:b.find('authored-hdr')]
w=lambda t: re.findall(r"[a-z0-9]+",html.unescape(re.sub('<[^>]+>',' ',t)).lower())
bw=w(b)
cm=json.load(open(os.path.join(d,'claim_map.json')))['claims']
qs={}
for c in cm:
    for s in c['sources']: qs[s['id']]=s['source_says']
sh=set(tuple(bw[i:i+10]) for i in range(len(bw)-9))
hits={}
for k,q in qs.items():
    qw=w(q)
    for i in range(len(qw)-9):
        t=tuple(qw[i:i+10])
        if t in sh: hits.setdefault(k,[]).append(' '.join(t))
for k,v in hits.items():
    # merge overlapping
    print(k, '|', v[0], '...' if len(v)>1 else '', len(v))
