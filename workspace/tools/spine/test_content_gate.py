#!/usr/bin/env python3
"""test_content_gate.py (s170 T6): offline tests for tools/spine/content_gate.py and its three gate checks.

  python3 tools/spine/test_content_gate.py        (from workspace/; exit 1 on any failure)
Synthetic briefs test the helpers; check() runs on mutated copies of the live index.html with a temporary repair/ root.
"""
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import content_gate as cg  # noqa: E402
from pagelib import briefs, read_page  # noqa: E402

bad = 0


def ok(cond, name):
    global bad
    print(('ok   ' if cond else 'FAIL ') + name)
    bad += not cond


def head(n, name):
    return '<h5 class="tsec sp-h" id="x-s%d"><b class="sp-n">%d</b>%s</h5>' % (n, n, name)


NB_Q = '<div class="pc-nbq"><span class="lbl">NBME question</span> Setup: sertraline stopped, then dizziness.</div>'
NB_FR = '<div class="pearls"><span class="lbl">NBME framing</span> The past illness is the clue here.</div>'
NB_ATTR = '<div data-nbme="f8-12">Stem detail kept for the answer.</div>'
LADDER = '<figure class="w5a"><div class="w5t first">First step order a lipid panel today</div></figure>'
P6 = '<p>PHQ-9 score of ten or more suggests major depression in adults.</p>'

# nbme_blocks
inner = (head(1, 'Illness script') + NB_Q + NB_FR + NB_ATTR
         + '<div class="sp-pause">' + NB_Q.replace('sertraline', 'paroxetine') + '</div>'
         + '<div class="pp-b"><span class="lbl">NBME question</span> In a pause point body block.</div>'
         + '<ol class="bank"><li>' + NB_Q.replace('sertraline', 'fluoxetine') + '</li></ol>')
nb = cg.nbme_blocks(inner)
ok(len(nb) == 3, 'nbme_blocks: pc-nbq, NBME-labelled div and data-nbme div found; pause point, pp-b and bank skipped (%d)' % len(nb))
ok(len(cg.nbme_blocks('<div class="pc-nbq"><div class="nbq">inner NBME block text</div></div>')) == 1, 'nbme_blocks: outermost only')
ok(cg.nbme_blocks('<div class="pearls"><span class="lbl">Mnemonic</span> no board label</div>') == [], 'nbme_blocks: other labels ignored')
ok(nb[0]['hash'] == cg.h8(cg.norm('NBME question Setup: sertraline stopped, then dizziness.')), 'nbme_blocks: hash is h8 of normalized text')

# workup_in_step2
b2 = head(1, 'Illness script') + '<p>x</p>' + head(2, 'Diagnostic criteria') + LADDER + head(5, 'Workup') + LADDER
ok(len(cg.workup_in_step2(b2)) == 1, 'workup_in_step2: ladder in step 2 found once (outermost), ladder in step 5 ignored')
ok(cg.workup_in_step2(head(1, 'A') + LADDER) == [], 'workup_in_step2: no step 2, no finding')
ok(len(cg.workup_in_step2(head(2, 'Diagnostic criteria') + '<div class="w5t">Ladder row alone order a test</div>')) == 1,
   'workup_in_step2: a bare div.w5t counts')

# moves
ref = head(2, 'Diagnostic criteria') + '<p>Five or more of nine symptoms for two weeks.</p>' + head(6, 'Severity') + P6
now_moved = head(2, 'Diagnostic criteria') + '<p>Five or more of nine symptoms for two weeks.</p>' + P6 + head(6, 'Severity')
mv = cg.moves(ref, now_moved)
ok(len(mv) == 1 and mv[0]['from'] == [6] and mv[0]['to'] == [2], 'moves: step 6 block now in step 2 is a move 6 -> 2 (%s)' % mv)
ok(cg.moves(ref, ref) == [], 'moves: unchanged brief has none')
ok(cg.moves(ref, ref + '<p>A brand new line that the batch wrote here.</p>') == [], 'moves: a block new to the brief is not a move')
ok(cg.moves(ref, ref.replace(P6, P6 + '<p>ok</p>')) == [], 'moves: blocks under 4 words are not tracked')
copy = ref.replace(head(6, 'Severity'), P6 + head(6, 'Severity'))
ok(len(cg.moves(ref, copy)) == 1, 'moves: a copy added to another step counts as a move')

