#!/usr/bin/env python3
"""Offline test for pointer_check.py: a drawer to a missing brief and an unrendered Pairs with block are reported."""
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PAGE = '''<!doctype html><html><body><div class="brief" id="a"><h4>Alpha</h4>
<button type="button" class="sp-drw" data-brief="nowhere">Nowhere</button>
<div class="pearls"><span class="lbl">Pairs with</span> Part I <i>Beta</i>: why.</div></div>
<div class="brief" id="b"><h4>Beta</h4></div></body></html>'''


def main():
    d = tempfile.mkdtemp()
    page = os.path.join(d, 'page.html')
    open(page, 'w').write(PAGE)
    r = subprocess.run([sys.executable, os.path.join(HERE, 'pointer_check.py'), page, 'a'], capture_output=True, text=True)
    out = r.stdout
    fails = 0
    for name, ok in (('exit 1 on problems', r.returncode == 1), ('missing target reported', 'target brief missing' in out),
                     ('unrendered Pairs with reported', 'not rendered as an owner list' in out)):
        fails += 0 if ok else 1
        print('%s %s' % ('ok  ' if ok else 'FAIL', name))
    print('test_pointer_check: %d failure(s)' % fails)
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
