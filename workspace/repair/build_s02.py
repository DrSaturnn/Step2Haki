import json,hashlib,html
def h(s):return hashlib.sha256(s.encode()).hexdigest()[:20]
NEW=[ # brief, stem, key, companion, d1, d2
("herpangina","5 yo in late summer with abrupt fever and sore throat; grey vesicles and shallow ulcers on the soft palate, uvula and anterior pillars; gums, lips and tongue normal; no rash","Herpangina","coxsackievirus A; supportive care","Herpetic gingivostomatitis","Hand-foot-and-mouth disease"),
("cgd","3 yo M with a Staphylococcus aureus liver abscess, a perirectal abscess drained in infancy and granulomas on biopsy","Chronic granulomatous disease","confirm with dihydrorhodamine flow cytometry","Leukocyte adhesion deficiency","X-linked agammaglobulinaemia"),
("gtps","Woman in her 50s with lateral hip pain she calls burning, worse lying on that side and on stairs; point tenderness over the greater trochanter, normal hip range of motion and normal neurologic exam","Greater trochanteric pain syndrome","activity modification, NSAIDs and physical therapy","Meralgia paresthetica","Hip osteoarthritis"),
("eczemaherp","Child with atopic dermatitis, fever and painful monomorphic vesicles evolving into punched-out erosions with hemorrhagic crust, worsening on TMP-SMX; conjunctiva and oropharynx clear","Eczema herpeticum","systemic acyclovir immediately","Impetigo","Stevens-Johnson syndrome"),
("lymphadenitis","3 yo with cough and rhinorrhea last week, now resolved, and a single neck node noticed yesterday that is 4 cm, tender, warm and red today; T 38.5","Acute bacterial lymphadenitis","empiric clindamycin","Reactive viral adenopathy","Cat-scratch disease"),
("cyanotic-chd","4 mo M with episodes of deep cyanosis while crying that resolve when held knees to chest, and a harsh systolic murmur at the left upper sternal border","Tetralogy of Fallot","RVOT obstruction drives right-to-left flow across the VSD","Truncus arteriosus","Tricuspid atresia"),
("bs-shunt-timing","6 wk old, acyanotic, feeding poorly and tachypneic, with a holosystolic murmur at the left lower sternal border that was absent on the newborn exam","Ventricular septal defect","murmur appears as pulmonary vascular resistance falls","Atrial septal defect","Patent ductus arteriosus"),
]
edits=[]
for b,stem,key,comp,d1,d2 in NEW:
    q='q_'+h(f"dx|{key}|{stem[:60]}")
    k,o1,o2=['o_'+h(f"{q}|{s}|{l}") for s,l in (('key',key),('d1',d1),('d2',d2))]
    e=lambda s:html.escape(s,quote=True)
    li=(f'<li data-type="dx" data-src="authored" data-d1="{e(d1)}" data-d2="{e(d2)}" data-item-id="{q}" data-item-version="1" '
        f'data-item-status="ready" data-key-id="{k}" data-d1-id="{o1}" data-d2-id="{o2}">{e(stem)} &rarr; <b>{e(key)}</b> &rarr; {e(comp)}</li>\n')
    edits.append({"scope":"brief:"+b,"op":"insert_before","anchor":"</ol>","text":li,"why":"brief's own diagnosis was never keyed; add dx item keying it"})
T=[("cgd","<h4>Chronic Granulomatous Disease</h4>","<h4>Recurrent Abscesses and Granulomas</h4>",'<a href="#cgd">Chronic Granulomatous Disease</a>','<a href="#cgd">Abscesses &amp; Granulomas</a>'),
   ("gtps","<h4>Greater Trochanteric Pain Syndrome</h4>","<h4>Pain Around the Hip and Thigh</h4>",'<a href="#gtps">Greater Trochanteric Pain Syndrome</a>','<a href="#gtps">Hip &amp; Thigh Pain</a>'),
   ("eczemaherp","<h4>Eczema Herpeticum</h4>","<h4>Atopic Dermatitis Complications</h4>",'<a href="#eczemaherp">Eczema Herpeticum</a>','<a href="#eczemaherp">Atopic Dermatitis Complications</a>'),
   ("lymphadenitis",None,None,'<a href="#lymphadenitis">Cervical Lymphadenitis</a>','<a href="#lymphadenitis">The Inflamed Neck Node</a>')]
for b,o,n,no,nn in T:
    if o: edits.append({"scope":"brief:"+b,"op":"replace","old":o,"new":n,"why":"title named the diagnosis (self-keying); id unchanged"})
    edits.append({"scope":"page","op":"replace","old":no,"new":nn,"why":"sidebar title named the diagnosis"})
json.dump({"pass":"s02-self-keying","date":"2026-09-22","reason":"7 briefs never keyed their own diagnosis (it appeared only as a distractor), and 3 titles named it. Retitle h4/nav (ids permanent), add one dx item per brief from the brief's own table/decision point. Distractors from each brief's table. No existing item touched.","expected":{"mcq_delta":7},"edits":edits},open('repair/LEDGER-s02.json','w'),indent=1,ensure_ascii=False)
print(len(edits),'edits')
