#!/usr/bin/env python3
"""restored_paths (s163b, Jonathan 2026-11-05: "patch.py sync and ship.sh skip untracked lanes copies restored from
local-only"): list the untracked, not-ignored files in the public repo that are copies of the private repo's
local-only/ tree, so a commit step can leave them out.

Session start restores local-only over workspace/ (cp -rn). A restored file that .gitignore does not cover (the s155 to
s158 repair/sNNN/lanes/ copies) shows as untracked, and `git add -A` stages it; the pre-commit guard then refuses the
commit (s163's first ship run). A file counts as restored when workspace/<rel> is untracked, not ignored, and
byte-identical to <private>/local-only/<rel>. Anything else untracked (new batch work) is left alone.

  python3 tools/restored_paths.py [--root <public repo root>] [--private <private clone>] [-0]
Prints repo-relative paths, one per line (NUL-separated with -0); exit 0 always.
"""
import filecmp
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def restored(root, priv):
    ws = os.path.join(root, 'workspace')
    lo = os.path.join(priv, 'local-only')
    if not os.path.isdir(lo):
        return []
    r = subprocess.run(['git', 'ls-files', '--others', '--exclude-standard', '-z', '--', 'workspace'],
                       cwd=root, capture_output=True)
    out = []
    for p in r.stdout.decode('utf-8', 'surrogateescape').split('\0'):
        if not p.startswith('workspace/'):
            continue
        src = os.path.join(lo, p[len('workspace/'):])
        dst = os.path.join(root, p)
        if os.path.isfile(src) and os.path.isfile(dst) and filecmp.cmp(src, dst, shallow=False):
            out.append(p)
    return out


def main(a):
    root = os.path.dirname(os.path.dirname(HERE))
    priv = os.environ.get('AX_PRIVATE', '/home/claude/step2haki-private')
    if '--root' in a:
        root = a[a.index('--root') + 1]
    if '--private' in a:
        priv = a[a.index('--private') + 1]
    sep = '\0' if '-0' in a else '\n'
    ps = restored(root, priv)
    if ps:
        sys.stdout.write(sep.join(ps) + sep)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
