#!/usr/bin/env python3
"""Offline tests for the pre-review lint (tools/spine/lint.py, s148 efficiency fix 6). Each positive case is an s148
round-1 MED (or the runbook's R3 example); each negative case is its fixed line.

  python3 tools/spine/test_lint.py
"""
import json
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lint as L  # noqa: E402

ok = bad = 0


def expect(name, cond):
    global ok, bad
    if cond:
        ok += 1
    else:
        bad += 1
        print('FAIL', name)


def clue_table(rows):
    body = ''.join('<tr><td>%s</td><td><span class="mask">%s</span></td><td><span><span class="mask">%s</span></span></td></tr>'
                   % r for r in rows)
    return ('<div class="brief" id="t"><table class="dense"><thead><tr><th>Clue</th><th>Points to</th>'
            '<th>Next best step</th></tr></thead><tbody>%s</tbody></table>'
            '<h5 class="authored-hdr" id="t-practice">Practice</h5><table><thead><tr><th>Next best step</th></tr></thead>'
            '<tbody><tr><td>Not in the bank</td></tr></tbody></table></div>' % body)


# ---- next-step: s148 round-1 MEDs (bs-puv read 2, scaphoid read 4, backpain read 3, gtps read 3)
for cell in ('Not the outlet: valves dilate both sides', 'Not valves', 'Not a nerve problem',
             'A palmar fascia cord, not a tendon', 'Not spondyloarthritis', 'Aortitis',
             'Hip abduction weak instead: L5 radiculopathy', 'Recognize it; not a cuff tear'):
    expect('next-step flags %r' % cell, len(L.lint_next_step(clue_table([('clue', 'dx', cell)]))) == 1)
for cell in ('Check vitamin B12; a one-sided thigh patch is not this',
             'Conservative care; a glucocorticoid injection if it persists', 'A motor deficit: MRI promptly',
             'Diagnose it clinically from the history and exam; the joint fluid is sterile', 'Treat GTPS',
             'Scrotal ultrasound and tumor markers', 'Insulin-like growth factor 1',
             'Follow the red-eye workup<div class="sp-chips"><button type="button" class="sp-drw">The Red Eye</button></div>'):
    expect('next-step passes %r' % cell[:40], L.lint_next_step(clue_table([('clue', 'dx', cell)])) == [])
expect('next-step ignores the Practice bank', L.lint_next_step(clue_table([])) == [])

# ---- alias (runbook section 3: other names at first mention and in the differential row)
TAB = [{'name': 'Reactive arthritis', 'aliases': ['Reiter syndrome']}]
bad_html = ('<div class="brief"><p>Reactive arthritis follows urethritis.</p><table><tr><td>Reactive arthritis</td>'
            '<td>sterile fluid</td></tr></table><h5 class="authored-hdr">Practice</h5></div>')
good_html = ('<div class="brief"><p>Reactive arthritis <span class="aka">(formerly Reiter syndrome)</span> follows '
             'urethritis.</p><table><tr><td>Reactive arthritis (Reiter syndrome)</td><td>sterile fluid</td></tr></table>'
             '<h5 class="authored-hdr">Practice</h5></div>')
expect('alias: missing at first mention and in the row', len(L.lint_alias(bad_html, TAB)) == 2)
expect('alias: present in both', L.lint_alias(good_html, TAB) == [])
expect('alias: a mention outside the first cell is no differential row',
       L.lint_alias(good_html.replace('<td>Reactive arthritis (Reiter syndrome)</td>', '<td>Gout</td>')
                    .replace('sterile fluid', 'not reactive arthritis'), TAB) == [])

# ---- hedge: a quote's hedge dropped from the claim (s148 round-1 flags LOW and MED family)
Q = 'A displaced waist fracture often disrupts the blood supply to the proximal pole'
expect('hedge: dropped "often" is flagged',
       len(L.lint_hedge([('S1', 'A displaced waist fracture disrupts the blood supply to the proximal pole', [Q])])) == 1)
expect('hedge: kept "often" passes',
       L.lint_hedge([('S1', 'A displaced waist fracture often disrupts the blood supply to the proximal pole', [Q])]) == [])
expect('hedge: "can" in the claim counts as its hedge',
       L.lint_hedge([('S2', 'Arteritis can appear later, even after an apparent cure of the aching',
                      ['Giant cell arteritis may develop at the onset or much later'])]) == [])
expect('hedge: permissive "can" in a quote is not a hedge',
       L.lint_hedge([('S3', 'Many nondisplaced fractures are treated with a thumb spica cast',
                      ['Many nondisplaced fractures can be treated definitively with a thumb spica cast'])]) == [])
expect('hedge: "the likely diagnosis" in a card stem is not a hedge',
       L.lint_hedge([('S4', 'Hand numbness in pregnancy points to carpal tunnel syndrome of pregnancy',
                      ['What is the likely diagnosis in a pregnant patient with hand numbness? carpal tunnel syndrome'])]) == [])
expect('hedge: a short label is skipped', L.lint_hedge([('S5', 'De Quervain tenosynovitis', ['it may be De Quervain tenosynovitis'])]) == [])

