#!/usr/bin/env python3
"""Lead fixes after the rewrite lanes (s175): airway label, cholestasis board answer line, infant-stool caption,
feeding-refusal pause point, bs-umbilical karyotype line. Run once from workspace/."""
import json, subprocess
def F(b): return subprocess.run(['python3', 'tools/spine/folder_of.py', b], capture_output=True, text=True).stdout.split('\t')[1].strip() + '/rewrite_s175/'
def load(b): return json.load(open(F(b) + 'rewrite_s175.json'))
def save(b, d): json.dump(d, open(F(b) + 'rewrite_s175.json', 'w'), indent=1, ensure_ascii=False)
def once(s, a, b):
    assert s.count(a) == 1, (a, s.count(a)); return s.replace(a, b)

d = load('airway')
r = next(x for x in d['raw'] if 'Risk factors, and the ones that are not' in x['old'])
r['new'] = once(r['new'], '<span class="lbl">Common wrong answers</span>', '<span class="lbl">Risk factors</span>')
r['lock_ok'] = sorted(set(r.get('lock_ok', []) + ['and', 'the', 'ones', 'that', 'are', 'not', 'negation', 'negation 3 of 4', '3 of 4']))
r['lock_reason'] = 'header list name "Risk factors"; the label tail held the fourth negation, every negation in the block body is kept (lead)'
save('airway', d)

d = load('cholestasis')
u = next(x for x in d['units'] if x['uid'] == 'U058')
u['new'] = once(u['new'], '</button> if the response is poor. ', '</button> if the response is poor: obeticholic acid. ')
u['new'] = once(u['new'], '<span class="sp-l">Obeticholic acid: second agent on board cards</span>', '')
u['note'] = (u.get('note', '') + '; lead: the visible line gives the board answer (obeticholic acid), the hover the practice fact (contract, "In practice" lines)').strip('; ')
save('cholestasis', d)

d = load('infant-stool')
pre = '<div class="sp-dx"><table class="dense">'
assert not any(x['uid'] == 'U009' for x in d['units'])
d['raw'].append({'old': pre + '<caption>Act now: the ill-appearing mimics</caption>',
                 'new': '<p class="sp-note">Setting: ill-appearing infant</p>' + pre + '<caption>Emergencies</caption>', 'claims': [],
                 'lock_ok': ['Act', 'now', 'the', 'mimics'], 'lock_reason': 'header rename H4; setting moved to the sp-note line', 'note': 'caption rename, setting note (lead)'})
save('infant-stool', d)

d = load('feeding-refusal')
d['raw'].append({'old': '<span class="si"><span class="mask">Neither decides it</span></span>\n<span class="pp-a">&rarr; <span class="mask">The biopsy decides it</span></span>',
                 'new': '<span class="si"><span class="mask">Skin testing: IgE sensitization only; celiac disease: refusal of gluten foods only</span></span>\n<span class="pp-a">&rarr; <span class="mask">Endoscopy with esophageal biopsy</span></span>',
                 'claims': [], 'lock_ok': ['Neither', 'negation', 'The', 'decides', 'it'],
                 'lock_reason': 'pause point content rule: the deciding line names the clue that defeats each offered test (S091, S047 rows), the answer names the test (S086)',
                 'note': 'pause point deciding line (lead)'})
d.setdefault('new_claims', []).extend([
    {'text': 'Skin testing: IgE sensitization only; celiac disease: refusal of gluten foods only', 'ids': ['L27', 'L30']},
    {'text': 'Endoscopy with esophageal biopsy', 'ids': ['L25']}])
save('feeding-refusal', d)

d = load('bs-umbilical')
r = next(x for x in d['raw'] if 'NBME framing' in x['old'])
r['new'] = once(r['new'], ', congenital adrenal hyperplasia or', ' or')
r['note'] = (r.get('note', '') + '; lead: congenital adrenal hyperplasia left out of the chromosomal examples (a single-gene disorder)').strip('; ')
for c in d['new_claims']:
    c['text'] = c['text'].replace(', congenital adrenal hyperplasia or', ' or')
save('bs-umbilical', d)
