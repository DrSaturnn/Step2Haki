#!/usr/bin/env python3
"""test_migrate_check.py: self-test for tools/migrate_check.py (run before trusting any migration).

The golden brief (tools/tests/migrate/golden_hip.html, the approved septic hip Type C brief) must PASS with no WARN.
Each mutation injects one defect that has happened or that a rule forbids; the checker must FAIL with the expected code.
When a reviewer or Jonathan finds a defect the checker missed, add a check to migrate_check.py AND a mutation here
in the same batch (tools/MIGRATION_CONTRACT.md, "defect to rule").

  python3 tools/test_migrate_check.py        exit 1 if any case misbehaves
"""
import json, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(HERE, 'tests', 'migrate')
GOLD = open(os.path.join(T, 'golden_hip.html'), encoding='utf-8').read()
GMAP = json.load(open(os.path.join(T, 'golden_hip.json')))
EMPTY = '<div></div>'
LIS = re.findall(r'<li [^>]*data-item-id="q_[0-9a-f]{20}"[^>]*>.*?</li>', GOLD, re.S)


def run(old, new, cmap, extra=()):
    d = tempfile.mkdtemp()
    paths = []
    for n, c in (('old.html', old), ('new.html', new), ('map.json', json.dumps(cmap))):
        p = os.path.join(d, n); open(p, 'w', encoding='utf-8').write(c); paths.append(p)
    r = subprocess.run([sys.executable, os.path.join(HERE, 'migrate_check.py'), *paths, '--json', *extra], capture_output=True, text=True)
    return json.loads(r.stdout)


def li_edit(i, fn):
    return GOLD.replace(LIS[i], fn(LIS[i]), 1)


def carried_map():
    m = dict(GMAP)
    m['items'] = [{'id': re.search(r'data-item-id="(q_\w+)"', li).group(1), 'disposition': 'carried'} for li in LIS]
    return m


