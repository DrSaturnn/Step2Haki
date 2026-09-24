#!/usr/bin/env python3
"""build.py: apply every repair/sNN/*.json (sorted by name) to index.html.

  python3 repair/build.py sNN [--page index.html] [--out FILE]
All files are applied in memory first; nothing is written unless every op applies.
An absent or empty repair/sNN/ is a no-op build (page written unchanged when --out).
Replaces the old per-batch repair/build_sNN.py scripts.
"""
import glob
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'tools'))
from pagelib import read_page, write_page  # noqa: E402
import apply_edits  # noqa: E402


def main(argv):
    if not argv or not argv[0].startswith('s'):
        print(__doc__)
        return 2
    batch = argv[0]
    page = os.path.join(REPO, 'index.html')
    out = None
    if '--page' in argv:
        page = argv[argv.index('--page') + 1]
    if '--out' in argv:
        out = argv[argv.index('--out') + 1]
    files = sorted(glob.glob(os.path.join(REPO, 'repair', batch, '*.json')))
    html = read_page(page)
    new, ops = html, 0
    for f in files:
        try:
            spec = json.load(open(f, encoding='utf-8'))
            new, log = apply_edits.apply(new, spec)
        except (ValueError, apply_edits.EditError) as ex:
            print('build %s: FAIL in %s: %s' % (batch, os.path.relpath(f, REPO), ex))
            return 1
        ops += len(log)
    write_page(out or page, new)
    print('build %s: OK %d file(s), %d op(s), %+d chars' % (batch, len(files), ops, len(new) - len(html)))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
