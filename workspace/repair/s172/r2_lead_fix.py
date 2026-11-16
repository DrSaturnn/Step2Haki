#!/usr/bin/env python3
"""s172 chat 2: round 2 lead fixes. substance acc pair ("generally", both seizure hovers); substance read MED (rung 6
hover body named the masked flumazenil: the trigger and hover move inside a mask); psych-medical read MED (job-loss
line moved from the visible Risk screen hover into the masked Interpretation cell, "the illness" named)."""
import json
WS = '/home/claude/Step2Haki/workspace/repair/migration/psych/'
def edit(f, pairs, claim=None):
    p = WS + f + '/spine/rewrite_s172/rewrite_s172.json'
    rw = json.load(open(p))
    for old, new, n in pairs:
        h = [e for e in rw['units'] + rw['raw'] if old in e.get('new', '')]
        assert len(h) == n and all(e['new'].count(old) == 1 for e in h), (old, len(h))
        for e in h:
            e['new'] = e['new'].replace(old, new)
    if claim:
        for c in rw['new_claims']:
            if c['text'] == claim[0]:
                c['text'] = claim[1]
    json.dump(rw, open(p, 'w'), ensure_ascii=False, indent=1)
edit('TOX', [
 ('Wider range: seizure onset 6 to 48 hours', 'Wider range: seizure onset generally 6 to 48 hours', 2),
 ('<p class="sp-note"><button type="button" class="sp-pop" aria-expanded="false" aria-controls="tox-pop-18">',
  '<p class="sp-note"><span><span class="mask"><button type="button" class="sp-pop" aria-expanded="false" aria-controls="tox-pop-18">', 1),
 ('during a procedure</span></span></p>', 'during a procedure</span></span></span></span></p>', 1)])
JL = 'Later job loss or financial strain: a result of the depression'
edit('MED', [
 ('<span class="sp-l">Job loss or financial strain that follows: a consequence of the illness</span>', '', 1),
 ('major depressive disorder and adjustment disorder do not fit</span>',
  'major depressive disorder and adjustment disorder do not fit<br>' + JL + '</span>', 1)],
 claim=('Job loss or financial strain that follows: a consequence of the illness', JL))
print('ok')
