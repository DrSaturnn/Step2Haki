"""s23: apnea of prematurity (bpd), galactosemia, HAE, short stature backfills; new bs-wilson (GI); vitamin D threshold note (researched).
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
for f in ['s23_a']:
    for o in load(f):
        for ed in o['edits']:
            edits.append(dict(ed))
        by={}
        for it in o['items']:
            if keep(it): by.setdefault(it['brief'],[]).append(li(it))
        for b,lis in by.items():
            edits.append({"scope":"brief:"+b,"op":"insert_before","anchor":"</ol>","text":''.join(lis),"why":"s23 backfill items"})
PLACE={'gi':'<!-- =================== RENAL'}
NAV={'gi':'    <a class="bs" href="#bs-water-soluble-vitamins">Water-Soluble Vitamins</a>'}
FIXH=[('Wilson Disease: Liver Disease with Neuropsychiatric Signs','Wilson Disease: Copper in the Liver, Brain and Eye')]
navadd={}
for o in load('s23_b'):
    h=o['html']
    for a,b in FIXH: h=h.replace(a,b)
    h=re.sub(r'<tr><td>Serum total copper</td>.*?</tr>\n?','',h,flags=re.S)
    shell='<ol class="bank authored">\n</ol>'
    assert h.count(shell)==1,o['id']
    h=h.replace(shell,'<ol class="bank authored">\n'+''.join(li(it) for it in o['items'] if keep(it))+'</ol>')
    edits.append({"scope":"page","op":"insert_before","anchor":PLACE[o['system']],"text":h+"\n\n","why":f"new board-style brief {o['id']} (s23)"})
    navadd.setdefault(o['system'],[]).append(f'\n    <a class="bs" href="#{o["id"]}">{e(o["nav_label"])}</a>')
    rl=o['reverse_links'][0]
    blk=rl['suggested_block']
    for a,b in FIXH: blk=blk.replace(a,b)
    edits.append({"scope":"brief:masld","op":"insert_after","anchor":'Kayser-Fleischer rings</b> → Wilson disease.</div>',"text":'\n'+blk,"why":"reverse link to bs-wilson"})
for sysid,adds in navadd.items():
    edits.append({"scope":"page","op":"insert_after","anchor":NAV[sysid],"text":''.join(adds),"why":"nav"})
old='<div class="bsband"><span class="n">6 briefs</span><span class="lbl">Board-Style &middot; Next-Step Questions</span><p class="t">Gastroenterology &amp; Hepatology</p></div>'
assert src.count(old)==1
edits.append({"scope":"page","op":"replace","old":old,"new":old.replace('6 briefs','7 briefs'),"why":"band count"})
m=re.search(r'<h3 class="system" id="gi">.*?</h3>',src);assert '+ 6 board-style' in m.group(0)
edits.append({"scope":"page","op":"replace","old":m.group(0),"new":m.group(0).replace('+ 6 board-style','+ 7 board-style'),"why":"header count"})
# vitamin D thresholds: researched 2026-09 (NASEM 2011 via NIH ODS; Global Consensus on rickets 2016; Endocrine Society 2011 and 2024)
V='brief:bs-fat-soluble-vitamins'
edits.append({"scope":V,"op":"replace","old":"(two thresholds in use; UWorld cites both)","new":"(two threshold sets appear in questions; see the note below)","why":"vit D note"})
edits.append({"scope":V,"op":"replace","old":"(Endocrine Society cutoffs)","new":"(Endocrine Society 2011 cutoffs, withdrawn in 2024)","why":"vit D: ES 2024 no longer endorses cutoffs"})
edits.append({"scope":V,"op":"replace","old":"by the other cutoff in use, <b>under 20</b> deficient, 20 to 30 insufficient","new":"by the older Endocrine Society 2011 set, <b>under 20</b> deficient, 20 to 30 insufficient","why":"vit D"})
NOTE=('<div class="pearls"><span class="lbl">Vitamin D thresholds: current status (checked Sept 2026)</span> '
 '<b>In force:</b> the National Academies (IOM 2011) cutoffs, still used by the NIH Office of Dietary Supplements and matched by the 2016 Global Consensus on nutritional rickets: 25-hydroxyvitamin D <b>under 12 ng/mL (30 nmol/L)</b> is deficient, <b>12 to under 20</b> is inadequate, <b>20 or more</b> is adequate, and over 50 ng/mL carries risk of harm &middot; '
 '<b>Retired:</b> the Endocrine Society 2011 set (under 20 deficient, 21 to 29 insufficient, 30 to 100 sufficient). The Endocrine Society&#39;s 2024 guideline no longer endorses any cutoff or a target of 30, and advises <b>against routine testing</b> in healthy people &middot; '
 '<b>2024 empiric supplementation</b> above the daily allowance: ages 1 to 18, over 75, pregnancy and high-risk prediabetes; adults 19 to 74 take only the usual allowance (600 IU, 800 IU over 70) &middot; '
 '<b>Unchanged:</b> 400 IU daily for every infant in the first year, and treatment of symptomatic deficiency (rickets, osteomalacia) whatever the cutoff &middot; '
 '<b>On the exam:</b> older questions may use the 20 and 30 cutoffs; read the level against the symptoms, not against a single number</div>\n')
edits.append({"scope":V,"op":"insert_before","anchor":'<h5 class="authored-hdr">Scenario bank</h5>',"text":NOTE,"why":"vit D threshold note, researched (NIH ODS; Global Consensus 2016; Endocrine Society 2011/2024)"})
json.dump({"pass":"s23","date":"2026-09-23","reason":"s23: apnea of prematurity, galactosemia, HAE, short stature backfills; bs-wilson; vitamin D threshold note.","expected":{},"edits":edits},
          open('repair/LEDGER-s23.json','w'),indent=1,ensure_ascii=False)
print(len(edits),'edits')
