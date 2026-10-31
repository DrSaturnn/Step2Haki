#!/usr/bin/env python3
"""verify_all: verify.py on a list of brief folders, three at a time (s148 efficiency fix 5: nine at once timed out
render.js), printing one line per brief: READY, MECH (mechanical pass, not ready, with the reason) or FAIL (with its
FIX lines). Each brief's full output goes to <folder>/verify_all.log only with --log (off by default: verify must not
write tracked files, and a log in a brief folder is untracked local-only data).

  python3 tools/spine/verify_all.py <brief dir> [<brief dir> ...] [--fast] [--mech] [--jobs 3] [--log]
Exit 0 when every brief is READY (with --mech: every brief passes the mechanical checks).
"""
import concurrent.futures as cf
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, '..', '..'))


def one(d, flags, log):
    r = subprocess.run([sys.executable, os.path.join(HERE, 'verify.py'), d] + flags, capture_output=True, text=True, cwd=WS)
    out = r.stdout + r.stderr
    if log:
        open(os.path.join(d, 'verify_all.log'), 'w', encoding='utf-8').write(out)
    last = [l for l in out.splitlines() if l.startswith('verify ')]
    fixes = [l for l in out.splitlines() if l.startswith('FIX ')]
    warns = sum(1 for l in out.splitlines() if l.startswith('warn lint '))
    tail = last[-1] if last else (out.strip().splitlines() or ['(no output)'])[-1]
    return d, r.returncode, tail, fixes, warns


def state(rc, last, mech):
    """verify exits 1 FAIL, 2 mechanical pass not READY, 0 READY (with --mech, 0 is a mechanical pass)"""
    if rc == 1:
        return 'FAIL'
    if rc == 2:
        return 'MECH'
    if mech:
        return 'PASS'
    return 'READY' if ': READY' in last else 'MECH'


def main(argv):
    dirs = [os.path.abspath(a) for a in argv if not a.startswith('--') and not re.fullmatch(r'\d+', a)]
    if not dirs:
        sys.exit(__doc__.strip().splitlines()[4].strip())
    jobs = int(argv[argv.index('--jobs') + 1]) if '--jobs' in argv else max(1, min(3, os.cpu_count() or 1))   # s156: 3 jsdom renders on 2 cores time out at 90 s
    flags = [f for f in ('--fast', '--mech') if f in argv]
    mech = '--mech' in argv
    bad = 0
    with cf.ThreadPoolExecutor(jobs) as ex:
        for d, rc, last, fixes, warns in ex.map(lambda d: one(d, flags, '--log' in argv), dirs):
            st = state(rc, last, mech)
            bad += st not in ('READY', 'PASS')
            print('%-5s %s  [%d lint warning(s)]  %s' % (st, os.path.relpath(d, WS), warns, last))
            for f in fixes:
                print('      ' + f)
    print('verify_all: %d brief(s), %d not %s' % (len(dirs), bad, 'passing' if mech else 'READY'))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
