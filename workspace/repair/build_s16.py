"""s16 pilot: workup-in-order tables (screen / first / next / confirms / skip) in 4 briefs,
same shape as the aq-bruising first-tests table (Test | Order | Result | What it points to, mask col 4).
secondary-htn: existing clue table gains a Confirms column instead of a second table."""
import json
A='<h5 class="authored-hdr">Scenario bank</h5>'
def tbl(cap,rows):
    body=''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>\n' for a,b,c,d in rows)
    return ('<div class="tw">\n<table data-mask="4"><caption>'+cap+'</caption>\n'
            '<thead><tr><th>Test</th><th>Order</th><th>Result</th><th>What it points to</th></tr></thead>\n<tbody>\n'
            +body+'</tbody>\n</table>\n</div>\n')
edits=[]
def ins(bid,html,why): edits.append({"scope":"brief:"+bid,"op":"insert_before","anchor":A,"text":html,"why":why})

ins('septic-hip',tbl('Workup, in the order you would order it',[
 ('CBC, ESR and CRP','First','Count the <b>Kocher</b> predictors: fever, refusal to bear weight, ESR over 40, WBC over 12,000, CRP over 2','3 or more: aspirate'),
 ('Hip ultrasound','First','<b>Effusion</b> present or absent','No effusion argues against septic arthritis; an effusion alone cannot separate septic from transient synovitis'),
 ('Hip radiographs','By branch','Usually <b>normal</b> early','Excludes the mimics: SCFE, Perthes disease, fracture'),
 ('Blood culture','Before antibiotics','<b>Positive</b> in a minority','Names the organism when the joint fluid does not'),
 ('Ultrasound-guided arthrocentesis','Confirms','Synovial WBC <b>over 50,000</b>, neutrophil-predominant; Gram stain and culture','Septic arthritis: surgical washout and IV antibiotics'),
 ('MRI','By branch','<b>Adjacent osteomyelitis</b> or pyomyositis','Child stays ill after a negative or equivocal aspirate'),
]),"workup pilot: screen/first/confirm order per NBME lead-in logic")

ins('congenital-hypothyroid',tbl('Workup, from the screen to the cause',[
 ('Newborn screen (heel prick at 24 to 48 hours)','Screen','<b>High TSH</b> (some programs measure T4 first)','Recall the infant for serum tests the same day'),
 ('Serum TSH and free T4','Confirms','<b>High TSH</b>, low free T4; or <b>low or normal TSH</b> with low free T4','Primary: start levothyroxine now. Central: cortisol before levothyroxine, then pituitary MRI'),
 ('Thyroid ultrasound or radionuclide scan','Cause, optional','<b>Absent or ectopic</b> gland; or an enlarged gland in place','Dysgenesis; or dyshormonogenesis. Never delays treatment'),
 ('Maternal TSH-receptor antibodies','By branch','<b>Positive</b> in a mother with autoimmune thyroid disease','Transient hypothyroidism from blocking antibody'),
 ('Serum thyroglobulin alone','Skip','Cannot stand in for imaging','Does not name the cause by itself'),
]),"workup pilot: screen then confirm then cause")

ins('bs-spherocytosis',tbl('Workup, in the order you would order it',[
 ('CBC with reticulocytes and indices','First','Anemia, <b>high reticulocytes</b>, MCHC over 36%','Hemolysis from a membrane that has lost surface'),
 ('Peripheral smear','First','<b>Spherocytes</b>','Hereditary spherocytosis or warm autoimmune hemolysis; in a newborn, ABO disease too'),
 ('Direct antiglobulin (Coombs) test','Next','<b>Negative</b>','A membrane defect, not antibody; positive means warm autoimmune hemolysis'),
 ('Bilirubin, LDH, haptoglobin','Supports','<b>Indirect</b> bilirubin up, haptoglobin down','Hemolysis, mainly extravascular in the spleen'),
 ('Eosin-5-maleimide binding by flow cytometry','Confirms','<b>Reduced</b> fluorescence','Hereditary spherocytosis'),
 ('Osmotic fragility','Confirms, older','<b>Increased</b> fragility','Hereditary spherocytosis; less sensitive than EMA binding'),
 ('Flow cytometry for CD55 and CD59','Skip','<b>Normal</b> expression expected','PNH: the other Coombs-negative hemolysis, with cytopenias and a bland smear'),
]),"workup pilot: first, next, confirm, skip")

old_head='<table><caption>Secondary hypertension — clue → diagnosis → first test</caption>\n<thead><tr><th>Clue in the stem</th><th>Diagnosis</th><th>First test</th></tr></thead>'
new_head='<table><caption>Secondary hypertension — clue → diagnosis → first test → confirms</caption>\n<thead><tr><th>Clue in the stem</th><th>Diagnosis</th><th>First test</th><th>Confirms, then</th></tr></thead>'
edits.append({"scope":"brief:secondary-htn","op":"replace","old":old_head,"new":new_head,"why":"add confirm column"})
rows=[('<td><b>Aldosterone-to-renin ratio</b></td></tr>','<td><b>Aldosterone-to-renin ratio</b></td><td>Aldosterone <b>fails to suppress</b> with salt loading; then adrenal CT and adrenal venous sampling to lateralize</td></tr>'),
 ('<td>Duplex / CTA renal arteries</td></tr>','<td>Duplex / CTA renal arteries</td><td>CT or MR angiography; <b>catheter angiography</b> is the reference standard</td></tr>'),
 ('<td>Plasma / urine metanephrines</td></tr>','<td>Plasma / urine metanephrines</td><td>Metanephrines <b>several-fold high</b>; then adrenal CT or MRI to locate the tumor</td></tr>'),
 ('<td>Polysomnography</td></tr>','<td>Polysomnography</td><td><b>Polysomnography</b> is itself the confirmatory test; a home study can screen</td></tr>'),
 ('<td>Echo / CT</td></tr>','<td>Echo / CT</td><td>Arm-leg <b>pressure gradient</b> first at the bedside; CT or MR angiography defines the narrowing</td></tr>'),
 ('<td>Low-dose dexamethasone / 24-h cortisol</td></tr>','<td>Low-dose dexamethasone / 24-h cortisol</td><td>A <b>second, different</b> screening test abnormal (late-night salivary cortisol, 24-h urine cortisol, 1 mg dexamethasone); then ACTH to localize</td></tr>')]
for o,n in rows: edits.append({"scope":"brief:secondary-htn","op":"replace","old":o,"new":n,"why":"add confirm cell"})
json.dump({"pass":"s16","date":"2026-09-23","reason":"Pilot: workup-in-order tables (screen, first, next, confirms, skip) in 4 briefs.","expected":{"mcq_delta":0},"edits":edits},
          open('repair/LEDGER-s16.json','w'),indent=1,ensure_ascii=False)
print(len(edits))
