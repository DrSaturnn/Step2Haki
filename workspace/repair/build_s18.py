"""s18: Diagnostic workup rollout. Drafts in repair/workup/g*.json (subagent drafts, reviewed).
new -> table 'Diagnostic workup' (Test | Order | Result | What it points to; mask col 4) before the brief's
first 'Scenario bank' h5 (else before its first ol.bank). Rows with a blank Test continue the row above
(tbody.grp, aq-bruising style). Skip rows move to the end. extend -> exact replace edits."""
import json,re,sys,glob
sys.path.insert(0,'tools');from axlib import parse_html
src=open('index.html',encoding='utf-8').read();doc=parse_html(src)
B={b.id:src[b.raw_start:b.raw_end] for b in doc.briefs}
drafts=[]
for f in sorted(glob.glob('repair/workup/g*.json')): drafts+=json.load(open(f))
# reviewer fixes
FIX={
 ('thyroid',3):lambda r:['',r[1],r[2],r[3]],
 ('ectopic',2):lambda r:['',r[1],r[2],r[3]],
 ('peutz-jeghers',0):lambda r:[r[0],r[1],'Microcytic anemia, other cell lines <b>normal</b>',r[3]],
 ('osteoporosis',1):lambda r:[r[0],r[1],r[2].replace('-2.5','&minus;2.5'),r[3]],
 ('lipid-screen',6):lambda r:[r[0],r[1],r[2],'Screen younger adults only with risk factors or suspected familial hypercholesterolemia'],
}
def groups(rows):
    g=[]
    for r in rows:
        if r[0].strip()=='' and g: g[-1].append(r)
        else: g.append([r])
    return g
def cell(x): return x
def table(bid,rows):
    rows=[FIX.get((bid,i),lambda r:r)(list(r)) for i,r in enumerate(rows)]
    gs=groups(rows)
    gs=[g for g in gs if g[0][1]!='Skip']+[g for g in gs if g[0][1]=='Skip']
    out=[]
    plain=[]
    def flush():
        if plain: out.append('<tbody>\n'+''.join(plain)+'</tbody>\n'); plain.clear()
    for g in gs:
        trs=''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>\n' for a,b,c,d in g)
        if len(g)>1: flush(); out.append('<tbody class="grp">\n'+trs+'</tbody>\n')
        else: plain.append(trs)
    flush()
    return ('<div class="tw">\n<table data-mask="4"><caption>Diagnostic workup</caption>\n'
            '<thead><tr><th>Test</th><th>Order</th><th>Result</th><th>What it points to</th></tr></thead>\n'+''.join(out)+'</table>\n</div>\n')
edits=[];report=[]
for x in drafts:
    bid=x['brief'];body=B[bid]
    if x['action']=='new':
        for r in x['rows']:
            assert len(r)==4,(bid,r)
            t=''.join(r)
            assert '—' not in t,(bid,r)
            assert not re.search(r'<(?!/?b>)',t),(bid,r)
            assert not re.search(r'&(?![a-zA-Z]+;|#\d+;)',t),(bid,r)
        m=re.search(r'<h5[^>]*>Scenario bank</h5>',body) or re.search(r'<ol class="bank',body)
        anchor=m.group(0) if m.group(0).startswith('<h5') else None
        if anchor is None or body.count(anchor)!=1:
            # fall back to the full opening tag of the first bank list
            anchor=re.search(r'<ol class="bank[^>]*>',body).group(0);assert body.count(anchor)==1,bid
        edits.append({"scope":"brief:"+bid,"op":"insert_before","anchor":anchor,"text":table(bid,x['rows']),"why":"diagnostic workup table"})
        report.append((bid,'new',len(x['rows'])))
    elif x['action']=='extend':
        for e in x['edits']:
            assert body.count(e['old'])==1,(bid,e['old'][:60])
            edits.append({"scope":"brief:"+bid,"op":"replace","old":e['old'],"new":e['new'],"why":"extend with confirmatory step"})
        report.append((bid,'extend',len(x['edits'])))
    else: report.append((bid,x['action'],0))
json.dump({"pass":"s18","date":"2026-09-23","reason":"Diagnostic workup tables page-wide.","expected":{"mcq_delta":0},"edits":edits},
          open('repair/LEDGER-s18.json','w'),indent=1,ensure_ascii=False)
print(len(edits),'edits;',sum(1 for r in report if r[1]=='new'),'new,',sum(1 for r in report if r[1]=='extend'),'extend')
