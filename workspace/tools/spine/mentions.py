#!/usr/bin/env python3
"""mentions: every line of a brief that names each diagnosis or finding, body and practice bank together (s152 close,
2026-10-25, runbook S2 and section 4 item 16). A consistency sheet, not a check: the builder (or lead) reads each group
and confirms the lines agree on site, side, timing, age, maneuver and next step, the kind of drift that drew most s152
round-1 MEDs (the venous hum placed "at", "below" and "above" the clavicle, by rotation and by flexion, across body and
stems).

  python3 tools/spine/mentions.py <folder> [--min 2]     writes <folder>/mentions.md; prints one summary line

Subjects: each table row's first cell in the body, each item's key (its <b>) and distractors (data-d1, data-d2), with a
parenthetical other name dropped. Lines: body blocks (p, li, tr, h4 to h6, figcaption, dd), and per item its stem, key
reason and distractor reasons. A subject named in fewer than --min lines is left out.
"""
import html as H
import os
import re
import sys

BLOCK = re.compile(r'<(p|li|tr|h4|h5|h6|figcaption|dd|summary)\b[^>]*>(.*?)</\1>', re.S | re.I)


def text(h):
    h = re.sub(r'<button[^>]*>.*?</button>', ' ', h, flags=re.S)
    return re.sub(r'\s+', ' ', H.unescape(re.sub(r'<[^>]+>', ' ', h))).strip()


def norm(s):
    s = re.sub(r'\([^)]*\)', ' ', s)
    return re.sub(r'\s+', ' ', s).strip(' .:;,').lower()


def split(brief_html):
    m = re.search(r'<(?:h5 class="[^"]*authored-hdr|ol class="bank)', brief_html)
    return (brief_html[:m.start()], brief_html[m.start():]) if m else (brief_html, '')


def items(bank_html):
    out = []
    for m in re.finditer(r'<li data-type=[^>]*>.*?</li>', bank_html, re.S):
        li = m.group(0)
        tag = li[:li.index('>') + 1]
        a = dict(re.findall(r'(data-[a-z0-9-]+)="([^"]*)"', tag))
        k = re.search(r'<b>(.*?)</b>', li, re.S)
        out.append({'id': a.get('data-item-id', '?')[:14], 'key': text(k.group(1)) if k else '',
                    'd': [H.unescape(a.get('data-d1', '')), H.unescape(a.get('data-d2', ''))],
                    'stem': text(li[len(tag):]), 'why': [H.unescape(a.get(x, '')) for x in
                                                         ('data-key-why', 'data-d1-why', 'data-d2-why')]})
    return out


def sheet(brief_html, minimum=2):
    body, bank = split(brief_html)
    subj = set()
    for tr in re.finditer(r'<tr\b[^>]*>(.*?)</tr>', body, re.S | re.I):
        c = re.search(r'<t[dh]\b[^>]*>(.*?)</t[dh]>', tr.group(1), re.S | re.I)
        if c:
            s = norm(text(c.group(1)))
            if 2 < len(s) <= 60 and len(s.split()) <= 6:
                subj.add(s)
    if 'data-entry="card"' in brief_html[:600]:
        # s159 card mode: danger rows, timed windows and the drugs are subjects too (serotonin syndrome, washouts)
        for pat in (r'<span class="sp-src">(.*?)</span>', r'<b class="nm[^"]*">(.*?)</b>', r'<p><b>([^<]{3,40})</b>'):
            for m in re.finditer(pat, body, re.S):
                s = norm(text(m.group(1)))
                if 2 < len(s) <= 60 and len(s.split()) <= 6:
                    subj.add(s)
    its = items(bank)
    for it in its:
        for s in [it['key']] + it['d']:
            s = norm(s)
            if 2 < len(s) <= 60:
                subj.add(s)
    lines = [('body', text(m.group(2))) for m in BLOCK.finditer(body)]
    for it in its:
        lines.append(('item %s stem' % it['id'], it['stem']))
        for lab, w in zip(('key why', 'd1 why', 'd2 why'), it['why']):
            if w:
                lines.append(('item %s %s' % (it['id'], lab), w))
    groups = {}
    for s in sorted(subj):
        pat = re.compile(r'(?<![a-z])%s(?:e?s)?(?![a-z])' % re.escape(s), re.I)
        hit = [(w, t) for w, t in lines if t and pat.search(t)]
        if len(hit) >= minimum:
            groups[s] = hit
    return groups


def main(argv):
    if not argv:
        sys.exit(__doc__.strip().splitlines()[-1].strip())
    folder = argv[0]
    minimum = int(argv[argv.index('--min') + 1]) if '--min' in argv else 2
    g = sheet(open(os.path.join(folder, 'brief.html'), encoding='utf-8').read(), minimum)
    out = os.path.join(folder, 'mentions.md')
    with open(out, 'w', encoding='utf-8') as fh:
        fh.write('# Mentions sheet (tools/spine/mentions.py): confirm each group agrees on site, side, timing, age, '
                 'maneuver and next step\n')
        for s, hit in g.items():
            fh.write('\n## %s (%d)\n' % (s, len(hit)))
            for w, t in hit:
                fh.write('- [%s] %s\n' % (w, t[:400]))
    print('mentions: %d subject(s), %d line(s) -> %s' % (len(g), sum(len(v) for v in g.values()), out))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
