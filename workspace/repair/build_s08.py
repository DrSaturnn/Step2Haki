import json,html,sys,re
sys.path.insert(0,'tools');from idgen import item_id,option_id;from axlib import parse_html
e=lambda s:html.escape(s,quote=True)
src=open('index.html').read();D=parse_html(src);BR={b.id:src[b.raw_start:b.raw_end] for b in D.briefs}
edits=[]
def item(b,t,stem,key,comp,d1,d2,lead=None,src_="authored",nid=None):
    q=item_id(b,t,key,stem);k,o1,o2=option_id(q,'key',key),option_id(q,'d1',d1),option_id(q,'d2',d2)
    li=(f'<li data-type="{t}" data-src="{src_}"'+(f' data-nid="{nid}"' if nid else '')+f' data-d1="{e(d1)}" data-d2="{e(d2)}" data-item-id="{q}" data-item-version="1" '
        f'data-item-status="ready" data-key-id="{k}" data-d1-id="{o1}" data-d2-id="{o2}"'+(f' data-lead-in="{e(lead)}"' if lead else '')+
        f'>{e(stem)} &rarr; <b>{e(key)}</b> &rarr; {e(comp)}</li>\n')
    edits.append({"scope":"brief:"+b,"op":"insert_before","anchor":"</ol>","text":li,"why":f"backfill {t} item"+(f" (source nid {nid})" if nid else "")})
P='<div class="pearls"><span class="lbl">Pearls'
def block(b,cls,label,parts,why,anchor=P):
    body=' &middot; '.join(f'<b>{e(t)}</b> &mdash; {e(d)}' for t,d in parts)
    edits.append({"scope":"brief:"+b,"op":"insert_before","anchor":anchor,"text":f'<div class="{cls}"><span class="lbl">{e(label)}</span> {body}</div>\n',"why":why})
def row(b,cells,why):
    edits.append({"scope":"brief:"+b,"op":"insert_before","anchor":"</tbody>","text":'<tr>'+''.join(f'<td>{c}</td>' for c in cells)+'</tr>\n',"why":why})
def trap(b,pill_cls,pill,why_text,why):
    t=BR[b];last=list(re.finditer(r'<span class="trapwhy">.*?</span></div>',t))[-1].group(0)
    assert t.count(last)==1
    edits.append({"scope":"brief:"+b,"op":"replace","old":last,"new":last+f'<div class="trapline"><span class="pill {pill_cls}">{pill}</span><span class="trapwhy">{e(why_text)}</span></div>',"why":why})

# ---------- 1. Anemia of prematurity -> bs-preterm-followup
N1="1516827641404"
block('bs-preterm-followup','danger','Anemia of prematurity',[
 ('Mechanism','oxygenation at birth (breathing, ductus closure) switches off erythropoietin; a preterm infant has also missed the third-trimester shift of erythropoietin production from liver to kidney'),
 ('Why worse than term','lower hematocrit at birth, shorter red cell life span, frequent NICU blood draws, iron depletion'),
 ('Timing','term physiologic anemia bottoms out at 9 to 11 g/dL at 2 to 3 months; the preterm nadir is deeper (about 7 g/dL) and earlier (1 to 2 months)'),
 ('Presentation','often asymptomatic; tachycardia, a flow murmur, apnea, poor weight gain'),
 ('Labs','normocytic, normochromic, normal platelets and white count; the absolute reticulocyte count may be normal for age, but there is no reticulocytosis for the degree of anemia'),
 ('Management','iron supplementation and fewer blood draws; red cell transfusion if severe or symptomatic'),
 ('Versus thalassemia','microcytic and hypochromic with target cells'),
 ('Versus hemolysis','erythropoietin rises and the reticulocytes climb'),
 ('Versus iron deficiency','microcytic, and unlikely on fortified formula with ferrous sulfate'),
 ('Versus anemia of chronic disease','iron trapped in macrophages by chronic inflammation, infection or malignancy, in older children and adults')],
 f"explanation facts for nid {N1}; the brief had no anemia content")
item('bs-preterm-followup','mech',"7 wk old born at 32 weeks, feeding and gaining well on fortified formula and ferrous sulfate, pulse 150 with a soft systolic flow murmur; hemoglobin 8, reticulocytes 1.4%, normal platelets and white count, normocytic normochromic smear",
 "Impaired erythropoietin production","anemia of prematurity; the marrow is not asked to respond","Iron sequestration in macrophages","Abnormal hemoglobin subunit ratio",
 lead="Which is the most likely underlying cause of this patient's laboratory findings?",src_="uworld",nid=N1)
