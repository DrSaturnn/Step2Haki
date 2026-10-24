#!/usr/bin/env python3
"""Offline test for squeeze_check.py: a sentence in a 70 px cell is flagged; the same sentence at full width passes."""
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SENT = 'Parent management training first for any persistent disruptive behavior in a young child'
PAGE = '''<!doctype html><html><body><div class="brief" id="t1"><table><tr><td style="width:70px;max-width:70px">%s</td>
<td>x</td></tr></table></div><div class="brief" id="t2"><p>%s</p></div></body></html>''' % (SENT, SENT)


def main():
    d = tempfile.mkdtemp()
    page = os.path.join(d, 'page.html')
    open(page, 'w').write(PAGE)
    run = lambda ids: subprocess.run([sys.executable, os.path.join(HERE, 'squeeze_check.py'), page, ids], capture_output=True, text=True)
    fails = 0
    for name, ids, want in (('narrow cell flagged', 't1', 1), ('full-width paragraph passes', 't2', 0)):
        r = run(ids)
        ok = r.returncode == want
        fails += 0 if ok else 1
        print('%s %s (exit %d) %s' % ('ok  ' if ok else 'FAIL', name, r.returncode, r.stdout.strip().splitlines()[-1:]))
    print('test_squeeze_check: %d failure(s)' % fails)
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
