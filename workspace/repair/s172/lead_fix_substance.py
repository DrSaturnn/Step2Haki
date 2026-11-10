#!/usr/bin/env python3
"""s172 chat 2: lead fixes for the substance MEDs that carry exact text (acc 1 to 3, read 1 to 3, lane_opus_1 r1)."""
import json
p = '/home/claude/Step2Haki/workspace/repair/migration/psych/TOX/spine/rewrite_s172/rewrite_s172.json'
rw = json.load(open(p))
E = {e.get('uid'): e for e in rw['units']}
R = [
 ('U028', 'In practice: seizure onset 6 to 48 hours', 'Wider range: seizure onset 6 to 48 hours', None),
 ('U077', 'In practice: seizure onset 6 to 48 hours', 'Wider range: seizure onset 6 to 48 hours', None),
 ('U063', 'Anorexia, weight loss in acquired immunodeficiency syndrome (AIDS)', 'Anorexia with weight loss in acquired immunodeficiency syndrome (AIDS)', None),
 ('U081', 'Hypomania: not present without elevated mood or grandiosity', 'Hypomania: unlikely with no elevated mood or grandiosity',
  (['2 of 3'], 'r1 acc 3: the general rule bound back to the case ("no elevated mood or grandiosity"); one negation fewer by design')),
 ('U090', 'Benzodiazepine: lowers central sympathetic outflow. Cocaine: nitrates or an alpha-blocker if chest pain or hypertension persists after the benzodiazepine.',
  'Lowers central sympathetic outflow. Cocaine: nitrates or an alpha-blocker if chest pain or hypertension persists after this first drug.',
  (['Benzodiazepine'], 'r1 read 1: the visible line named the masked answer; the drug stays in the mask')),
 ('U093', 'Withdrawal seizures: also a benzodiazepine (not routine phenytoin). Delirium tremens: intravenous benzodiazepine, promptly.',
  'Withdrawal seizures: same drug (not routine phenytoin). Delirium tremens: same drug, intravenously and promptly.',
  (['benzodiazepine'], 'r1 read 2: the visible lines named the masked answer; the drug stays in the mask')),
 ('U102', '>Flumazenil use</button>', '>Reversal agent use</button>', None),
]
for uid, old, new, lock in R:
    e = E[uid]
    assert e['new'].count(old) == 1, (uid, e['new'].count(old))
    e['new'] = e['new'].replace(old, new)
    if lock:
        e['lock_ok'] = list(dict.fromkeys((e.get('lock_ok') or []) + lock[0]))
        e['lock_reason'] = ((e['lock_reason'] + '; ') if e.get('lock_reason') else '') + lock[1]
json.dump(rw, open(p, 'w'), ensure_ascii=False, indent=1)
print('applied', len(R))