dxi = next(i for i, li in enumerate(LIS) if 'data-type="dx"' in li)
CASES = [
    # (name, old, new, map, expected code or text in a FAIL line)
    ('lead-in missing', EMPTY, li_edit(0, lambda s: re.sub(r' data-lead-in="[^"]*"', '', s)), GMAP, 'I1'),
    ('data-src missing', EMPTY, li_edit(0, lambda s: s.replace(' data-src="authored"', '')), GMAP, 'I1'),
    ('shorthand age', EMPTY, li_edit(0, lambda s: s.replace('2-year-old girl', '2 yo F')), GMAP, 'I2'),
    ('no age/sex opening', EMPTY, li_edit(0, lambda s: s.replace('2-year-old girl with', 'Girl with')), GMAP, 'I2'),
    ('no companion', EMPTY, li_edit(0, lambda s: re.sub(r'(</b>)\s*&rarr;.*?</li>', r'\1</li>', s, flags=re.S)), GMAP, 'I3'),
    ('dx stem names topic', EMPTY, li_edit(dxi, lambda s: s.replace('>', '>Known septic arthritis; ', 1).replace('>Known septic arthritis; ', '>', 0)), GMAP, None),
    ('options not distinct', EMPTY, li_edit(0, lambda s: s.replace('data-d2="NSAIDs and re-examination in 48 hours"', 'data-d2="Aspiration of the right hip"')), GMAP, 'I5'),
    ('stem changed, no version bump', GOLD, li_edit(1, lambda s: s.replace('4-year-old boy limping', '4-year-old boy who has been limping')), carried_map(), 'I6'),
    ('NBME item after authored', EMPTY, li_edit(2, lambda s: s.replace('data-src="authored"', 'data-src="nbme"')), GMAP, 'I9'),
    ('acronym expansion lost', '<p>CRP (C-reactive protein) high</p>', GOLD.replace('CRP (C-reactive protein)', 'CRP'), GMAP, 'A1'),
    ('acronym never written out', EMPTY, GOLD.replace('ESR (erythrocyte sedimentation rate)', 'ESR'), GMAP, 'V1'),
    ('em dash', EMPTY, GOLD.replace('</h4>', ' — test</h4>', 1), GMAP, 'em dash'),
    ('banned wording', EMPTY, GOLD.replace('</h4>', ' noise</h4>', 1), GMAP, 'banned wording'),
    ('UWorld item on page', EMPTY, li_edit(0, lambda s: s.replace('data-src="authored"', 'data-src="uworld"')), GMAP, 'uworld'),
    ('Same patient stem', EMPTY, li_edit(0, lambda s: s.replace('2-year-old girl with', 'Same patient, 2-year-old girl with')), GMAP, 'depends on another item'),
    ('table not wrapped', EMPTY, GOLD.replace('<div class="tw">', '<div>', 1), GMAP, 'not in a .tw wrapper'),
    ('alias missing', EMPTY, GOLD.replace('<span class="alias" id="synovitis"></span>', ''), GMAP, 'no alias span'),
    ('clue dropped', EMPTY, GOLD, dict(GMAP, claims=[{'id': 'k1', 'kind': 'clue', 'text': 'afebrile', 'role': 'excludes', 'disposition': 'dropped', 'reason': 'x'}]), 'clue dropped'),
    ('clue without role', EMPTY, GOLD, dict(GMAP, claims=[{'id': 'k1', 'kind': 'clue', 'text': 'afebrile', 'disposition': 'carried', 'new_text': 'afebrile'}]), 'valid role'),
    ('carried text absent', EMPTY, GOLD, dict(GMAP, claims=[{'id': 'c1', 'kind': 'claim', 'text': 'x', 'disposition': 'carried', 'new_text': 'this phrase is not in the brief'}]), 'not found'),
    ('old item unaccounted', GOLD, GOLD, GMAP, 'not accounted for'),
    ('no topic terms', EMPTY, GOLD, dict(GMAP, topic_terms=[]), 'I0'),
    ('qualifier softened', EMPTY, GOLD, dict(GMAP, claims=[{'id': 'q1', 'kind': 'claim', 'text': 'especially in infants', 'disposition': 'carried', 'new_text': 'Kocher'}]), 'Q1'),
    ('corrected value left behind', EMPTY, GOLD, dict(GMAP, claims=[{'id': 's1', 'kind': 'number', 'text': 'old', 'disposition': 'corrected', 'new_text': 'Kocher', 'reason': 'src', 'currency': 'verified', 'source': 'src', 'stale_patterns': ['Kocher']}]), 'S1'),
    ('corrected number without stale patterns', EMPTY, GOLD, dict(GMAP, claims=[{'id': 's2', 'kind': 'number', 'text': 'old', 'disposition': 'corrected', 'new_text': 'Kocher', 'reason': 'src', 'currency': 'verified', 'source': 'src'}]), 'S1'),
    ('acronym used before written out', EMPTY, GOLD.replace('</h4>', ' ESR</h4>', 1), GMAP, 'V1'),
    ('mask on Tier table', EMPTY, re.sub(r'<table( class="[^"]*")?>(\s*<caption>[^<]*</caption>\s*<thead><tr><th>Tier)', r'<table\1 data-mask="3">\2', GOLD, count=1), GMAP, 'M1'),
    ('differential without mask 3', EMPTY, re.sub(r'<table([^>]*) data-mask="3"([^>]*>\s*<caption>[^<]*</caption>\s*<thead><tr><th>Diagnosis)', r'<table\1\2', GOLD, count=1), GMAP, 'M1'),
    ('mixed-case acronym not written out', EMPTY, GOLD.replace('</h4>', ' IgM</h4>', 1), GMAP, 'V1'),
    ('lowercase abbreviation not written out', EMPTY, li_edit(0, lambda x: x.replace('WBC 16,500', '20 white cells/hpf; WBC 16,500')), GMAP, 'V1'),
    ('and became or', EMPTY, GOLD, dict(GMAP, claims=[{'id': 'q2', 'kind': 'claim', 'text': 'labs and echo supportive', 'disposition': 'carried', 'new_text': 'Kocher or'}]), 'Q1'),
    ('source clue without role basis', EMPTY, GOLD, dict(GMAP, claims=[{'id': 'r1', 'kind': 'clue', 'source': 'NBME stem', 'text': 'afebrile', 'role': 'excludes', 'disposition': 'carried', 'new_text': 'afebrile'}]), 'R1'),
    ('inferred role not flagged', EMPTY, GOLD, dict(GMAP, claims=[{'id': 'r2', 'kind': 'clue', 'source': 'NBME stem', 'text': 'afebrile', 'role': 'excludes', 'role_basis': 'inferred', 'disposition': 'carried', 'new_text': 'Well, afebrile, walks with a limp'}]), 'R1'),
    ('stem without objective data', EMPTY, li_edit(0, lambda x: re.sub(r'(data-d2-id="[^"]*"[^>]*>).*?(&rarr;)', r'\1 2-year-old girl who will not stand \2', x, count=1, flags=re.S)), GMAP, 'I8'),
    ('intensity softened in a source clue', EMPTY, GOLD, dict(GMAP, claims=[{'id': 'q3', 'kind': 'claim', 'text': 'in obvious discomfort', 'disposition': 'carried', 'new_text': 'Kocher'}]), 'Q1'),
    ('script not in a scriptcard', EMPTY, GOLD.replace('<div class="scriptcard multi">', '<div>', 1), GMAP, 'L1'),
    ('two-disease script without multi', EMPTY, GOLD.replace('<table class="script multi"', '<table class="script"', 1), GMAP, 'L1'),
    ('tests table not dense', EMPTY, GOLD.replace('<table class="dense" data-mask="4"><caption>First tests', '<table data-mask="4"><caption>First tests', 1), GMAP, 'L3'),
    ('first step split out of the group', EMPTY, GOLD.replace('<tr><td>Hip ultrasound</td><td>First</td>', '</tbody><tbody><tr><td>Hip ultrasound</td><td>First</td>', 1), GMAP, 'L2'),
    ('new claim without a source', EMPTY, GOLD, dict(GMAP, claims=[{'id': 'n9', 'kind': 'claim', 'text': 'x', 'disposition': 'new', 'new_text': 'Kocher'}]), 'new claim without a source'),
    ('illness script line untraced', EMPTY, GOLD, dict(GMAP, claims=[{'id': 'n8', 'kind': 'claim', 'text': 'x', 'disposition': 'carried', 'new_text': 'Kocher'}]), 'N2'),
    ('grouped first tests route to each other', EMPTY, GOLD.replace('Gray zone: decide on aspiration by the clinical picture and the ultrasound', 'Gray zone: ultrasound', 1), GMAP, 'L2'),
    ('sequence word dropped', EMPTY, GOLD, dict(GMAP, claims=[{'id': 'q4', 'kind': 'claim', 'text': 'CRP triggers supplemental labs', 'disposition': 'carried', 'new_text': 'Kocher'}]), 'Q1'),
    ('order label changed for style', '<table><thead><tr><th>Test</th><th>Order</th></tr></thead><tbody><tr><td>Blood culture</td><td>By branch</td></tr></tbody></table>', GOLD, GMAP, 'O1'),
    ('number without currency', EMPTY, GOLD, dict(GMAP, claims=[{'id': 'n1', 'kind': 'number', 'text': 'x', 'disposition': 'carried', 'new_text': 'Kocher'}]), 'N1'),
]
# a dx stem that names the topic diagnosis
CASES[5] = ('dx stem names topic', EMPTY, li_edit(dxi, lambda s: re.sub(r'(data-d2-id="[^"]*"[^>]*>)', r'\1Known septic arthritis of the hip; ', s, count=1)), GMAP, 'I4')

