#!/usr/bin/env python3
"""changelog.py: readable summary of what changed on the page between two versions.

  python3 tools/changelog.py <old.html> <new.html> [--check "gate: ..."]... [--site "<line>"]
                             [--entry "sNN: message"] [--changelog CHANGELOG.md]

Prints the commit body: counts before -> after, briefs added (id: title), briefs changed
(id, title and what: items added, items edited, versions bumped, attributes set, prose
edited), other page changes, the site line and the check lines. With --changelog it also
prepends the same text as a dated entry headed by --entry.
"""
import datetime
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pagelib import briefs, items, read_page  # noqa: E402


def strip_items(inner, its, base):
    """Brief inner HTML with every bank item removed (offsets are page offsets)."""
    out, last = [], 0
    for it in sorted(its, key=lambda i: i.start):
        out.append(inner[last:it.start - base])
        last = it.end - base
        if inner[last:last + 1] == '\n':
            last += 1
    out.append(inner[last:])
    return ''.join(out)


def outside(html, bl):
    out, last = [], 0
    for b in sorted(bl, key=lambda x: x.start):
        out.append(html[last:b.start])
        last = b.end
    out.append(html[last:])
    return ''.join(out)


def summarize(old, new):
    ob, nb = briefs(old), briefs(new)
    oi, ni = items(old), items(new)
    obm, nbm = {b.id: b for b in ob}, {b.id: b for b in nb}
    oim = {i.id: i for i in oi}
    by_new = {}
    for i in ni:
        by_new.setdefault(i.brief_id, []).append(i)
    by_old = {}
    for i in oi:
        by_old.setdefault(i.brief_id, []).append(i)
    lines = ['Page: %d briefs, %d items -> %d briefs, %d items' % (len(ob), len(oi), len(nb), len(ni))]
    added = [b for b in nb if b.id not in obm]
    removed = [b for b in ob if b.id not in nbm]
    if added:
        lines.append('Briefs added (%d):' % len(added))
        lines += ['  - %s: %s (%d items)' % (b.id, b.title, len(by_new.get(b.id, []))) for b in added]
    if removed:
        lines.append('Briefs REMOVED (%d): %s' % (len(removed), ', '.join(b.id for b in removed)))
    changed = []
    for b in nb:
        o = obm.get(b.id)
        if not o or html_of(old, o) == html_of(new, b):
            continue
        what = []
        new_items = [i for i in by_new.get(b.id, []) if i.id not in oim]
        if new_items:
            what.append('%d item%s added (%s)' % (len(new_items), '' if len(new_items) == 1 else 's', ', '.join(i.id for i in new_items)))
        bumped, edited, attrs = [], [], []
        for i in by_new.get(b.id, []):
            p = oim.get(i.id)
            if not p:
                continue
            ov, nv = p.attrs.get('data-item-version'), i.attrs.get('data-item-version')
            if ov != nv:
                bumped.append('%s v%s->v%s' % (i.id, ov, nv))
            if p.inner != i.inner:
                edited.append(i.id)
            ch = sorted(k for k in set(p.attrs) | set(i.attrs) if k != 'data-item-version' and p.attrs.get(k) != i.attrs.get(k))
            if ch:
                attrs.append('%s %s' % (i.id, ','.join(ch)))
        gone = [i.id for i in by_old.get(b.id, []) if i.id not in {x.id for x in by_new.get(b.id, [])}]
        if edited:
            what.append('items edited (%s)' % ', '.join(edited))
        if bumped:
            what.append('versions bumped (%s)' % ', '.join(bumped))
        bch = sorted(k for k in set(o.attrs) | set(b.attrs) if o.attrs.get(k) != b.attrs.get(k))
        if bch:
            attrs.insert(0, 'brief %s' % ','.join(bch))
        if attrs:
            what.append('attrs set (%s)' % '; '.join(attrs))
        if gone:
            what.append('ITEMS REMOVED (%s)' % ', '.join(gone))
        po = strip_items(o.inner, by_old.get(b.id, []), o.inner_start)
        pn = strip_items(b.inner, by_new.get(b.id, []), b.inner_start)
        if po != pn:
            what.append('prose edited (%+d chars)' % (len(pn) - len(po)))
        changed.append('  - %s (%s): %s' % (b.id, b.title, '; '.join(what) or 'markup changed'))
    if changed:
        lines.append('Briefs changed (%d):' % len(changed))
        lines += changed
    oo, no = outside(old, ob), outside(new, nb)
    if oo != no:
        lines.append('Other page changes (nav, headers, scripts): %+d chars' % (len(no) - len(oo)))
    if not added and not removed and not changed and oo == no:
        lines.append('Page content unchanged.')
    return lines


def html_of(page, b):
    return page[b.start:b.end]


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    old, new = read_page(argv[0]), read_page(argv[1])
    checks, site, entry, cl = [], None, None, None
    i = 2
    while i < len(argv):
        k, v = argv[i], argv[i + 1]
        if k == '--check':
            checks.append(v)
        elif k == '--site':
            site = v
        elif k == '--entry':
            entry = v
        elif k == '--changelog':
            cl = v
        i += 2
    lines = summarize(old, new)
    if site:
        lines.append(site)
    if checks:
        lines.append('Checks:')
        lines += ['  ' + c for c in checks]
    body = '\n'.join(lines)
    print(body)
    if cl:
        head = '# Changelog\n\nNewest first. Each entry is the commit body written by tools/ship.sh.\n'
        prev = open(cl, encoding='utf-8').read() if os.path.exists(cl) else head
        if prev.startswith('# Changelog'):
            cut = prev.find('\n## ')
            top, rest = (prev, '') if cut < 0 else (prev[:cut + 1], prev[cut + 1:])
        else:
            top, rest = head, prev
        e = '## %s %s\n\n```\n%s\n```\n\n' % (datetime.date.today().isoformat(), entry or '', body)
        with open(cl, 'w', encoding='utf-8') as f:
            f.write(top.rstrip('\n') + '\n\n' + e + rest)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
