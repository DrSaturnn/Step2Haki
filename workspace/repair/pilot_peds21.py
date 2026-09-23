"""Pilot: Aquifer Peds 21 (6-year-old with bruising) authored two ways.
A = board-brief format (bs-purpura), B = Aquifer symptom-workup format (aq-bruising).
Writes the two brief fragments and a scratch page with both injected. Not applied to index.html."""
import html,sys,re
sys.path.insert(0,'tools');from idgen import item_id,option_id
e=lambda s:html.escape(s,quote=False)
ea=lambda s:html.escape(s,quote=True)
W='⚠︎'

def li(b,t,stem,key,comp,d1,d2,lead=None,src="authored"):
    q=item_id(b,t,key,stem);k,o1,o2=option_id(q,'key',key),option_id(q,'d1',d1),option_id(q,'d2',d2)
    return (f'<li data-type="{t}" data-src="{src}" data-d1="{ea(d1)}" data-d2="{ea(d2)}" data-item-id="{q}" data-item-version="1" '
            f'data-item-status="ready" data-key-id="{k}" data-d1-id="{o1}" data-d2-id="{o2}"'+(f' data-lead-in="{ea(lead)}"' if lead else '')+
            f'>{e(stem)} &rarr; <b>{e(key)}</b>'+(f' &rarr; {e(comp)}' if comp else '')+'</li>\n')
def grid(cls,label,parts):
    return f'<div class="{cls}"><span class="lbl">{e(label)}</span> '+' &middot; '.join(f'<b>{e(a)}</b> &mdash; {b}' for a,b in parts)+'</div>\n'
def table(caption,heads,rows,mask=None):
    m=f' data-mask="{mask}"' if mask else ''
    h=''.join(f'<th>{e(x)}</th>' for x in heads)
    r=''.join('<tr>'+''.join(f'<td>{c}</td>' for c in row)+'</tr>\n' for row in rows)
    return f'<div class="tw">\n<table{m}><caption>{e(caption)}</caption>\n<thead><tr>{h}</tr></thead>\n<tbody>\n{r}</tbody>\n</table>\n</div>\n'
def traps(lines):
    return '<div class="traps">'+''.join(f'<div class="trapline"><span class="pill {c}">{p}</span><span class="trapwhy">{e(w)}</span></div>' for c,p,w in lines)+'</div>\n'

VIG=('<div class="vignette" data-recon="partial"><span class="lbl">Source case</span> <b>Pt</b> &mdash; 6 yo with new bruising, '
     'Aquifer Pediatrics 21; the case works through purpura and petechiae to IgA vasculitis &middot; <b>Q</b> &mdash; build the differential for '
     'purpura in a school-age child, then narrow it by history, examination and a first set of tests</div>\n')

# ======================================================================
# A. BOARD-BRIEF FORMAT
# ======================================================================
A='bs-purpura'
bankA=''.join([
 li(A,'dx',"6 yo, well-appearing, palpable purpura clustered on the legs and buttocks, swollen ankles and crampy abdominal pain a week after a cold; platelets normal",
    "IgA vasculitis","urinalysis, then supportive care","Immune thrombocytopenia","Acute lymphoblastic leukemia",src="aquifer"),
 li(A,'dx',"4 yo, well-appearing, generalized flat petechiae and gum bleeding two weeks after a viral illness; platelets 12,000, hemoglobin and white count normal, no organomegaly",
    "Immune thrombocytopenia","isolated thrombocytopenia in a well child","IgA vasculitis","Acute lymphoblastic leukemia"),
 li(A,'dx',"5 yo with bruising and petechiae, fever and fatigue for three weeks, bone pain, a palpable spleen and cervical nodes; platelets 40,000",
    "Acute lymphoblastic leukemia","marrow replacement; bone marrow biopsy","Immune thrombocytopenia","IgA vasculitis"),
 li(A,'test',"6 yo with palpable purpura on the legs, knee pain and normal platelets, diagnosed with IgA vasculitis",
    "Urinalysis","the only test the diagnosis itself requires","Serum IgA level","Skin biopsy"),
 li(A,'next',"6 yo with IgA vasculitis, painful swollen ankles, a normal urinalysis and no blood in the stool",
    "NSAID or acetaminophen for pain","supportive care","Oral prednisone","Admission for IV fluids"),
 li(A,'test',"5 yo with IgA vasculitis who develops sudden severe colicky abdominal pain with vomiting",
    "Abdominal ultrasound","looking for intussusception","Air contrast enema","Upper endoscopy"),
 li(A,'next',"6 yo with IgA vasculitis whose purpura has faded; urinalysis and blood pressure are normal at diagnosis",
    "Urinalysis and blood pressure every 1 to 2 weeks","renal disease can appear after the rash","No further follow-up needed","Repeat serum IgA monthly"),
 li(A,'dx',"3 yo with bruises on the back, buttocks and ears, one shaped like a hand, a history that does not match, and a normal CBC",
    "Nonaccidental trauma","location and pattern, with normal counts","Immune thrombocytopenia","IgA vasculitis"),
])
briefA=f'''<div class="brief bs" id="{A}" data-shelf="peds">
<h4>Purpura in a Well Child</h4>
<p class="sub">the platelet count splits vessel from platelet &middot; Aquifer &middot; is the purpura palpable, and is the spleen?</p>
{VIG}<div class="dp"><span class="lbl">The decision point</span>
<p>In a well-appearing child with purpura, the <b>platelet count</b> makes the first cut. <b>Normal platelets</b> with <b>palpable</b> purpura in a gravity-dependent distribution (legs, buttocks), plus joint pain, colicky abdominal pain or hematuria, is <b>IgA vasculitis</b>: the vessel wall is inflamed, so the purpura is raised. <b>Isolated thrombocytopenia</b> with flat petechiae and normal hemoglobin and white count is <b>immune thrombocytopenia</b>. Two or more abnormal cell lines, or constitutional symptoms and bone pain, is <b>leukemia</b> until the marrow says otherwise.</p>
<p><b>The exception is the spleen.</b> Neither ITP nor IgA vasculitis enlarges it, so a palpable spleen (or hepatomegaly or adenopathy) in a child who otherwise looks like either one sends the workup to leukemia or another systemic cause.</p></div>
{grid('pearls','Pertinent positives & negatives',[
 ('Palpable purpura on the legs and buttocks','inflammation in the vessel wall; favors IgA vasculitis over any platelet disorder'),
 ('Normal platelet count','non-thrombocytopenic purpura; excludes ITP and argues against leukemia'),
 ('A URI in the preceding weeks','precedes about half of IgA vasculitis and more than half of ITP, so it does not split them'),
 ('Knee and ankle pain, crampy abdominal pain','the extracutaneous organs of IgA vasculitis'),
 ('No splenomegaly','keeps ITP and IgA vasculitis in play; its presence would reopen leukemia'),
 ('Well appearance','fits ITP and IgA vasculitis; leukemia usually brings fever, malaise and weight loss'),
])}{table('Purpura in a child: the differential',['Diagnosis','Illness script','Key discriminator','Why less likely here'],[
 ['<b>IgA vasculitis</b>','4 to 6 yo, boys twice as often, often after a URI; small-vessel IgA vasculitis of skin, gut, joints and kidney','<b>Palpable purpura with a normal platelet count</b>','Fits: the answer'],
 ['Immune thrombocytopenia','2 to 5 yo, well, often after a viral illness; antiplatelet antibody','Isolated thrombocytopenia, usually below 20,000; flat petechiae, mucosal bleeding','Platelets are normal and the purpura is raised'],
 ['Acute lymphoblastic leukemia','Constitutional symptoms, bone pain, ill appearance','Two or more cytopenias; spleen, liver or nodes enlarged','Well child, normal counts, no organomegaly'],
 ['Coagulation disorder (hemophilia, von Willebrand)','Bleeding after procedures, circumcision or dental work; family history','Deep hematomas and hemarthroses rather than petechiae','No bleeding history; purpura is palpable and dependent'],
 ['Nonaccidental trauma','History that does not fit the injury or the child’s development','Bruises on the back, buttocks, face or ears; patterned shapes','Distribution is symmetric and dependent, with systemic features'],
],mask=3)}{grid('danger','Management, in one line',[
 ('IgA vasculitis','supportive: acetaminophen or an NSAID (not with GI bleeding or glomerulonephritis); steroids are debated and reserved for severe abdominal pain'),
 ('Monitoring','urinalysis and blood pressure every 1 to 2 weeks for 1 to 2 months, then monthly to every other month for a year'),
 ('Escalate when','severe abdominal pain, GI bleeding, suspected intussusception (ileoileal, so not reducible by enema) or renal involvement'),
])}{grid('pearls','Decision spine',[
 ('Is the child well or ill?','ill appearance and constitutional symptoms point to leukemia first'),
 ('What is the platelet count?','normal splits vessel from platelet'),
 ('Is the purpura palpable and dependent?','raised, clustered on the legs and buttocks is vasculitis'),
 ('Is the spleen palpable?','yes reopens leukemia'),
 ('What does the urinalysis show?','hematuria or proteinuria adds BUN and creatinine'),
])}<h5 class="authored-hdr">Scenario bank</h5>
<ol class="bank authored">
{bankA}</ol>
{grid('danger','Decoy note',[('The preceding URI','shared by ITP and IgA vasculitis in roughly half of cases each; it confirms nothing about which one')])}<div class="pearls"><span class="lbl">Pearls</span> A urinalysis is the only study the diagnosis of IgA vasculitis requires; serum IgA is high in only about half and rarely ordered &middot; renal disease affects about a third and can appear after the rash has gone, which is why monitoring runs for a year &middot; about 5% progress to chronic kidney disease, fewer than 1% to end-stage disease &middot; recurrence is about 30%, weeks to months later, and restarts the urine and blood pressure checks.</div>
<div class="pearls"><span class="lbl">Pairs with</span> Part I <b>Anemia with Thrombocytopenia</b>, where two cell lines are down and the smear and Coombs name the process. Part II <b>Pediatric Acute Lymphoblastic Leukemia</b> owns the child whose purpura comes with bone pain and a big spleen.</div>
<div class="rule"><span class="lbl">Transferable rule</span> Purpura in a child is sorted by the platelet count before anything else, and a palpable spleen overrides a reassuring story.</div>
{traps([('p-salient','Salient decoy','The preceding URI is shared by ITP and IgA vasculitis and cannot separate them.'),
        ('p-attr','Unchecked attribute','Purpura is read as a platelet problem without checking whether it is palpable, which is the vessel-wall tell.')])}</div>
'''

