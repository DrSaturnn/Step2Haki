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
r = run(EMPTY, li_edit(0, lambda x: re.sub(r'data-lead-in="[^"]*"', 'data-lead-in="Which of the following is the most likely mechanism of this patient&#39;s tachypnea?"', x)), GMAP, ('--source=' + src,))
hit = any('V2' in f for f in r['fails'])
print(('ok  ' if hit else 'BAD ') + 'vendor lead-in copied: expects FAIL V2')
bad += not hit
total = len(CASES) + 5
print(f'{total - bad}/{total} passed')
sys.exit(1 if bad else 0)