# ---- threshold: backpain "past 4 to 6 weeks" against "past 6 weeks" (s148 round-2 read MED)
TH = '<div class="brief"><p>Radicular pain past 4 to 6 weeks: MRI.</p><p>MRI only for pain past 6 weeks.</p>%s</div>'
expect('threshold: overlapping values flagged', len(L.lint_threshold(TH % '')) == 1)
expect('threshold: the fixed line passes', L.lint_threshold(TH.replace('4 to 6', '6') % '') == [])
expect('threshold: "after" and "past" are one phrase', len(L.lint_threshold(
    '<p>Image after 6 weeks.</p><p>Image past 4 to 8 weeks.</p>')) == 1)
expect('threshold: separate facts pass', L.lint_threshold('<p>Fix within 6 hours.</p><p>Reduce within 24 hours.</p>') == [])
expect('threshold: bank lines are not body lines', L.lint_threshold(
    '<p>past 6 weeks</p><h5 class="authored-hdr">Practice</h5><p>past 4 to 6 weeks</p>') == [])

# ---- number: runbook R3 "median 3" (a number with no quote)
expect('number: no quote holds it', len(L.lint_number([('S1', 'Relapses, median 3', ['Relapses are common'])])) == 1)
expect('number: quoted range holds both ends',
       L.lint_number([('S2', 'Prednisone 15 to 20 mg daily', ['Prednisone started at 15 to 20 mg orally'])]) == [])
expect('number: "beta-2" is a name', L.lint_number([('S3', 'Beta-2 microglobulin amyloidosis', ['amyloid'])]) == [])
expect('number: "rung 2" is a label', L.lint_number([('S4', 'MRI (the ladder, rung 2)', ['MRI for a deficit'])]) == [])
expect('number: a number word in the quote counts',
       L.lint_number([('S5', 'Repeat films in 2 weeks', ['repeat radiographs in two weeks'])]) == [])
expect('number: 50,000 matches 50,000', L.lint_number([('S6', 'over 50,000 cells', ['WBC > 50,000/mcL'])]) == [])

# ---- prose (s148f; Jonathan 2026-10-19: "chase the medical cause is an ai euphemism", "A night by stage", "by presentation")
w5 = '<figure class="lcp w5a"><p class="w5z">%s</p><div class="w5t"><div class="w5b"><div class="w5c">Clue</div><div class="w5o"><span class="mask w5om"><span class="w5ol">%s</span></span></div></div></div></figure>'
expect('prose: "Chase the medical cause" in a workup step', len(L.lint_prose(w5 % ('Next step', 'Chase the medical cause'))) == 1)
expect('prose: a concrete test passes', L.lint_prose(w5 % ('Next step', 'TSH, CBC, metabolic panel')) == [])
expect('prose: zone "By presentation" flagged', any('By presentation' in x for x in L.lint_prose(w5 % ('By presentation', 'ECG'))))
expect('prose: zone "Targeted tests" passes', L.lint_prose(w5 % ('Targeted tests', 'ECG')) == [])
cap = '<div class="sp-dx"><table class="dense"><caption>%s</caption><thead><tr><th>Stage</th><th>Means</th></tr></thead><tbody><tr><td>N3</td><td>%s</td></tr></tbody></table></div>'
expect('prose: caption "A night by stage" flagged', len(L.lint_prose(cap % ('A night by stage', 'Delta waves'))) == 1)
expect('prose: caption "Sleep stages" passes', L.lint_prose(cap % ('Sleep stages', 'Delta waves')) == [])
expect('prose: "Look-alikes, most tempting first" passes', L.lint_prose(cap % ('Look-alikes, most tempting first', 'Order a TSH')) == [])
expect('prose: a "Means" cell with a figure flagged', len(L.lint_prose(cap % ('Sleep stages', 'The smoking gun for narcolepsy'))) == 1)
expect('prose: header "The tell" flagged', len(L.lint_prose('<table><thead><tr><th>Dx</th><th>The tell</th></tr></thead><tbody><tr><td>a</td><td>b</td></tr></tbody></table>')) == 1)
expect('prose: practice bank not swept', L.lint_prose('<h5 class="tsec authored-hdr">Practice</h5>' + (w5 % ('Next step', 'Chase it'))) == [])

# ---- whole folder: brief.html plus claim map and facts
d = tempfile.mkdtemp()
try:
    open(os.path.join(d, 'brief.html'), 'w').write(clue_table([('clue', 'dx', 'Not valves')]))
    json.dump({'claims': [{'id': 'S1', 'new_text': 'Relapses happen in a median of 3 years of follow up',
                           'sources': [{'id': 'f1', 'source_says': 'relapses happen'}]}]},
              open(os.path.join(d, 'claim_map.json'), 'w'))
    json.dump({'facts': [{'id': 'f1', 'quote': 'relapses happen'}]}, open(os.path.join(d, 'facts.json'), 'w'))
    got = L.lint(d)
    expect('folder: next-step and number found', sorted(g.split(':')[0] for g in got) == ['next-step', 'number'])
    expect('folder: main exits 0 (advisory)', L.main([d, '--quiet']) == 0)
finally:
    shutil.rmtree(d, ignore_errors=True)

print('test_lint: %d passed, %d failed' % (ok, bad))
sys.exit(1 if bad else 0)
