#!/usr/bin/env python3
"""Offline test for vendor_scan.file_hits (s147): AnKing-only shingles in repo files are not flagged; any shingle with
a UWorld, NBME or Aquifer source still is."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
from vendor_scan import file_hits
src = {'a': {'anki/anki_cards.txt'}, 'b': {'s22_questions.md'}, 'c': {'anki/anki_cards.txt', 's35_questions.md'},
       'd': {'aq/case31.txt'}}
ok = 0
assert file_hits({'a'}, src) == set(); ok += 1                      # AnKing only: not flagged
assert file_hits({'b'}, src) == {'b'}; ok += 1                      # UWorld: flagged
assert file_hits({'c'}, src) == {'c'}; ok += 1                      # AnKing and NBME: flagged
assert file_hits({'a', 'b', 'd'}, src) == {'b', 'd'}; ok += 1       # Aquifer: flagged
print('test_vendor_anki: %d/4 passed' % ok)
