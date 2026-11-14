#!/usr/bin/env python3
"""Offline tests for rewrite_lanes.copy_lock_keys: the lock waiver is honored only for a header-row rename."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rewrite_lanes as RL


def run(x):
    d = {}
    RL.copy_lock_keys(x, d)
    return d


def main():
    fails = 0
    cases = [
        ({'lock': False, 'lock_reason': 'H12: caption renamed; ladder rule moved'}, True),
        ({'lock': False, 'lock_reason': 'shorter wording'}, False),
        ({'lock': False}, False),
        ({'lock_ok': ['most'], 'lock_reason': 'header rename H13'}, False),
    ]
    for x, waived in cases:
        d = run(x)
        got = d.get('lock') is False
        if got != waived:
            fails += 1
            print('FAIL', x, d)
    d = run({'lock_ok': ['a'], 'lock_reason': 'r', 'cut': 'C1', 'note': 'n'})
    if set(d) != {'lock_ok', 'lock_reason', 'cut', 'note'}:
        fails += 1
        print('FAIL copy', d)
    print('test_rewrite_lock_keys: %d of %d passed' % (len(cases) + 1 - fails, len(cases) + 1))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
