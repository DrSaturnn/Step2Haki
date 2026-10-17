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
d = RP.part_rules('display')
expect('display rules carry progressive recall and the 5a spec', 'progressive recall' in d and 'Diagnostic workup template: layout 5a' in d)
expect('display rules carry the glance and s137 display-layer decisions', 'Numbered workup zones adopted' in d and 'Test | Result | Means' in d)
r = RP.part_rules('read')
expect('read rules carry absent steps greyed', 'Absent steps stay numbered and greyed' in r and '## Display' not in r)
expect('acc gets the card-disposition rule (s146b); flags gets no rules file', 'Card dispositions' in RP.part_rules('acc') and RP.part_rules('flags') == '')
# s142 R1 packet error: text after a masked span (a rung note) must not read as masked
_t = RP.text_of('<div><b class="sp-f"><span class="mask">Move <span class="x">a</span> b</span></b><p class="sp-note">Note</p></div>')
expect('mask closes at its own span end', '[masked in study mode: Move a b]' in _t and '[masked in study mode: Note' not in _t)
# s144: the flags packet lists every line's sources, so old-brief (L id) citations are visible
_cm = {'claims': [{'id': 'S001', 'new_text': 'Chest x-ray first', 'sources': [{'id': 'L09', 'source': 'old brief cough', 'source_says': 'Chest x-ray first in all chronic cough'}]},
                  {'id': 'S002', 'new_text': 'Switch to an ARB', 'sources': [{'id': 'b02', 'source': 'AnKing card', 'source_says': 'Switch to an ARB'}, {'id': 'L09', 'source': 'old brief cough', 'source_says': 'Chest x-ray first in all chronic cough'}]}]}
_ls = RP.line_sources(_cm)
expect('line_sources lists every claim line with its ids', 'S001: "Chest x-ray first"  <- L09' in _ls and '<- b02, L09' in _ls)
expect('line_sources lists each quote once', _ls.count('[L09]') == 1 and _ls.count('[b02]') == 1)

print('test_review_packet: %d passed, %d failed' % (ok, fail)); sys.exit(1 if fail else 0)
