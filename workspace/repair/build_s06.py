import json,html,sys
sys.path.insert(0,'tools');from idgen import item_id,option_id
e=lambda s:html.escape(s,quote=True)
edits=[]
def item(b,t,stem,key,comp,d1,d2,lead=None,src="authored",nid=None):
    q=item_id(b,t,key,stem);k,o1,o2=option_id(q,'key',key),option_id(q,'d1',d1),option_id(q,'d2',d2)
    li=(f'<li data-type="{t}" data-src="{src}"'+(f' data-nid="{nid}"' if nid else '')+f' data-d1="{e(d1)}" data-d2="{e(d2)}" data-item-id="{q}" data-item-version="1" '
        f'data-item-status="ready" data-key-id="{k}" data-d1-id="{o1}" data-d2-id="{o2}"'+(f' data-lead-in="{e(lead)}"' if lead else '')+
        f'>{e(stem)} &rarr; <b>{e(key)}</b> &rarr; {e(comp)}</li>\n')
    edits.append({"scope":"brief:"+b,"op":"insert_before","anchor":"</ol>","text":li,"why":f"backfill {t} item"+(f" (source nid {nid})" if nid else " from the pasted explanation")})
def block(b,cls,label,parts,anchor,why):
    body=' &middot; '.join(f'<b>{e(t)}</b> &mdash; {e(d)}' for t,d in parts)
    edits.append({"scope":"brief:"+b,"op":"insert_before","anchor":anchor,"text":f'<div class="{cls}"><span class="lbl">{e(label)}</span> {body}</div>\n',"why":why})
P='<div class="pearls"><span class="lbl">Pearls'
# ---------- IVH -> bs-preterm-followup
N1="1473707601064 1483930621644 1520636289409 1521430529603"
block('bs-preterm-followup','danger','Intraventricular hemorrhage',[
 ('Mechanism','fragile germinal matrix vessels rupture with swings in cerebral perfusion (hypotension, hypoxia, hypo- or hyperventilation), and the blood can extend into the lateral ventricles'),
 ('Who','under 32 weeks gestation or under 1500 g'),
 ('When','the first few days of life, and often asymptomatic'),
 ('Symptomatic signs','lethargy, hypotonia, seizures, apnea, bradycardia, a bulging fontanelle, a rapidly rising head circumference, acute anemia'),
 ('Diagnosis','cranial ultrasound, repeated to follow progression; routine screening under 32 weeks'),
 ('Versus hypoglycemia or hypocalcemia','lethargy, hypotonia and seizures, but never a growing head'),
 ('Versus hypoxic ischemic encephalopathy','needs perinatal asphyxia and acidosis, not a day-3 onset after Apgar scores of 8 and 9'),
 ('Versus meningitis','needs fever or risk factors such as maternal fever or prolonged rupture of membranes')],P,
 "explanation facts for nid 1473707601064: symptomatic IVH was not on the page (only screening)")
item('bs-preterm-followup','dx',"3-day-old born at 28 weeks, 1.04 kg, Apgar scores 8 and 9, afebrile, no maternal fever, membranes ruptured 3 hours before birth; an hour of lethargy and hypotonia, apnea with bradycardia, a tense fontanelle, head circumference up 3 cm since yesterday, then a generalized seizure",
 "Intraventricular hemorrhage","germinal matrix bleed; confirm with cranial ultrasound","Hypoxic ischemic encephalopathy","Hypoglycemia",
 "Which is the most likely cause of this patient's condition?","uworld",N1)
item('bs-preterm-followup','test',"Neonate born at 29 weeks who on day 2 develops apnea, lethargy and a bulging anterior fontanelle",
 "Cranial ultrasound","sees blood in the germinal matrix and ventricles through the open fontanelle","CT of the head","Electroencephalography")
# ---------- branchial cleft cyst -> lymphadenitis
N2="1462808874657 1489115594180 1535323341478"
edits.append({"scope":"brief:lymphadenitis","op":"insert_before","anchor":"</tbody>","text":
 '<tr><td>Infected branchial cleft cyst</td><td>Congenital second-arch remnant that declares itself after a URI, often in later childhood</td><td><b>Cystic lateral mass with a draining pit anterior to the sternocleidomastoid</b></td><td>A solid tender node with no pit or sinus tract</td></tr>\n',
 "why":"the node's closest congenital mimic (nid 1462808874657)"})
