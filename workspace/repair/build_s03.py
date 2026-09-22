import json,hashlib,html
def h(s):return hashlib.sha256(s.encode()).hexdigest()[:20]
# brief, type, stem, key, companion, d1, d2, lead-in(optional)
N=[
("secondary-htn","test","29 yo M with BP 168/102, potassium 2.8, metabolic alkalosis and normal creatinine","Aldosterone-to-renin ratio","suppressed renin separates primary hyperaldosteronism from renovascular disease","Renal artery duplex ultrasound","Plasma free metanephrines",None),
("secondary-htn","next","44 yo F with primary hyperaldosteronism confirmed biochemically and a unilateral adrenal nodule on CT, planning surgery","Adrenal venous sampling","bilateral hyperplasia is more common than adenoma, so lateralize before resecting","Left adrenalectomy","Repeat CT imaging",None),
("secondary-htn","avoid","Older man with peripheral vascular disease, severe hypertension and bilateral renal artery stenosis","An ACE inhibitor","the efferent arteriole needs angiotensin II to hold GFR, so blocking it causes AKI","A calcium channel blocker","A thiazide diuretic",None),
("secondary-htn","mech","Hypertension from renal artery stenosis","Angiotensin II","renin initiates the cascade; aldosterone causes the hypokalemia","Renin","Aldosterone","Which of the following directly mediates the vasoconstriction?"),
("cough","next","55 yo M with 10 weeks of cough and no imaging yet","Chest X-ray","first in all chronic cough, before any empiric trial","Empiric proton pump inhibitor trial","Spirometry",None),
("cough","next","45 yo F on lisinopril with 3 months of dry cough and a normal chest X-ray","Stop lisinopril","ACE-inhibitor cough resolves in 1 to 4 weeks","Switch to a different ACE inhibitor","First-generation antihistamine trial",None),
("cough","test","30 yo M with chronic cough at night and with exercise and cold air; normal exam and normal spirometry","Methacholine challenge","normal spirometry does not exclude cough-variant asthma","24-hour esophageal pH monitoring","Chest CT",None),
("cough","next","45 yo F with 3 months of dry cough, normal chest X-ray and no heartburn, after failed antihistamine-decongestant and inhaled corticosteroid trials","Proton pump inhibitor for 8 weeks","GERD cough is often silent; the failed trials have eliminated the other two","Methacholine challenge","High-resolution chest CT",None),
("pneumoconiosis","screen","55 yo M sandblaster and never smoker with silicosis","Annual tuberculin skin test","silicosis raises tuberculosis risk","Annual low-dose chest CT","Annual sputum cytology",None),
("pneumoconiosis","next","66 yo M, retired shipyard worker, asymptomatic, with calcified pleural plaques and normal lung parenchyma on imaging","No treatment","plaques alone mark exposure and are benign","CT-guided pleural biopsy","Oral corticosteroids",None),
("pneumoconiosis","mech","62 yo M with decades of asbestos exposure who also smokes heavily","Bronchogenic carcinoma","smoking multiplies bronchogenic risk only, not mesothelioma","Mesothelioma","Pleural plaques","Which of the following is he at greatest multiplied risk of developing?"),
("pneumoconiosis","next","50 yo M aerospace machinist with progressive dyspnea and noncaseating granulomas on biopsy, now removed from exposure","Oral corticosteroids","berylliosis responds to steroids","Antituberculous therapy","Observation alone",None),
("liver-preg","next","26 yo F at 34 weeks with intractable palmar pruritus and raised bile acids, taking ursodeoxycholic acid","Delivery at 36 to 37 weeks","intrahepatic cholestasis carries stillbirth risk","Delivery at 40 weeks","Immediate delivery",None),
("liver-preg","next","29 yo F at 35 weeks with hypoglycemia, coagulopathy, raised ammonia and rising creatinine","Emergent delivery","acute fatty liver of pregnancy is treated by delivering","Ursodeoxycholic acid","Magnesium sulfate and expectant management",None),
("liver-preg","next","28 yo F at 32 weeks with alkaline phosphatase three times normal on routine labs; AST, ALT and bilirubin normal; no symptoms","Reassurance","the placenta makes alkaline phosphatase","Right upper quadrant ultrasound","Serum bile acids",None),
("thyroid","test","32 yo F with low TSH, high T4, a small nontender goiter and no eye signs","Radioactive iodine uptake","splits a gland making hormone from one leaking it","Thyroid ultrasound","Fine-needle aspiration",None),
("thyroid","next","55 yo F with Graves disease, fever 40, delirium and atrial fibrillation the day after surgery","Beta-blocker","then PTU, then iodine at least 1 hour later, then steroids","Potassium iodide","Radioactive iodine ablation","Which of the following should be given first?"),
("thyroid","next","28 yo F with newly diagnosed Graves disease at 8 weeks of pregnancy","Propylthiouracil","PTU in the first trimester, methimazole after, radioactive iodine never","Methimazole","Radioactive iodine ablation",None),
("thyroid","next","30 yo F, 3 months postpartum, with palpitations, a painless small goiter, positive TPO antibodies and low radioactive iodine uptake","Beta-blocker alone","nothing is being made, so antithyroid drugs are useless","Methimazole","Radioactive iodine ablation",None),
("psoriasis","next","34 yo M with a few silvery extensor plaques on the elbows and knees and nail pitting","Topical steroid plus calcipotriene","first rung before phototherapy and systemics","Narrowband UVB phototherapy","Secukinumab",None),
("psoriasis","test","34 yo M with a single annular scaly trunk plaque with central clearing and an active border","KOH preparation","if tinea, a steroid causes tinea incognito","Skin biopsy","Wood lamp examination",None),
("psoriasis","next","34 yo M with severe psoriasis and psoriatic arthritis about to start a TNF-alpha inhibitor","Test for latent tuberculosis","TNF blockade can reactivate tuberculosis","Baseline echocardiogram","Baseline pulmonary function tests","Which of the following is required before the first dose?"),
("psoriasis","avoid","34 yo M with extensive plaque psoriasis who was started on oral prednisone for an asthma flare","Abrupt discontinuation of prednisone","abrupt steroid withdrawal can trigger a pustular flare","A gradual prednisone taper","Continuing topical calcipotriene",None),
("neonatal-rash","next","3 wk F bundled in a fleece swaddle in a warm room, with fine erythematous papules in the neck folds and axillae","Lighter, cooler clothing","miliaria rubra has a removable cause: thin cotton and a cool room","Topical nystatin","Reassurance without changes",None),
("neonatal-rash","next","10 day old, afebrile and feeding well, with clustered vesicles on an erythematous base on the scalp","HSV PCR and IV acyclovir","any vesicular rash in a neonate is HSV until proven otherwise","Reassurance","Topical mupirocin",None),
("neonatal-rash","next","4 mo with a beefy red diaper rash involving the inguinal creases, with satellite papules","Topical nystatin","candida involves the creases; irritant dermatitis spares them","Zinc oxide barrier cream alone","Low-potency topical corticosteroid",None),
("neonatal-rash","next","4 mo with blue-grey macules over the sacrum and buttocks noted on a well-child exam","Document the finding and reassure","congenital dermal melanocytosis is benign; documenting it prevents confusion with abuse","Skeletal survey","Report to child protective services",None),
]
edits=[]
for b,t,stem,key,comp,d1,d2,lead in N:
    q='q_'+h(f"{t}|{key}|{stem[:60]}")
    k,o1,o2=['o_'+h(f"{q}|{s}|{l}") for s,l in (('key',key),('d1',d1),('d2',d2))]
    e=lambda s:html.escape(s,quote=True)
    li=(f'<li data-type="{t}" data-src="authored" data-d1="{e(d1)}" data-d2="{e(d2)}" data-item-id="{q}" data-item-version="1" '
        f'data-item-status="ready" data-key-id="{k}" data-d1-id="{o1}" data-d2-id="{o2}"'+(f' data-lead-in="{e(lead)}"' if lead else '')+
        f'>{e(stem)} &rarr; <b>{e(key)}</b> &rarr; {e(comp)}</li>\n')
    edits.append({"scope":"brief:"+b,"op":"insert_before","anchor":"</ol>","text":li,"why":f"all-dx brief; {t} item from content already in the brief"})
json.dump({"pass":"s03-all-dx","date":"2026-09-22","reason":"7 briefs tested only diagnosis. Added next/test/avoid/screen/mech items whose keys, distractors and numbers already appear in each brief's table, decision point or pearls. No new numbers; no existing item touched.","expected":{"mcq_delta":len(N)},"edits":edits},open('repair/LEDGER-s03.json','w'),indent=1,ensure_ascii=False)
print(len(N))
