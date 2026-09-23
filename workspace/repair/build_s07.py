import json,html,sys,re
sys.path.insert(0,'tools');from idgen import item_id,option_id
e=lambda s:html.escape(s,quote=True)
edits=[]
def li(b,t,stem,key,comp,d1,d2,lead=None,src="authored",nid=None):
    q=item_id(b,t,key,stem);k,o1,o2=option_id(q,'key',key),option_id(q,'d1',d1),option_id(q,'d2',d2)
    return (f'<li data-type="{t}" data-src="{src}"'+(f' data-nid="{nid}"' if nid else '')+f' data-d1="{e(d1)}" data-d2="{e(d2)}" data-item-id="{q}" data-item-version="1" '
        f'data-item-status="ready" data-key-id="{k}" data-d1-id="{o1}" data-d2-id="{o2}"'+(f' data-lead-in="{e(lead)}"' if lead else '')+
        f'>{e(stem)} &rarr; <b>{e(key)}</b>'+(f' &rarr; {e(comp)}' if comp else '')+'</li>\n')
def item(b,*a,**k):
    edits.append({"scope":"brief:"+b,"op":"insert_before","anchor":"</ol>","text":li(b,*a,**k),"why":"backfill item"+(f" (source nid {k['nid']})" if k.get('nid') else "")})
def parts(ps): return ' &middot; '.join(f'<b>{e(t)}</b> &mdash; {e(d)}' for t,d in ps)
src=open('index.html').read()

# ---------- 1. PDA: rewrite the bs-murmur-map copy as a murmur-reading dx variant (ids kept, v2)
old=re.search(r'<li [^>]*data-item-id="q_3f503b9a2dee51438e7c"[^>]*>.*?</li>',src).group(0)
new=('<li data-type="dx" data-src="authored" data-d1="Aortic regurgitation" data-d2="Ventricular septal defect" '
     'data-item-id="q_3f503b9a2dee51438e7c" data-item-version="2" data-item-status="ready" data-key-id="o_c452375e56f65d26b1b6" '
     'data-d1-id="o_9dee98f6a1655fa98a35" data-d2-id="o_b154a6ac060458649db4">2 yo with a continuous machine-like murmur below the left clavicle '
     'that runs through S2, bounding pulses and a wide pulse pressure &rarr; <b>Patent ductus arteriosus</b> &rarr; the only murmur that crosses a heart sound</li>')
edits.append({"scope":"brief:bs-murmur-map","op":"replace","old":old,"new":new,
 "why":"was a word-for-word twin of q_9696867d34855f3c8457 in bs-shunt-timing (treatment). This brief teaches murmur reading, so the copy becomes a dx variant keyed on the murmur; ids kept, version 2."})

# ---------- 2. Neonatal polycythemia -> bs-nrd
NP="1516823438451 1516823700116 1516932371546 1538073399623 1556397078881"
edits.append({"scope":"brief:bs-nrd","op":"insert_before","anchor":"</tbody>","text":
 '<tr><td>Neonatal polycythemia</td><td>Intrauterine hypoxia (preeclampsia, maternal diabetes or hypertension, smoking, growth restriction) or placental transfusion (delayed cord clamping, twin-twin transfusion)</td>'
 '<td><b>Plethora with hypoglycemia</b> and a clear chest film; venous hematocrit above 65%</td></tr>\n',
 "why":f"source nid {NP.split()[0]}: tachypnea from hyperviscosity belongs in this differential"})
edits.append({"scope":"brief:bs-nrd","op":"insert_before","anchor":'<div class="pearls"><span class="lbl">Pearls',"text":
 '<div class="danger"><span class="lbl">Neonatal polycythemia</span> '+parts([
 ('Definition','venous hematocrit above 65% in a term neonate'),
 ('Causes','intrauterine hypoxia drives erythropoietin (preeclampsia, maternal diabetes or hypertension, smoking, growth restriction); or extra blood from delayed cord clamping or twin-twin transfusion'),
 ('Presentation','most are asymptomatic and ruddy; hyperviscosity brings lethargy, irritability and jitteriness, and in severe cases tachypnea, respiratory distress, poor feeding and cyanosis'),
 ('Metabolic','hypoglycemia and hypocalcemia from uptake by the expanded red cell mass; hyperbilirubinemia as the cells break down'),
 ('Treatment','hydration by feeds or glucose-containing IV fluids; partial exchange transfusion when hyperviscosity is symptomatic'),
 ('Versus transient tachypnea','fluid in the fissures; the polycythemic film is clear'),
 ('Versus dehydration','rare in the first 2 days, while the neonate still carries excess extracellular fluid'),
 ('Versus salt-wasting CAH','ambiguous genitalia in girls, hyponatremia and hyperkalemia, days later'),
 ('Versus glycogen storage disease type I','hepatomegaly and lactic acidosis'),
 ('Versus cyanotic heart disease','a normal cardiac silhouette and exam')])+'</div>\n',
 "why":f"explanation facts for nid {NP.split()[0]}; polycythemia was on the page only in copd"})
