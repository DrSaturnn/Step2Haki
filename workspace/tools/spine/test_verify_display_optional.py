#!/usr/bin/env python3
"""Offline test (Jonathan 2026-10-24, no screenshots): READY needs acc, read and flags; display counts only when current.

Runs Verify.holistic() on stub receipts in a temporary workspace (no page, no brief folder needed).

  python3 tools/spine/test_verify_display_optional.py
"""
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import verify as V  # noqa: E402

DEPS = {'brief': 'b' * 10, 'live': '1' * 10, 'bank': '2' * 10, 'facts': 'f' * 10, 'claims': 'c' * 10,
        'specs': '3' * 10, 'siblings': '4' * 10, 'display': 'd' * 10, 'outline': 'none'}   # hex, as real hashes


def receipt(part, verdict='PASS', deps=None):
    d = dict(DEPS, **(deps or {}))
    return 'part: %s\ndeps: %s\nbrief-sha: %s\nVerdict: %s\n\nFindings\n\nChecked and fine:\n- stub\n' % (
        part, ' '.join('%s=%s' % (k, d[k]) for k in V.Verify.PARTS[part]), d['brief'], verdict)


def ready_with(files):
    ws = tempfile.mkdtemp()
    rdir = os.path.join(ws, 'repair', 'migration', 'spine', 'reviews')
    os.makedirs(rdir)
    folder = os.path.join(ws, 'folder')
    os.makedirs(folder)
    for name, text in files.items():
        open(os.path.join(rdir, name), 'w', encoding='utf-8').write(text)
    old = V.WS
    try:
        V.WS = ws
        v = V.Verify.__new__(V.Verify)
        v.bid, v.brief_html, v.d = 'zz-test', '<div class="brief" id="zz-test"></div>', folder
        v.deps = lambda: dict(DEPS)
        v.holistic()
        return v.ready
    finally:
        V.WS = old
        shutil.rmtree(ws)


def main():
    base = {'zz-test_%s_r1.md' % p: receipt(p) for p in ('acc', 'read', 'flags')}
    cases = [
        ('three parts, no display receipt: READY', base, True),
        ('a current display PASS: READY', dict(base, **{'zz-test_display_r1.md': receipt('display')}), True),
        ('a current display FAIL: not READY', dict(base, **{'zz-test_display_r1.md': receipt('display', 'FAIL')}), False),
        ('a stale display receipt: ignored, READY',
         dict(base, **{'zz-test_display_r1.md': receipt('display', 'FAIL', {'display': 'e' * 10})}), True),
        ('no flags receipt: not READY', {k: v for k, v in base.items() if '_flags_' not in k}, False),
        ('a stale acc receipt: not READY', dict(base, **{'zz-test_acc_r2.md': receipt('acc', deps={'brief': 'a' * 10})}), False),
    ]
    fails = 0
    for name, files, want in cases:
        got = ready_with(files)
        ok = (got == 'READY') == want
        fails += 0 if ok else 1
        print('%s %s (%s)' % ('ok  ' if ok else 'FAIL', name, got))
    print('test_verify_display_optional: %d case(s), %d failure(s)' % (len(cases), fails))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
