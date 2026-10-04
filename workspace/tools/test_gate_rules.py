#!/usr/bin/env python3
"""test_gate_rules.py: proves the source-and-scope rules (tools/content_rules.py) reach every brief type.

The page gate (tools/gate.py, run by tools/ship.sh on every ship) must fail a placeholder, a hedged
failure trigger and a sourceless mnemonic in a topic brief, a Part II (bs) brief and an Aquifer (aq)
brief alike, whatever skill wrote it. The live page must pass as is (pre-existing findings are baselined
in tools/gate_allowlist.txt).

  python3 tools/test_gate_rules.py        exit 1 if any case misbehaves
"""
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from pagelib import items, briefs, read_page  # noqa: E402

# ship.sh sets AXBX_PAGE to the page it is about to ship (its coverage rows and allowlist match that page, not the old one)
PAGE = read_page(os.environ.get('AXBX_PAGE') or os.path.join(os.path.dirname(HERE), 'index.html'))


def gate(html):
    d = tempfile.mkdtemp()
    p = os.path.join(d, 'index.html')
    open(p, 'w', encoding='utf-8').write(html)
    r = subprocess.run([sys.executable, os.path.join(HERE, 'gate.py'), p, '--base', 'none'], capture_output=True, text=True)
    return r.returncode, r.stdout


bad = 0
rc, out = gate(PAGE)
ok = rc == 0
print(('ok  ' if ok else 'BAD ') + ('page to ship' if os.environ.get('AXBX_PAGE') else 'live page') + ' passes the gate (pre-existing findings baselined)' + ('' if ok else '\n' + out[:600]))
bad += not ok

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
def with_figs(*figs):
    return gate(PAGE[:at] + ''.join(figs) + PAGE[at:])[1]
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
total = 1 + 9 + 2 + 3 + 3
print('%d/%d passed' % (total - bad, total))
sys.exit(1 if bad else 0)
