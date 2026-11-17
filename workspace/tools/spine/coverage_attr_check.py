#!/usr/bin/env python3
"""coverage_attr_check: proves that every brief on PAGE equals the same brief on REF byte for byte once the coverage
attributes (data-bp, data-bps) are removed from its opening tag.

  python3 tools/spine/coverage_attr_check.py PAGE REF

Prints the number of briefs compared, how many differ only in coverage attributes, and every brief that differs in
anything else (opening tag or inner bytes), or that is new or missing. Exit 0 when no brief differs beyond the
coverage attributes; exit 1 otherwise.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pagelib  # noqa: E402

COVERAGE = ('data-bp', 'data-bps')
_ATTR = re.compile(r'\s(%s)="[^"]*"' % '|'.join(re.escape(a) for a in COVERAGE))


def strip(tag):
    return _ATTR.sub('', tag)


def compare(page_html, ref_html):
    cur = {b.id: b for b in pagelib.briefs(page_html)}
    ref = {b.id: b for b in pagelib.briefs(ref_html)}
    same, attr_only, other = 0, [], []
    for bid in sorted(set(cur) | set(ref)):
        c, r = cur.get(bid), ref.get(bid)
        if c is None or r is None:
            other.append((bid, 'missing on page' if c is None else 'new on page'))
            continue
        ct, rt = page_html[c.start:c.open_end], ref_html[r.start:r.open_end]
        if c.inner != r.inner:
            other.append((bid, 'inner bytes differ'))
        elif ct == rt:
            same += 1
        elif strip(ct) == strip(rt):
            attr_only.append(bid)
        else:
            other.append((bid, 'opening tag differs beyond %s' % ', '.join(COVERAGE)))
    return same, attr_only, other


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    page, ref = (pagelib.read_page(p) for p in argv)
    same, attr_only, other = compare(page, ref)
    print('coverage_attr_check: %d briefs identical, %d differ only in %s, %d differ otherwise'
          % (same, len(attr_only), ' / '.join(COVERAGE), len(other)))
    for bid, why in other:
        print('  %s: %s' % (bid, why))
    return 1 if other else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