block('lymphadenitis','pearls','Congenital neck masses, sorted by location',[
 ('Midline, moves with swallowing or tongue protrusion','thyroglossal duct cyst, often found after a URI'),
 ('Midline, does not move with the tongue','dermoid cyst, along an embryologic fusion plane'),
 ('Lateral, anterior to the sternocleidomastoid, below the mandible','branchial cleft cyst, usually second arch, between the internal and external carotids; cured by resecting the cyst and its tract'),
 ('Lateral, necrotic node with violaceous skin and a fistula','nontuberculous mycobacterial adenitis'),
 ('Posterior triangle, from birth or on prenatal ultrasound','cystic hygroma'),
 ('Lateral, enlarges with Valsalva','laryngocele, through the thyrohyoid membrane; glassblowers and trumpet players'),
 ('Submandibular sinus draining sulfur granules','actinomyces, after dental infection or trauma')],P,
 "explanation table for nid 1462808874657: location sorts congenital neck masses; not on the page")
item('lymphadenitis','dx',"12 yo M with a painful left neck lump a week after a febrile URI, now cystic, with a small pit anterior to the sternocleidomastoid draining mucopurulent fluid",
 "Branchial cleft cyst","second-arch remnant infected after a URI; resect cyst and tract","Actinomyces lymphadenitis","Thyroglossal duct cyst",None,"uworld",N2)
item('lymphadenitis','dx',"8 yo with a tender midline neck cyst after a cold that rises when she sticks out her tongue",
 "Thyroglossal duct cyst","follows the path of thyroid descent from the foramen cecum","Dermoid cyst","Branchial cleft cyst")
item('lymphadenitis','dx',"Adult trumpet player with a soft lateral neck swelling that enlarges when he bears down",
 "Laryngocele","laryngeal mucosa pouching through the thyrohyoid membrane, inflated by pressure","Branchial cleft cyst","Cystic hygroma")
# ---------- hyper-IgE -> cgd
N3="1487727748709 1487727748710"
edits.append({"scope":"brief:cgd","op":"insert_before","anchor":"</tbody>","text":
 '<tr><td>Impaired Th17 signalling (JAK-STAT)</td><td>Hyper-IgE (Job) syndrome</td><td><b>Cold staphylococcal and Candida abscesses, severe eczema, eosinophilia</b> with a normal white count</td><td>No eczema or eosinophilia; granulomas and Burkholderia point to the oxidative burst</td></tr>\n',
 "why":"hyper-IgE belongs in the which-defect table (nid 1487727748709)"})
block('cgd','pearls','Reading the CBC in recurrent abscesses',[
 ('Eosinophilia, normal white count','hyper-IgE syndrome'),
 ('Marked leukocytosis with neutrophilia','leukocyte adhesion deficiency'),
 ('Neutropenia with oculocutaneous albinism','Chédiak-Higashi syndrome'),
 ('Small platelets with bruising','Wiskott-Aldrich syndrome'),
 ('Lymphopenia','DiGeorge syndrome, whose infections are invasive viral, fungal and bacterial rather than cold abscesses'),
 ('Unremarkable CBC with Candida infections','myeloperoxidase deficiency'),
 ('Job syndrome, the rest','autosomal dominant; eczema from the first weeks of life, recurrent sinopulmonary infection, broad nose and prominent forehead, retained primary teeth; genetic testing confirms; skin care and antibiotic prophylaxis')],P,
 "explanation for nid 1487727748709: every distractor fails on a CBC finding")
item('cgd','dx',"3 yo M with eczema since infancy and recurrent Staphylococcus aureus and Candida abscesses, now a nontender fluctuant buttock abscess, afebrile; leukocytes 9,000 with 30% neutrophils and 40% eosinophils",
 "Hyper-IgE syndrome","impaired Th17 signalling blunts neutrophil recruitment","Myeloperoxidase deficiency","Wiskott-Aldrich syndrome",
 "Which is the most likely underlying diagnosis?","uworld",N3)
item('cgd','dx',"2 yo with recurrent staphylococcal skin infections, silvery hair, pale skin and neutropenia",
 "Chédiak-Higashi syndrome","lysosomal trafficking defect","Hyper-IgE syndrome","Leukocyte adhesion deficiency")
item('cgd','mech',"Why the abscesses of hyper-IgE syndrome are cold, without erythema or tenderness",
 "Th17 defect blunts neutrophil recruitment","few neutrophils arrive, so little inflammation","NADPH oxidase cannot generate superoxide","Neutrophils cannot adhere to the endothelium")
json.dump({"pass":"s06-backfill","date":"2026-09-22","reason":"Three pasted UWorld questions, none already on the page, backfilled into owning briefs with explanation facts.","expected":{"mcq_delta":8},"edits":edits},open('repair/LEDGER-s06.json','w'),indent=1,ensure_ascii=False)
print(len(edits))
