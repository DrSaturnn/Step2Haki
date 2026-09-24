"""s27: four Aquifer symptom-workup briefs (Peds 10, Neuro 10, Peds 29, Peds 31).
s26: 7-question batch; new bs-foodborne (id).
s25: 8-question batch; new bs-nat-fracture (peds).
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
# ---- Aquifer workup briefs
CFG={'peds10':('id','<!-- =================== NEURO','    <a class="aq" href="#bs-febrile-infant">The Febrile Infant</a>'),
     'neuro10':('neuro','<!-- =================== DERM','    <a class="aq" href="#bs-posterior-fossa">Posterior Fossa Localization</a>'),
     'peds29':('peds','<!-- =================== CV','    <a class="aq" href="#bs-preterm-followup">Prematurity Follow-Up</a>'),
     'peds31':('renal','<!-- =================== ENDO',None)}
for k,(sysid,place,nav) in CFG.items():
    o=load('s27_'+k)[0]
    for it in o['items']:
        if it['type']=='avoid' and it.get('lead')=='Which of the following is not indicated?': it['lead']=None
    h=o['html'];shell='<ol class="bank authored">\n</ol>';assert h.count(shell)==1,k
    h=h.replace(shell,'<ol class="bank authored">\n'+''.join(li(it) for it in o['items'])+'</ol>')
    if sysid=='renal':
        h='<div class="bsband aqband"><span class="n">1 brief</span><span class="lbl">Aquifer &middot; Case-Based Briefs</span><p class="t">Renal &amp; Genitourinary</p></div>\n\n'+h
    assert src.count(place)==1
    edits.append({"scope":"page","op":"insert_before","anchor":place,"text":h+"\n\n","why":f"new Aquifer workup brief {o['id']} (s27)"})
    link=f'\n    <a class="aq" href="#{o["id"]}">{e(o["nav_label"])}</a>'
    if nav:
        assert src.count(nav)==1
        edits.append({"scope":"page","op":"insert_after","anchor":nav,"text":link,"why":"nav"})
    else:
        a='    <a class="bs" href="#bs-abdominal-mass">Abdominal mass (Wilms)</a>';assert src.count(a)==1
        edits.append({"scope":"page","op":"insert_after","anchor":a,"text":'\n    <div class="navsub aq">Aquifer</div>'+link,"why":"nav"})
    for rl in o.get('reverse_links',[]):
        t=BR[rl['brief']];assert t.count(rl['anchor'])==1,(k,rl['brief'])
        edits.append({"scope":"brief:"+rl['brief'],"op":"insert_after","anchor":rl['anchor'],"text":' '+rl['sentence'],"why":f"reverse link to {o['id']}"})
# band and header counts
for name,a,b in [('Infectious Disease','1 brief','2 briefs'),('Neurology &amp; HEENT','1 brief','2 briefs'),('Pediatrics','5 briefs','6 briefs')]:
    old=f'<div class="bsband aqband"><span class="n">{a}</span><span class="lbl">Aquifer &middot; Case-Based Briefs</span><p class="t">{name}</p></div>'
    assert src.count(old)==1,name
    edits.append({"scope":"page","op":"replace","old":old,"new":old.replace(a,b),"why":"aquifer band count"})
for sysid,a,b in [('id','+ 1 Aquifer','+ 2 Aquifer'),('neuro','+ 1 Aquifer','+ 2 Aquifer'),('peds','+ 5 Aquifer','+ 6 Aquifer'),('renal','+ 6 board-style</span>','+ 6 board-style</span> <span style="color:#1F6A7E">+ 1 Aquifer</span>')]:
    m=re.search(rf'<h3 class="system" id="{sysid}">.*?</h3>',src);assert a in m.group(0),sysid
    edits.append({"scope":"page","op":"replace","old":m.group(0),"new":m.group(0).replace(a,b),"why":"header count"})
json.dump({"pass":"s27","date":"2026-09-23","reason":"s27: Aquifer workup briefs aq-infant-fever, aq-child-headache, aq-infant-hypotonia, aq-puffy-eyes; renal Aquifer band.","expected":{},"edits":edits},
          open('repair/LEDGER-s27.json','w'),indent=1,ensure_ascii=False)
print(len(edits),'edits')
