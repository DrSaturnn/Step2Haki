#!/usr/bin/env python3
"""Offline test for restored_paths.py (s163b): a temporary public repo and private tree."""
import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import restored_paths as R  # noqa: E402

ok = bad = 0


def expect(name, cond):
    global ok, bad
    ok, bad = (ok + 1, bad) if cond else (ok, bad + 1)
    if not cond:
        print('FAIL', name)


def put(p, s):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w').write(s)


t = tempfile.mkdtemp()
root, priv = os.path.join(t, 'pub'), os.path.join(t, 'priv')
subprocess.run(['git', 'init', '-q', root], check=True)
put(os.path.join(root, 'workspace', '.gitignore'), 'ignored/\n')
put(os.path.join(root, 'workspace', 'tracked.txt'), 'a')
subprocess.run(['git', '-C', root, 'add', '-A'], check=True)
subprocess.run(['git', '-C', root, '-c', 'user.email=x@y', '-c', 'user.name=x', 'commit', '-qm', 'i'], check=True)
for rel, body in (('repair/s155/lanes/l.json', '{}'), ('ignored/f.txt', 'i'), ('changed.txt', 'priv')):
    put(os.path.join(priv, 'local-only', rel), body)
    put(os.path.join(root, 'workspace', rel), body if rel != 'changed.txt' else 'public edit')
put(os.path.join(root, 'workspace', 'repair', 's999', 'new.json'), '[]')
got = R.restored(root, priv)
expect('an identical untracked restored copy is listed', 'workspace/repair/s155/lanes/l.json' in got)
expect('an ignored restored copy is not listed (git already skips it)', not any('ignored/' in p for p in got))
expect('a restored path edited since is not listed', 'workspace/changed.txt' not in got)
expect('new batch work is not listed', 'workspace/repair/s999/new.json' not in got)
expect('a missing private tree lists nothing', R.restored(root, os.path.join(t, 'none')) == [])
print('test_restored_paths: %d passed, %d failed' % (ok, bad))
sys.exit(1 if bad else 0)