item('bs-nrd','dx',"6-hour-old, ruddy and jittery, breathing fast with no retractions; glucose is low and the chest film is clear",
 "Polycythemia","hyperviscosity; check a venous hematocrit","Transient tachypnea of the newborn","Glycogen storage disease",
 lead="Which is the most likely cause of this patient's symptoms?",src="uworld",nid=NP)
item('bs-nrd','mech',"Term neonate after delayed cord clamping, plethoric with a venous hematocrit of 70%, whose glucose is low",
 "Red cells consume glucose","the expanded red cell mass takes up glucose","Liver congestion blocks gluconeogenesis","Adrenal insufficiency",
 lead="Which is the most likely cause of this patient's hypoglycemia?")
item('bs-nrd','next',"Plethoric neonate with a venous hematocrit of 72%, still lethargic and feeding poorly after IV fluids",
 "Partial exchange transfusion","swaps blood for saline to lower viscosity","Double-volume exchange transfusion","Intravenous furosemide")

# ---------- 3. New Part II brief: stroke in a child or adolescent
B='bs-peds-stroke'
NT="1471806144718 1471806149857 1471806157855 1471806162437 1471806170265"
L=lambda *a,**k: li(B,*a,**k)
bank=''.join([
 L('dx',"15 yo with weeks of fatigue, weight loss and joint aches and episodes of light-headedness, now an acute focal deficit; the arm pulses are unequal",
   "Vasculitis","Takayasu arteritis narrowing the aorta and its branches","Bacterial endocarditis","Fibromuscular dysplasia",
   lead="Which is the most likely cause of this patient's stroke?",src="uworld",nid=NT),
 L('test',"15 yo with fever, weight loss, a 20 mm Hg difference in arm pressures and a carotid bruit",
   "Aortic angiography","CT or MR angiography of the aorta and branches","Temporal artery biopsy","Echocardiography"),
 L('next',"15 yo F whose angiogram shows long smooth stenoses of both subclavian arteries; ESR is high and she is still losing weight",
   "High-dose glucocorticoids","then a steroid-sparing agent","Low-dose aspirin alone","Surgical arterial bypass"),
 L('mech',"15 yo with Takayasu arteritis who becomes light-headed whenever she exercises her left arm",
   "Subclavian steal","reversed vertebral flow feeds the arm beyond the stenosis","Orthostatic hypotension","Vasovagal syncope"),
 L('dx',"16 yo who injects drugs, febrile with a new regurgitant murmur and splinter hemorrhages, then sudden aphasia",
   "Infective endocarditis","septic embolus; draw blood cultures","Takayasu arteritis","Arterial dissection",
   lead="Which is the most likely cause of this patient's stroke?"),
 L('dx',"14 yo struck in the neck during hockey, with neck pain and a left Horner syndrome, then right arm weakness the next day",
   "Carotid dissection","a single tapered vessel on angiography","Moyamoya disease","Paradoxical embolism",
   lead="Which is the most likely cause of this patient's stroke?"),
 L('dx',"Young woman with severe hypertension, an abdominal bruit, a normal ESR and a string of beads on renal angiography, who has a TIA",
   "Fibromuscular dysplasia","noninflammatory; no constitutional symptoms","Takayasu arteritis","Atherosclerosis"),
 L('dx',"7 yo with Down syndrome who develops transient arm weakness when crying hard or blowing out candles",
   "Moyamoya disease","hyperventilation constricts the collateral vessels","Complicated migraine","Todd paralysis"),
])
brief=f'''

<div class="brief bs" id="{B}" data-shelf="fm peds" data-nid="{NT}">
<h4>Stroke in a Child or Adolescent</h4>
<p class="sub">Find the arteriopathy &middot; UWorld &middot; constitutional symptoms plus unequal pulses make it inflammatory</p>
<div class="vignette"><span class="lbl">Source vignette</span> <b>Pt</b> &mdash; 15 yo with weeks of constitutional symptoms and episodic light-headedness, now an acute focal neurologic deficit, with asymmetric upper-extremity pulses &middot; <b>Q</b> &mdash; the most likely cause of the stroke; options spanned the pediatric stroke categories: vasculitis, bacterial endocarditis, fibromuscular dysplasia and others</div>

<div class="dp"><span class="lbl">The decision point</span>
<p>A stroke in a teenager is never "just a stroke": the question is <b>what made the artery fail</b>. Two findings decide it here. <b>Weeks of fever, weight loss and aches</b> say systemic inflammation. <b>Unequal pulses or arm pressures</b> say several large arteries are narrowed at once. Inflammation plus multiple fixed large-artery stenoses is a <b>large-vessel vasculitis</b>, and in an adolescent that is <b>Takayasu arteritis</b>.</p>
<p><b>The exception is endocarditis.</b> It also brings fever and stroke, but emboli occlude one vessel at a time and never narrow the aorta's branches, so the pulses stay equal. Look for the murmur and the embolic skin findings instead.</p></div>

<div class="crit"><span class="lbl">Pediatric stroke, by category</span> {parts([
 ('Cardiac','congenital heart disease with a right-to-left shunt, endocarditis, cardiomyopathy, arrhythmia'),
 ('Vascular, noninflammatory','arterial dissection, moyamoya, fibromuscular dysplasia'),
 ('Vascular, inflammatory','Takayasu arteritis, lupus, primary CNS vasculitis, post-varicella arteriopathy, meningitis'),
 ('Hematologic','sickle cell disease, inherited thrombophilia such as factor V Leiden, antiphospholipid antibodies'),
 ('Takayasu arteritis','granulomatous vasculitis of the aorta and its primary branches in a young patient, most often female; a systemic phase (fever, weight loss, arthralgia) then an occlusive phase (arm claudication, weak or absent pulses, unequal arm pressures, bruits, renovascular hypertension, TIA and stroke)')])}</div>

<div class="tw">
<table data-mask="3"><caption>Stroke in a young patient: the causes and their tells</caption>
<thead><tr><th>Cause</th><th>Illness script</th><th>The tell</th></tr></thead>
<tbody>
<tr><td><b>Vasculitis (Takayasu)</b></td><td>Adolescent with weeks of fever, weight loss and arthralgia; high ESR</td><td><b>Unequal arm pulses or pressures, bruits, long smooth stenoses of the aorta and branches</b></td></tr>
<tr><td>Bacterial endocarditis</td><td>Fever with a damaged valve or injection drug use</td><td>New regurgitant murmur, embolic skin lesions, positive blood cultures; pulses equal</td></tr>
<tr><td>Fibromuscular dysplasia</td><td>Young woman, renovascular hypertension, no inflammation</td><td>String of beads on angiography, normal ESR</td></tr>
<tr><td>Arterial dissection</td><td>Neck trauma, contact sports, neck manipulation</td><td>Neck pain or headache, Horner syndrome, one tapered vessel</td></tr>
<tr><td>Moyamoya disease</td><td>Down syndrome, neurofibromatosis type 1, sickle cell disease</td><td>Deficits provoked by hyperventilation (crying, blowing); puff-of-smoke collaterals</td></tr>
<tr><td>Sickle cell disease</td><td>Known disease or unexplained anemia</td><td>Large-artery vasculopathy; exchange transfusion for the acute stroke</td></tr>
<tr><td>Factor V Leiden</td><td>Family history of clots</td><td>Venous thrombosis; arterial stroke only by paradoxical embolism through a patent foramen ovale</td></tr>
<tr><td>Atherosclerosis</td><td>Diabetes, smoking, hyperlipidemia in adults</td><td>Rare in adolescents without familial hypercholesterolemia; no systemic inflammation</td></tr>
</tbody>
</table>
</div>

<h5 class="authored-hdr">Scenario bank</h5>
<ol class="bank authored">
{bank}</ol>

<div class="pearls"><span class="lbl">Pearls</span> Check <b>both arm pressures and every pulse</b> in any young stroke with constitutional symptoms; the older name is pulseless disease &middot; Takayasu and <b>giant cell arteritis</b> share the granulomatous large-vessel histology and are split by age, with giant cell arteritis over 50 &middot; diagnose with <b>CT or MR angiography</b> of the aorta and its branches, and treat with <b>high-dose glucocorticoids</b> plus a steroid-sparing agent &middot; renal artery involvement makes it a cause of <b>secondary hypertension</b> in a young patient &middot; light-headedness or syncope comes from carotid, vertebral or subclavian narrowing, including subclavian steal.</div>

<div class="pearls"><span class="lbl">Pairs with</span> Part I <b>Polymyalgia Rheumatica</b>, whose giant cell arteritis row is the same vasculitis in patients over 50. Part I <b>Secondary Hypertension</b> owns fibromuscular dysplasia and the abdominal bruit, the noninflammatory twin. Part II <b>Sickle Cell Trait versus Disease</b> owns the sickle cell stroke and its exchange transfusion.</div>

<div class="rule"><span class="lbl">Transferable rule</span> When a young patient has a stroke, name what made the artery fail. Systemic inflammation with unequal pulses is vasculitis; fever with a murmur is an embolus; neck strain with Horner syndrome is a dissection; a string of beads with no inflammation is fibromuscular dysplasia.</div>
<div class="traps">
  <div class="trapline"><span class="pill p-salient">Salient decoy</span><span class="trapwhy">Bacterial endocarditis: fever plus stroke looks embolic, but emboli do not narrow several arteries or unequalize the pulses.</span></div>
  <div class="trapline"><span class="pill p-mirror">Mirror twin</span><span class="trapwhy">Fibromuscular dysplasia: a young woman with arterial stenoses, but no fever, weight loss or raised ESR.</span></div>
  <div class="trapline"><span class="pill p-class">Class-vs-member</span><span class="trapwhy">The options name the class (vasculitis), not the member (Takayasu); answer at the level offered.</span></div>
</div>
</div>'''
tail='<div class="traps"><span class="pill p-slot">True-fact-wrong-slot</span><span class="pill p-salient">Salient decoy</span></div>\n</div>\n\n\n<!-- =================== DERM'
anchor=tail[:-len('\n\n\n<!-- =================== DERM')]
assert src.count(tail)==1
edits.append({"scope":"page","op":"replace","old":tail,"new":anchor+brief+'\n\n\n<!-- =================== DERM',
 "why":f"new Part II brief {B}: no brief owns pediatric stroke or Takayasu (source nids {NT})"})
