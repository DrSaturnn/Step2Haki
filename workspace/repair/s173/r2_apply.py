#!/usr/bin/env python3
"""Round 2 pairs: the lane_opus_2 receipt's pairs and the lane_opus_1 pairs (that lane ran out of calls before its
receipt; the pairs come from its hand-back) applied to each card's rewrite file where the old text occurs once."""
import json, re, subprocess
P = {
 'pc-atypical': [('after starting a selective serotonin reuptake inhibitor, a tricyclic and risperidone', 'after starting a selective serotonin reuptake inhibitor and risperidone'),
                 ('Atypical antipsychotics as a class: weight gain, lipids and glucose all rise', 'Atypical antipsychotics as a class: can raise weight, lipids and glucose')],
 'pc-antichol': [('Antihistamine action: present, with no established therapeutic role', 'Antihistamine action: present, with no established therapeutic role in parkinsonism'),
                 ('further tests unnecessary at this stage', 'further tests unnecessary until a trial off the drug')],
 'mood-anticonv': [('Leukocyte count may be decreased in valproate toxicity; GI symptoms with altered mental status implicate liver function', 'Leukocyte count may be decreased in valproate toxicity'),
                   ('concerning for a potentially life-threatening condition', 'concerning for potentially life-threatening nephrogenic diabetes insipidus')],
 'pc-benzo': [('Reported with alprazolam in panic disorder on maintenance doses', 'Reported in panic disorder on maintenance doses')],
 'sud-meds': [('Hepatitis may develop after many months of therapy, sometimes fatal', 'Hepatitis may develop as late as many months into therapy, sometimes fatal'),
              ('A sometimes fatal organ injury that may develop after many months of therapy', 'A sometimes fatal organ injury that may develop as late as many months into therapy'),
              ('methadone outlasts a dose', 'methadone outlasts a naloxone dose')],
 'pc-other': [('In practice: uncontrolled hypertension is a listed contraindication', 'Uncontrolled hypertension: a listed contraindication'),
              ('Toxic epidermal necrolysis: also reported with modafinil', 'Toxic epidermal necrolysis: also reported'),
              ('Drug rash with eosinophilia and systemic symptoms: also reported with modafinil', 'Drug rash with eosinophilia and systemic symptoms: also reported')],
}
txt = open('repair/efficiency/lanes/s173/r2/lane_opus_2/receipt.md').read()
for sec in re.split(r'^=== ', txt, flags=re.M)[1:]:
    bid = sec.split('\n', 1)[0].split()[0]
    for m in re.finditer(r'old: \{\{(.*?)\}\}\s*\n\s*new: \{\{(.*?)\}\}', sec, flags=re.S):
        if '⚠' in m.group(1) and '⚠' not in m.group(2):
            print('held for the owner (unverified mark):', bid, m.group(1)[:60]); continue
        P.setdefault(bid, []).append((m.group(1), m.group(2)))
for bid, ps in P.items():
    f = subprocess.run(['python3', 'tools/spine/folder_of.py', bid], capture_output=True, text=True).stdout.split('\t')[1].strip()
    p = f + '/rewrite_s173/rewrite_s173.json'
    j = json.load(open(p))
    for old, new in ps:
        hits = [e for e in j['units'] + j['raw'] if old in e.get('new', '')]
        if len(hits) == 1 and hits[0]['new'].count(old) == 1:
            hits[0]['new'] = hits[0]['new'].replace(old, new); print('applied', bid, hits[0].get('uid', 'raw'), '|', new[:50])
        else:
            print('LEFT', bid, len(hits), '|', old[:90], '=>', new[:90])
    json.dump(j, open(p, 'w'), ensure_ascii=False, indent=1)