bad = 0
g = run(EMPTY, GOLD, GMAP)
ok = not g['fails'] and not g['warns']
print(('ok  ' if ok else 'BAD ') + 'golden brief passes clean' + ('' if ok else f": {g['fails'] + g['warns']}"))
bad += not ok
for name, old, new, cmap, code in CASES:
    r = run(old, new, cmap)
    hit = any(code in f for f in r['fails'])
    print(('ok  ' if hit else 'BAD ') + f'{name}: expects FAIL {code}' + ('' if hit else f" (got {r['fails'][:3]})"))
    bad += not hit
# H1: title changed while other briefs still name the old title (pilot M1 audit run, 2026-09-28)
pg = os.path.join(tempfile.mkdtemp(), 'page.html')
open(pg, 'w').write('<div class="pearls"><span class="lbl">Pairs with</span> Part I <b>Old Hip Title</b> covers it.</div>')
r = run('<div class="brief" id="septic-hip"><h4>Old Hip Title</h4></div>', GOLD, GMAP, ('--page=' + pg,))
hit = any('H1' in f for f in r['fails'])
print(('ok  ' if hit else 'BAD ') + 'title changed, inbound references break: expects FAIL H1')
bad += not hit
r = run('<div class="brief" id="septic-hip"><h4>Old Hip Title</h4></div>', GOLD, dict(GMAP, inbound_rewrites=['Old Hip Title']), ('--page=' + pg,))
ok = not any('H1' in f for f in r['fails'])
print(('ok  ' if ok else 'BAD ') + 'title change with planned inbound rewrites passes H1')
bad += not ok
open(pg, 'w').write('<h4>The Limping Child</h4>')
r = run(EMPTY, GOLD.replace('<b>The Limping Child</b>', '<b>The Limping Kid</b>'), GMAP, ('--page=' + pg,))
hit = any('P1' in f for f in r['fails'])
print(('ok  ' if hit else 'BAD ') + 'Pairs-with partner not on the page: expects FAIL P1')
bad += not hit
src = os.path.join(tempfile.mkdtemp(), 'src.md')
open(src, 'w').write('Which of the following is the most likely mechanism of this patient\'s tachypnea?')
open(src, 'w').write('A 2-year-old girl is brought to the office because of one day of irritability and she cries whenever her diaper is changed.')
r = run(EMPTY, li_edit(0, lambda x: x.replace('2-year-old girl with 1 day of irritability', '2-year-old girl is brought to the office because of one day of irritability and she cries whenever her diaper is changed;')), GMAP, ('--source=' + src,))
hit = any('V2' in f for f in r['fails'])
print(('ok  ' if hit else 'BAD ') + 'vendor stem wording copied: expects FAIL V2')
bad += not hit
open(src, 'w').write('Which of the following is the most likely mechanism of this patient\'s tachypnea?')
r = run(EMPTY, li_edit(0, lambda x: re.sub(r'data-lead-in="[^"]*"', 'data-lead-in="Which of the following is the most likely mechanism of this patient&#39;s tachypnea?"', x)), GMAP, ('--source=' + src,))
ok = not any('V2' in f for f in r['fails'])
print(('ok  ' if ok else 'BAD ') + 'exact NBME lead-in allowed (Rule 11): no V2')
bad += not ok
# C1: an old stem clue with no clue row (the claim map must census every fragment of every old stem)
r = run(LIS[0], GOLD, dict(GMAP, items=[{'id': re.search(r'data-item-id="(q_\w+)"', LIS[0]).group(1), 'disposition': 'carried'}]))
hit = any(f.startswith('C1') for f in r['fails'])
print(('ok  ' if hit else 'BAD ') + 'old stem clue without a clue row: expects FAIL C1')
bad += not hit
# K1/K2: a highlighted mnemonic and its scale reference (Jonathan 2026-09-28: CRASH and Burn was flattened into a tile)
MN_OLD = ('<div class="crit"><b>Diagnosis</b> 4 of 5 <span class="scaleref" data-scale="t-mn">ABC criteria</span></div>'
          '<h5>ABC Rule</h5><ul class="plain" id="t-mn"><li><b>A</b>lpha &ndash; <b>first</b> thing</li>'
          '<li><b>B</b>eta &ndash; second</li><li><b>C</b>harlie &ndash; third</li></ul>')
