#!/usr/bin/env python3
"""Offline tests for the s159 card tools (CARD_SPEC.md, the psych pharm class card): apply_edits retire_brief and the
new_brief "after" fallbacks, lint card_check, the outline_render card blocks (keypoint, owners, lcw, script2 and rows
"cls") and outline_check's card entry. No page, no network.

  python3 tools/spine/test_cards.py
"""
import json
import os
import re
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..'))
import apply_edits as AE  # noqa: E402
import lint as L  # noqa: E402
import outline_check as OC  # noqa: E402
import outline_render as OR  # noqa: E402

ok = bad = 0


def expect(name, cond, detail=''):
    global ok, bad
    if cond:
        ok += 1
    else:
        bad += 1
        print('FAIL', name, detail)


def raises(name, fn, needle):
    try:
        fn()
    except AE.EditError as e:
        expect(name, needle in str(e), str(e)[:160])
        return
    expect(name, False, 'no EditError')


# ---------------------------------------------------------------- outline_render card blocks
tmp = tempfile.mkdtemp(prefix='test-cards-')
try:
    json.dump({'f1': ['test cite', 'test quote']}, open(os.path.join(tmp, 'src.json'), 'w'))
    o = {'prefix': 'tcx', 'src': ['src.json'], 'steps': [], 'bank_id': 'tcx-bank'}
    R = OR.Renderer(o, tmp)
    T = lambda s: {'t': s, 'ids': ['f1']}
    kp = R.block({'type': 'keypoint', 'lines': [[{'b': T('Never combine')}, ' ', T('with a serotonergic drug')], T('Diet rule')]})
    expect('keypoint box', kp.startswith('<div class="dp"><span class="lbl">Key point</span><ul class="bl">') and kp.count('<li>') == 2, kp[:120])
    own = R.block({'type': 'owners', 'lines': [[T('Which antidepressant first'), ' ', {'drawer': 'mdd', 'label': T('Depression')}]]})
    expect('owners box', own.startswith('<div class="pc-owners"><span class="lbl">Where the choice is made</span>') and 'class="sp-drw" data-brief="mdd"' in own, own[:160])
    sc = R.block({'type': 'script2', 'cls': 'pc-script', 'rows': [['Drugs', [T('Phenelzine')]], ['Mechanism', [T('MAO block')]]]})
    expect('script2 cls', '<div class="sp-script sp-s2 pc-script">' in sc, sc[:80])
    rw = R.block({'type': 'rows', 'cls': 'pc-blocks', 'rows': [{'src': 'Tyramine crisis', 'finding': T('Headache, high blood pressure'),
                                                                'commit': [T('a crisis'), T('phentolamine')]}]})
    expect('rows cls', rw.startswith('<div class="sp-rows pc-blocks">') and '<span class="mask">phentolamine</span>' in rw, rw[:120])
    ticks = [[0, '0'], [50, '1 wk'], [100, '2 wk']]
    chart = {'type': 'lcw', 'title': T('Washouts'), 'small': 'weeks', 'ticks': ticks, 'rows': [
        {'name': T('SSRI to MAOI'), 'win': T('2 weeks'), 'bar': [0, 100], 'c': 1, 'lab': 'Why', 'wl': T('serotonin'), 'mask': 'win'},
        {'name': T('Fluoxetine to MAOI'), 'win': T('5 weeks'), 'bar': [0, 100], 'c': 2, 'lab': 'Why', 'wl': T('long half-life'), 'mask': 'win'}]}
    lc = R.block(chart)
    expect('lcw figure', lc.startswith('<figure class="lcw pc-lcw">') and lc.count('<li class="wr">') == 2, lc[:80])
    expect('lcw ticks on every row', lc.count('<div class="rax"') == 2 and lc.count('>1 wk</span>') == 2)
    expect('lcw mask win', lc.count('<span class="win"><span class="mask">') == 2 and '<b class="nm mask">' not in lc)
    chart_n = dict(chart, rows=[dict(r, mask='name') for r in chart['rows']])
    lcn = R.block(chart_n)
    expect('lcw mask name', lcn.count('<b class="nm mask">') == 2 and '<span class="win"><span class="mask">' not in lcn)
    tb = R.block({'type': 'table', 'caption': T('Interactions'), 'heads': [T('Combined with'), T('Result'), T('Rule')],
                  'rows': [[T('Meperidine'), T('Serotonin syndrome'), T('Avoid')]], 'mask_cols': [2], 'cls': 'sp-dx pc-tbl'})
    expect('table cls', '<div class="sp-dx pc-tbl">' in tb, tb[:80])

    # ------------------------------------------------------------ card_check
    head = ('<div class="brief sp pc" id="pc-test" data-entry="card" data-lens="psych" data-spine="2" data-shelf="psych" '
            'data-bp="behav">\n<p class="pc-grp">01 Antidepressants &middot; class card</p>\n<h4>Test class</h4>\n'
            '<p class="sub">test inhibitors &middot; drug a &middot; drug b</p>\n')
    bank = ('<h5 class="authored-hdr" id="tcx-bank">Practice</h5>\n<ol class="bank authored">\n<li data-type="avoid" '
            'data-item-id="q_00000000000000000001" data-item-version="1">stem &rarr; <b>Key</b> &rarr; why</li>\n</ol>\n</div>')

    def card(*blocks):
        return head + '\n'.join(blocks) + '\n' + bank
    good = card(kp, sc, rw, lc, tb, own)
    expect('card_check passes a well-formed card', L.card_check(good) == [], L.card_check(good))
    expect('card_check ignores a non-card brief', L.card_check(good.replace('data-entry="card"', 'data-entry="drug"', 1)) == [])
    has = lambda html, s: any(s in p for p in L.card_check(html))
    expect('missing Key point', has(card(sc, rw, lc, tb, own), 'no Key point'))
    expect('missing drug rows', has(card(kp, rw, lc, own), 'no drug rows'))
    expect('head out of order', has(card(sc, kp, own), 'out of order'))
    expect('missing owners', has(card(kp, sc, rw), 'no "Where the choice is made"'))
    expect('owners without drawer', has(card(kp, sc, own.replace('class="sp-drw"', 'class="x"')), 'points to no brief'))
    expect('block below owners', has(card(kp, sc, own, tb), 'below the "Where the choice is made"'))
    expect('chart below owners', has(card(kp, sc, own, lc), 'below the "Where the choice is made"'))
    expect('no practice item', has(good.replace('data-item-id=', 'data-x='), 'holds no item'))
    expect('no practice header', has(good.replace('authored-hdr', 'x-hdr'), 'no Practice header'))
    i = lc.index('</li>')
    odd = lc[:i] + lc[i:].replace('>1 wk</span>', '>10 d</span>', 1)
    expect('ticks differ between rows', has(card(kp, sc, odd, own), 'ticks differ'))
    one = re.sub(r'<div class="rax"[^>]*>.*?</div>', '<div class="rax"></div>', lc, count=1, flags=re.S)
    expect('row with no tick labels', has(card(kp, sc, one, own), 'no tick labels'))
    dup = R.block(dict(chart_n, rows=[chart_n['rows'][0], dict(chart_n['rows'][1], name=T('SSRI to MAOI'))]))
    expect('duplicate timed window', has(card(kp, sc, dup, own), 'named twice'))
    expect('duplicate window across charts', has(card(kp, sc, lcn, lcn.replace('Washouts', 'Again'), own), 'named twice'))
    expect('not pc-lcw', has(card(kp, sc, lc.replace('lcw pc-lcw', 'lcw'), own), 'not figure.lcw.pc-lcw'))
    expect('spine stepper', has(card(kp, sc, '<nav class="sp-step">x</nav>', own), 'stepper'))
    expect('pause point', has(card(kp, sc, '<div class="sp-pause">x</div>', own), 'pause point'))
    expect('bottom line', has(card(kp, sc, '<div class="bl2"><span class="lbl">Bottom line</span></div>', own), 'bottom line'))
    expect('dot timeline', has(card(kp, sc, '<div class="sp-on">x</div>', own), 'dot-on-line'))
    expect('mockup furniture', has(card(kp, sc, '<p class="pc-src pc-opt">x</p>', own), 'mockup review'))
    nbq_ok = '<div class="pc-nbq"><span class="pc-nbi" data-nbme="1">item</span></div>'
    expect('NBME block after owners passes', not has(card(kp, sc, own, nbq_ok), 'NBME'))
    expect('NBME block above owners', has(card(kp, sc, nbq_ok, own), 'NBME block sits'))
    expect('empty NBME block', has(card(kp, sc, own, '<div class="pc-nbq">nothing</div>'), 'no logged NBME item'))
    expect('lint_card is card_check', L.lint_card(good) == [])

    # ------------------------------------------------------------ outline_check card entry
    def oc_errors(body, steps=None):
        p = os.path.join(tmp, 'outline.json')
        json.dump({'brief': 'pc-test', 'prefix': 'tcx', 'entry': 'card', 'lens': 'psych', 'steps': steps or [],
                   'src': ['src.json'], 'body': body}, open(p, 'w'))
        c = OC.Check(p, None, None)
        c.s1()
        return c.errors
    blocks = [{'type': 'keypoint', 'lines': [T('x')]}, {'type': 'owners', 'lines': [T('y')]}]
    expect('outline_check card: card blocks pass S1', oc_errors(blocks) == [], oc_errors(blocks))
    for furn in ({'type': 'h', 'n': 1, 'title': 'Frame', 'id': 'x'}, {'type': 'stepper'}, {'type': 'pause', 'text': 'x'},
                 {'type': 'bottom', 'lines': []}, {'type': 'workup5a', 'zones': []}, {'type': 'ladder', 'rungs': []}):
        e = oc_errors(blocks + [furn])
        expect('outline_check card refuses %s' % furn['type'], any('spine furniture' in str(x) for x in e), e)
    e = oc_errors(blocks, steps=[[1, 'Frame', 'x']])
    expect('outline_check card refuses steps', any('spine furniture' in str(x) for x in e), e)
    expect('outline_check card cap 600', OC.CAPS.get('card') == 600)
