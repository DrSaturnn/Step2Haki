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
    # s142: a hub folder sits one level deeper (repair/migration/psych/HUB/voices/spine)
    for e in glob.glob(os.path.join(WS, 'repair', 'migration', '*', '*', 'spine', '10_*_spine.json')) + glob.glob(os.path.join(WS, 'repair', 'migration', '*', '*', '*', 'spine', '10_*_spine.json')):
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
            if e.get('op') == 'new_brief' and 'data-spine="2"' in (e.get('html') or ''):
                # s148e: a new brief enters as a plain shell (05_<id>_new.json) and gets its spine body by replace_brief,
                # so a spine body can never skip this gate by arriving inside a new_brief op
                builds.append('%s (spine body inside new_brief: ship it as a shell plus a replace_brief)' % (e.get('html') or '?')[:60])
                continue
            if e.get('op') in ('replace_brief', 'replace_cluster') and \
                    any('data-spine="2"' in v for v in e.values() if isinstance(v, str)):
                builds.append(e.get('brief') or e.get('anchor') or '?')
    if not builds:
        print('ready: no spine builds in %s' % b)
        return 0
    have, bad = folders(), []
    todo = []
    for bid in builds:
        d = have.get(bid)
        if not d:
            bad.append('%s: no local spine folder' % bid)
            continue
        todo.append(d)

    def one(d):
        r = subprocess.run([sys.executable, os.path.join(WS, 'tools', 'spine', 'verify.py'), d], capture_output=True,
                           text=True, cwd=WS)
        return r.returncode, (r.stdout.strip().splitlines() or ['?'])[-1]
    # s154c (105 briefs, about 95 s each): AX_READY_JOBS runs the same full verify on several folders at once; the
    # check per brief is unchanged and the default stays one at a time
    jobs = max(1, int(os.environ.get('AX_READY_JOBS', '1') or 1))
    if jobs > 1:
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(jobs) as ex:
            results = list(ex.map(one, todo))
    else:
        results = [one(d) for d in todo]
    for rc, last in results:
        if rc != 0:
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