flat = GOLD.replace('</h4>', '</h4><div class="crit"><b>Alpha:</b> first thing &middot; <b>Beta:</b> second &middot; <b>Charlie:</b> third</div>', 1)
r = run(MN_OLD, flat, GMAP)
hit = any(f.startswith('K1') for f in r['fails']) and any(f.startswith('K2') for f in r['fails'])
print(('ok  ' if hit else 'BAD ') + 'mnemonic flattened and scale reference dropped: expects FAIL K1 and K2')
bad += not hit
kept = GOLD.replace('</h4>', '</h4>' + MN_OLD.replace('<ul class="plain"', '<ul class="plain mnem"').replace('<li><b>', '<li><b class="mn">'), 1)
r = run(MN_OLD, kept, GMAP)
ok = not any(f[:2] in ('K1', 'K2') for f in r['fails'])
print(('ok  ' if ok else 'BAD ') + 'mnemonic carried with highlights passes K1 and K2' + ('' if ok else f": {[f for f in r['fails'] if f[:2] in ('K1','K2')]}"))
bad += not ok
nob = kept.replace('<b>first</b>', 'first')
r = run(MN_OLD, nob, GMAP)
hit = any('highlighted phrases lost' in f for f in r['fails'])
print(('ok  ' if hit else 'BAD ') + 'mnemonic highlight removed: expects FAIL K1')
bad += not hit
plainmn = GOLD.replace('</h4>', '</h4>' + MN_OLD, 1)
r = run(MN_OLD, plainmn, GMAP)
hit = any('is not highlighted' in f for f in r['fails'])
print(('ok  ' if hit else 'BAD ') + 'mnemonic carried without letter highlighting: expects FAIL K1')
bad += not hit
r = run('<div class="pearls"><span class="lbl">Mnemonic</span> <b>5 Ts</b> the cyanotic lesions</div>', GOLD, GMAP)
hit = any('5 ts' in f for f in r['fails'])
print(('ok  ' if hit else 'BAD ') + 'pearl mnemonic term lost: expects FAIL K1')
bad += not hit
# ---- source and scope (Jonathan 2026-09-29: content from the pasted or a verified source, Step 2 scope, mnemonics
# identified not invented; tools/content_rules.py is shared with tools/gate.py, which runs it on every brief type)
LAD = '<td>Still febrile or CRP not falling at 48 to 72 h &#x26A0;&#xFE0E;: MRI, repeat drainage</td>'
assert LAD in GOLD
EXTRA = 0
def expect(name, new_, code, want_fail=True, cmap=None, old_=EMPTY, text=None):
    global bad, EXTRA
    EXTRA += 1
    r = run(old_, new_, cmap or GMAP)
    hit = any(f.startswith(code) and (text is None or text in f) for f in r['fails'])
    ok = hit if want_fail else not hit
    print(('ok  ' if ok else 'BAD ') + name + (f': expects FAIL {code}' if want_fail else f': no {code}') + ('' if ok else f" {r['fails'][:3]}"))
    bad += not ok
