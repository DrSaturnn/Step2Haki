#!/usr/bin/env python3
"""idgen.py: deterministic permanent ids for new bank items.

Ids are q_/o_ + 20 hex of sha256 over the FULL keyed answer and the FULL stem
(a truncated seed once collided). Each option id also folds in its role and label.
Uniqueness is guaranteed against every q_/o_ token already on the page and within
the batch: on a clash the seed gets a counter salt and is rehashed.

  python3 tools/idgen.py "<key>" "<stem>" ["<d1>" "<d2>"] [--page index.html]
prints data-item-id / data-key-id / data-d1-id / data-d2-id attributes.
Library: new_item_ids(key, stem, d1, d2, taken:set) -> dict (adds to `taken`).
"""
import hashlib
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pagelib import read_page, text  # noqa: E402

TOKEN = re.compile(r'\b[qo]_[0-9a-f]{20}\b')


def _norm(s):
    return re.sub(r'\s+', ' ', text(s or '')).strip()


def taken_ids(html):
    return set(TOKEN.findall(html))


def _mint(prefix, seed, taken):
    salt = 0
    while True:
        s = seed if salt == 0 else '%s#%d' % (seed, salt)
        cand = '%s_%s' % (prefix, hashlib.sha256(s.encode('utf-8')).hexdigest()[:20])
        if cand not in taken:
            taken.add(cand)
            return cand
        salt += 1


def new_item_ids(key, stem, d1='', d2='', taken=None):
    taken = set() if taken is None else taken
    k, st = _norm(key), _norm(stem)
    if not k or not st:
        raise ValueError('idgen needs the full key and the full stem')
    base = 'axbx|%s|%s' % (k, st)
    return {
        'data-item-id': _mint('q', 'q|' + base, taken),
        'data-key-id': _mint('o', 'o|key|%s|%s' % (k, base), taken),
        'data-d1-id': _mint('o', 'o|d1|%s|%s' % (_norm(d1), base), taken),
        'data-d2-id': _mint('o', 'o|d2|%s|%s' % (_norm(d2), base), taken),
    }


def main(argv):
    page = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'index.html')
    if '--page' in argv:
        i = argv.index('--page')
        page = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    if len(argv) < 2:
        print(__doc__)
        return 2
    key, stem = argv[0], argv[1]
    d1 = argv[2] if len(argv) > 2 else ''
    d2 = argv[3] if len(argv) > 3 else ''
    taken = taken_ids(read_page(page)) if os.path.exists(page) else set()
    ids = new_item_ids(key, stem, d1, d2, taken)
    print(' '.join('%s="%s"' % kv for kv in ids.items()))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
