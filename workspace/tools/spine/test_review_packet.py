"""offline checks for review_packet.py text_of and item_line (s135 S5 packet errors)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import review_packet as RP  # noqa: E402
ok = fail = 0
def expect(name, cond):
    global ok, fail
    print(('ok   ' if cond else 'FAIL ') + name); ok += cond; fail += (not cond)
t = RP.text_of('<p>first 5 years <span class="op op-a" role="img" aria-label="leads to"></span> then plateaus</p>')
expect('arrow glyph kept', '→ then plateaus' in t and 'years →' in t)
t = RP.text_of('<p>A <span class="op op-p" role="img" aria-label="and"></span> B</p>')
expect('and glyph as +', 'A + B' in t)
t = RP.text_of('<figure role="img" aria-label="Flowchart: x"><p>keep</p></figure>')
expect('a labeled figure with content is left alone', 'keep' in t and 'Flowchart' not in t)
t = RP.text_of('<ol class="bank"><li data-type="next" data-d1="Fluoxetine" data-d2="Parent management training" data-item-id="q_1" data-lead-in="Next?">stem &rarr; <b>Guanfacine</b></li></ol>')
expect('distractors named on the item line', 'distractors: Fluoxetine / Parent management training' in t)
t = RP.text_of('<ol class="bank"><li data-type="dx" data-item-id="q_2">stem</li></ol>')
expect('no distractor clause without d1/d2', '[item q_2, type dx] Lead-in: (none)' in t and 'distractors' not in t)
print('test_review_packet: %d passed, %d failed' % (ok, fail)); sys.exit(1 if fail else 0)
