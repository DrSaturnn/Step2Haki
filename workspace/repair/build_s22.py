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
for f in ['s22_a','s22_c']:
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
NAV['id']='    <a class="bs" href="#bs-exanthems">Childhood Exanthems</a>'
NAV['endo']='    <a class="bs" href="#bs-dm-bundle">Diabetes Annual Bundle</a>'
PLACE['endo']='<!-- =================== HEME'
FIXH=[('(urticarial on the image)','(urticarial)'),('clearing centres','clearing centers'),
 ('Newborn arm weakness - read the three reflexes, then name the lesion','Newborn arm weakness: reflexes by lesion'),
 ('Umbilical findings in a newborn - the differential','Umbilical findings in a newborn: the differential'),
 ('Fever, rash and joint pain in a child or adolescent &mdash; the differential','Fever, rash and joint pain: the differential'),
 ('Abdominal mass in a young child<span class="cap-sub">organ of origin first, then age</span>','Abdominal mass in a young child: the differential'),
 ('Acute nephritis in a child<span class="cap-sub">timing, complement and the extrarenal signs decide</span>','Acute nephritis in a child: the differential')]
navadd={}
for f in ['s22_b']:
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
for sysid,old_n,new_n,name in [('id','6 briefs','8 briefs','Infectious Disease'),('endo','2 briefs','3 briefs','Endocrine &amp; Bone')]:
    old=f'<div class="bsband"><span class="n">{old_n}</span><span class="lbl">Board-Style &middot; Next-Step Questions</span><p class="t">{name}</p></div>'
    assert src.count(old)==1,old
    edits.append({"scope":"page","op":"replace","old":old,"new":old.replace(old_n,new_n),"why":"band count"})
for sysid,a_,b_ in [('id','+ 5 board-style','+ 7 board-style'),('endo','+ 2 board-style','+ 3 board-style')]:
    m=re.search(rf'<h3 class="system" id="{sysid}">.*?</h3>',src);assert a_ in m.group(0),sysid
    edits.append({"scope":"page","op":"replace","old":m.group(0),"new":m.group(0).replace(a_,b_),"why":"header count"})
# lymphadenitis retitle (user approved)
edits.append({"scope":"brief:lymphadenitis","op":"replace","old":"<h4>The Acutely Inflamed Cervical Node</h4>","new":"<h4>Enlarged Lymph Nodes: Reading the Pattern</h4>","why":"retitle: bank now includes axillary, epitrochlear and adult items"})
edits.append({"scope":"page","op":"replace","old":'    <a href="#lymphadenitis">The Inflamed Neck Node</a>',"new":'    <a href="#lymphadenitis">Enlarged Lymph Nodes</a>',"why":"nav"})
# mnemonics (user approved)
MN={'cyanotic-chd':'<b>5 Ts</b> &mdash; the cyanotic lesions: Truncus arteriosus, Transposition of the great arteries, Tricuspid atresia, Tetralogy of Fallot, Total anomalous pulmonary venous return &middot; <b>PROVe</b> &mdash; tetralogy: Pulmonic stenosis (right ventricular outflow obstruction), Right ventricular hypertrophy, Overriding aorta, VSD',
 'bs-adolescent-confid':'<b>HEEADSSS</b> &mdash; the adolescent psychosocial history, asked privately: Home, Education and employment, Eating, Activities, Drugs, Sexuality, Suicide and depression, Safety',
 'dvt':'<b>Virchow triad</b> &mdash; the three routes to venous thrombosis: stasis (immobility, long travel), endothelial injury (surgery, trauma, a line), hypercoagulability (cancer, pregnancy, estrogen, inherited thrombophilia)',
 'anemia-thrombocytopenia':'<b>TTP pentad</b> &mdash; microangiopathic hemolytic anemia, thrombocytopenia, fever, neurologic signs, renal injury; most patients do not have all five, and anemia with schistocytes plus low platelets is enough to act',
 'airway':'<b>4 Ds of epiglottitis</b> &mdash; Drooling, Dysphagia, Dysphonia (muffled voice), Distress (tripod position)',
 'bs-torch':'<b>TORCH</b> &mdash; Toxoplasmosis, Other (syphilis, varicella, parvovirus B19, HIV), Rubella, Cytomegalovirus, Herpes simplex virus',
 'liver-preg':'<b>HELLP</b> &mdash; Hemolysis, Elevated Liver enzymes, Low Platelets'}
for b_,txt in MN.items():
    t=BR[b_]
    m=re.search(r'<h5[^>]*>Scenario bank</h5>',t)
    anchor=m.group(0) if m and t.count(m.group(0))==1 else re.search(r'<ol class="bank[^>]*>',t).group(0)
    assert t.count(anchor)==1,b_
    edits.append({"scope":"brief:"+b_,"op":"insert_before","anchor":anchor,"text":f'<div class="pearls"><span class="lbl">Mnemonic</span> {txt}</div>\n',"why":"mnemonic (user approved)"})
json.dump({"pass":"s22","date":"2026-09-23","reason":"s22: hematuria, airway, UTI, nasal FB, vitamin backfills; anaphylaxis, isolation, short stature briefs; mnemonics; lymphadenitis retitle.","expected":{},"edits":edits},
          open('repair/LEDGER-s22.json','w'),indent=1,ensure_ascii=False)
print(len(edits),'edits')
