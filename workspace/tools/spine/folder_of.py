#!/usr/bin/env python3
"""folder_of (Jonathan 2026-10-24, fewer lead calls): the local spine folder that builds a brief, found from each
folder's 10_*_spine.json (or claim_map.json primary_id), so a lead never searches for "DEM" or "N4" by hand.

  python3 tools/spine/folder_of.py <brief-id> [<brief-id> ...]   one line per id: id, then its folder (or "no folder")
  python3 tools/spine/folder_of.py --all                         every brief id with a local spine folder
"""
import glob
import json
import os
import sys

WS = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))


def folders():
    out = {}
    pats = ('repair/migration/*/*/spine', 'repair/migration/*/*/*/spine')
    for d in sorted(p for pat in pats for p in glob.glob(os.path.join(WS, pat))):
        bid = None
        for f in glob.glob(os.path.join(d, '10_*_spine.json')):
            try:
                bid = json.load(open(f, encoding='utf-8'))['edits'][0]['brief']
            except (ValueError, KeyError, IndexError, OSError):
                pass
        if not bid:
            try:
                bid = json.load(open(os.path.join(d, 'claim_map.json'), encoding='utf-8')).get('primary_id')
            except (ValueError, OSError):
                pass
        if bid:
            out.setdefault(bid, os.path.relpath(d, WS))
    return out


def main(argv):
    if not argv:
        sys.exit(__doc__.strip().splitlines()[3].strip())
    m = folders()
    ids = sorted(m) if argv == ['--all'] else argv
    for i in ids:
        print('%s\t%s' % (i, m.get(i, 'no folder')))
    return 0 if all(i in m for i in ids) else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
