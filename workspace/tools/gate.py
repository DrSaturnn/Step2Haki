"""Duplicate and identity gate. Canary always runs; diagnostics only on failure.
Usage: python3 tools/gate.py index.html [--base <git-rev>]"""
import sys,re,html,subprocess,collections,time
sys.path.insert(0,'tools');import axlib
t0=time.perf_counter()
path=sys.argv[1];base=sys.argv[sys.argv.index('--base')+1] if '--base' in sys.argv else None
src=open(path,encoding='utf-8').read();doc=axlib.parse_html(src)
items=list(doc.items);briefs=list(doc.briefs);fail=[]
def canary(name,vals):
    n,d=len(vals),len(set(vals))
    if n!=d: fail.append((name,[k for k,v in collections.Counter(vals).items() if v>1]))
    return f"{name}: {n}/{d}"
norm=lambda s:re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]+>','',s or ''))).strip().lower()
seg=lambda it:[norm(p) for p in re.split(r'\s*(?:→|&rarr;)\s*',it.raw_html.split('>',1)[1].rsplit('</li>',1)[0])]
out=[]
# 1-3: the three corpus id spaces (parser-based: script text is never an element, so no JS-literal miscount)
out.append(canary('item ids',[i.attr_map['data-item-id'] for i in items]))
out.append(canary('option ids',[i.attr_map[k] for i in items for k in('data-key-id','data-d1-id','data-d2-id')]))
out.append(canary('brief ids',[b.id for b in briefs]))
# 4: within-item answerability: 3 distinct option ids AND 3 distinct option texts
bad=[]
for i in items:
    a=i.attr_map;s=seg(i)
    key=norm(a.get('data-label-answer')) or (s[1] if len(s)>1 else '')
    txt=[key,norm(a.get('data-d1')),norm(a.get('data-d2'))]
    ids=[a['data-key-id'],a['data-d1-id'],a['data-d2-id']]
    if len(set(ids))<3 or len(set(txt))<3 or '' in txt: bad.append((a['data-item-id'],txt))
out.append(f"answerable items: {len(items)-len(bad)}/{len(items)}")
if bad: fail.append(('unanswerable',bad[:10]))
# 5: permanence -- no existing item or brief id may disappear
if base:
    old=subprocess.run(['git','show',f'{base}:{path}'],capture_output=True,text=True).stdout
    od=axlib.parse_html(old)
    lost_i={i.attr_map['data-item-id'] for i in od.items}-{i.attr_map['data-item-id'] for i in items}
    lost_b={b.id for b in od.briefs}-{b.id for b in briefs}
    out.append(f"permanence vs {base}: lost items {len(lost_i)}, lost briefs {len(lost_b)}")
    if lost_i or lost_b: fail.append(('lost ids',sorted(lost_i|lost_b)[:20]))
# 6: question-level duplicates -- nid reused on two different items
nids=[(n,i.attr_map['data-item-id']) for i in items for n in (i.attr_map.get('data-nid') or '').split()]
nmap=collections.defaultdict(set)
for n,q in nids: nmap[n].add(q)
dn={n:q for n,q in nmap.items() if len(q)>1}
out.append(f"nids: {len(nmap)} distinct on items, reused {len(dn)}")
# 7: content near-duplicates -- same keyed answer + near-identical stem, via an inverted index (no pairwise loop)
def sh(t):
    w=re.findall(r'[a-z0-9]+',t);return {' '.join(w[k:k+4]) for k in range(max(1,len(w)-3))}
S={};idx=collections.defaultdict(set)
for i in items:
    s=seg(i);q=i.attr_map['data-item-id'];S[q]=(sh(s[0]),s[1] if len(s)>1 else '')
    for g in S[q][0]: idx[g].add(q)
pairs=collections.Counter()
for g,qs in idx.items():
    if len(qs)<2 or len(qs)>40: continue
    qs=sorted(qs)
    for x in range(len(qs)):
        for y in range(x+1,len(qs)): pairs[(qs[x],qs[y])]+=1
near=[]
for (x,y),c in pairs.items():
    j=c/len(S[x][0]|S[y][0])
    if j>=0.6 and S[x][1]==S[y][1]: near.append((round(j,2),x,y))
out.append(f"near-duplicate items (same key, stem Jaccard>=0.6): {len(near)}")
# 8: blueprint tags -- once any brief is tagged, every brief needs one valid primary system
import json,os,csv
try: CODES=set(json.load(open('repair/nbme/outlines.json'))['codes'])
except Exception: CODES=set()
bp=[(b.id,(b.attr_map.get('data-bp') or '').split()) for b in briefs]
if CODES and any(v for _,v in bp):
    badbp=[bid for bid,v in bp if not v or len(v)>2 or any(c not in CODES for c in v)]
    out.append(f"blueprint tags: {len(bp)-len(badbp)}/{len(bp)}")
    if badbp: fail.append(('blueprint tag missing or invalid',badbp[:20]))
# 9: NBME links -- every data-nbme id on an item has a coverage row naming that item, and the reverse
covp='repair/nbme/coverage.csv'
if os.path.exists(covp):
    rows=list(csv.DictReader(open(covp,encoding='utf-8')))
    page={(n,i.attr_map['data-item-id']) for i in items for n in (i.attr_map.get('data-nbme') or '').split()}
    filed={(r['nbme_id'],r['item_id']) for r in rows if r.get('item_id')}
    allids={i.attr_map['data-item-id'] for i in items}
    orphan_page=sorted(page-filed);orphan_file=sorted(x for x in filed-page)
    ghost=[r['item_id'] for r in rows if r.get('item_id') and r['item_id'] not in allids]
    fp=collections.Counter(r['fingerprint'] for r in rows if r.get('fingerprint') and not r.get('same_as'))
    dupfp=[k for k,v in fp.items() if v>1]
    out.append(f"nbme links: {len(page)} on page, {len(filed)} filed")
    if orphan_page or orphan_file or ghost: fail.append(('nbme link mismatch',{'page_only':orphan_page[:10],'file_only':orphan_file[:10],'no_such_item':ghost[:10]}))
    if dupfp: fail.append(('nbme fingerprint repeated without same_as',dupfp[:10]))
# 10: attribute-only pass -- with --attr-only <rev>, no existing item may change text, options, ids or version
if '--attr-only' in sys.argv:
    ref=sys.argv[sys.argv.index('--attr-only')+1]
    od=axlib.parse_html(subprocess.run(['git','show',f'{ref}:{path}'],capture_output=True,text=True).stdout)
    KEEP=('data-type','data-d1','data-d2','data-item-version','data-key-id','data-d1-id','data-d2-id','data-lead-in','data-item-status')
    sig=lambda i:(tuple(i.attr_map.get(k) for k in KEEP),seg(i))
    oldm={i.attr_map['data-item-id']:sig(i) for i in od.items}
    changed=[q for q,v in ((i.attr_map['data-item-id'],sig(i)) for i in items) if q in oldm and oldm[q]!=v]
    out.append(f"attr-only vs {ref}: {len(changed)} items changed")
    if changed: fail.append(('attribute-only pass changed item content',changed[:10]))
print(' | '.join(out));print(f"{(time.perf_counter()-t0)*1000:.0f} ms")
for f in fail: print('FAIL',f)
for n in sorted(near,reverse=True)[:15]: print('NEAR',n)
if dn: print('NID REUSED',list(dn.items())[:10])
sys.exit(1 if fail else 0)