# check() on the live page
PAGE_PATH = os.environ.get('AXBX_PAGE') or os.path.join(os.path.dirname(os.path.dirname(HERE)), 'index.html')
if not os.path.exists(PAGE_PATH):
    print('skip check() cases: no page at %s' % PAGE_PATH)
else:
    page = read_page(PAGE_PATH)
    bl = {b.id: b for b in briefs(page)}
    root = tempfile.mkdtemp()
    os.makedirs(os.path.join(root, 'repair', 'sx'))

    def write(name, rows):
        json.dump(rows, open(os.path.join(root, 'repair', 'sx', name), 'w'))

    def clear():
        for n in ('nbme_keep.json', 'step_moves.json'):
            p = os.path.join(root, 'repair', 'sx', n)
            if os.path.exists(p):
                os.remove(p)

    ok(cg.check(page, page, set(), root=root) == [], 'check: live page against itself passes')
    ok(cg.check(None, page, set(), root=root) == [], 'check: no base, nothing changed: passes')

    ss = bl['pc-ssri']
    ssnb = cg.nbme_blocks(ss.inner)
    f = cg.check(page, page, {'pc-ssri'}, root=root)
    ok(any(c == 'nbme-block' and 'pc-ssri' in k for c, k, _ in f) and len(ssnb) >= 1,
       'check: changed pc-ssri with its card NBME block fails nbme-block')
    write('nbme_keep.json', [{'brief': 'pc-ssri', 'hash': x['hash'], 'reason': 'test'} for x in ssnb])
    ok(not [1 for c, k, _ in cg.check(page, page, {'pc-ssri'}, root=root) if c == 'nbme-block'], 'check: nbme_keep.json row clears it')
    clear()

    vo = bl['voices']
    added = page[:vo.inner_end] + NB_Q + page[vo.inner_end:]
    f = cg.check(page, added, set(), root=root)
    ok(any(c == 'nbme-block' and k == 'voices count' for c, k, _ in f), 'check: NBME block count rising on voices fails')

    md = bl['mdd']
    i2 = page.index(head(2, 'Diagnostic criteria').replace('x-s2', 'md-s2'), md.inner_start)
    i2 = page.index('</h5>', i2) + 5
    lad = page[:i2] + LADDER + page[i2:]
    f = cg.check(page, lad, {'mdd'}, root=root)
    ok(any(c == 'step2-workup' and k.startswith('mdd') for c, k, _ in f), 'check: ladder injected in mdd step 2 fails step2-workup')
    ok(not [1 for c, k, _ in cg.check(page, lad, set(), root=root) if c == 'step2-workup'],
       'check: step2-workup applies only to changed briefs')

    sev = cg.step_regions(md.inner)[6][1]
    blk = cg.top_blocks(sev)[1]
    mv_html = page[:i2] + '<p>' + blk[1] + '</p>' + page[i2:]
    f = cg.check(page, mv_html, {'mdd'}, root=root)
    ok(any(c == 'step-moves' and blk[0] in k for c, k, _ in f), 'check: mdd step 6 block in step 2 with no row fails step-moves')
    write('step_moves.json', [{'brief': 'mdd', 'hash': blk[0], 'from': 6, 'to': 2, 'class': 'criteria', 'reason': 'N10 test'}])
    ok(not [1 for c, k, _ in cg.check(page, mv_html, {'mdd'}, root=root) if c == 'step-moves'], 'check: step_moves.json row clears it')
    write('step_moves.json', [{'brief': 'mdd', 'hash': blk[0], 'from': 6, 'to': 2, 'class': 'criteria', 'reason': ''}])
    f = cg.check(page, mv_html, {'mdd'}, root=root)
    ok(any(c == 'step-moves' and 'lacks' in m for c, k, m in f), 'check: a row without a reason fails')
    open(os.path.join(root, 'repair', 'sx', 'step_moves.json'), 'w').write('{bad json')
    try:
        cg.check(page, mv_html, {'mdd'}, root=root)
        ok(False, 'check: unparsable step_moves.json raises ValueError')
    except ValueError:
        ok(True, 'check: unparsable step_moves.json raises ValueError')
    clear()

print('test_content_gate: %d failure(s)' % bad)
sys.exit(1 if bad else 0)
