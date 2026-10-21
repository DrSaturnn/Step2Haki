#!/usr/bin/env python3
"""s148h S7 follow-up packets: per brief, the lead's decisions on round 1 (data/r1_fixes.tsv, data/r1_closed.tsv) and
every changed item as it now reads, from the round-2 packets that packets.py wrote from the rebuilt batch page.

  python3 repair/s148h/followup.py <round-2 packets dir> [--full-flags b1,b2,...]

Writes <dir>/<brief>/<part>/review.md for acc, read and flags:
  1. "Lead decisions": each round-1 fix (old reason, new reason, the finding it answers, A accept or P partial with the
     lead's wording) and each finding closed without a reason change (with the reason);
  2. "Changed items as they now read": the item line, stem and explanation chain, with (acc, flags) the source map of
     each changed reason (best brief line, claims, quotes), and the brief's First step changes against the live page;
  3. flags only, for the --full-flags briefs (not reviewed in round 1): the whole flags packet.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SLOT = {'key': 'key', 'd1': 'd1', 'd2': 'd2'}


def rows(name):
    return [l.rstrip('\n').split('\t') for l in open(os.path.join(HERE, 'data', name), encoding='utf-8')
            if l.strip() and not l.startswith('#')]


def items_of(text):
    """{item id: [lines]} from an acc reasons.md: the [item ...] line through the line before the next item."""
    out, cur = {}, None
    for ln in text.split('\n## Items', 1)[-1].splitlines():
        m = re.match(r'\[item (\S+), type', ln)
        if m:
            cur = m.group(1)
            out[cur] = []
        if ln.startswith('Sources by id:'):
            cur = None
        if cur:
            out[cur].append(ln)
    return out


def main(argv):
    pk = argv[0]
    full = (argv[argv.index('--full-flags') + 1].split(',') if '--full-flags' in argv else [])
    fixes, closed = rows('r1_fixes.tsv'), rows('r1_closed.tsv')
    briefs = sorted({f[0] for f in fixes} | {c[0] for c in closed if c[0] != 'all' and ',' not in c[0]} | set(full))
    for b in briefs:
        acc = open(os.path.join(pk, b, 'acc', 'reasons.md'), encoding='utf-8').read()
        its = items_of(acc)
        ch = acc.split('## Items', 1)[0]
        ch = ch[ch.find('## Changes besides'):] if '## Changes besides' in ch else ''
        dec = ['## %s' % b, '', '### Lead decisions on round 1', '']
        for f in fixes:
            if f[0] == b:
                dec.append('- %s %s (%s): "%s" -> now "%s" [%s]' % (f[1], f[2], f[5], f[3], f[4],
                                                                   'accepted as proposed' if ' A' in f[5] else 'lead wording'))
        for c in closed:
            if c[0] == b or c[0] == 'all' or b in c[0].split(', '):
                dec.append('- %s: %s. %s' % (c[1], c[2], c[3]))
        changed = {}
        for f in fixes:
            if f[0] != b:
                continue
            hit = [i for i, ls in its.items() if (f[1] == '*' or i.startswith(f[1])) and any('"%s"' % f[4] in x for x in ls)]
            for i in hit[:1]:
                changed.setdefault(i, set()).add(f[4])
        for part in ('acc', 'read', 'flags'):
            out = list(dec) + ['', '### Changed items as they now read', '']
            for i, news in changed.items():
                ls = its[i]
                out += ls[:2] if part == 'read' else []
                if part != 'read':
                    keep, on = [], False
                    for x in ls:
                        if x.startswith('[item') or not x.startswith(('- ', '  ')):
                            keep.append(x)
                            continue
                        if x.startswith('- '):
                            on = any('"%s"' % n in x for n in news)
                        if on:
                            keep.append(x)
                    out += keep
                out.append('')
            if ch and 'No change.' not in ch:
                out += [ch.replace('## Changes besides the reasons, since', '### First step changes, since')]
            if part == 'flags' and b in full:
                out += ['### Full flags packet (not reviewed in round 1)', '',
                        open(os.path.join(pk, b, 'flags', 'reasons.md'), encoding='utf-8').read()]
            d = os.path.join(pk, b, part)
            open(os.path.join(d, 'review.md'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
        print('%-20s %2d decision(s), %2d changed item(s)%s' % (b, len(dec) - 4, len(changed), ', full flags' if b in full else ''))


if __name__ == '__main__':
    main(sys.argv[1:])
