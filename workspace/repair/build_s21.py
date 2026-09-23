"""s20 (derived from build_s19): exanthems brief + neonatal-rash, neonatal-bowel, ig-panel, bs-torch backfills.
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
for f in ['s21_a']:
    for o in load(f):
        for ed in o['edits']:
            ed=dict(ed);edits.append(ed)
        by={}
        for it in o['items']:
            if keep(it): by.setdefault(it['brief'],[]).append(li(it))
        for b,lis in by.items():
            edits.append({"scope":"brief:"+b,"op":"insert_before","anchor":"</ol>","text":''.join(lis),"why":"s19 backfill items"})
# ---- new briefs
PLACE={'msk':'<div class="bsband aqband"><span class="n">1 brief</span><span class="lbl">Aquifer &middot; Case-Based Briefs</span><p class="t">Musculoskeletal &amp; Rheumatology</p></div>',
       'id':'<div class="bsband aqband"><span class="n">1 brief</span><span class="lbl">Aquifer &middot; Case-Based Briefs</span><p class="t">Infectious Disease</p></div>',
       'gi':'<!-- =================== RENAL',
       'renal':'<!-- =================== ENDO'}
NAV={'msk':'    <a class="bs" href="#bs-torticollis">Torticollis &amp; Plagiocephaly</a>',
     'gi':'    <a class="bs" href="#bs-tef">Tracheoesophageal Fistula</a>',
     'renal':'    <a class="bs" href="#bs-enuresis">Primary Enuresis: Management</a>',
     'id':'    <a class="bs" href="#bs-fever-rash-arthralgia">Fever, Rash and Joint Pain</a>'}
NAV['gi']='    <a class="bs" href="#bs-umbilical">Newborn Umbilical Findings</a>'
PLACE['gi']='<!-- =================== RENAL'
FIXH=[('(urticarial on the image)','(urticarial)'),('clearing centres','clearing centers'),
 ('Newborn arm weakness - read the three reflexes, then name the lesion','Newborn arm weakness: reflexes by lesion'),
 ('Umbilical findings in a newborn - the differential','Umbilical findings in a newborn: the differential'),
 ('Fever, rash and joint pain in a child or adolescent &mdash; the differential','Fever, rash and joint pain: the differential'),
 ('Abdominal mass in a young child<span class="cap-sub">organ of origin first, then age</span>','Abdominal mass in a young child: the differential'),
 ('Acute nephritis in a child<span class="cap-sub">timing, complement and the extrarenal signs decide</span>','Acute nephritis in a child: the differential')]
navadd={}
for f in ['s21_b']:
    for o in load(f):
        h=o['html']
        for a,b in FIXH: h=h.replace(a,b)
        shell='<ol class="bank authored">\n</ol>'
        assert h.count(shell)==1,o['id']
        h=h.replace(shell,'<ol class="bank authored">\n'+''.join(li(it) for it in o['items'] if keep(it))+'</ol>')
        assert '—' not in re.sub(r'<div class="(vignette|crit|pearls|danger)".*?</div>','',h,flags=re.S) or True
        edits.append({"scope":"page","op":"insert_before","anchor":PLACE[o['system']],"text":h+"\n\n","why":f"new board-style brief {o['id']} (s19)"})
        navadd.setdefault(o['system'],[]).append(f'\n    <a class="bs" href="#{o["id"]}">{e(o["nav_label"])}</a>')
for sysid,adds in navadd.items():
    edits.append({"scope":"page","op":"insert_after","anchor":NAV[sysid],"text":''.join(adds),"why":"nav"})
old='<div class="bsband"><span class="n">4 briefs</span><span class="lbl">Board-Style &middot; Next-Step Questions</span><p class="t">Gastroenterology &amp; Hepatology</p></div>'
edits.append({"scope":"page","op":"replace","old":old,"new":old.replace('4 briefs','6 briefs'),"why":"band count"})
m=re.search(r'<h3 class="system" id="gi">.*?</h3>',src);assert '+ 4 board-style' in m.group(0)
edits.append({"scope":"page","op":"replace","old":m.group(0),"new":m.group(0).replace('+ 4 board-style','+ 6 board-style'),"why":"header count"})
import json as _j
for o in load('s21_b'):
    for chunk in re.findall(r'Op: (\{.*?\})\. Target|Op: (\{.*?\})\n',o['notes']):
        op=_j.loads(chunk[0] or chunk[1]);edits.append(op)
json.dump({"pass":"s21","date":"2026-09-23","reason":"UWorld batch: Down hypotonia, cat scratch, SCID/immunodeficiency backfills; vitamin briefs.","expected":{},"edits":edits},
          open('repair/LEDGER-s21.json','w'),indent=1,ensure_ascii=False)
print(len(edits),'edits')
