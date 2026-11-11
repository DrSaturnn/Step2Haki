#!/usr/bin/env python3
"""test_githooks.py: offline tests of the commit-msg check and the pre-commit guard, in a scratch repo.

  python3 tools/githooks/test_githooks.py      exit 1 if any case misbehaves
"""
import importlib.machinery
import importlib.util
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))


def load(name):
    loader = importlib.machinery.SourceFileLoader(name.replace('-', '_'), os.path.join(HERE, name))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    return mod


bad = 0


def case(ok, label):
    global bad
    print(('ok  ' if ok else 'BAD ') + label)
    bad += not ok


d = tempfile.mkdtemp()
guard = os.path.join(d, 'guard.txt')
open(guard, 'w', encoding='utf-8').write('# test list\nZebediah\n')
os.environ['S2H_PUBLIC_GUARD'] = guard
cm = load('commit-msg')
BODY = '\n\nMove the rule self-test to a fixture page so one gate run\ntakes a second.\n\nBatch: s999\n'
for msg, size in (('fix(gate): compare prose counts with the page under test' + BODY, (80, 4)),
                  ('chore: update the budget record', (4, 1)),
                  ('content(psych): add the lithium toxicity table' + BODY, (300, 2)),
                  ('Merge branch main into wip', (0, 0))):
    case(cm.errors(msg, size) == [], 'accepted: ' + msg.split('\n')[0])
for msg, size, why in (('s999: s999: hover anchors re-judged', (4, 1), 'no type'),
                       ('feat: added the launch guard', (4, 1), 'not imperative'),
                       ('fix(ship): s999 timers', (4, 1), 'batch id in the subject'),
                       ('fix(ship): time every step', (90, 5), 'large change with no body'),
                       ('docs: cite the decision (Zebediah, 20:14)', (4, 1), 'guarded name'),
                       ('feat: ' + 'x' * 70, (4, 1), 'subject over 72 characters'),
                       ('fix: wrap\n\n' + 'y' * 80 + '\n', (4, 1), 'body line over 72 characters')):
    case(cm.errors(msg, size) != [], 'refused (%s): %s' % (why, msg.split('\n')[0][:50]))

# pre-commit, in a scratch repo
repo = os.path.join(d, 'repo')
os.makedirs(os.path.join(repo, 'workspace', 'repair', 's999'))
env = dict(os.environ, GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_SYSTEM='/dev/null')


def git(*a):
    return subprocess.run(['git', '-C', repo] + list(a), capture_output=True, text=True, env=env)


def pre():
    return subprocess.run([sys.executable, os.path.join(HERE, 'pre-commit')], capture_output=True, text=True, cwd=repo, env=env)


git('init', '-q')
for rel, text, want, label in (
        ('workspace/repair/s999/PLAN.md', 'a plan\n', 1, 'a staged PLAN.md is refused'),
        ('workspace/repair/s999/S999.md', 'a record\n', 1, 'a staged batch record S999.md is refused'),
        ('workspace/tools/x.py', '# Zebediah 2026-01-01: "do it"\n', 1, 'an added line with a guarded name is refused'),
        ('workspace/tools/y.py', '# the rule (D-20260101-1)\n', 0, 'a line citing a digest id passes')):
    p = os.path.join(repo, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8').write(text)
    git('add', rel)
    r = pre()
    case(r.returncode == want, label + ('' if r.returncode == want else ': ' + r.stderr[:200]))
    git('rm', '-q', '--cached', rel)
    os.remove(p)
del os.environ['S2H_PUBLIC_GUARD']
print('%s' % ('githooks: all passed' if not bad else 'githooks: %d failed' % bad))
sys.exit(1 if bad else 0)