PSY = li_edit(dxi, lambda x: re.sub(r'(data-item-id="q_\w+"[^>]*>)([^&]*?)(&rarr;)', r'\g<1>24-year-old woman brought in by police after shouting at a rental agent; declares she is fabulously wealthy; speech loud and rapid; urine toxicology screening negative; mental status examination shows grandiose delusions \g<3>', x, count=1))
expect('psych stem with mental status findings and negative toxicology has objective data', PSY, 'I8', False)
expect('psych stem with labels only has no objective data', li_edit(dxi, lambda x: re.sub(r'(data-item-id="q_\w+"[^>]*>)([^&]*?)(&rarr;)', r'\g<1>24-year-old woman who seems manic and grandiose \g<3>', x, count=1)), 'I8')
expect('study gap on the page', GOLD.replace(LAD, '<td>Trigger unknown: study gap</td>'), 'G1')
expect('TBD on the page', GOLD.replace('</h4>', ' (dosing TBD)</h4>', 1), 'G1')
expect('hedged failure trigger', GOLD.replace(LAD, '<td>Surgical review if no improvement</td>'), 'G2')
expect('failure trigger with a time is fine', GOLD.replace(LAD, '<td>Surgical review if no improvement at 48 h</td>'), 'G2', False)
expect('empty Escalate-when cell', GOLD.replace(LAD, '<td></td>'), 'G3')
expect('Top rung on the last ladder row is fine', GOLD.replace(LAD, '<td>Top rung</td>'), 'G3', False)
expect('Top rung on a middle row', GOLD.replace('<td>Effusion with fever or rising ESR or CRP</td>', '<td>Top rung</td>'), 'G3')
MNB = ('<h5>ABC Rule</h5><ul class="plain mnem" id="t-mn"{src}><li><b class="mn">A</b>lpha &ndash; first</li>'
       '<li><b class="mn">B</b>eta &ndash; second</li><li><b class="mn">C</b>harlie &ndash; third</li></ul>')
