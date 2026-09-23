import json,hashlib,html
def h(s):return hashlib.sha256(s.encode()).hexdigest()[:20]
e=lambda s:html.escape(s,quote=True)
edits=[]
def item(b,t,stem,key,comp,d1,d2,lead=None,src="authored",nid=None):
    q='q_'+h(f"{t}|{key}|{stem[:60]}")
    k,o1,o2=['o_'+h(f"{q}|{s}|{l}") for s,l in (('key',key),('d1',d1),('d2',d2))]
    li=(f'<li data-type="{t}" data-src="{src}"'+(f' data-nid="{nid}"' if nid else '')+f' data-d1="{e(d1)}" data-d2="{e(d2)}" data-item-id="{q}" data-item-version="1" '
        f'data-item-status="ready" data-key-id="{k}" data-d1-id="{o1}" data-d2-id="{o2}"'+(f' data-lead-in="{e(lead)}"' if lead else '')+
        f'>{e(stem)} &rarr; <b>{e(key)}</b> &rarr; {e(comp)}</li>\n')
    edits.append({"scope":"brief:"+b,"op":"insert_before","anchor":"</ol>","text":li,"why":f"backfill {t} item"+(f" (source nid {nid})" if nid else " from the pasted explanation")})
# ---- nid provenance on earlier source items (metadata only, no version bump)
for q,add in [("q_f4911f58dd7176f6eabc",' data-src="uworld" data-nid="1517598242747"'),
              ("q_287157d11cade1003c9a",' data-src="uworld" data-nid="1520972870099 1539169569607"'),
              ("q_6ad8368a69544663af2f",' data-src="uworld" data-nid="1462209898939 1462210183851 1462210190761 1522298058967"'),
              ("q_2ee63804dd34cb933cbf",' data-nid="1482289546088"')]:
    edits.append({"scope":"page","op":"replace","old":f'data-item-id="{q}"',"new":f'data-item-id="{q}"{add}',"why":"provenance: source question nid (dedupe key); metadata only"})
# ---- meningitis: early meningococcal disease
MEN_N="1481771577462 1556473561662 1580485347506"
edits.append({"scope":"brief:meningitis","op":"insert_before","anchor":'<div class="pearls"><span class="lbl">Follow-up facts',"text":
'<div class="danger"><span class="lbl">Early meningococcal disease</span> <b>Onset</b> &mdash; nonspecific fever, headache, vomiting, myalgia or sore throat, easily mistaken for a viral or streptococcal pharyngitis &middot; <b>Red flags</b> &mdash; severe myalgia such as leg pain, poor perfusion with pallor, mottling or cold hands and feet, and the worst illness the patient has ever felt &middot; <b>Tempo</b> &mdash; petechiae, meningeal signs and altered mental status follow within 12 to 24 hours &middot; <b>Workup</b> &mdash; blood cultures and lumbar puncture, with ceftriaxone given without waiting for either &middot; <b>CT first only for</b> &mdash; recent seizure, obtundation, focal deficit, papilledema or immunocompromise &middot; <b>Complications</b> &mdash; shock, disseminated intravascular coagulation, adrenal haemorrhage &middot; <b>Prevention</b> &mdash; droplet precautions and chemoprophylaxis for close contacts</div>\n',
 "why":"explanation facts for nid 1481771577462 not on the page: early presentation, red flags, tempo"})
item("meningitis","test","16 yo M, 8 hours of abrupt high fever and sore throat with severe diffuse leg pain, says he has never felt this terrible; pale, nonexudative pharyngitis, supple neck, mottled tender legs; rapid strep and influenza negative; CBC and blood culture drawn",
     "Lumbar puncture","early meningococcal disease; no seizure, obtundation, focal deficit, papilledema or immunocompromise, so no CT first, and ceftriaxone does not wait",
     "Heterophile antibody test","CT scan of the neck","Which additional diagnostic test is the best next step?","uworld",MEN_N)
item("meningitis","dx","Adolescent 10 hours into an abrupt febrile illness with severe leg pain, cold hands and feet and mottled skin, no rash yet",
     "Meningococcemia","poor perfusion and severe myalgia arrive before the petechiae","Influenza","Infectious mononucleosis")
