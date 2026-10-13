#!/usr/bin/env python3
"""G-READY for ship.sh: a batch that replaces a brief with a spine build (replace_brief or replace_cluster whose HTML
carries data-spine="2") ships only when tools/spine/verify.py says READY for that brief's local folder (mechanical
checks plus the four current review receipts). Small replace or set_attr edits to a spine brief are not spine builds;
they are covered by the approval gate (approval.py), not by READY.

  python3 tools/hooks/ready_gate.py sNN      exit 0 if every spine build in the batch is READY
"""
import glob
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, '..', '..'))


def folders():
    out = {}
    for e in glob.glob(os.path.join(WS, 'repair', 'migration', '*', '*', 'spine', '10_*_spine.json')):
        try:
            out[json.load(open(e, encoding='utf-8'))['edits'][0]['brief']] = os.path.dirname(e)
        except (ValueError, KeyError, IndexError):
            pass
    return out


def main(b):
    builds = []
    for f in sorted(glob.glob(os.path.join(WS, 'repair', b, '*.json'))):
        for e in json.load(open(f, encoding='utf-8')).get('edits', []):
            # the raw strings, not json.dumps(e), whose escaped quotes never matched (found at the s132 ship)
            if e.get('op') in ('replace_brief', 'replace_cluster') and \
                    any('data-spine="2"' in v for v in e.values() if isinstance(v, str)):
                builds.append(e.get('brief') or e.get('anchor') or '?')
    if not builds:
        print('ready: no spine builds in %s' % b)
        return 0
    have, bad = folders(), []
    for bid in builds:
        d = have.get(bid)
        if not d:
            bad.append('%s: no local spine folder' % bid)
            continue
        r = subprocess.run([sys.executable, os.path.join(WS, 'tools', 'spine', 'verify.py'), d], capture_output=True,
                           text=True, cwd=WS)
        last = (r.stdout.strip().splitlines() or ['?'])[-1]
        if r.returncode != 0:
            bad.append(last)
    if bad:
        print('ready: NOT READY: ' + ' | '.join(bad))
        return 1
    print('ready: %d spine build(s) READY: %s' % (len(builds), ', '.join(builds)))
    return 0


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__.strip().splitlines()[-1].strip())
    sys.exit(main(sys.argv[1]))