# ======================================================================
# B. AQUIFER SYMPTOM-WORKUP FORMAT
# ======================================================================
B='aq-bruising'
bankB=''.join([
 li(B,'dx',"6 yo, well-appearing, palpable purpura clustered on the legs and buttocks, swollen ankles and crampy abdominal pain a week after a cold; platelets normal",
    "IgA vasculitis","urinalysis, then supportive care","Immune thrombocytopenia","Acute lymphoblastic leukemia",src="aquifer"),
 li(B,'next',"School-age child with new widespread bruising and petechiae, afebrile and alert, normal vital signs",
    "Complete blood count with smear","the platelet count makes the first cut","Coagulation studies alone","Skeletal survey"),
 li(B,'mech',"Well child with purpura, a normal platelet count, and raised lesions that can be felt with a fingertip",
    "Inflamed small-vessel walls","vasculitis, not a platelet problem","Too few platelets","Clotting factor deficiency"),
 li(B,'dx',"4 yo, well-appearing, flat petechiae everywhere and a nosebleed two weeks after a viral illness; platelets 12,000, hemoglobin and white count normal, no organomegaly",
    "Immune thrombocytopenia","isolated thrombocytopenia in a well child","IgA vasculitis","Acute lymphoblastic leukemia"),
 li(B,'next',"5 yo who looks like ITP (petechiae, platelets 20,000) but has a spleen tip 3 cm below the costal margin",
    "Evaluate for leukemia","splenomegaly is not part of ITP","Observe as ITP","Start IVIG"),
 li(B,'dx',"7 yo boy with a swollen, painful knee after a minor fall, a deep thigh hematoma last year, and an uncle who bled after surgery",
    "Coagulation factor disorder","hemarthrosis and deep hematomas, not petechiae","Immune thrombocytopenia","IgA vasculitis"),
 li(B,'dx',"3 yo with bruises on the back, buttocks and ears, one shaped like a hand, a history that does not match, and a normal CBC",
    "Nonaccidental trauma","location and pattern, with normal counts","Immune thrombocytopenia","IgA vasculitis"),
 li(B,'test',"6 yo with IgA vasculitis diagnosed on examination and a normal platelet count",
    "Urinalysis","the only test the diagnosis itself requires","Serum IgA level","Skin biopsy"),
 li(B,'test',"6 yo with IgA vasculitis whose urinalysis shows hematuria and proteinuria",
    "BUN and creatinine","measure the extent of renal disease","Serum IgA level","Renal ultrasound"),
 li(B,'test',"5 yo with IgA vasculitis who develops sudden severe colicky abdominal pain with vomiting",
    "Abdominal ultrasound","looking for intussusception","Air contrast enema","Upper endoscopy"),
 li(B,'next',"Intussusception confirmed in a 5 yo with IgA vasculitis; it is ileoileal and does not reduce on its own",
    "Surgical reduction","an enema cannot reach an ileoileal intussusception","Air contrast enema","Observation with serial ultrasound"),
 li(B,'next',"6 yo with IgA vasculitis whose purpura has faded; urinalysis and blood pressure are normal at diagnosis",
    "Urinalysis and blood pressure every 1 to 2 weeks","renal disease can appear after the rash","No further follow-up needed","Repeat serum IgA monthly"),
 li(B,'next',"4 yo with ITP, platelets 15,000, petechiae only, no mucosal or other bleeding",
    "Observation with activity limits","non-severe ITP often needs no medication","IVIG","Platelet transfusion"),
 li(B,'avoid',"4 yo with ITP and a painful sprained ankle",
    "Ibuprofen","antiplatelet effect; use acetaminophen","Acetaminophen","Ice and elevation"),
])
briefB=f'''<div class="brief aq" id="{B}" data-shelf="peds" data-src="aquifer" data-case="Pediatrics 21">
<h4>Bruising and Purpura in a Child</h4>
<p class="sub">Aquifer Pediatrics 21 &middot; symptom workup &middot; sort by what failed: the vessel, the platelet, the clotting factor, or the story</p>
{VIG}<div class="dp"><span class="lbl">The approach</span>
<p>Bruising is a finding, not a diagnosis. Ask <b>what failed</b>: the <b>vessel wall</b> (IgA vasculitis), the <b>platelet count</b> (ITP, leukemia), the <b>clotting factors</b> (hemophilia, von Willebrand disease), or the <b>story</b> (accidental or nonaccidental trauma). Each failure leaves a different bruise, a different history and a different first test. Check first whether the child needs intervention now; then let the history, the examination and the platelet count remove whole branches at a time.</p></div>
{table('First look: does this child need something now?',['Finding','What it means','Urgency'],[
 ['Altered mental status','Lethargy, agitation, poor eye contact or no age-appropriate response; can mean poor cerebral perfusion and threatens the airway','<b>Now</b>: circulation, airway, breathing'],
 ['Respiratory distress or depression, cyanosis','Tachypnea, grunting and work of breathing, or slow shallow breathing; central cyanosis is hypoxemia','<b>Now</b>'],
 ['Delayed capillary refill','Peripheral perfusion falling to protect brain, heart and kidneys; an early sign of circulatory failure','<b>Now</b>'],
 ['Severe pain','Not always life-threatening, but needs prompt attention','<b>Now</b>'],
 ['Fever, pallor, mild tachycardia','Infection, anemia, or fever, pain and volume loss; a heart rate above 200 is urgent','History and examination first'],
])}{table('Build the differential by what failed',['Mechanism','Diagnoses','What the bleeding looks like','First clue'],[
 ['<b>Accidental trauma</b>','Bumps, scrapes, falls','Bruises over bony prominences: shins, elbows, forehead','A story that fits the injury and the child’s development'],
 ['<b>Nonaccidental trauma</b>','Abuse','Back, buttocks, face or ears; the shape of a hand, fingers, a bite or a buckle','A story that does not fit, or bruising in a child who is not yet mobile'],
 ['<b>Vessel wall</b>','IgA vasculitis','Palpable purpura or petechiae clustered on the legs and buttocks','Normal platelets; joints, abdomen, kidneys'],
 ['<b>Platelet count</b>','Immune thrombocytopenia; leukemia','Flat generalized petechiae, bruising, mucosal bleeding','Low platelets; the other cell lines decide between them'],
 ['<b>Clotting factors</b>','Hemophilia; von Willebrand disease','Deep tissue hematomas and hemarthroses more than petechiae','Bleeding after trauma, circumcision, immunizations or dental work; family history'],
 [f'<b>Infection with purpura</b> {W}','Meningococcemia and other sepsis','Rapidly spreading purpura in a febrile, ill child','Ill appearance; treat before the workup finishes'],
])}{grid('pearls','History that narrows it',[
 ('A URI in the past weeks','precedes about half of IgA vasculitis and more than half of ITP; keeps both, separates neither'),
 ('Bleeding after procedures, circumcision, immunizations or dental work','a clotting factor disorder, especially with a family history'),
 ('Joint pain or swelling, mostly knees and ankles','IgA vasculitis (about 75%); leukemia can also infiltrate joints'),
 ('Crampy abdominal pain, blood in the stool','IgA vasculitis; pain can come before the rash; sudden severe pain raises intussusception'),
 ('Fever, malaise, weight loss, bone pain','leukemia, from marrow expansion'),
 ('Nosebleeds or gum bleeding','platelet disorder; about 40% of ITP has mucosal bleeding'),
 ('A mechanism that does not fit, or a child not yet mobile','nonaccidental trauma'),
 ('The child’s own account','ask what they think is wrong, what worries them, and what they expect; it guides the history and the advice'),
])}{grid('pearls','Examination that narrows it',[
 ('Describe the lesion','location, arrangement, type, shape, size, color, palpation (raised or flat, blanching or not), secondary features, progression'),
 ('Raised, clustered, dependent','palpable purpura on the legs and buttocks is vasculitis'),
 ('Flat and generalized','petechiae from too few platelets'),
 ('Over bony prominences','accidental'),
 ('Back, buttocks, face, ears, or patterned','nonaccidental until proven otherwise'),
 ('Joints','hemarthrosis points to a factor disorder; periarticular swelling of knees and ankles to IgA vasculitis'),
 ('Spleen','neither ITP nor IgA vasculitis enlarges it; a palpable spleen sends the workup to leukemia, infection or another systemic cause. Supine with knees flexed, or rolled onto the right side, on deep inspiration; more than 2 cm below the costal margin is enlargement'),
 ('Lymph nodes','small cervical, axillary and inguinal nodes are normal; over 2 cm, supraclavicular, or hard, matted and fixed raises malignancy'),
])}{table('First tests, and what each result does',['Test','Result','What it changes'],[
 ['<b>CBC with platelet count</b>','Normal platelets','Non-thrombocytopenic purpura: IgA vasculitis'],
 ['','Low platelets, hemoglobin and white count normal','Isolated thrombocytopenia: ITP'],
 ['','Low platelets with anemia or an abnormal white count','Leukemia: marrow examination'],
 ['<b>Urinalysis</b>','Hematuria or proteinuria','Renal involvement in IgA vasculitis; add BUN and creatinine'],
 ['<b>BUN and creatinine</b>','Raised','Extent of renal disease'],
 ['<b>Stool occult blood</b>','Positive','GI involvement when there is abdominal pain'],
 ['<b>Serum IgA</b>','High in about half','Rarely needed; does not make the diagnosis'],
 [f'<b>PT and aPTT</b> {W}','Prolonged aPTT','Pursue a factor disorder when the history suggests one'],
 ['<b>Abdominal ultrasound</b>','Target sign','Intussusception; a negative study does not rule out an intermittent one'],
])}{table('The finalists: IgA vasculitis, ITP and leukemia',['Feature','IgA vasculitis','Immune thrombocytopenia','Leukemia'],[
 ['Who','Peak 4 to 6 yo (range 2 to 17); boys twice as often; about 10 per 100,000 a year','Peak 2 to 5 yo (range 2 to 10); boys and girls equally; about 5 per 100,000 a year','Constitutional symptoms and ill appearance'],
 ['Cause','Suspected IgA-dominated response to infection; leukocytoclastic vasculitis with IgA deposits','Antiplatelet antibody; platelets destroyed in spleen and liver','Marrow replaced by malignant cells'],
 ['Skin','<b>Palpable purpura</b>, symmetric, gravity-dependent; may start as macules or urticarial wheals','<b>Flat petechiae</b> and bruising, sometimes mucosal bleeding','Diffuse purpura and petechiae'],
 ['Elsewhere','Joints, colicky abdominal pain, kidneys','Nothing; no liver or spleen enlargement','Hepatomegaly, splenomegaly, adenopathy, bone pain'],
 ['Labs','<b>Platelets normal</b>; urinalysis decides renal involvement','<b>Isolated low platelets</b>, usually below 20,000','Two or more cytopenias'],
 ['Management','Supportive; watch for kidney disease and intussusception','Limit risky activity, avoid antiplatelet drugs; IVIG, IV methylprednisolone, or platelets only for severe bleeding','Oncology'],
],mask=3)}{grid('danger','IgA vasculitis: course, complications, counselling',[
 ('Hallmark','non-thrombocytopenic purpura; the commonest childhood vasculitis, about half of cases'),
 ('Kidney','about a third, usually hematuria; less common under 2 (about 25%); about 5% reach chronic kidney disease, fewer than 1% end-stage'),
 ('Gut','colicky pain in about 65%, sometimes before the rash; about half have guaiac-positive stool'),
 ('Intussusception','usually ileoileal, starting at a patch of edema or submucosal hemorrhage, so an enema cannot reduce it and non-reducing cases go to surgery'),
 ('Treatment','acetaminophen or an NSAID unless there is GI bleeding or glomerulonephritis; steroids are debated, used for severe abdominal pain, without proven renal protection'),
 ('Follow-up','urinalysis and blood pressure every 1 to 2 weeks for 1 to 2 months, then monthly to every other month for a year'),
 ('Recurrence','about 30%, weeks to months later, starting with any symptom; recheck urine and blood pressure'),
 ('Tell the family to return for','sudden or severe abdominal pain, blood in the stool, vomiting that stops fluids, puffy face, hands or feet, severe headache, blurred vision or confusion'),
])}<h5 class="authored-hdr">Scenario bank</h5>
<ol class="bank authored">
{bankB}</ol>
<div class="pearls"><span class="lbl">Pairs with</span> Part I <b>Anemia with Thrombocytopenia</b> picks up once two cell lines are down. Part II <b>Pediatric Acute Lymphoblastic Leukemia</b> owns the marrow branch. Part I <b>Hematuria</b> owns the glomerular workup that renal IgA vasculitis enters.</div>
<div class="rule"><span class="lbl">Transferable rule</span> For any bleeding complaint, name what failed (vessel, platelet, factor, or story) before naming a disease; the lesion's feel and location, the spleen, and the platelet count each remove a whole branch.</div>
{traps([('p-salient','Salient decoy','The preceding URI is shared by ITP and IgA vasculitis and cannot separate them.'),
        ('p-attr','Unchecked attribute','Purpura is read as a platelet problem without checking whether it is palpable, which is the vessel-wall tell.'),
        ('p-mirror','Mirror twin','A child who looks like ITP but has a palpable spleen is not ITP.')])}</div>
'''

