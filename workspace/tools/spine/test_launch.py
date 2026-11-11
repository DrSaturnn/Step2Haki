#!/usr/bin/env python3
"""Offline tests: the launch guard (launch.py refuses a batch that is already open; the remote is stubbed) and the
checks step of batch.py (AX_SESSION first; a failing ship.sh --checks-only stops before the presentation; ship.sh is
stubbed through AX_SHIP_SH).

  python3 tools/spine/test_launch.py      exit 1 if any case misbehaves
"""
import contextlib
import io
import os
import stat
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import batch as BT  # noqa: E402
import launch as LA  # noqa: E402

bad = 0


def case(ok, label):
    global bad
    print(('ok  ' if ok else 'BAD ') + label)
    bad += not ok


HAND = '''# handoff

## State (rewrite after every step)

- **s900 OPEN 2026-01-01** (a patch; step s3).
- **s899 SHIPPED 2025-12-31** (commit abc).

## Where the rest lives
'''
REPOS = [('public', '/pub'), ('private', '/priv')]
none = lambda repo, b: []                                                      # noqa: E731
pub = lambda repo, b: ['refs/heads/wip/' + b] if repo == '/pub' else []        # noqa: E731
r = LA.open_reasons('s900', HAND, none, REPOS)
case(len(r) == 1 and 's900 OPEN 2026-01-01' in r[0], 'a batch the State shows OPEN is refused')
case(LA.open_reasons('s901', HAND, none, REPOS) == [], 'a new id with no remote branch passes')
case(LA.open_reasons('s899', HAND, none, REPOS) == [], 'a shipped batch id is not reported open by the State')
r = LA.open_reasons('s901', HAND, pub, REPOS)
case(len(r) == 1 and 'public repo has the remote branch wip/s901' in r[0], 'a remote branch wip/<id> in one repo is refused')
case(LA.open_reasons('s90', HAND, none, REPOS) == [], 'an id that is a prefix of the open id passes')


def run_checks(session, ship_rc):
    d = tempfile.mkdtemp()
    stub = os.path.join(d, 'ship.sh')
    open(stub, 'w').write('#!/bin/sh\necho "ship $1: %s"\nexit %d\n' % (
        'checks only: every check passed (nothing written)' if ship_rc == 0 else 'ABORT at ui-gate (nothing written)', ship_rc))
    os.chmod(stub, os.stat(stub).st_mode | stat.S_IXUSR)
    keep = {k: os.environ.get(k) for k in ('AX_SESSION', 'AX_SHIP_SH', 'AX_LEAD')}
    os.environ.pop('AX_LEAD', None)
    os.environ['AX_SHIP_SH'] = stub
    if session:
        os.environ['AX_SESSION'] = session
    else:
        os.environ.pop('AX_SESSION', None)
    out = io.StringIO()
    try:
        with contextlib.redirect_stdout(out):
            rc = BT.checks(['s000selftest'])
    finally:
        for k, v in keep.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
    return rc, out.getvalue()


rc, o = run_checks('', 0)
case(rc == 1 and 'AX_SESSION' in o, 'checks without AX_SESSION stop before ship.sh runs')
rc, o = run_checks('https://claude.ai/code/session_abc123', 1)
case(rc == 1 and 'ABORT at ui-gate' in o, 'a failing checks-only run returns 1 (s8 then does not present)')
rc, o = run_checks('https://claude.ai/code/session_abc123', 0)
case(rc == 0 and 'every check passed' in o, 'a passing checks-only run returns 0')
import shutil  # noqa: E402
shutil.rmtree(os.path.join(BT.WS, 'local', 's000selftest'), ignore_errors=True)
print('launch and checks: %s' % ('all passed' if not bad else '%d failed' % bad))
sys.exit(1 if bad else 0)
