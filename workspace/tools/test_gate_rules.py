#!/usr/bin/env python3
"""test_gate_rules.py: proves the source-and-scope rules (tools/content_rules.py) reach every brief type.

The page gate (tools/gate.py, run by tools/ship.sh on every ship) must fail a placeholder, a hedged
failure trigger and a sourceless mnemonic in a topic brief, a Part II (bs) brief and an Aquifer (aq)
brief alike, whatever skill wrote it. The live page must pass as is (pre-existing findings are baselined
in tools/gate_allowlist.txt).

  python3 tools/test_gate_rules.py        exit 1 if any case misbehaves
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from pagelib import items, briefs, read_page  # noqa: E402

# ship.sh sets AXBX_PAGE to the page it is about to ship (its coverage rows and allowlist match that page, not the old one)
PAGE_PATH = os.environ.get('AXBX_PAGE') or os.path.join(os.path.dirname(HERE), 'index.html')
PAGE = read_page(PAGE_PATH)
# s164c: a wrapped page's prebuilt search index (search.json beside it) is gate-checked; content-rule cases below run on
# mutated copies with no index of their own, so they skip that check (AXBX_GATE_SKIP_INDEX=1)
INDEX = os.path.join(os.path.dirname(os.path.abspath(PAGE_PATH)), 'search.json')
WRAPPED = '<template class="axl">' in PAGE


def gate(html, index=None):
    """index None: skip the search index check; a path: copy it beside the page; '' : no index file"""
    d = tempfile.mkdtemp()
    p = os.path.join(d, 'index.html')
    open(p, 'w', encoding='utf-8').write(html)
    if index:
        shutil.copyfile(index, os.path.join(d, 'search.json'))
    env = dict(os.environ, AXBX_GATE_SKIP_INDEX='1' if index is None else '0')
    r = subprocess.run([sys.executable, os.path.join(HERE, 'gate.py'), p, '--base', 'none'], capture_output=True, text=True, env=env)
    return r.returncode, r.stdout


bad = 0
rc, out = gate(PAGE, INDEX if (WRAPPED and os.path.exists(INDEX)) else None)
ok = rc == 0
print(('ok  ' if ok else 'BAD ') + ('page to ship' if os.environ.get('AXBX_PAGE') else 'live page') + ' passes the gate (pre-existing findings baselined)' + ('' if ok else '\n' + out[:600]))
bad += not ok
if WRAPPED:
    rc, out = gate(PAGE, '')
    hit = rc == 1 and '[search-index]' in out
    print(('ok  ' if hit else 'BAD ') + 'wrapped page with no search.json beside it: expects gate FAIL search-index')
    bad += not hit

bl = briefs(PAGE)
for kind in ('brief', 'bs', 'aq'):
    b = next(x for x in bl if x.kind == kind)
    for code, inject in (('G1', '<p>Dose: to be determined</p>'),
                         ('G2', '<p>Refer if no improvement.</p>'),
                         ('K3', '<div class="pearls"><span class="lbl">Mnemonic</span> ABC: alpha, beta, charlie</div>')):
        html = PAGE[:b.inner_end] + inject + PAGE[b.inner_end:]
        rc, out = gate(html)
        hit = rc == 1 and ('[%s] %s' % (code, b.id)) in out
        print(('ok  ' if hit else 'BAD ') + '%s in a %s brief (%s): expects gate FAIL %s' % (code, kind, b.id, code))
        bad += not hit
# retired items (2026-09-30): removing an item fails never-delete unless the ledger names it and its HTML is archived
it0 = next(i for i in items(PAGE) if i.brief_id == bl[0].id)
cut = PAGE[:it0.start] + PAGE[it0.end:]
d = tempfile.mkdtemp(); ref = os.path.join(d, 'ref.html'); open(ref, 'w', encoding='utf-8').write(PAGE)
cur = os.path.join(d, 'index.html'); open(cur, 'w', encoding='utf-8').write(cut)
def gate_base(env):
    r = subprocess.run([sys.executable, os.path.join(HERE, 'gate.py'), cur, '--base', ref], capture_output=True, text=True, env=dict(os.environ, **env))
    return r.stdout
arch = os.path.join(os.path.dirname(HERE), 'repair', 'archive', '_selftest.html')
os.makedirs(os.path.dirname(arch), exist_ok=True); open(arch, 'w', encoding='utf-8').write(PAGE[it0.start:it0.end])
led = os.path.join(d, 'led.csv')
open(led, 'w', encoding='utf-8').write('item_id,brief,date,reason,archive\n')
hit = ('[never-delete] item ' + it0.id) in gate_base({'AXBX_RETIRED': led})
print(('ok  ' if hit else 'BAD ') + 'item removed with no ledger row: expects gate FAIL never-delete'); bad += not hit
open(led, 'a', encoding='utf-8').write('%s,%s,2026-09-30,self-test,repair/archive/_selftest.html\n' % (it0.id, it0.brief_id))
hit = ('[never-delete] item ' + it0.id) not in gate_base({'AXBX_RETIRED': led})
print(('ok  ' if hit else 'BAD ') + 'item retired through the ledger with its HTML archived passes'); bad += not hit
os.remove(arch)
# merged briefs (2026-10-01): a brief folded into another through data-replaces with an alias span passes never-delete,
# and its items may move to a cluster brief; the same removal without the alias fails, and moving an item between two
# live briefs still fails id-immutable
b1, b2, b3 = bl[0], bl[1], bl[2]
mv = next(i for i in items(PAGE) if i.brief_id == b2.id)
def merged(alias):
    body = PAGE[b2.inner_start:b2.inner_end].replace(PAGE[mv.start:mv.end], '')
    open1 = PAGE[b1.start:b1.open_end]
    head = (open1[:-1] + ' data-replaces="%s">' % b2.id) + ('<span class="alias" id="%s"></span>' % b2.id if alias else '')
    out = PAGE[:b1.start] + head + PAGE[b1.open_end:b1.inner_end] + body + PAGE[b1.inner_end:b2.start] + PAGE[b2.end:b3.inner_end] + PAGE[mv.start:mv.end] + PAGE[b3.inner_end:]
    open(cur, 'w', encoding='utf-8').write(out)
    return gate_base({'AXBX_RETIRED': led})
o = merged(True)
hit = ('[never-delete] brief %s ' % b2.id) not in o and ('[id-immutable] %s moved' % mv.id) not in o
print(('ok  ' if hit else 'BAD ') + 'brief merged through data-replaces with an alias, its item moved to a cluster brief: passes'); bad += not hit
o = merged(False)
hit = ('[never-delete] brief %s ' % b2.id) in o
print(('ok  ' if hit else 'BAD ') + 'brief removed without an alias span: expects gate FAIL never-delete'); bad += not hit
it3 = next(i for i in items(PAGE) if i.brief_id == b3.id)
open(cur, 'w', encoding='utf-8').write(PAGE[:b1.inner_end] + PAGE[it3.start:it3.end] + PAGE[b1.inner_end:it3.start] + PAGE[it3.end:])  # b3 sits after b1
o = gate_base({'AXBX_RETIRED': led})
hit = ('[id-immutable] %s moved' % it3.id) in o
print(('ok  ' if hit else 'BAD ') + 'item moved between two live briefs: expects gate FAIL id-immutable'); bad += not hit
# mimic rows (hub and spoke, 2026-10-03): a row edited by hand, or two copies that differ, fail; a spoke row missing
# from its hub fails; byte-identical copies pass
sys.path.insert(0, os.path.join(HERE, 'typec'))
import lifechart as LC, mimics as MM  # noqa: E402
hubfig = LC.course_table('Hub', MM.ROWS, MM.AXIS, 'voices', groups=MM.HUBS['voices']['groups'], full=True)
spk = LC.course_table('Slice', {k: MM.ROWS[k] for k in MM.SPOKES['psychosis-duration']['rows']}, MM.AXIS, 'voices')
at = bl[0].inner_end
import re as _re0
def with_figs(*figs):
    # the page's own mimic figures are stripped first, so the test holds whether or not the page's rows match the current
    # tools/typec rows (between a registry edit and the ship that rebuilds them) and whether or not a real hub is on the page
    base = _re0.sub(r'<figure class="lcw lcc".*?</figure>', '', PAGE[:at], flags=_re0.S)
    rest = _re0.sub(r'<figure class="lcw lcc".*?</figure>', '', PAGE[at:], flags=_re0.S)
    return gate(base + ''.join(figs) + rest)[1]
o = with_figs(hubfig, spk)
hit = '[mimic-row]' not in o
print(('ok  ' if hit else 'BAD ') + 'hub and spoke with byte-identical rows pass'); bad += not hit
o = with_figs(hubfig, spk.replace('Often begins around 40', 'Often begins around 45', 1))
hit = '[mimic-row] mimic row delusional was edited' in o
print(('ok  ' if hit else 'BAD ') + 'a hand-edited spoke row: expects gate FAIL mimic-row'); bad += not hit
import re as _re
o = with_figs(_re.sub(r'<li class="cr" data-mrow="paranoid-pd".*?</li>', '', hubfig, flags=_re.S), spk)
hit = '[mimic-row] spoke row paranoid-pd is missing' in o
print(('ok  ' if hit else 'BAD ') + 'a spoke row missing from its hub: expects gate FAIL mimic-row'); bad += not hit
# s146c, s161c: the Presentations group. A hub has its one plain link there and none in its system; a non-hub may not be
# there. The page under test is given a Presentations group first if it has none.
nav0 = PAGE.find('<div id="navlinks">\n')
hub_ids = [b.id for b in bl if b.attrs.get('data-entry') == 'hub']
plain_brief = next(b.id for b in bl if b.kind == 'brief' and b.attrs.get('data-entry') != 'hub')
def with_pres(ids, page=PAGE):
    p = page
    if '<div class="sect">Presentations' in p:
        a = p.find('<div class="sect">Presentations'); z = p.find('<div class="sect">', a + 10)
        p = p[:a] + p[z:]
    blk = '<div id="navlinks">\n    <div class="sect">Presentations <span class="count">%d</span></div>\n' % len(ids) + ''.join('    <a href="#%s">x</a>\n' % i for i in ids)
    return p.replace('<div id="navlinks">\n', blk, 1)
o = gate(with_pres(hub_ids))[1]
hit = '[nav-link]' not in o and '[nav-count]' not in o
print(('ok  ' if hit else 'BAD ') + 'every hub listed once, in Presentations, passes'); bad += not hit
o = gate(with_pres(hub_ids + [plain_brief]))[1]
hit = '[nav-link] %s is in Presentations but is not a hub' % plain_brief in o
print(('ok  ' if hit else 'BAD ') + 'a non-hub in Presentations: expects gate FAIL nav-link'); bad += not hit
h = hub_ids[0]
_p = with_pres(hub_ids); _m = _p.find('<div class="sect">Musculoskeletal'); _e = _p.find('</div>', _m) + 6
p2 = _p[:_e] + '\n    <a href="#%s">x</a>' % h + _p[_e:]
o = gate(p2)[1]
hit = '[nav-link] %s has 2 nav links' % h in o
print(('ok  ' if hit else 'BAD ') + 'a hub also listed in its system: expects gate FAIL nav-link'); bad += not hit
o = gate(with_pres(hub_ids[1:]))[1]
hit = '[nav-link] %s is a hub but has no link in Presentations' % hub_ids[0] in o
print(('ok  ' if hit else 'BAD ') + 'a hub missing from Presentations: expects gate FAIL nav-link'); bad += not hit
# s148g per-choice reasons: all three or none
# s148h: the page may already carry reasons, so take an item without them and expect the page's own count plus one
_it = next(i for i in items(PAGE) if 'data-key-why=' not in PAGE[i.start:PAGE.index('>', i.start)])
_tag = PAGE[_it.start:PAGE.index('>', _it.start)]
_m = re.search(r'\((\d+) with reasons\)', gate(PAGE)[1])
_base = int(_m.group(1)) if _m else 0
_two = _tag + ' data-key-why="a" data-d1-why="b"'
o = gate(PAGE.replace(_tag, _two, 1))[1]
hit = '[item-why]' in o
print(('ok  ' if hit else 'BAD ') + 'an item with two of its three reasons: expects gate FAIL item-why'); bad += not hit
o = gate(PAGE.replace(_tag, _two + ' data-d2-why="c"', 1))[1]
hit = '[item-why]' not in o and '(%d with reasons)' % (_base + 1) in o
print(('ok  ' if hit else 'BAD ') + 'an item with all three reasons: no item-why, counted'); bad += not hit
# s163: structural wording and rail order (C6, C1)
_sb = next(x for x in bl if '<nav class="sp-step"' in PAGE[x.start:x.end])
o = gate(PAGE[:_sb.inner_end] + '<p>Give it now (step 3); this brief owns it.</p>' + PAGE[_sb.inner_end:])[1]
hit = '[structural] %s' % _sb.id in o and 'ownership' in o
print(('ok  ' if hit else 'BAD ') + 'a step number and "owns" in brief text: expects gate FAIL structural'); bad += not hit
o = gate(PAGE[:_sb.inner_end] + '<p>What Step 2 CK rewards.</p>' + PAGE[_sb.inner_end:])[1]
hit = '[structural]' not in o
print(('ok  ' if hit else 'BAD ') + 'the exam name Step 2 CK: no structural failure'); bad += not hit
_seg = PAGE[_sb.start:_sb.end]
_rail = re.search(r'<nav class="sp-step"[^>]*>.*?</nav>', _seg, re.S).group(0)
_old = re.sub(r'<span>Criteria</span>', '<span>X</span>', _rail).replace('<span>Urgent</span>', '<span>Criteria</span>').replace('<span>X</span>', '<span>Urgent</span>')
o = gate(PAGE[:_sb.start] + _seg.replace(_rail, _old, 1) + PAGE[_sb.end:])[1]
hit = '[rail-order] %s' % _sb.id in o
print(('ok  ' if hit else 'BAD ') + 'a rail in the old order: expects gate FAIL rail-order'); bad += not hit
# s165b (D-20261106-11): the UI and prose ratchets
o = gate(PAGE[:_sb.inner_end] + '<p>Fix the class, not the instance.</p>' + PAGE[_sb.inner_end:])[1]
hit = '[prose-lint] %s' % _sb.id in o
print(('ok  ' if hit else 'BAD ') + 'a brief whose prose count rose above its baseline: expects gate FAIL prose-lint'); bad += not hit
_d = tempfile.mkdtemp(); _bp = os.path.join(_d, 'base.html'); open(_bp, 'w', encoding='utf-8').write(PAGE)
_mp = os.path.join(_d, 'index.html'); open(_mp, 'w', encoding='utf-8').write(PAGE[:_sb.inner_end] + '<p>Onset within days.</p>' + PAGE[_sb.inner_end:])
_r = subprocess.run([sys.executable, os.path.join(HERE, 'gate.py'), _mp, '--base', _bp], capture_output=True, text=True,
                    env=dict(os.environ, AXBX_GATE_SKIP_INDEX='1'))
hit = '[prose-touched] %s' % _sb.id in _r.stdout
print(('ok  ' if hit else 'BAD ') + 'a changed brief that still has prose hits: expects gate FAIL prose-touched'); bad += not hit
_i = PAGE.find('</style>')
o = gate(PAGE[:_i] + 'a.zz{transition:opacity .3s ease}' + PAGE[_i:])[1]
hit = '[ui-lint] motion_not_spring' in o
print(('ok  ' if hit else 'BAD ') + 'a new non-spring transition: expects gate FAIL ui-lint'); bad += not hit
total = 1 + WRAPPED + 9 + 2 + 3 + 3 + 4 + 2 + 3 + 3
print('%d/%d passed' % (total - bad, total))
sys.exit(1 if bad else 0)