open('/tmp/claude-0/briefA.html','w').write(briefA)
open('/tmp/claude-0/briefB.html','w').write(briefB)
s=open('index.html').read()
anchor='<div class="brief bs" id="bs-sickle-trait"'
assert s.count(anchor)==1
s=s.replace(anchor,briefA+'\n'+briefB+'\n'+anchor)
open('/tmp/claude-0/scratch.html','w').write(s)
print('ok', bankA.count('<li'), bankB.count('<li'))

# ======================================================================
# B2. AQUIFER SYMPTOM WORKUP, revised after the adversarial audit
# ======================================================================
B2='aq-bruising'
bankB2=''.join([
 li(B2,'dx',"6 yo boy, a week after a cold, with raised, nonblanching red-purple spots on the backs of both legs and the buttocks, swollen tender ankles and crampy periumbilical pain; platelets 280,000",
    "IgA vasculitis","urinalysis next","Immune thrombocytopenia","Acute lymphoblastic leukemia",src="aquifer"),
 li(B2,'next',"6 yo with 3 days of new bruises and pinpoint red spots on the legs and trunk; afebrile, alert, normal vital signs, no history of trauma",
    "Complete blood count with smear","the platelet count makes the first cut","PT and aPTT","Skeletal survey"),
 li(B2,'dx',"4 yo, well-appearing, flat petechiae everywhere and a nosebleed two weeks after a viral illness; platelets 12,000, hemoglobin and white count normal, no organomegaly",
    "Immune thrombocytopenia","low platelets, nothing else","IgA vasculitis","Acute lymphoblastic leukemia"),
 li(B2,'next',"5 yo with petechiae and platelets of 20,000 who otherwise looks like ITP, except that the spleen is palpable 3 cm below the costal margin",
    "Bone marrow examination","splenomegaly is not part of ITP","Observe as ITP","Intravenous immunoglobulin"),
 li(B2,'dx',"8 yo girl with frequent nosebleeds, easy bruising and bleeding for a day after a tooth extraction; platelet count normal; her mother has heavy periods",
    "Von Willebrand disease","a platelet-plug defect with a normal count","Hemophilia A","Immune thrombocytopenia"),
 li(B2,'dx',"7 yo boy with a hot, swollen knee after a minor fall, a deep thigh hematoma last year, and an uncle who bled after surgery; platelet count normal",
    "Hemophilia A","deep bleeding is a clotting-factor defect","Von Willebrand disease","IgA vasculitis"),
 li(B2,'next',"9-month-old who is not yet crawling, with a bruise on the ear and another on the upper back; the parent says he bruises easily; CBC and coagulation studies are normal",
    "Skeletal survey","bruises a non-mobile infant cannot get by accident","Reassurance","Bone marrow examination"),
 li(B2,'dx',"5 yo with purpura on the legs, abdominal pain and hematuria a week after bloody diarrhea; hemoglobin 7, platelets 40,000, schistocytes on the smear",
    "Hemolytic uremic syndrome","low platelets and hemolysis; IgA vasculitis keeps both normal","IgA vasculitis","Immune thrombocytopenia"),
 li(B2,'test',"6 yo diagnosed with IgA vasculitis on examination, with a normal platelet count",
    "Urinalysis","the only test the diagnosis itself requires","Serum IgA level","Skin biopsy"),
 li(B2,'test',"6 yo with IgA vasculitis whose urinalysis shows hematuria and proteinuria",
    "BUN and creatinine","measures the extent of renal disease","Serum IgA level","Renal ultrasound"),
 li(B2,'test',"5 yo with IgA vasculitis who develops sudden severe colicky abdominal pain with vomiting",
    "Abdominal ultrasound","looking for intussusception","Air contrast enema","Upper endoscopy"),
 li(B2,'next',"Intussusception in a 5 yo with IgA vasculitis; it is ileoileal and has not reduced on its own",
    "Surgical reduction","an enema cannot reach the small bowel","Air contrast enema","Observation with serial ultrasound"),
 li(B2,'next',"6 yo with IgA vasculitis whose purpura has faded; urinalysis and blood pressure were normal at diagnosis",
    "Urinalysis and blood pressure every 1 to 2 weeks","renal disease can follow the rash","No further follow-up needed","Repeat CBC and serum IgA every month"),
 li(B2,'next',"4 yo with ITP, platelets 15,000, skin petechiae only, no mucosal or other bleeding",
    "Observation with activity limits","count alone does not trigger treatment","Intravenous immunoglobulin","Platelet transfusion"),
 li(B2,'avoid',"4 yo with ITP and a painful sprained ankle",
    "Ibuprofen","impairs platelet function","Acetaminophen","Ice and elevation"),
])
briefB2=f'''<div class="brief aq" id="{B2}" data-shelf="peds" data-src="aquifer" data-case="Pediatrics 21">
<h4>Bruising and Purpura in a Child</h4>
<p class="sub">Aquifer Pediatrics 21 &middot; symptom workup &middot; name what failed before you name a disease</p>
{VIG}<div class="dp"><span class="lbl">The approach</span>
<p>A bruise is blood outside a vessel, so ask <b>what let it out</b>. Either the <b>vessel wall</b> is inflamed, the <b>platelet plug</b> is missing or faulty, the <b>clotting factors</b> are short, or something <b>hit the child</b>. Each failure leaves its own kind of bleed, and one blood count separates most of them. <i>Read the bleed, cut with the platelet count, and let the spleen overrule a reassuring story.</i></p></div>
{table('What failed: read it off the bleed',['','Vessel wall','Platelet plug','Clotting factors'],[
 ['<b>Looks like</b>','<b>Raised</b> purpura you can feel, on dependent skin','<b>Flat</b> petechiae and bruises; nose and gum bleeding','<b>Deep</b> bleeding into joints and muscle'],
 ['<b>After a cut</b>','Not a bleeding problem',f'Bleeds <b>at once</b> {W}',f'Stops, then bleeds again <b>later</b> {W}'],
 ['<b>Platelet count</b>','<b>Normal</b>','<b>Low</b> (ITP, leukemia), or normal with a faulty plug (von Willebrand)','<b>Normal</b>; the aPTT or PT is long'],
 ['<b>Children</b>','IgA vasculitis','ITP, leukemia, von Willebrand disease','Hemophilia A and B'],
],mask='none')}<div class="pearls"><span class="lbl">And the story</span> <b>Accidental</b> bruises sit on <b>shins, elbows and forehead</b>. Bruises on the <b>back, buttocks, face or ears</b>, bruises shaped like a hand, fingers, a bite or a buckle, or <b>any bruise in a child who cannot yet move about</b> are nonaccidental until proven otherwise.</div>
{grid('danger','Act before you finish the history',[
 ('Altered mental status, respiratory distress, delayed capillary refill','circulation, airway, breathing first'),
 (f'Fever with spreading purpura in an ill child {W}','sepsis, meningococcemia: antibiotics before the workup'),
 ('Pallor, fatigue, bone pain, a big spleen or nodes','marrow infiltration: CBC and smear today'),
 (f'Headache or confusion with low platelets {W}','intracranial bleeding'),
 ('Sudden severe abdominal pain, vomiting, bloody stool','intussusception'),
])}{grid('pearls','History: each answer moves a branch',[
 ('A cold 1 to 3 weeks ago','vessel or platelet; it precedes about half of IgA vasculitis and more than half of ITP, so it splits neither'),
 ('Bleeding after circumcision, shots, dental work or surgery; a family history','a <b>factor</b> or <b>plug</b> disorder'),
 ('Knee and ankle pain, crampy belly pain','<b>vessel</b>: IgA vasculitis'),
 ('Fever, malaise, weight loss, bone pain','<b>marrow</b>: leukemia'),
 ('Nose and gum bleeding','<b>platelet plug</b>; about 40% of ITP'),
 ('A story that does not fit the injury or the child’s age','<b>nonaccidental</b> trauma'),
])}{grid('pearls','Examination: three moves',[
 ('Feel the lesion','<b>raised</b> means the vessel wall; <b>flat</b> means blood leaking past a normal vessel'),
 ('Map it','<b>dependent</b> (legs, buttocks) is vasculitis; <b>bony prominences</b> is play; <b>protected</b> skin is abuse'),
 ('Feel the spleen and nodes','<b>neither ITP nor IgA vasculitis enlarges the spleen</b>, so a spleen more than 2 cm below the costal margin, or nodes over 2 cm, supraclavicular, hard or matted, send you to leukemia'),
])}{table('First tests, and what each result does',['Test','Result','What it changes'],[
 ['<b>CBC with platelet count</b>','<b>Normal</b> platelets','Vessel wall: <b>IgA vasculitis</b>'],
 ['','<b>Low</b> platelets, everything else normal','Isolated thrombocytopenia: <b>ITP</b>'],
 ['','<b>Low</b> platelets with anemia or an abnormal white count','Marrow or consumption: <b>smear next</b>'],
 [f'<b>Peripheral smear</b> {W}','<b>Blasts</b>','Leukemia: bone marrow examination'],
 ['','<b>Schistocytes</b>','Hemolytic uremic syndrome'],
 ['<b>Urinalysis</b>','<b>Blood or protein</b>','Kidney involved: add BUN and creatinine'],
 ['<b>Stool occult blood</b>','<b>Positive</b>','Gut involved; watch for intussusception'],
 [f'<b>PT and aPTT</b> {W}','<b>Long</b>','Factor disorder: pursue when the history points there'],
 ['<b>Abdominal ultrasound</b>','<b>Target sign</b>','Intussusception; a negative study does not exclude an intermittent one'],
 ['<b>Serum IgA</b>','High in about half','Changes nothing; rarely ordered'],
])}{table('The finalists, one decider per row',['','IgA vasculitis','Immune thrombocytopenia','Leukemia'],[
 ['<b>Platelets</b>','<b>Normal</b>','<b>Low</b>, usually under 20,000; nothing else abnormal','<b>Low</b>, with anemia or an abnormal white count'],
 ['<b>Skin</b>','<b>Raised</b> purpura, legs and buttocks','<b>Flat</b> petechiae; nose and gum bleeding','Petechiae and bruising, pallor'],
 ['<b>The child</b>','Well','Well','<b>Ill</b>: fever, malaise, weight loss, bone pain'],
 ['<b>Beyond the skin</b>','Joints, belly, <b>kidneys</b>','Nothing','<b>Spleen, liver, nodes</b>'],
 ['<b>Next</b>','<b>Urinalysis</b>','Nothing more if typical','<b>Smear, then marrow</b>'],
 ['<b>Treatment</b>','Supportive; NSAID unless GI bleeding or nephritis','Watch; IVIG or IV steroids only for serious bleeding','Oncology'],
 ['<b>Typical age</b>','4 to 6; boys twice as often','2 to 5','2 to 5'],
],mask='none')}{grid('danger','The answer here: IgA vasculitis',[
 ('Mechanism','<i>IgA-rich immune complexes inflame small vessels</i> in skin, gut, joints and kidney; biopsy shows leukocytoclastic vasculitis with IgA'),
 ('Kidney','about a third, usually hematuria, and it can appear after the rash; about 5% reach chronic kidney disease'),
 ('Gut','colicky pain, sometimes before the rash; about half have occult blood; intussusception is usually <b>ileoileal</b>, so an enema cannot reduce it'),
 ('Treatment','acetaminophen or an NSAID unless there is GI bleeding or nephritis; steroids for severe abdominal pain, with no proven kidney benefit'),
 ('Follow-up','<b>urinalysis and blood pressure every 1 to 2 weeks for 1 to 2 months</b>, then monthly to every other month for a year; about 30% recur'),
 ('Send them back for','severe belly pain, blood in the stool, vomiting that stops fluids, puffiness, severe headache, blurred vision or confusion'),
])}<h5 class="authored-hdr">Scenario bank</h5>
<ol class="bank authored">
{bankB2}</ol>
<div class="pearls"><span class="lbl">Pairs with</span> Part I <b>Anemia with Thrombocytopenia</b> picks up once two cell lines are down. Part II <b>Pediatric Acute Lymphoblastic Leukemia</b> owns the marrow branch. Part I <b>Hematuria</b> owns the glomerular workup that renal IgA vasculitis enters.</div>
<div class="rule"><span class="lbl">Transferable rule</span> For any bleeding complaint, name what failed (vessel, plug, factor, or force) before you name a disease; the feel of the lesion, the platelet count and the spleen each remove a whole branch.</div>
{traps([('p-salient','Salient decoy','The preceding cold is shared by ITP and IgA vasculitis and cannot separate them.'),
        ('p-attr','Unchecked attribute','Purpura read as a platelet problem without checking whether it is raised.'),
        ('p-mirror','Mirror twin','A child who looks like ITP but has a palpable spleen is not ITP.')])}</div>
'''
open('/tmp/claude-0/briefB2.html','w').write(briefB2)
s2=open('index.html').read()
s2=s2.replace('<div class="brief bs" id="bs-sickle-trait"',briefB2+'\n<div class="brief bs" id="bs-sickle-trait"')
open('/tmp/claude-0/scratch2.html','w').write(s2)
print('B2 items', bankB2.count('<li'))

