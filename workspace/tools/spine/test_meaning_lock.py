#!/usr/bin/env python3
"""Offline tests for meaning_lock.py (s170 T2). Run: python3 tools/spine/test_meaning_lock.py"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import meaning_lock as M  # noqa: E402

FAILS = []


def expect(name, got, want):
    if got != want:
        FAILS.append('%s: got %r, want %r' % (name, got, want))


def classes(old, new):
    return sorted({c for c, _ in M.check_pair(old, new)})


# 1. single pairs
expect('number kept', classes('<li>Erection over <b>4 hours</b></li>', '<li>Erection lasting over 4 hours: urologic emergency</li>'), [])
expect('number dropped', classes('<li>maximum 40 mg a day</li>', '<li>maximum dose</li>'), ['number'])
expect('number word double', classes('<li>under a 2-fold rise</li>', '<li>↑ risk (less than double baseline)</li>'), [])
expect('5-HT digits', classes('<p>Type 1 receptors, type 2, type 3</p>', '<p>5-HT1: x / 5-HT2: y / 5-HT3: z</p>'), [])
expect('hedge kept by group', classes('<li>heart rate may rise</li>', '<li>heart rate can also rise</li>'), [])
expect('hedge kept by quantifier', classes('<p>a few may grow agitated</p>', '<p>Agitation in some patients</p>'), [])
expect('hedge dropped', classes('<li>venlafaxine is typically avoided</li>', '<li>Venlafaxine: avoided in hypertension</li>'), ['hedge'])
expect('most of all is not a hedge', classes('<li>most of all with venlafaxine</li>', '<li>Highest risk: venlafaxine</li>'), [])
expect('negation kept', classes('<li>without seizures</li>', '<li>no seizures</li>'), [])
expect('negation dropped', classes('<li>no seizures</li>', '<li>seizures</li>'), ['negation'])
expect('side dropped', classes('<li>left lower quadrant</li>', '<li>lower quadrant</li>'), ['side'])
expect('direction arrow', classes('<li>raises appetite</li>', '<li>↑ appetite</li>'), [])
expect('take up is not a direction', classes('<p>platelets take up less serotonin</p>', '<p>↓ platelet serotonin uptake</p>'), [])
expect('bold name dropped', classes('<li><b>Linezolid</b> with an SSRI</li>', '<li>With an SSRI</li>'), ['name'])
expect('bold name kept by words', classes('<li><b>bulimia or anorexia</b></li>', '<li>bulimia nervosa, anorexia nervosa</li>'), [])
expect('mnemonic bold letters join', classes('<p>"Can\'t Concentrate Serum Na+"</p>', '<p><b>C</b>an\'t <b>C</b>oncentrate <b>S</b>erum <b>N</b>a+</p>'), [])
expect('source needs data-src', classes('<p>On the Zoloft label, newborns needed care</p>', '<p>Some newborns need care</p>'),
       ['hedge', 'source'] if M.hedges('Some newborns') == [] else ['source'])
expect('source to data-src passes', classes('<p>On the Zoloft label, newborns needed care</p>',
                                           '<p data-src="Zoloft label">newborns need care</p>'), [])
expect('half-life is not a number', classes('<li>short half-life venlafaxine</li>', '<li>venlafaxine (short half-life)</li>'), [])

# 2. deltas: carried_by, lock_ok, removal
d = {'changes': [{'old': '<p>Paresthesias, dizziness worse with head movement</p>', 'new': ''},
                 {'old': '<li>Symptoms: flu-like</li>', 'new': '<li>Symptoms: flu-like, paresthesias, dizziness worse with head movement</li>'}]}
expect('removal without carry fails', [i for i, _ in M.check_delta(d)], [0])
d['changes'][0]['carried_by'] = [1]
expect('removal carried passes', M.check_delta(d), [])
d2 = {'changes': [{'old': '<li>venlafaxine is typically avoided</li>', 'new': '<li>Venlafaxine: avoided</li>',
                   'lock_ok': ['usually/typically'], 'lock_reason': 'approved row P1'}]}
expect('lock_ok with reason passes', M.check_delta(d2), [])
d2['changes'][0].pop('lock_reason')
expect('lock_ok without reason fails', len(M.check_delta(d2)), 1)
d3 = {'changes': [{'old': '<div>NBME block</div>', 'new': '', 'cut': 's170-cut-1'}]}
expect('cut removal passes', M.check_delta(d3), [])

# 3. the approved rows: every flag is a hedge, negation, number in a title, a source to data-src, or a test artifact
t = open(os.path.join(HERE, '..', '..', 'repair', 'efficiency', 'TEXTBOOK_STYLE.md'), encoding='utf-8').read()
rows = 0
for line in t.splitlines():
    m = re.match(r'\| (P\d+|T\d+) \| ([^|]*) \| (.*?) \| (.*?) \|', line)
    if not m:
        continue
    rows += 1
    live = re.sub(r'\[trigger "[^"]*"\]', '', m.group(3))
    tb = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', m.group(4).replace('_', ''))
    live = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', live)
    bad = [c for c, tok in M.check_pair(live, tb) if c not in ('hedge', 'negation', 'source') and not
           (c == 'name' and tok in ('Hover', 'GICounsel')) and not (c == 'number' and m.group(1) == 'T10')]
    expect('approved row %s' % m.group(1), bad, [])
expect('approved rows read', rows, 40)

print('test_meaning_lock: %d failure(s)' % len(FAILS))
for f in FAILS:
    print('  ' + f)
sys.exit(1 if FAILS else 0)
