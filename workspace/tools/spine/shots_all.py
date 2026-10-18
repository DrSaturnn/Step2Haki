#!/usr/bin/env python3
"""shots_all: shots.py in all four review modes, one after another (s148 efficiency fix 5): phone, phone-study,
desktop and desktop-study. Four parallel shots.py runs were killed for memory in s148; this runs them in sequence.

  python3 tools/spine/shots_all.py <page.html> <out-dir> <brief-id>[,<brief-id>...] [--mode steps|charts|both]
                                   [--width 1280]

A separate script, not a shots.py flag: every display receipt is bound to the hash of shots.py (verify.py deps
"display"), so changing that file would make every display receipt stale.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

MODES = ((['--phone'], 'phone'), (['--phone', '--study'], 'phone-study'), ([], 'desktop'), (['--study'], 'desktop-study'))


def main(argv):
    if len(argv) < 3:
        sys.exit(__doc__.strip().splitlines()[3].strip())
    import shots
    base = [a for a in argv if a not in ('--phone', '--study', '--dark')]
    for flags, name in MODES:
        print('shots_all: %s' % name, flush=True)
        shots.main(base + flags)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
