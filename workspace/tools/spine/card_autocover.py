#!/usr/bin/env python3
"""card_autocover (lead tool, s147): propose dispositions. cards cited by a fact (nid) -> covered by the claims citing that fact.
usage: cardmap.py <folder> [--claims]  writes <folder>/_auto_disp.json (merged later by hand) and prints the uncited cards"""
import json,sys,re,os
d=sys.argv[1]
facts={f['id']:f for f in json.load(open(os.path.join(d,'facts.json')))['facts']}
cm=json.load(open(os.path.join(d,'claim_map.json')))['claims']
by={}
for c in cm:
    for s in c['sources']:
        n=facts.get(s['id'],{}).get('nid')
        if n: by.setdefault(str(n),[]).append(c['id'])
t=open(os.path.join(d,'cards.md')).read()
cards=re.findall(r'^## (?:card|candidate) (\S+)',t,re.M)
blocks=dict(zip(cards,re.split(r'^## (?:card|candidate) \S+.*$',t,flags=re.M)[1:]))
auto={}; un=[]
for n in cards:
    if n in by: auto[n]='covered:%s' % ','.join(sorted(set(by[n]))[:4])
    else: un.append(n)
json.dump(auto,open(os.path.join(d,'_auto_disp.json'),'w'),indent=1)
print('cited',len(auto),'uncited',len(un))
for n in un:
    b=blocks[n]; tx=re.search(r'- card text: (.*)',b); st=re.findall(r'^- \[\S+\] (.*)',b,re.M)
    print(n,'|',(tx.group(1) if tx else '')[:150],'| hy:',' / '.join(x[:60] for x in st[:2]))
if '--claims' in sys.argv:
    for c in cm: print(c['id'],c['new_text'][:90])