finally:
    shutil.rmtree(tmp, ignore_errors=True)

# ---------------------------------------------------------------- apply_edits: new_brief fallbacks, retire_brief
ITEM = ('<li data-type="avoid" data-d1="A" data-d2="B" data-item-id="%s" data-item-version="%s" data-item-status="ready" '
        'data-src="authored"><span class="sl">%s</span> &rarr; <b>Key</b> &rarr; why</li>')


def brief(bid, items, cls='brief'):
    return ('<div class="%s" id="%s" data-shelf="psych">\n<h4>%s</h4>\n<p class="sub">sub</p>\n'
            '<h5 class="authored-hdr" id="%s-bank">Practice</h5>\n<ol class="bank authored">\n%s\n</ol>\n</div>'
            % (cls, bid, bid, bid, '\n'.join(ITEM % i for i in items)))


def page(*briefs_):
    return ('<html><body>\n<div id="navlinks">\n  <div class="sect"><span class="ttl">Psychiatry</span><span class="count">2</span>\n'
            '    <a href="#anchor">Anchor</a>\n    <a href="#old">Old</a>\n  </div>\n'
            '  <div class="sect pc-sect"><span class="ttl">Psych Pharmacology</span><span class="count">0</span>\n'
            '    <a class="pc-plan" href="#psych-pharm">SNRIs</a>\n  </div>\n</div>\n'
            '<h3 class="system" id="psych">Psychiatry</h3>\n'
            + brief('anchor', [('q_aaaaaaaaaaaaaaaaaaa1', '1', 'anchor stem')]) + '\n\n'
            + brief('old', [('q_bbbbbbbbbbbbbbbbbbb1', '1', 'old stem one'), ('q_bbbbbbbbbbbbbbbbbbb2', '2', 'old stem two')]) + '\n\n'
            '<h3 class="system" id="psych-pharm">Psych Pharmacology</h3>\n<p class="system-note">3 of 18 class cards</p>\n'
            + '\n'.join(briefs_) + '\n</body></html>')


