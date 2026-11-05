"""s164 item 6: section-name pointers sweep (STANDING "No structural wording", C6: nothing on the page names the page's
structure). Survey local/s164/survey_ptr.py (34 hits in 20 briefs; brief titles used as drawers, e.g. "Osteoporosis
Screening and Treatment", and the cluster-c "Criteria needed" grid labels are not pointers and stay). Each pointer is
dropped where the sentence already states the action, or replaced by the deciding place's own words (B3), inside the
same Recall mask. Writes repair/s164/70_pointers.json; prints the op count."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), 'tools'))
from pagelib import read_page, briefs
ROWS = [
    ('backpain', 'Emergent MRI (Urgent risks)</span>', 'Emergent MRI</span>'),
    ('growing-pains', 'Guillain-Barr&eacute; syndrome: see Next step</span>',
     'Guillain-Barr&eacute; syndrome: admit; CSF analysis, nerve conduction studies; serial spirometry</span>'),
    ('bone-tumors', 'Aggressive: see Next step</span>', 'Aggressive: MRI of the whole involved extremity, then biopsy</span>'),
    ('bs-umbilical', 'Omphalocele or gastroschisis: the Act now row in Urgent risks, then surgery</span>',
     'Omphalocele or gastroschisis: cover it with a sterile, moist dressing, place a nasogastric tube, start IV fluids and antibiotics and keep the infant warm; then surgery</span>'),
    ('bs-umbilical', 'fluids and antibiotics in Urgent risks come before surgery', 'fluids and antibiotics come before surgery'),
    ('dementia', 'Thiamine, as for any undernourished patient (Urgent risks);', 'Thiamine, as for any undernourished patient;'),
    ('pmr', 'monitor glucose and blood pressure (Follow-up)<div', 'monitor glucose and blood pressure<div'),
    ('septic-hip', 'Tap an effusion even when the blood tests are normal (Urgent risks)</span>',
     'Tap an effusion even when the blood tests are normal</span>'),
    ('septic-hip', 'MRI, as in Targeted tests</span>', 'MRI</span>'),
    ('septic-hip', 'Radiographs of both hips (Workup, Targeted tests)<div', 'Radiographs of both hips<div'),
    ('bs-brachial-plexus', 'Apply the specialist referral criteria in Treatment;', 'Refer if no improvement over 1 to 2 months;'),
    ('zenker', 'This study is the diagnostic test (Diagnostic test)</span>', 'This study is the diagnostic test</span>'),
    ('zenker', 'Achalasia pathway (Next step)</span>', 'Esophageal manometry, then upper endoscopy</span>'),
    ('peds-uti-recurrent', 'IV (intravenous) antibiotics; the drug, by age, is in Treatment</span>',
     'IV (intravenous) antibiotics, the drug chosen by age</span>'),
    ('cluster-b', 'Diagnose it; screen for comorbid disorders as in Next step', 'Diagnose it; screen for depression and substance use'),
    ('cluster-b', 'Diagnose it; screen for substance use as in Next step', 'Diagnose it; screen for substance use'),
    ('trauma-stress', 'Order toxicology and a neurologic check first, as in First step', 'Order toxicology and a neurologic check first'),
    ('lithium-effects', 'a level past the cutoffs in Urgent risks</li>', 'a level past the dialysis cutoffs</li>'),
    ('lithium-effects', 'a level past the cutoffs in Urgent risks</span></p>', 'a level past the dialysis cutoffs</span></p>'),
    ('lithium-effects', 'Toxicity; dialysis if an Urgent risks criterion is met', 'Toxicity; hemodialysis when a dialysis criterion is met'),
]
if __name__ == '__main__':
    page = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.dirname(HERE)), 'index.html')
    html = read_page(page)
    B = {b.id: html[b.start:b.end] for b in briefs(html)}
    ops = []
    for bid, old, new in ROWS:
        n = B[bid].count(old)
        assert n == 1, (bid, n, old)
        ops.append({'op': 'replace', 'brief': bid, 'find': old, 'with': new, 'note': 's164 item 6: section-name pointer (C6)'})
    json.dump({'edits': ops}, open(os.path.join(HERE, '70_pointers.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print('70_pointers.json', len(ops), 'ops in', len({o['brief'] for o in ops}), 'briefs')
