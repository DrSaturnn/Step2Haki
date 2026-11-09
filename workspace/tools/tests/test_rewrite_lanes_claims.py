#!/usr/bin/env python3
"""s171 claim-map fix in rewrite_lanes.collect: shared one-word claims stay put, raws carry claims, empty "claims"
lists count as unset, removed raws with "cut" cut their claims."""
import json, os, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'spine'))
import rewrite_lanes as RL  # noqa: E402

BASE = ('<div class="brief"><p>Borderline: fear of abandonment</p><p>Borderline: self-harm common</p>'
        '<div class="rule"><span class="lbl">Transferable rule</span><p>Ask where erections still work</p></div>'
        '<div class="pp"><span>Shy guard avoids people</span></div></div>')


def run(rw):
    d = tempfile.mkdtemp()
    os.makedirs(os.path.join(d, 'rewrite_t'))
    open(os.path.join(d, 'baseline_t.html'), 'w').write(BASE)
    claims = [{'id': 'S1', 'new_text': 'Borderline'}, {'id': 'S2', 'new_text': 'Ask where erections still work'},
              {'id': 'S3', 'new_text': 'Shy guard avoids people'}, {'id': 'S4', 'new_text': 'self-harm common'}]
    json.dump({'claims': claims}, open(os.path.join(d, 'claims_before_t.json'), 'w'))
    units = RL.units_of(BASE)
    RL.claims_for(units, {'claims': claims})
    json.dump({'units': units}, open(os.path.join(d, 'rewrite_t', 'units.json'), 'w'))
    json.dump(rw, open(os.path.join(d, 'rewrite_t', 'rewrite_t.json'), 'w'))
    RL.folder_of = lambda bid: d
    probs, n = RL.collect('t', 'x')
    delta = json.load(open(os.path.join(d, 'delta_t.json')))
    ups = {u['id']: u['new_text'] for c in delta['changes'] for u in c.get('claim_updates', [])}
    cuts = {u['id'] for c in delta['changes'] for u in c.get('claim_cuts', [])}
    return probs, ups, cuts


def test_all():
    units = RL.units_of(BASE)
    u2 = [u['uid'] for u in units if 'self-harm' in u['text']][0]
    probs, ups, cuts = run({'units': [{'uid': u2, 'new': '<p>Borderline: self-harm frequent</p>', 'claims': []}],
                            'raw': [{'old': '<p>Ask where erections still work</p>', 'new': '<p>Ask where erections persist</p>', 'claims': []},
                                    {'old': '<div class="pp"><span>Shy guard avoids people</span></div>', 'new': '', 'claims': [], 'cut': 'pause point removed'}]})
    assert not probs, probs
    assert 'S1' not in ups, ups            # shared one-word claim survives in the brief: untouched
    assert ups.get('S4') == 'Borderline: self-harm frequent', ups
    assert ups.get('S2') == 'Ask where erections persist', ups   # raw with "claims": [] carries its claim
    assert cuts == {'S3'}, cuts
    print('test_rewrite_lanes_claims: 1 passed')


if __name__ == '__main__':
    test_all()