expect('mnemonic without a named source', GOLD.replace('</h4>', '</h4>' + MNB.format(src=''), 1), 'K3')
expect('mnemonic sourced as authored', GOLD.replace('</h4>', '</h4>' + MNB.format(src=' data-mn-src="authored"'), 1), 'K3')
expect('mnemonic credited to a book with nothing to open (R12)', GOLD.replace('</h4>', '</h4>' + MNB.format(src=' data-mn-src="First Aid for the USMLE Step 1"'), 1), 'K3')
expect('mnemonic from a widely taught resource with a URL is fine', GOLD.replace('</h4>', '</h4>' + MNB.format(src=' data-mn-src="Osmosis https://www.osmosis.org/answers/abc"'), 1), 'K3', False)
expect('mnemonic from a pasted AnKing card is fine', GOLD.replace('</h4>', '</h4>' + MNB.format(src=' data-mn-src="AnKing card, pasted 2026-09-29"'), 1), 'K3', False)
expect('pearl mnemonic without a named source', GOLD.replace('</h4>', '</h4><div class="pearls"><span class="lbl">Mnemonic</span> ABC: alpha, beta, charlie</div>', 1), 'K3')
def one(row):
    return dict(GMAP, claims=[dict(row)])
SRC_OK = GOLD  # the rows below trace text that is in the golden brief
row = {'id': 's1', 'kind': 'claim', 'text': 'x', 'disposition': 'new', 'new_text': 'Kocher 2', 'source': 'AHA 2017 guideline'}
expect('guideline-sourced new content with no Step 2 basis', SRC_OK, 'S2', cmap=one(row))
expect('Step 2 basis that names no place', SRC_OK, 'S2', cmap=one(dict(row, step2='high yield')))
expect('Step 2 basis named is fine', SRC_OK, 'S2', False, cmap=one(dict(row, step2='template: management ladder tier (board-brief Part 2)')))
expect('Step 2 basis citing a question written for this brief (R12)', SRC_OK, 'S2', cmap=one(dict(row, step2='tested by item q_' + 'ab' * 10)))
expect('Step 2 basis pointing at "this bank" (R12)', SRC_OK, 'S2', cmap=one(dict(row, step2='follow-up item in this bank')))
GL = dict(row, step2='template: management ladder tier (board-brief Part 2)')
expect('guideline content with no source statement (R13)', SRC_OK, 'Q2', cmap=one(GL))
expect('guideline "and" becomes "or" on the page (R13)', SRC_OK, 'Q2', cmap=one(dict(GL, new_text='give IVIG while fever or a raised CRP or ESR persists', source_says='either persistent fever or coronary abnormalities together with ongoing inflammation, as shown by a raised ESR or CRP')))
expect('"6 months or younger" is not an or-for-and swap', SRC_OK, 'Q2', False, cmap=one(dict(GL, new_text='infant 6 months or younger with 7 or more days of fever', source_says='infants 6 months or younger and fever for 7 days or more')))
expect('source named only as a textbook (R13)', SRC_OK, 'Q2', cmap=one(dict(GL, source='standard textbook', source_says='Kocher 2')))
expect('guideline content that keeps the source statement is fine', SRC_OK, 'Q2', False, cmap=one(dict(GL, source_says='Kocher 2')))
expect('content from the pasted NBME explanation needs no extra basis', SRC_OK, 'S2', False, cmap=one(dict(row, source='NBME Q9 explanation')))
total = len(CASES) + 12 + EXTRA
print(f'{total - bad}/{total} passed')
sys.exit(1 if bad else 0)
