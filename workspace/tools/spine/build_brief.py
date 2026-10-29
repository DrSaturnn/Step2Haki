#!/usr/bin/env python3
"""build_brief: run one spine brief folder's build in order (shared from s152build.py at the s152 close).

  python3 tools/spine/build_brief.py <folder> [<folder> ...] [--verify]

For each folder: author.py, then author_lib.build (facts_from_spec, outline_render), then disp.py when present (a new
brief with build.py and no author.py, s157: facts_from_spec, then build.py, then disp.py);
--verify then runs verify.py <folder> --mech and prints its verdict line and the count of FIX and warn lines (the full
output goes to <folder>/mech.log). Run from anywhere; set AX_BATCH to the batch id (author_lib.live_src reads it).
One line per folder; exit 1 if any step failed.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import author_lib as L  # noqa: E402


def run(folder, verify):
    f = os.path.abspath(folder)
    name = os.path.basename(os.path.dirname(f)) if os.path.basename(f) == 'spine' else os.path.basename(f)
    if not os.path.exists(os.path.join(f, 'author.py')) and os.path.exists(os.path.join(f, 'build.py')):
        # s157: a brief new in its batch builds by build.py on spinelib and newspine (the s148e tca-tox pattern:
        # shell first, then Spine.finish), the same file verify runs in place; facts.json is made first
        if os.path.exists(os.path.join(f, 'facts_spec.json')):
            r = subprocess.run([sys.executable, os.path.join(L.WS, 'tools', 'spine', 'facts_from_spec.py'),
                                os.path.join(f, 'facts_spec.json')], capture_output=True, text=True, cwd=L.WS)
            if r.returncode:
                print('%s facts FAIL: %s' % (name, (r.stdout + r.stderr).strip()[-1200:]))
                return False
        r = subprocess.run([sys.executable, os.path.join(f, 'build.py')], capture_output=True, text=True, cwd=L.WS)
        if r.returncode:
            print('%s build.py FAIL: %s' % (name, (r.stdout + r.stderr).strip()[-1200:]))
            return False
        print(name, 'build.py:', (r.stdout + r.stderr).strip()[-400:])
    else:
        r = subprocess.run([sys.executable, os.path.join(f, 'author.py')], capture_output=True, text=True, cwd=L.WS)
        if r.returncode:
            print('%s author FAIL: %s' % (name, (r.stdout + r.stderr).strip()[-1200:]))
            return False
        print(name, end=' ')
        L.build(f)
    if os.path.exists(os.path.join(f, 'disp.py')):
        r = subprocess.run([sys.executable, os.path.join(f, 'disp.py')], capture_output=True, text=True, cwd=L.WS)
        print((r.stdout + r.stderr).strip()[-600:])
        if r.returncode:
            return False
    if verify:
        r = subprocess.run([sys.executable, os.path.join(L.WS, 'tools', 'spine', 'verify.py'), f, '--mech'],
                           capture_output=True, text=True, cwd=L.WS)
        out = r.stdout + r.stderr
        open(os.path.join(f, 'mech.log'), 'w', encoding='utf-8').write(out)
        lines = out.splitlines()
        verdict = [l for l in lines if 'MECHANICAL' in l or l.startswith('verify')][-1:] or lines[-1:]
        print('%s verify: %s | %d FIX, %d warn (mech.log)' % (name, ' '.join(verdict).strip()[:200],
              sum(l.startswith('FIX') for l in lines), sum(l.startswith('warn') for l in lines)))
        return r.returncode == 0
    return True


def main(argv):
    verify = '--verify' in argv
    folders = [a for a in argv if not a.startswith('--')]
    if not folders:
        sys.exit(__doc__.strip().splitlines()[2].strip())
    ok = [run(f, verify) for f in folders]
    return 0 if all(ok) else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