def nb(bid, items, after):
    return {'op': 'new_brief', 'after': after, 'html': brief(bid, items, 'brief sp pc')}


base = page()
moved = [('q_bbbbbbbbbbbbbbbbbbb1', '1', 'old stem one'), ('q_bbbbbbbbbbbbbbbbbbb2', '2', 'old stem two')]
h, log = AE.apply(base, {'edits': [nb('pc-snri', [moved[0]], 'pc-maoi|#psych-pharm')]})
expect('new_brief "#heading" fallback lands after the system note',
       re.search(r'<p class="system-note">[^<]*</p>\s*<div class="brief sp pc" id="pc-snri"', h) is not None, log)
h2, _ = AE.apply(h, {'edits': [nb('pc-antidep', [moved[1]], 'pc-snri|#psych-pharm')]})
expect('new_brief first fallback wins when present', h2.index('id="pc-antidep"') > h2.index('id="pc-snri"')
       and re.search(r'id="pc-snri".*?</div>\s*<div class="brief sp pc" id="pc-antidep"', h2, re.S) is not None)
raises('new_brief with no anchor on the page', lambda: AE.apply(base, {'edits': [nb('pc-x', [], 'nope|#nosuch')]}), 'no anchor')
raises('new_brief id already used', lambda: AE.apply(h, {'edits': [nb('pc-snri', [], '#psych-pharm')]}), 'already used')

