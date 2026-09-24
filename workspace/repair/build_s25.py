"""s25: 8-question batch; new bs-nat-fracture (peds).
s23: apnea of prematurity (bpd), galactosemia, HAE, short stature backfills; new bs-wilson (GI); vitamin D threshold note (researched).
s20 (derived from build_s19): exanthems brief + neonatal-rash, neonatal-bowel, ig-panel, bs-torch backfills.
s19 docstring follows: UWorld batch (16 questions). Backfills into sjia, abrs-complications, peds-alopecia, factor-inhibitor,
bs-spherocytosis, cgd, vpshunt, neonatal-bowel; new board-style briefs bs-fever-rash-arthralgia (ID), bs-umbilical (GI),
bs-brachial-plexus (MSK), bs-nephritic and bs-abdominal-mass (renal). Drafts: repair/workup/s19_*.json (subagents,
reviewed). Q1 and Q2 were already on the page (s08)."""
import json,html,re,sys
sys.path.insert(0,'tools');from idgen import item_id,option_id;from axlib import parse_html
e=lambda s:html.escape(s,quote=True)
src=open('index.html',encoding='utf-8').read();D=parse_html(src);BR={b.id:src[b.raw_start:b.raw_end] for b in D.briefs}
def load(f):
    x=json.load(open(f'repair/workup/{f}.json'));return x if isinstance(x,list) else [x]
DROP={("bs-brachial-plexus","Maternal diabetes")}
def li(it):
    b,t=it['brief'],it['type'];stem,key,comp,d1,d2=it['stem'],it['key'],it['companion'],it['d1'],it['d2']
    q=item_id(b,t,key,stem);k,o1,o2=option_id(q,'key',key),option_id(q,'d1',d1),option_id(q,'d2',d2)
    nid=it.get('nid');lead=it.get('lead')
    return (f'<li data-type="{t}" data-src="{it.get("src") or "authored"}"'+(f' data-nid="{nid}"' if nid else '')+
            f' data-d1="{e(d1)}" data-d2="{e(d2)}" data-item-id="{q}" data-item-version="1" data-item-status="ready" '
            f'data-key-id="{k}" data-d1-id="{o1}" data-d2-id="{o2}"'+(f' data-lead-in="{e(lead)}"' if lead else '')+
            f'>{e(stem)} &rarr; <b>{e(key)}</b> &rarr; {e(comp)}</li>\n')
def keep(it): return (it['brief'],it['key']) not in DROP
edits=[]
# ---- backfills
for f in ['s25_a','s25_c']:
    for o in load(f):
        for ed in o['edits']:
            edits.append(dict(ed))
        by={}
        for it in o['items']:
            if keep(it): by.setdefault(it['brief'],[]).append(li(it))
        for b,lis in by.items():
            edits.append({"scope":"brief:"+b,"op":"insert_before","anchor":"</ol>","text":''.join(lis),"why":"s25 backfill items"})
PLACE={'peds':'<div class="bsband aqband"><span class="n">5 briefs</span><span class="lbl">Aquifer &middot; Case-Based Briefs</span><p class="t">Pediatrics</p></div>'}
NAV={'peds':'    <a class="bs" href="#bs-learning">Specific Learning Disorder</a>'}
assert src.count(PLACE['peds'])==1 and src.count(NAV['peds'])==1
for o in load('s25_b'):
    h=o['html'].replace('data-shelf="peds fm"','data-shelf="fm peds"')
    shell='<ol class="bank authored">\n</ol>'
    assert h.count(shell)==1
    h=h.replace(shell,'<ol class="bank authored">\n'+''.join(li(it) for it in o['items'])+'</ol>')
    edits.append({"scope":"page","op":"insert_before","anchor":PLACE['peds'],"text":h+"\n\n","why":"new board-style brief bs-nat-fracture (s25)"})
    edits.append({"scope":"page","op":"insert_after","anchor":NAV['peds'],"text":f'\n    <a class="bs" href="#{o["id"]}">{e(o["nav_label"])}</a>',"why":"nav"})
    for rl in o.get('reverse_links',[]):
        print('RL',rl)
        a=rl.get('anchor') or rl.get('anchor_hint');txt=rl.get('sentence')
        t=BR[rl['brief']];assert t.count(a)==1,(rl['brief'],a)
        edits.append({"scope":"brief:"+rl['brief'],"op":"insert_after","anchor":a,"text":' '+txt,"why":"reverse link to bs-nat-fracture"})
old='<div class="bsband"><span class="n">6 briefs</span><span class="lbl">Board-Style &middot; Next-Step Questions</span><p class="t">Pediatrics</p></div>'
assert src.count(old)==1
edits.append({"scope":"page","op":"replace","old":old,"new":old.replace('6 briefs','7 briefs'),"why":"band count"})
m=re.search(r'<h3 class="system" id="peds">.*?</h3>',src);assert '+ 1 board-style' in m.group(0)
edits.append({"scope":"page","op":"replace","old":m.group(0),"new":m.group(0).replace('+ 1 board-style','+ 2 board-style'),"why":"header count"})
json.dump({"pass":"s25","date":"2026-09-23","reason":"s25: 8 UWorld Qs; bs-nat-fracture; backfills neonatal-bowel, newborn-cyanosis, aneuploidy, bs-exanthems, bs-leukemia, cerebral-palsy, nephrotic-child.","expected":{},"edits":edits},
          open('repair/LEDGER-s25.json','w'),indent=1,ensure_ascii=False)
print(len(edits),'edits')