# ======================================================================
# B3. Workup, rebuilt from the user's review of B2
#   rows = one entity read across; plain sentences; one bold per cell;
#   tests ordered first -> by branch -> confirm; NBME lead-ins verbatim
# ======================================================================
B3='aq-bruising'
# proposed page CSS for two-column clue tables (history, exam, red flags): the clue stays plain, the pointer carries the emphasis
CLUE_CSS='''<style>
table.cluet tbody td:first-child{font-weight:400;color:var(--ink-2);width:46%}
@media (max-width:640px){
  .tw table.cluet tbody tr{padding:10px 14px;margin:0 0 7px}
  .tw table.cluet tbody td:first-child{font-family:var(--sans);font-size:14px;font-weight:400;color:var(--ink-2);border-bottom:none;padding:0 0 2px;margin:0}
  .tw table.cluet tbody td:not(:first-child)::before{content:"\\2192  ";display:inline;font-size:14px;letter-spacing:0;text-transform:none;font-weight:400;color:var(--faint)}
  .tw table.cluet tbody td{padding:2px 0}
  .tw table.cluet tbody td:first-child{width:100%}
}
</style>'''
L_STUDY="Which of the following is the most appropriate diagnostic study to obtain at this time?"
L_CONFIRM="Which of the following laboratory studies is most likely to confirm the diagnosis?"
bankB3=''.join([
 li(B3,'dx',"6 yo boy, a week after a cold, with raised, nonblanching red-purple spots on the backs of both legs and the buttocks, swollen tender ankles and crampy periumbilical pain; platelets 280,000",
    "IgA vasculitis","urinalysis next","Immune thrombocytopenia","Nonaccidental trauma",src="aquifer"),
 li(B3,'test',"6 yo with 3 days of new bruises and pinpoint red spots on the legs and trunk; afebrile, alert, normal vital signs, no history of injury",
    "CBC with smear","the platelet count sorts every branch","PT and aPTT","Skeletal survey",lead=L_STUDY),
 li(B3,'dx',"4 yo, well-appearing, flat petechiae everywhere and a nosebleed two weeks after a viral illness; platelets 12,000, hemoglobin and white count normal, no organomegaly",
    "Immune thrombocytopenia","low platelets and nothing else","IgA vasculitis","Acute lymphoblastic leukemia"),
 li(B3,'next',"5 yo with petechiae and platelets of 20,000 who otherwise looks like ITP, except that the spleen is palpable 3 cm below the costal margin",
    "Bone marrow examination","a spleen this size is not ITP","Observe as ITP","Intravenous immunoglobulin"),
 li(B3,'dx',"8 yo girl with frequent nosebleeds, easy bruising and bleeding for a day after a tooth extraction; platelet count normal; her mother has heavy periods",
    "Von Willebrand disease","platelets that do not stick, at a normal count","Hemophilia","Immune thrombocytopenia"),
 li(B3,'dx',"7 yo boy, afebrile, with a warm, tense, swollen knee after a minor fall, a deep thigh hematoma last year, and an uncle who bled after surgery; platelet count normal",
    "Hemophilia","deep bleeding means a clotting factor","Von Willebrand disease","Septic arthritis"),
 li(B3,'test',"7 yo boy with a swollen knee after a minor fall; platelet count and PT normal, aPTT prolonged",
    "Factor VIII and IX activity","names the missing factor","Mixing study","Von Willebrand factor antigen",lead=L_CONFIRM),
 li(B3,'next',"9-month-old who cannot yet crawl, with a bruise on the ear and another on the upper back; the parent says he bruises easily; CBC and coagulation studies are normal",
    "Skeletal survey","a child who cannot crawl cannot bruise his back by accident","Reassurance","Hematology referral"),
 li(B3,'dx',"5 yo with purpura on the legs, abdominal pain and hematuria a week after bloody diarrhea; hemoglobin 7, platelets 40,000, schistocytes on the smear",
    "Hemolytic uremic syndrome","low platelets and hemolysis; IgA vasculitis keeps both normal","IgA vasculitis","Immune thrombocytopenia"),
 li(B3,'test',"6 yo diagnosed with IgA vasculitis on examination, platelet count normal",
    "Urinalysis","the only test the diagnosis itself requires","Serum IgA level","Skin biopsy",lead=L_STUDY),
 li(B3,'claim',"6 yo with raised purpura on both legs, ankle pain and a normal platelet count, whose serum IgA level comes back normal",
    "It does not exclude IgA vasculitis","serum IgA is high in only about half","It excludes IgA vasculitis","A skin biopsy is needed to decide",
    lead="Which of the following is the most appropriate interpretation of this result?"),
 li(B3,'test',"6 yo with IgA vasculitis whose urinalysis shows hematuria and proteinuria",
    "BUN and creatinine","measures the extent of renal disease","Serum IgA level","Renal ultrasound",lead=L_STUDY),
 li(B3,'test',"5 yo with IgA vasculitis who develops sudden severe colicky abdominal pain with vomiting",
    "Abdominal ultrasound","looking for intussusception","Air contrast enema","Abdominal radiograph",lead=L_STUDY),
 li(B3,'next',"5 yo with IgA vasculitis and an ileoileal intussusception that is still present on repeat ultrasound hours later, with ongoing pain",
    "Surgical reduction","an enema cannot reach the small bowel","Air contrast enema","Continued observation"),
 li(B3,'next',"6 yo with IgA vasculitis whose purpura has faded; urinalysis and blood pressure were normal at diagnosis",
    "Serial urine and BP checks","kidney disease can come after the rash","Serial CBC and serum IgA","No further follow-up"),
 li(B3,'next',"4 yo with ITP, platelets 15,000, skin petechiae only, no mucosal or other bleeding",
    "Observation","with activity limits; the count alone does not call for treatment","Intravenous immunoglobulin","Platelet transfusion"),
 li(B3,'avoid',"4 yo with ITP and a painful sprained ankle",
    "Ibuprofen","impairs platelet function","Acetaminophen","Ice and elevation"),
])
def t(caption,heads,rows,mask=None):   # plain first column (CSS already bolds it)
    return table(caption,heads,rows,mask)
