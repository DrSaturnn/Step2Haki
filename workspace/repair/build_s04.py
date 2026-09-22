import json,hashlib,html
def h(s):return hashlib.sha256(s.encode()).hexdigest()[:20]
e=lambda s:html.escape(s,quote=True)
edits=[]
# --- fix 1: del22q11 flag retired with the IDSA gate stated
edits.append({"scope":"brief:del22q11","op":"replace",
 "old":'data-item-version="2" data-item-status="ready" data-key-id="o_376635c5a0cc51288789"',
 "new":'data-item-version="3" data-item-status="ready" data-key-id="o_376635c5a0cc51288789"',"why":"explanation content changed; v2 to v3"})
edits.append({"scope":"brief:del22q11","op":"replace",
 "old":"&rarr; live vaccines are withheld until T-cell function is established &#9888;&#65038;</li>",
 "new":"&rarr; live vaccines are withheld until CD3 and CD4 exceed 500/mm3 and CD8 exceeds 200/mm3 with a normal mitogen response</li>",
 "why":"flag verified: IDSA 2013 live-vaccine gate in 22q11.2 deletion (CD3 >500, CD4 >500, CD8 >200, normal mitogen response), as cited by Berkhout et al 2020 (doi 10.1177/2515135520957139). Key unchanged and correct at CD3 210."})
# --- fix 2: galactosemia key: add CSF (AAP 2021, all febrile infants 8-21 d get LP), remove the flag glyph from the key label, parallel distractors
edits.append({"scope":"brief:bs-galactosemia","op":"replace",
 "old":'data-d1="Observe with repeat examination in 12 hours" data-d2="Exchange transfusion" data-item-id="q_3b3b3b16ecad50c28538" data-item-version="1"',
 "new":'data-d1="Blood and urine cultures, then IV ceftriaxone" data-d2="Blood and urine cultures, then observe off antibiotics" data-item-id="q_3b3b3b16ecad50c28538" data-item-version="2"',
 "why":"distractors rewritten as parallel same-task workups (old d2 exchange transfusion was an F6 dead option); ceftriaxone is avoided in neonates; v1 to v2"})
edits.append({"scope":"brief:bs-galactosemia","op":"replace",
 "old":"&rarr; <b>Blood and urine cultures with empiric intravenous ampicillin and gentamicin &#9888;</b> &rarr; Escherichia coli sepsis</li>",
 "new":"&rarr; <b>Blood, urine and CSF cultures, then IV ampicillin and gentamicin</b> &rarr; Escherichia coli sepsis; every febrile neonate gets a lumbar puncture</li>",
 "why":"the flag glyph sat inside the key and rendered on the correct option button only (answer cue). Verified: AAP 2021 febrile infant guideline, 8-21 days: LP for all, empiric ampicillin plus ceftazidime or gentamicin. Key content kept (cultures, ampicillin, gentamicin); CSF added."})
# --- gap-filling items
N=[
("microcytic-anemia","dx","16 yo F with heavy menses, a low MCV, a low erythrocyte count, an elevated RDW and a low ferritin","Iron deficiency anemia","oral iron","Beta-thalassemia minor","Anemia of chronic disease",None),
("microcytic-anemia","dx","58 yo M with rheumatoid arthritis and a microcytic anemia; serum iron low, TIBC low, ferritin normal","Anemia of chronic disease","iron is sequestered, not absent","Iron deficiency anemia","Beta-thalassemia minor",None),
("ped-murmur","next","7 yo F, well and growing normally, with a grade 2 vibratory midsystolic murmur at the left lower sternal border that softens on standing; normal S2 and pulses","Reassurance","the full benign profile is present","ECG and echocardiography","Chest X-ray",None),
("ped-murmur","next","15 yo soccer player, asymptomatic, with a grade 2 systolic murmur that grows louder when he stands from a squat","Hold sports pending ECG and echo","louder on standing is hypertrophic cardiomyopathy until excluded","Reassurance and clearance for sports","Exercise stress test alone",None),
("bs-puv","mech","Newborn boy with posterior urethral valves and Potter sequence","Pulmonary hypoplasia","fetal urine makes the amniotic fluid that grows the lungs","Renal failure","Urosepsis","Which of the following is the usual cause of death?"),
("bs-puv","mech","Fetus with duodenal atresia","Polyhydramnios","the fetus cannot swallow amniotic fluid; the mirror of the renal lesions","Oligohydramnios","Normal amniotic fluid volume","Which amniotic fluid finding is expected?"),
("bs-leukemia","next","7 yo M on day 3 of ALL induction with rising potassium, phosphate and uric acid, a low calcium and a rising creatinine","IV hydration and urate-lowering therapy","tumor lysis syndrome","Oral calcium supplementation","Stop induction chemotherapy",None),
("bs-leukemia","stage","14 yo M with pancytopenia, marrow lymphoblasts and an anterior mediastinal mass on chest film","T-cell lineage","a mediastinal mass points to T-cell ALL","B-cell lineage","Myeloid lineage","Which lineage is most likely?"),
]
for b,t,stem,key,comp,d1,d2,lead in N:
    q='q_'+h(f"{t}|{key}|{stem[:60]}")
    k,o1,o2=['o_'+h(f"{q}|{s}|{l}") for s,l in (('key',key),('d1',d1),('d2',d2))]
    li=(f'<li data-type="{t}" data-src="authored" data-d1="{e(d1)}" data-d2="{e(d2)}" data-item-id="{q}" data-item-version="1" '
        f'data-item-status="ready" data-key-id="{k}" data-d1-id="{o1}" data-d2-id="{o2}"'+(f' data-lead-in="{e(lead)}"' if lead else '')+
        f'>{e(stem)} &rarr; <b>{e(key)}</b> &rarr; {e(comp)}</li>\n')
    edits.append({"scope":"brief:"+b,"op":"insert_before","anchor":"</ol>","text":li,"why":f"residual gap: {t} item from content already in the brief"})
json.dump({"pass":"s04-residuals","date":"2026-09-22","reason":"Tuple-set residuals were largely already applied (RDW/RBC present in microcytic-anemia). Filled the remaining gaps from brief content; resolved the two bank-item flags that could ship a wrong key, by targeted verification.","expected":{"mcq_delta":len(N)},"edits":edits},open('repair/LEDGER-s04.json','w'),indent=1,ensure_ascii=False)
