#!/usr/bin/env python3
"""Offline tests for the 2026-10-12 rules: alias words are not counted against the soft cap (outline_check.strip_aka),
and verify's V1 allowlist reads repair/efficiency/ABBREV.json.

  python3 tools/spine/test_caps_abbrev.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from outline_check import strip_aka  # noqa: E402
from verify import ACR_OK  # noqa: E402

ok = bad = 0


def expect(name, cond):
    global ok, bad
    if cond:
        ok += 1
    else:
        bad += 1
        print('FAIL', name)


h = '<td>Minimal change disease <span class="aka">(lipoid nephrosis)</span>; protein mainly albumin</td>'
expect('aka words dropped', 'lipoid' not in strip_aka(h) and 'albumin' in strip_aka(h))
expect('two aka spans', strip_aka(h + h).count('lipoid') == 0)
expect('other spans kept', 'keep' in strip_aka('<span class="mask">keep</span>'))
for a in ('CBC', 'BUN', 'US', 'CT', 'MRI', 'BP', 'HR'):
    expect('allowlist has %s' % a, a in ACR_OK)
for a in ('MRV', 'ECG', 'UA', 'FSGS', 'PSGN'):
    expect('allowlist does not have %s' % a, a not in ACR_OK)
print('test_caps_abbrev: %d passed, %d failed' % (ok, bad))
sys.exit(1 if bad else 0)