ret = {'op': 'retire_brief', 'brief': 'old', 'alias_before': 'pc-antidep', 'ledger': 'repair/s159/S159.md'}
r, log = AE.apply(h2, {'edits': [ret]})
expect('retire_brief removes the brief', 'id="old"' not in r.replace('<span class="alias" id="old">', ''))
expect('retire_brief alias span before alias_before', '<span class="alias" id="old"></span>\n<div class="brief sp pc" id="pc-antidep"' in r)
expect('retire_brief drops the nav link', 'href="#old"' not in r)
expect('retire_brief drops the section count', '<span class="ttl">Psychiatry</span><span class="count">1</span>' in r)
expect('retire_brief keeps the moved items once', r.count('q_bbbbbbbbbbbbbbbbbbb1') == 1 and r.count('q_bbbbbbbbbbbbbbbbbbb2') == 1)
expect('retire_brief logs the ledger', any('retire_brief old' in x and 'S159.md' in x for x in log), log)
raises('retire_brief: an item on no other brief', lambda: AE.apply(h, {'edits': [dict(ret, alias_before='pc-snri')]}), 'on no other brief')
low = AE.apply(h, {'edits': [nb('pc-antidep', [(moved[1][0], '1', moved[1][2])], 'pc-snri|#psych-pharm')]})[0]
raises('retire_brief: a lowered version', lambda: AE.apply(low, {'edits': [ret]}), 'version 2 -> 1')
chg = AE.apply(h, {'edits': [nb('pc-antidep', [(moved[1][0], '2', 'a changed stem')], 'pc-snri|#psych-pharm')]})[0]
raises('retire_brief: a changed stem without a bump', lambda: AE.apply(chg, {'edits': [ret]}), 'version 2 -> 2')
bump = AE.apply(h, {'edits': [nb('pc-antidep', [(moved[1][0], '3', 'a changed stem')], 'pc-snri|#psych-pharm')]})[0]
expect('retire_brief: a changed stem with a bump passes', 'id="old"' not in AE.apply(bump, {'edits': [ret]})[0].replace('class="alias" id="old"', ''))
raises('retire_brief: alias_before not on the page', lambda: AE.apply(h2, {'edits': [dict(ret, alias_before='pc-none')]}), 'pc-none')
raises('retire_brief: schema needs ledger', lambda: AE.apply(h2, {'edits': [{'op': 'retire_brief', 'brief': 'old', 'alias_before': 'pc-antidep'}]}), 'ledger')

# ---------------------------------------------------------------- gate: items of a retired brief may move (s159 chat 3)
import gate as G  # noqa: E402


def gate_codes(cur, ref, root):
    old = os.environ.get('AXBX_RETIRE_ROOT')
    os.environ['AXBX_RETIRE_ROOT'] = root
    try:
        g = G.Gate({})
        G.check_base(cur, ref, G.briefs(cur), G.items(cur), g)
        return [(c, k) for c, k, _ in g.fails]
    finally:
        if old is None:
            os.environ.pop('AXBX_RETIRE_ROOT', None)
        else:
            os.environ['AXBX_RETIRE_ROOT'] = old


groot = tempfile.mkdtemp(prefix='test-cards-gate-')
try:
    nospec = gate_codes(r, base, groot)
    expect('gate without a retire spec: the retired brief and its moves fail',
           ('never-delete', 'old') in nospec and any(c == 'id-immutable' and k.endswith(':brief') for c, k in nospec), nospec)
    os.makedirs(os.path.join(groot, 'repair', 'migration', 'x', 'spine'))
    json.dump({'edits': [ret]}, open(os.path.join(groot, 'repair', 'migration', 'x', 'spine', '06_old_retire.json'), 'w'))
    withspec = gate_codes(r, base, groot)
    expect('gate with a retire spec: the retired brief and its moved items pass', withspec == [], withspec)
    lowered = r.replace('data-item-id="q_bbbbbbbbbbbbbbbbbbb2" data-item-version="2"', 'data-item-id="q_bbbbbbbbbbbbbbbbbbb2" data-item-version="1"')
    expect('gate with a retire spec: a lowered version still fails',
           ('version-bump', 'q_bbbbbbbbbbbbbbbbbbb2') in gate_codes(lowered, base, groot))
    noalias = r.replace('<span class="alias" id="old"></span>\n', '')
    expect('gate with a retire spec but no alias span: the brief fails never-delete',
           ('never-delete', 'old') in gate_codes(noalias, base, groot))
    expect('gate with a retire spec while the brief is still on the page: moves still fail',
           any(c == 'id-immutable' for c, _ in gate_codes(h2.replace('id="q_bbbbbbbbbbbbbbbbbbb1"', 'id="q_cccccccccccccccccccc1"', 1), base, groot)))
finally:
    shutil.rmtree(groot, ignore_errors=True)

print('test_cards: %d passed, %d failed' % (ok, bad))
sys.exit(1 if bad else 0)