item('bs-preterm-followup','dx',"10 wk old term infant, thriving and asymptomatic, hemoglobin 10 with a normocytic smear and normal platelets and white count",
 "Physiologic anemia of infancy","the normal erythropoietin nadir at 2 to 3 months","Anemia of prematurity","Iron deficiency anemia")
item('bs-preterm-followup','next',"6 wk old former 28-week infant with new apnea spells and flat weight gain; hemoglobin 6.5, low reticulocytes, no hemolysis",
 "Red cell transfusion","symptomatic anemia of prematurity","Double the ferrous sulfate dose","Recheck the count in 4 weeks")

# ---------- 2. Campylobacter treatment and its mimics -> rlq-pain
N2="1575404882954 1580504776948"
block('rlq-pain','pearls','Bacterial diarrhea: who gets antibiotics',[
 ('Campylobacter','self-limited within about a week; supportive care. Treat only for symptoms beyond 7 days, bloody stools, high fever, or pregnancy, immunocompromise or old age; choose by susceptibility'),
 ('The culture trap','a positive culture with a susceptibility panel is not an indication; culture exists for protracted or severe illness and for outbreak control in day care and nursing homes'),
 ('Shiga toxin-producing E. coli','bloody diarrhea with little fever; never give antibiotics, which raise the risk of hemolytic uremic syndrome'),
 ('Shigella','high fever, bloody diarrhea, sometimes a febrile seizure; antibiotics (azithromycin) shorten illness and spread ⚠︎'),
 ('Nontyphoidal Salmonella','supportive in a healthy child; treat infants under 3 months, sickle cell disease, immunocompromise or bacteremia, because treatment otherwise prolongs carriage ⚠︎'),
 ('Yersinia','pseudoappendicitis like Campylobacter; supportive unless bacteremic or immunocompromised ⚠︎'),
 ('Clostridioides difficile','recent antibiotics; oral vancomycin or fidaximicin ⚠︎'),
 ('Doxycycline under 8','avoided when another agent covers the organism, for tooth staining')],
 f"nid {N2.split()[0]} explanation plus user request: the mimics whose treatment differs. Non-Campylobacter treatment lines are from memory and flagged")
item('rlq-pain','next',"5 yo M, 4 days of mucoid diarrhea after a low-grade fever that has resolved, still 5 or 6 stools a day, well hydrated, afebrile, guaiac negative; stool culture grows Campylobacter coli, ciprofloxacin resistant, ampicillin and tetracycline sensitive",
 "Symptomatic care only","mild and self-limited; the susceptibility panel is not an indication","Amoxicillin per susceptibility","Doxycycline",
 lead="Which is the most appropriate treatment for this patient's condition?",src_="uworld",nid=N2)
item('rlq-pain','next',"6 yo with Campylobacter coli enteritis now on day 9 with bloody stools; ciprofloxacin resistant, erythromycin intermediate, ampicillin and tetracycline sensitive",
 "Amoxicillin","sensitive, and safe under 8","Doxycycline","Levofloxacin")
item('rlq-pain','next',"4 yo in day care with high fever, bloody diarrhea and a brief generalized seizure; stool grows Shigella",
 "Azithromycin","treating shortens illness and spread","Symptomatic care only","Loperamide")
trap('rlq-pain','p-test','Test-overrides-findings',"A susceptibility panel invites treatment, but a mild, improving, afebrile child is treated by the clinical picture, not the culture report.",f"trap from nid {N2.split()[0]}")

# ---------- 3. Hemophilic arthropathy -> factor-inhibitor
N3="1516755705218"
block('factor-inhibitor','danger','Hemophilic arthropathy: where the bleeding meets the joint',[
 ('Hemophilia','X-linked recessive deficiency of factor VIII (A) or factor IX (B); prolonged aPTT with normal PT and platelets; severity tracks factor activity'),
 ('Hemarthrosis','spontaneous or trivial-trauma bleeding into a large joint, often a knee, with sudden severe swelling'),
 ('The link','iron from the extravasated red cells is stored as hemosiderin in the synovium, which inflames it'),
 ('Then','the synovium thickens and turns boggy, fibroses, and the cartilage and subchondral bone are destroyed'),
 ('Result','chronic pain, swelling and loss of motion, including a joint that will not fully extend actively or passively'),
 ('Imaging','radiographs show only late disease; MRI detects damage earlier'),
 ('Prevention','early prophylaxis with factor concentrate lowers the risk'),
 ('Treatment','factor replacement; desmopressin for mild hemophilia A'),
 ('Versus JIA or RA','autoimmune cartilage destruction, no bleeding history'),
 ('Versus disseminated gonococcal infection','acute onset, not 6 months'),
 ('Versus avascular necrosis','sickle cell disease, or Legg-Calvé-Perthes at the hip between 4 and 12'),
 ('Versus Lyme arthritis','knee effusion, but no bleeding history')],
 f"explanation facts for nid {N3}; the brief covered hemarthrosis but not what repeated bleeds do to the joint")
