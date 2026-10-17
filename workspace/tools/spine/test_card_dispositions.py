#!/usr/bin/env python3
"""offline tests for card_dispositions.check (s146b): a temp folder with a fake cards.md, claim map and dispositions"""
import json, os, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import card_dispositions as CD
ok = bad = 0
def expect(name, cond):
    global ok, bad
    print(('ok   ' if cond else 'FAIL ') + name); ok += cond; bad += (not cond)
T = tempfile.mkdtemp()
page = os.path.join(T, 'page.html')
open(page, 'w').write('<div class="brief" id="hypercalcemia"></div><div class="brief sp" id="polyuria"></div>')
open(os.path.join(T, 'cards.md'), 'w').write('''# Card checklist
## card 111 (deck)
- anchor (cloze): water restriction
- card text: Primary polydipsia can be treated with [water restriction]
- [111.aa] This normalizes urine output
## candidate 222 (deck)
- anchor (cloze): lithium
- card text: Lithium causes nephrogenic DI
## candidate 333 (deck)
- anchor (cloze): hemophilia A
- card text: desmopressin treats hemophilia A
''')
json.dump({'claims': [{'id': 'S001'}, {'id': 'S002'}]}, open(os.path.join(T, 'claim_map.json'), 'w'))
json.dump({'facts': [{'id': 'b01'}]}, open(os.path.join(T, 'facts.json'), 'w'))
open(os.path.join(T, 'brief.html'), 'w').write('<p>Primary polydipsia: water restriction normalizes the urine output.</p>')
def run(d):
    json.dump(d, open(os.path.join(T, 'cards_disposition.json'), 'w'))
    return CD.check(T, page, quiet=True)
e, w = run({'111': 'covered:S001 clue table', '222': 'owner:polyuria', '333': 'not-topic'})
expect('a complete, valid set passes', not e and not w)
e, w = run({'111': 'covered:S001', '222': 'owner:polyuria'})
expect('a card with no disposition fails', any('333' in x for x in e))
e, w = run({'111': 'covered:S009', '222': 'owner:polyuria', '333': 'not-topic'})
expect('covered with an unknown claim id fails', any('S009' in x for x in e))
e, w = run({'111': 'covered: the clue table', '222': 'owner:polyuria', '333': 'not-topic'})
expect('covered with no claim id fails', any('no claim id' in x for x in e))
e, w = run({'111': 'covered:S001', '222': 'owner:lithium-tox', '333': 'not-topic'})
expect('owner that is not a live brief fails', any('lithium-tox' in x for x in e))
e, w = run({'111': 'covered:S001', '222': 'scope:', '333': 'not-topic'})
expect('scope without a reason fails', any('scope needs a reason' in x for x in e))
e, w = run({'111': 'covered:S001', '222': 'conflict:m99 msd differs', '333': 'not-topic'})
expect('conflict naming an unknown fact fails', any('m99' in x for x in e))
e, w = run({'111': 'covered:S001', '222': 'maybe', '333': 'not-topic'})
expect('an unknown kind fails', any('unknown disposition' in x for x in e))
open(os.path.join(T, 'brief.html'), 'w').write('<p>Primary polydipsia: water restriction.</p>')
e, w = run({'111': 'covered:S001', '222': 'owner:polyuria', '333': 'not-topic'})
expect('a covered statement whose words are absent is warned, not failed', not e and any('111.aa' in x for x in w))
os.remove(os.path.join(T, 'cards.md'))
e, w = CD.check(T, page, quiet=True)
expect('no cards.md is an error from check', bool(e))
print('test_card_dispositions: %d passed, %d failed' % (ok, bad))
sys.exit(1 if bad else 0)
