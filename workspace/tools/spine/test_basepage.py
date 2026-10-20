#!/usr/bin/env python3
"""Offline tests for basepage.py and the s148e READY-gate rule (a spine body never arrives inside new_brief)."""
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(WS, 'tools'))
import basepage as BP  # noqa: E402
import pagelib as P  # noqa: E402

FAIL = []


def ok(cond, name):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        FAIL.append(name)


def has(page, bid):
    return any(b.id == bid for b in P.briefs(page))


def shell(bid, spine=False):
    page = P.read_page(BP.PAGE)
    after = P.briefs(page)[-1].id
    attrs = ' data-entry="drug" data-lens="psych" data-spine="2"' if spine else ''
    html = ('<div class="brief" id="%s"%s data-shelf="psych" data-bp="behav">\n<h4>Test Shell</h4>\n'
            '<p class="sub">a &middot; b</p>\n<h5 class="authored-hdr" id="zz-bank">Practice</h5>\n'
            '<ol class="bank authored">\n</ol>\n</div>') % (bid, attrs)
    return {'edits': [{'op': 'new_brief', 'after': after, 'html': html}]}


def main():
    tmp = tempfile.mkdtemp(prefix='bp-')
    try:
        live = P.read_page(BP.PAGE)
        ok(BP.base_page(tmp) == live, 'no shell: the base page is the working page')
        ok(BP.base_page_path(tmp, tmp) == BP.PAGE, 'no shell: base_page_path is the working page path')
        json.dump(shell('zz-shell-test'), open(os.path.join(tmp, '05_zz_shell_test_new.json'), 'w'))
        bp = BP.base_page(tmp)
        ok(has(bp, 'zz-shell-test') and not has(live, 'zz-shell-test'),
           'a shell adds the new brief to the base page only')
        p = BP.base_page_path(tmp, os.path.join(tmp, 'o'))
        ok(p != BP.PAGE and has(P.read_page(p), 'zz-shell-test'), 'base_page_path writes the shell page')
        json.dump(shell('zz-shell-test', spine=True), open(os.path.join(tmp, '05_zz_shell_test_new.json'), 'w'))
        try:
            BP.base_page(tmp)
            ok(False, 'a shell carrying data-spine="2" is refused')
        except ValueError:
            ok(True, 'a shell carrying data-spine="2" is refused')
        ok(BP.check_shell({'edits': [{'op': 'replace_brief'}]}) != [], 'a shell file holds only a new_brief op')
        # READY gate: a spine body inside new_brief makes the batch NOT READY
        bdir = os.path.join(WS, 'repair', '_t_basepage_gate')
        os.makedirs(bdir, exist_ok=True)
        json.dump(shell('zz-shell-test', spine=True), open(os.path.join(bdir, '05_x.json'), 'w'))
        r = subprocess.run([sys.executable, os.path.join(WS, 'tools', 'hooks', 'ready_gate.py'), '_t_basepage_gate'],
                           capture_output=True, text=True, cwd=WS)
        ok(r.returncode == 1 and 'NOT READY' in r.stdout, 'ready_gate refuses a spine body inside new_brief')
        json.dump(shell('zz-shell-test'), open(os.path.join(bdir, '05_x.json'), 'w'))
        r = subprocess.run([sys.executable, os.path.join(WS, 'tools', 'hooks', 'ready_gate.py'), '_t_basepage_gate'],
                           capture_output=True, text=True, cwd=WS)
        ok(r.returncode == 0 and 'no spine builds' in r.stdout, 'ready_gate passes a plain shell (no spine build)')
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
        shutil.rmtree(os.path.join(WS, 'repair', '_t_basepage_gate'), ignore_errors=True)
    print('test_basepage: %d failed' % len(FAIL))
    sys.exit(1 if FAIL else 0)


if __name__ == '__main__':
    main()
