"""s15: NBME-style lead-ins for test and screen items.
Initial study vs confirmatory study vs predicted result vs screening/surveillance, using the NBME
Item-Writing Guide wording where it exists (verbatim marked V) and USMLE Physician Task wording otherwise.
Task phrases that were embedded in stems move into the lead-in; stems become the patient only.
Every changed item bumps data-item-version."""
import json,re,sys,html
sys.path.insert(0,'tools');from axlib import parse_html
src=open('index.html',encoding='utf-8').read();doc=parse_html(src)
B={b.id:src[b.raw_start:b.raw_end] for b in doc.briefs}
items=json.load(open('/tmp/claude-0/test_items.json'))
S ="Which of the following is the most appropriate diagnostic study to obtain at this time?"   # V
CL="Which of the following laboratory studies is most likely to confirm the diagnosis?"         # V (all options are labs)
C ="Which of the following is most likely to confirm the diagnosis?"                            # adapted (options not all labs)
SCR="Which of the following is the most appropriate screening test?"                            # USMLE task wording
SURV="Which of the following is the most appropriate surveillance?"                             # USMLE task wording
PROG="Based on these findings, this patient is most likely to develop which of the following?"  # V
KD="When should screening for diabetic kidney disease begin?"
# n: (new type or None, lead-in or None to leave, new stem or None to leave)
P={
 1:(None,S,"44 yo M with classic meralgia paresthetica"),
 2:(None,S,None),3:(None,S,None),
 4:(None,S,"Young adult with inflammatory back pain and normal sacroiliac joint radiographs, suspicion still high"),
 5:(None,S,None),6:(None,S,None),
 8:(None,"Which of the following sets of laboratory findings is most likely in this patient?","Child with suspected systemic juvenile idiopathic arthritis"),
 10:(None,S,"16 yo M with rigid thoracic kyphosis on exam"),
 12:(None,"Which of the following is the most appropriate way to assess the infant's own renal function?","Newborn of a mother with end-stage renal disease, serum creatinine 4.2 on day 1"),
 13:(None,CL,"Newborn with dysmorphic features and suspected trisomy 18"),
 14:('test',"Which of the following is most likely to establish the diagnosis?","Pregnant woman whose first-trimester screen shows low PAPP-A, low hCG and an enlarged nuchal translucency"),
 15:(None,CL,"Newborn with coloboma, choanal atresia and a ventricular septal defect"),
 19:(None,S,None),20:(None,S,None),
 21:(None,"Which of the following agents is most appropriate for this patient's stress test?",None),
 22:(None,S,None),25:(None,S,None),26:(None,S,None),27:(None,S,None),28:(None,S,None),
 29:(None,"Which of the following is the most appropriate initial diagnostic step?","Newborn with cyanosis that worsens with feeding and improves with crying"),
 30:(None,"Which of the following laboratory studies is most likely to support the diagnosis?","9 yo M with suspected acute rheumatic fever"),
 32:(None,CL,None),
 33:(None,S,"Adult with classic episodic wheeze and cough but normal spirometry"),
 34:(None,S,"40 yo with lower-lobe emphysema and minimal smoking history"),
 35:(None,"Which of the following best distinguishes emphysema from chronic bronchitis?","Smoker with chronic airflow obstruction"),
 36:(None,S,None),
 38:(None,C,None),
 40:(None,S,None),41:(None,S,None),
 42:(None,C,"Adolescent with cystic fibrosis, antibiotic-refractory symptoms and a total IgE above 1,000 IU/mL"),
 43:('screen',"Which of the following is the most appropriate screening test for allergic bronchopulmonary aspergillosis?","Well 14-year-old with cystic fibrosis at routine annual review"),
 44:(None,"Which of the following pulmonary function findings would confirm the diagnosis?","Adolescent with sickle cell disease and suspected asthma"),
 45:(None,C,"Adolescent with recurrent stridor unresponsive to albuterol and a normal saturation"),
 48:(None,S,None),
 49:(None,S,"79 yo M with regurgitation of undigested food, halitosis and a gurgling neck"),
 53:(None,S,None),
 54:('claim',"Which of the following is the main reason allergy testing may still be performed?","Child with confirmed eosinophilic esophagitis"),
 55:('next',None,None),
 56:(None,S,"Term newborn jaundiced at 14 hours of life"),
 57:(None,"Which of the following findings on abdominal radiograph is most likely?","Preterm neonate on enteral feeds with abdominal distension and bloody stools"),
 58:(None,C,"Stable infant with suspected malrotation"),
 59:(None,S,None),60:(None,S,None),
 61:(None,C,None),
 66:(None,"Which of the following measures glomerular filtration rate most accurately?","56 yo M with type 2 diabetes"),
 67:(None,S,"Older adult smoker with painless gross hematuria"),
 68:(None,S,"Well child with isolated microscopic hematuria, normal blood pressure and no proteinuria"),
 69:(None,S,"Sexually active adolescent with dysuria and sterile pyuria"),
 71:(None,"Which of the following best distinguishes AVP deficiency from AVP resistance?","Child with polyuria whose urine remains dilute when fluids are withheld"),
 72:(None,S,None),73:(None,S,None),75:(None,S,None),
 80:(None,"Which of the following is the most appropriate study to identify the cause?","3 wk M with poor feeding and prolonged jaundice, TSH 90 and T4 0.6, no palpable goiter"),
 85:(None,"Which of the following best distinguishes central from peripheral precocious puberty?","Child with signs of precocious puberty"),
 86:(None,"Which of the following best distinguishes the two most likely diagnoses?","16 yo M with Marfanoid habitus and bilateral lens subluxation"),
 94:(None,S,None),
 95:(None,"Which of the following best distinguishes hemoglobinuria from myoglobinuria?","45 yo F with dark urine and a heme-positive dipstick showing 0 RBCs on microscopy"),
 96:(None,S,"15 yo F vegan with heavy menses, MCV 68, hemoglobin 9.2"),
 97:(None,C,None),
 98:(None,"Which of the following laboratory findings is most likely in this patient?",None),
 99:(None,CL,None),100:(None,C,None),101:(None,S,None),
 102:(None,S,"5 yo M with 2 wk of fatigue, 1 wk of leg pain and 1 day of fever with petechiae, pale, liver 4 cm below the costal margin, cervical and axillary adenopathy"),
 103:(None,C,"5 yo M whose complete blood count shows hemoglobin 7, platelets 22,000 and WBC 3,100"),
 104:(None,CL,None),105:(None,C,None),
 115:(None,S,None),116:(None,S,None),
 119:(None,CL,None),
 121:(None,CL,"Child already started on doxycycline for suspected Rocky Mountain spotted fever"),
 122:(None,CL,None),123:(None,S,None),
 124:(None,C,"Newborn with suspected congenital CMV"),
 126:(None,S,None),127:(None,S,None),
 128:('next',None,None),
 129:(None,S,None),131:(None,S,None),132:(None,S,None),135:(None,S,None),
 136:(None,"Which of the following is the most appropriate next step?",None),
 137:(None,"Which of the following is the most appropriate staging study?","7 yo F with newly confirmed medulloblastoma"),
 138:(None,S,None),
 139:(None,C,"Child with a scaly patch of alopecia and regional lymphadenopathy"),
 150:(None,S,"Adolescent with heavy menses since menarche, easy bruising and a family history of bleeding"),
 151:(None,S,"Adolescent with galactorrhea and amenorrhea"),
 152:(None,S,"Woman with 4 months of amenorrhea and a negative pregnancy test"),
 # screen items
 11:(None,"Which of the following is the most appropriate screening study for an associated condition?","2 mo F with congenital muscular torticollis"),
 31:(None,"Which of the following is most likely to prevent recurrence?","9 yo M recovering from acute rheumatic fever"),
 37:(None,SCR,None),
 52:(None,SURV,"Patient with established Peutz-Jeghers syndrome"),
 62:(None,"Which of the following is the most appropriate evaluation for associated anomalies?","Term newborn boy with esophageal atresia and a distal fistula confirmed on x-ray, before surgical repair"),
 63:(None,KD,"56 yo M with type 2 diabetes diagnosed today"),
 64:(None,KD,"24 yo F with type 1 diabetes diagnosed at 16"),
 65:(None,SCR,"56 yo M with type 2 diabetes due for nephropathy screening"),
 70:(None,"Which of the following should be monitored long term?","Child with severe reflux and established renal scarring"),
 81:(None,"Which of the following is the most appropriate monitoring for this patient?","Patient with newly confirmed von Hippel-Lindau disease"),
 82:(None,"Which of the following is the most appropriate recommendation for her brother?","22 yo F newly diagnosed with von Hippel-Lindau disease who has an asymptomatic 15-year-old brother"),
 83:('mech',PROG,"9 year old with painless firm rubbery tongue nodules, marfanoid habitus and long fingers"),
 84:('mech',PROG,"Newborn with bilateral absence of the iris, hypospadias and an undescended left testis"),
 93:(None,"In addition to influenza vaccine, which of the following is indicated?","28 yo F with type 2 diabetes due for vaccines"),
 107:('dx',None,None),
 118:('next',None,None),
 120:(None,"Which of the following measures most reduces his infection risk at home?","4 yo M with CD40 ligand deficiency on immunoglobulin replacement"),
 134:(None,"Which of the following is most appropriate for her brother?","Newly diagnosed 17 yo F with retinitis pigmentosa who has an asymptomatic 12 yo brother"),
 140:(None,"Which of the following is the most appropriate household measure?","Child newly diagnosed with tinea capitis"),
 163:(None,"Which additional screening tests are indicated?","17 yo F newly diagnosed with pelvic inflammatory disease"),
 164:(None,SCR,None),
 166:(None,"Which additional vaccines are indicated?","48 yo M with cirrhosis"),
 171:(None,"Which supplement does she require?","24 yo F on a strict unprocessed vegan diet, no supplements"),
 172:(None,"Beyond vitamin B12 and vitamin D, which supplements does this child need most?","2 yo child raised on the family's unprocessed vegan diet"),
 174:(None,"Which other vaccines are due at this visit?","11 yo F receiving Tdap today"),
}
SEP=re.compile(r' (?:&rarr;|→) ')
edits=[];log=[]
byn={x['n']:x for x in items}
for n,(nt,lead,stem) in sorted(P.items()):
    x=byn[n];old=x['raw'];bid=x['brief']
    assert B[bid].count(old)==1,(n,bid)
    otag,rest=old.split('>',1)
    tag=otag
    if nt:
        assert f'data-type="{x["type"]}"' in tag;tag=tag.replace(f'data-type="{x["type"]}"',f'data-type="{nt}"',1)
    if lead:
        esc=html.escape(lead,quote=True)
        if 'data-lead-in="' in tag: tag=re.sub(r'data-lead-in="[^"]*"',f'data-lead-in="{esc}"',tag)
        else: tag=tag+f' data-lead-in="{esc}"'
    v=int(re.search(r'data-item-version="(\d+)"',tag).group(1))
    tag=tag.replace(f'data-item-version="{v}"',f'data-item-version="{v+1}"',1)
    body=rest
    if stem:
        m=SEP.search(body);assert m,(n,body[:80])
        body=html.escape(stem,quote=False)+body[m.start():]
    new=tag+'>'+body
    assert new!=old
    edits.append({"scope":"brief:"+bid,"op":"replace","old":old,"new":new,
                  "why":f"s15 lead-in: {x['type']}->{nt or x['type']}; "+("stem task phrase moved to lead-in" if stem else "lead-in only")})
    log.append((n,bid,x['type'],nt or x['type'],lead,stem))
json.dump({"pass":"s15","date":"2026-09-23","reason":"NBME-style lead-ins on test and screen items: initial vs confirmatory vs predicted result vs screening/surveillance; task phrases moved out of stems.",
           "expected":{"mcq_delta":0},"edits":edits},open('repair/LEDGER-s15.json','w'),indent=1,ensure_ascii=False)
json.dump(log,open('/tmp/claude-0/s15_log.json','w'),ensure_ascii=False)
print(len(edits),'edits')
