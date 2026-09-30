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
from pagelib import briefs, read_page  # noqa: E402

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
total = 1 + 9
print('%d/%d passed' % (total - bad, total))
sys.exit(1 if bad else 0)