edits.append({"scope":"brief:meningitis","op":"insert_before_end","text":
'<div class="traps">\n<div class="trapline"><span class="pill p-salient">Salient decoy</span><span class="trapwhy">Heterophile antibody test &mdash; mononucleosis gives exudate and posterior cervical nodes, not leg pain, mottling and a collapse measured in hours.</span></div>\n<div class="trapline"><span class="pill p-salient">Salient decoy</span><span class="trapwhy">CT scan of the neck &mdash; deep neck infection brings trismus, uvular deviation or a bulging pharyngeal wall.</span></div>\n<div class="trapline"><span class="pill p-salient">Salient decoy</span><span class="trapwhy">Throat culture for diphtheria &mdash; needs a gray, adherent pharyngeal pseudomembrane.</span></div>\n<div class="trapline"><span class="pill p-salient">Salient decoy</span><span class="trapwhy">HIV antigen/antibody test &mdash; acute HIV adds diffuse lymphadenopathy, rash and diarrhoea.</span></div>\n</div>\n',
 "why":"distractor analysis for nid 1481771577462; sore throat is the decoy in all four"})
# ---- febrile seizure
FS_N="1513200856433 1537634414880 1539283381665 1583177614030"
edits.append({"scope":"brief:febrile-seizure","op":"replace","old":"The same trigger, but focal, prolonged, or recurrent within 24 hours ⚠︎</td>","new":"The same trigger, but focal, prolonged, or recurrent within 24 hours</td>",
 "why":"flag verified in-context: UWorld library entry, febrile seizure (complex = over 15 min, focal, or clustered; simple does not recur within 24 h)"})
edits.append({"scope":"brief:febrile-seizure","op":"insert_before","anchor":'<div class="pearls"><span class="lbl">Pearls',"text":
'<div class="pearls"><span class="lbl">Counselling, and what each test is for</span> <b>Recurrence</b> &mdash; about 30% have another febrile seizure &middot; <b>Epilepsy</b> &mdash; risk slightly raised, about 1% overall &middot; <b>Antipyretics</b> &mdash; treat discomfort, do not prevent the next seizure &middot; <b>Course</b> &mdash; resolves by school age, with no effect on development &middot; <b>Risk factors</b> &mdash; fever of 39.5 &deg;C or higher, a viral illness such as roseola or influenza, recent immunisation, a family history of febrile seizures or epilepsy &middot; <b>Timing</b> &mdash; usually the first day of the illness, sometimes before the viral symptoms appear &middot; <b>Brain imaging</b> &mdash; focal neurologic signs &middot; <b>EEG</b> &mdash; recurrent unprovoked seizures, not a simple febrile seizure &middot; <b>Admission</b> &mdash; not back to neurologic baseline &middot; <b>Electrolytes and glucose</b> &mdash; vomiting or diarrhoea, since hypoglycaemia and hyponatraemia can provoke a seizure &middot; <b>Lumbar puncture</b> &mdash; also at 6 to 12 months with incomplete pneumococcal or Hib immunisation, or when already on antibiotics</div>\n',
 "why":"explanation (nid 1513200856433) and library entry facts not on the page: counselling, risk factors, per-test indications"})
item("febrile-seizure","next","2 yo M, 2 days of rhinorrhea, fever 39.2 C this morning, a 3-minute generalized seizure, sleepy and confused when paramedics arrived, now alert and playful with a normal examination; uncle has epilepsy; immunizations current",
     "Reassurance and discharge home","simple febrile seizure; the postictal drowsiness has resolved and an uncle's epilepsy changes nothing",
     "Electroencephalography","Hospitalization for observation","After acetaminophen, which is the best next step in management?","uworld",FS_N)
item("febrile-seizure","claim","Parents of a 2 yo after a first simple febrile seizure ask what to expect",
     "About 30% have another; epilepsy risk stays near 1%","antipyretics do not prevent the next one",
     "Scheduled antipyretics during fevers prevent recurrence","About 30% go on to develop epilepsy","Which statement about the prognosis is correct?")
item("febrile-seizure","next","2 yo back to baseline after a brief generalized febrile seizure, but with 2 days of profuse vomiting and diarrhea and dry mucous membranes",
     "Serum electrolytes and glucose","hypoglycemia or hyponatremia can provoke a seizure","Electroencephalography","Reassurance and discharge home")
item("febrile-seizure","next","11-month-old back to baseline after a first simple febrile seizure, with no pneumococcal or Hib vaccine doses",
     "Lumbar puncture","incomplete immunization at 6 to 12 months lowers the bar to tap","Reassurance and discharge home","Electroencephalography")
json.dump({"pass":"s05-backfill","date":"2026-09-22","reason":"Two pasted UWorld questions (nids absent from page) backfilled into their owning briefs; explanation and library facts added; earlier batch source items given nids.","expected":{"mcq_delta":6},"edits":edits},open('repair/LEDGER-s05.json','w'),indent=1,ensure_ascii=False)
print(len(edits))