edits.append({"scope":"page","op":"insert_after","anchor":'<a class="bs" href="#bs-reye">Cerebral Edema: Reye</a>',
 "text":f'\n    <a class="bs" href="#{B}">Stroke in a Child: the Arteriopathy</a>',"why":"nav"})
edits.append({"scope":"page","op":"replace","old":'id="neuro">Neurology &amp; HEENT <span class="n">12 topics <span style="color:#9A5B0E">+ 3 board-style',
 "new":'id="neuro">Neurology &amp; HEENT <span class="n">12 topics <span style="color:#9A5B0E">+ 4 board-style',"why":"system header count"})
# reverse Pairs-with mentions
edits.append({"scope":"brief:secondary-htn","op":"replace","old":"Part I <b>Inherited Tumor Syndromes</b> owns the case where the hypertension is one organ in a heritable pattern.</div>",
 "new":"Part I <b>Inherited Tumor Syndromes</b> owns the case where the hypertension is one organ in a heritable pattern. Part II <b>Stroke in a Child or Adolescent</b> sets fibromuscular dysplasia beside Takayasu arteritis, the inflammatory cause of renal artery stenosis in a young patient.</div>","why":"reverse link"})
edits.append({"scope":"brief:bs-sickle-trait","op":"replace","old":"owns the chronic pulmonary sequelae that follow the acute chest syndrome named here.</div>",
 "new":"owns the chronic pulmonary sequelae that follow the acute chest syndrome named here. Part II <b>Stroke in a Child or Adolescent</b> places the sickle cell stroke among the other pediatric causes.</div>","why":"reverse link"})
json.dump({"pass":"s07","date":"2026-09-22","reason":"PDA twin rewritten as a murmur dx variant; neonatal polycythemia backfilled into bs-nrd; new Part II brief for pediatric stroke (Takayasu).","expected":{"mcq_delta":11},"edits":edits},open('repair/LEDGER-s07.json','w'),indent=1,ensure_ascii=False)
print(len(edits))