item('factor-inhibitor','mech',"16 yo M with past episodes of sudden knee swelling without injury and prolonged bleeding after a tooth extraction, now 6 months of worsening knee pain with a boggy swelling and a knee he cannot fully extend",
 "Hemosiderin deposition and fibrosis","hemophilic arthropathy after recurrent hemarthroses","Disseminated gonococcal infection","Autoimmune cartilage destruction",
 lead="Which is the most likely cause of this patient's knee joint findings?",src_="uworld",nid=N3)
item('factor-inhibitor','next',"3 yo M with severe hemophilia A and a second spontaneous knee hemarthrosis this year",
 "Regular factor VIII prophylaxis","prevents the bleeds that build arthropathy","Factor VIII only when bleeds occur","Desmopressin before activity")
item('factor-inhibitor','test',"14 yo M with hemophilia A, repeated bleeds into the same knee and persistent swelling, with normal radiographs",
 "MRI of the knee","shows synovial and cartilage damage before radiographs","Bone scintigraphy","Diagnostic arthrocentesis")
item('factor-inhibitor','next',"Adult with mild hemophilia A due for a dental extraction",
 "Desmopressin","releases stored factor VIII and von Willebrand factor","Recombinant factor VIIa","Platelet transfusion")

# ---------- 4. ALL with a trauma story -> bs-leukemia
N4="1539706410374 1582407354587 1582488811568 1582488955319"
row('bs-leukemia',['Nonaccidental trauma','Vague or shifting history, bruises in areas that are not injury-prone (trunk, ears, neck)','<b>Normal blood counts</b>; trauma never lowers them'],f"nid {N4.split()[0]}: the NAT distractor")
block('bs-leukemia','danger','The fall is the decoy',[
 ('The story','families often date leukemic bone pain to a fall; the pain is dull, in the long-bone shafts, worse at night, and the child limps or refuses to walk'),
 ('What makes it systemic','fever, hepatomegaly, bilateral tibial tenderness and two or more cytopenias'),
 ('The bruises','thrombocytopenia explains truncal bruising; trauma cannot depress three cell lines'),
 ('When to think abuse','a vague history with bruising away from injury-prone areas, and normal counts'),
 ('The white count','often low early, since normal production falls; later high as blasts spill into the blood'),
 ('Versus aplastic anemia','pancytopenia from a hypocellular marrow, so no bone pain and rarely hepatomegaly'),
 ('Versus immune thrombocytopenia','hemoglobin and white count normal, no bone pain or organomegaly'),
 ('Workup','marrow biopsy with flow cytometry (20% or more blasts), then lumbar puncture for CNS disease'),
 ('Prognosis','5-year survival above 85% in children with multidrug chemotherapy')],
 f"explanation facts for nid {N4.split()[0]}")
item('bs-leukemia','dx',"5 yo F brought by her mother and the mother's boyfriend a week after a fall from the couch, now leg pain worse at night and refusing to walk; a month of dry cough, temperature 38.3 C, pale, liver 3 cm below the costal margin, bilateral proximal tibial tenderness, scattered bruises on the chest and back; hemoglobin 8, platelets 30,000, WBC 3,000",
 "Acute lymphoblastic leukemia","bone pain plus pancytopenia","Severe aplastic anemia","Nonaccidental trauma",
 lead="Which is the most likely cause of this patient's symptoms?",src_="uworld",nid=N4)
item('bs-leukemia','dx',"2 yo with bruises of different ages on the ears, neck and trunk, a history that changes between caregivers, and a normal CBC and coagulation profile",
 "Nonaccidental trauma","normal counts; bruises away from injury-prone areas","Acute lymphoblastic leukemia","Immune thrombocytopenia")
item('bs-leukemia','mech',"5 yo with ALL and scattered truncal bruises whose family links them to a recent fall",
 "Marrow replacement by blasts","thrombocytopenia, not trauma","Blunt soft-tissue trauma","Vitamin K deficiency coagulopathy")
trap('bs-leukemia','p-salient','Salient decoy',"The fall and the mother's boyfriend pull toward abuse, but trauma cannot explain fever, hepatomegaly or three low cell lines.",f"trap from nid {N4.split()[0]}")

json.dump({"pass":"s08","date":"2026-09-22","reason":"Four pasted UWorld questions, none on the page, backfilled into owning briefs.","expected":{"mcq_delta":16},"edits":edits},open('repair/LEDGER-s08.json','w'),indent=1,ensure_ascii=False)
print(len(edits))