briefB3=f'''<div class="brief aq" id="{B3}" data-shelf="peds" data-src="aquifer" data-case="Pediatrics 21">
<h4>Bruising and Purpura in a Child</h4>
<p class="sub">Aquifer Pediatrics 21 &middot; symptom workup &middot; vessel, platelets, clotting factors, or trauma</p>
{VIG}<div class="dp"><span class="lbl">The approach</span>
<p>Bruising is a finding, not a diagnosis. Ask what failed: the <b>vessel wall</b> (IgA vasculitis), the <b>platelets</b> (ITP, leukemia, von Willebrand disease), the <b>clotting factors</b> (hemophilia), or the <b>story</b> (accidental or nonaccidental trauma). Each leaves a different bruise, a different history and a different first test. Check first whether the child needs intervention now; then let the history, the examination and the platelet count remove whole branches at a time. The confirmatory test comes last, once one branch is left.</p></div>
{t('Red flags: act before the full history',['Finding','What it points to'],[
 ['Altered mental status, labored breathing, slow capillary refill','Unstable: <b>circulation, airway, breathing</b> first'],
 [f'Fever with fast-spreading purpura, ill child {W}','<b>Sepsis</b> or meningococcemia: antibiotics before the workup'],
 ['Pallor, fatigue, bone pain, big spleen or nodes','<b>Marrow</b> disease: CBC and smear today'],
 [f'Headache or confusion with low platelets {W}','<b>Intracranial</b> bleeding'],
 ['Sudden severe belly pain, vomiting, bloody stool','<b>Intussusception</b>'],
],mask='none')}{t('The differential, by what failed',['What failed','Diagnoses','What the bleeding looks like','First clue'],[
 ['Vessel wall','IgA vasculitis','<b>Raised</b> purpura, symmetric, on both legs and buttocks','Normal platelets; sore joints, belly pain, blood in the urine'],
 ['Platelets','ITP, leukemia, von Willebrand disease','<b>Flat</b> petechiae and bruises; nose and gum bleeding','Low count (ITP, leukemia), or a normal count with a family history (von Willebrand)'],
 ['Clotting factors','Hemophilia A and B','<b>Deep</b> bleeding into joints and muscle','Bleeding after circumcision, shots or surgery; bleeding relatives'],
 ['Accidental trauma','Play, falls','Flat bruises over <b>shins, elbows, forehead</b>','The story fits the injury and the child’s age'],
 ['Nonaccidental trauma','Abuse','Flat bruises on the <b>back, buttocks, face or ears</b>; patterned; different ages','The story does not fit, or the child cannot yet crawl'],
 [f'Infection {W}','Meningococcemia, sepsis','Purpura that <b>spreads</b> within hours','Fever in an ill-looking child'],
],mask=3)}{t('History: what each answer points to',['Clue','What it points to'],[
 ['A recent cold','Vessel or platelets: it comes before about half of IgA vasculitis and more than half of ITP, so it <b>separates neither</b>'],
 ['Bleeding after circumcision, shots or dental work; bleeding relatives','<b>Clotting factors</b> or von Willebrand disease'],
 ['Nose or gum bleeding','<b>Platelets</b>: about 40% of ITP'],
 ['Sore knees and ankles with crampy belly pain','<b>IgA vasculitis</b>'],
 ['Fever, weight loss, bone pain','<b>Leukemia</b>'],
 ['A story that does not fit the injury or the child’s age','<b>Nonaccidental</b> trauma'],
],mask='none')}{t('Examination: what each finding points to',['Finding','What it points to'],[
 ['Does not blanch when pressed','Blood outside the vessel: <b>purpura</b>, not a rash'],
 ['Raised, symmetric, on both legs and buttocks','<b>IgA vasculitis</b>'],
 ['Flat petechiae all over','<b>Low platelets</b>'],
 ['Flat bruises over shins, elbows, forehead','<b>Accidental</b>'],
 ['Flat, patterned, on the back, ears or face','<b>Nonaccidental</b> trauma'],
 ['Swollen joint after little or no injury','Joint bleed: <b>clotting factors</b>'],
 ['Spleen more than 2 cm below the ribs','Not ITP or IgA vasculitis: <b>leukemia or infection</b> (EBV is the commonest cause); a tip alone is normal in about 10%'],
 ['Nodes over 2 cm, supraclavicular, or hard and matted','<b>Malignancy</b>'],
],mask='none')}{t('First tests, in the order you would order them',['Test','Order','Result','What it points to'],[
 ['CBC with platelet count','First','<b>Normal</b> platelets','Vessel wall: IgA vasculitis'],
 ['CBC','First','<b>Low</b> platelets, nothing else abnormal','ITP'],
 ['CBC','First','<b>Low</b> platelets with anemia or an abnormal white count','Marrow or consumption: smear next'],
 [f'Peripheral smear {W}','By branch','<b>Blasts</b> or schistocytes','Leukemia, or hemolytic uremic syndrome'],
 ['Urinalysis and blood pressure','By branch','<b>Blood or protein</b>, or high blood pressure','Kidney involved: BUN and creatinine'],
 [f'PT and aPTT {W}','By branch','<b>aPTT long</b>, PT normal','Hemophilia or von Willebrand disease'],
 ['Abdominal ultrasound','By branch','<b>Intussusception</b>','A negative study does not exclude an intermittent one'],
 ['Bone marrow biopsy with flow cytometry','Confirms','<b>20% or more</b> blasts','Leukemia'],
 [f'Factor VIII, IX and von Willebrand studies {W}','Confirms','<b>Low</b> level','Names the bleeding disorder'],
 ['Skin biopsy, only if atypical','Confirms','<b>IgA</b> in the vessel walls','IgA vasculitis; rarely needed'],
 ['Serum IgA','Skip','High in only <b>about half</b>','Cannot confirm or exclude IgA vasculitis'],
],mask=4)}{t('The finalists, in the order of the workup',['','On arrival','CBC','Next','Confirms','Treatment and follow-up'],[
 ['IgA vasculitis','Well; raised purpura on the legs, sore ankles, belly pain','Platelets <b>normal</b>','Urinalysis and blood pressure','Clinical; biopsy only if atypical','Supportive; NSAID unless GI bleeding or nephritis; urine and BP checks for a year'],
 ['Immune thrombocytopenia','Well; flat petechiae, nose or gum bleeding','Platelets <b>low</b>, nothing else','Smear','Low platelets alone, in a typical story','Observe; IVIG or steroids for serious bleeding; no NSAIDs, limit contact sports'],
 ['Leukemia','Ill; fever, bone pain, big spleen or nodes','<b>Two or more</b> cell lines abnormal','Smear','Marrow: 20% or more blasts; lumbar puncture for CNS spread','Oncology'],
],mask=5)}{grid('danger','IgA vasculitis (formerly Henoch-Schönlein purpura)',[
 ('What it is','the commonest vasculitis of childhood, about half of cases; an IgA-mediated small-vessel vasculitis of the skin, gut, joints and kidneys that usually settles in about a month'),
 ('Who','4 to 6 years (range 2 to 17), boys about twice as often; about half follow a URI'),
 ('Mechanism','<i>an IgA-dominated immune response, often to an infection, inflames small vessels</i>; biopsy shows leukocytoclastic vasculitis with IgA deposits'),
 ('Features','<b>palpable purpura with a normal platelet count</b>, symmetric and gravity-dependent, sometimes starting as macules or hives; arthritis of the knees and ankles; colicky belly pain, sometimes before the rash; hematuria; <b>no big spleen</b>'),
 ('Diagnosis','clinical; the <b>urinalysis</b> is the one test it needs, with BUN and creatinine if the urine or blood pressure is abnormal'),
 ('Treatment','acetaminophen or an NSAID unless there is GI bleeding or nephritis; steroids are debated, used for severe belly pain, and have not been shown to protect the kidney'),
 ('Complications','kidney disease in about a third (about 5% chronic renal failure, under 1% end-stage); GI bleeding, with occult blood in about half; intussusception, usually <b>ileoileal</b>, so an enema cannot reduce it'),
 ('Follow-up','urinalysis and blood pressure every 1 to 2 weeks for 1 to 2 months, then monthly to every other month for a year; about 30% recur, weeks to months later'),
 ('Return for','severe belly pain, blood in the stool, vomiting that stops fluids, puffy face, hands or feet, severe headache, blurred vision or confusion'),
])}{grid('pearls','What sets it apart',[
 ('Versus ITP','platelets <b>normal</b>, and the purpura is raised'),
 ('Versus leukemia','a well child with normal counts and <b>no big spleen</b>'),
 ('Versus hemolytic uremic syndrome','<b>no anemia</b> or schistocytes, platelets normal'),
 ('Versus abuse','raised, <b>symmetric</b>, dependent lesions with joint, belly or kidney findings'),
])}<h5 class="authored-hdr">Scenario bank</h5>
<ol class="bank authored">
{bankB3}</ol>
<div class="pearls"><span class="lbl">Pairs with</span> Part I <b>Anemia with Thrombocytopenia</b> picks up once two cell lines are down. Part II <b>Pediatric Acute Lymphoblastic Leukemia</b> owns the marrow branch and its confirmatory biopsy. Part I <b>Hematuria</b> owns the glomerular workup that renal IgA vasculitis enters.</div>
<div class="rule"><span class="lbl">Transferable rule</span> For bruising in a child, decide whether the vessel, the platelets, the clotting factors or the story failed; the feel of the lesion, the platelet count and the spleen each remove a branch, and the confirmatory test comes only after one branch is left.</div>
{traps([('p-salient','Salient decoy','The recent cold is shared by ITP and IgA vasculitis and cannot separate them.'),
        ('p-attr','Unchecked attribute','Purpura read as a platelet problem without checking whether it is raised.'),
        ('p-mirror','Mirror twin','A child who looks like ITP but has a spleen more than 2 cm down is not ITP.'),
        ('p-test','Test-overrides-findings','A normal serum IgA offered as exclusion, when it is high in only about half.')])}</div>
'''
for cap in ('Red flags','History','Examination'):
    briefB3=briefB3.replace('<table data-mask="none"><caption>'+cap,'<table class="cluet" data-mask="none"><caption>'+cap)
open('/tmp/claude-0/briefB3.html','w').write(briefB3)
s3=open('index.html').read()
s3=s3.replace('<div class="brief bs" id="bs-sickle-trait"',briefB3+'\n<div class="brief bs" id="bs-sickle-trait"')
s3=s3.replace('</head>',CLUE_CSS+'</head>',1)
open('/tmp/claude-0/scratch3.html','w').write(s3)
print('B3 items', bankB3.count('<li'))
