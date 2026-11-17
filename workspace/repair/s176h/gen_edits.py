#!/usr/bin/env python3
"""Writes repair/s176h/10_page.json, the page text edits of the batch, from workspace/index.html, and proves that the
edits give the same page as the direct regex edits of the approved pilot (pilot r4, page_edits.py).

  python3 repair/s176h/gen_edits.py            (run from workspace/)

Edits: the method guide card and the "How to Use This" header and note leave the page; every trap species pill leaves
its trap line, and a traps row holding only pills leaves whole (waiver W-20261116-1); the species count leaves the page
header; the NBME card gets its new title and note.
"""
import json
import os
import re
import sys

WS = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.insert(0, os.path.join(WS, 'tools'))
from pagelib import briefs, read_page  # noqa: E402
import apply_edits  # noqa: E402

PAGE = os.path.join(WS, 'index.html')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '10_page.json')
PILL = r'<span class="pill p-[a-z]+">[^<]*</span>'
ROW = r'<div class="traps">(?:' + PILL + r'\s*)+</div>\n?'

GUIDE = ('<details class="fmdrop">\n<summary><span class="t">Method guide', '</details>\n')
STRATEGY = ('<h3 class="system" id="strategy">How to Use This</h3>\n<p class="system-note">The clinical content is '
            'downstream of the method. Read this section once, then let the briefs reinforce it.</p>\n')
COUNT = '      <span><b>10</b> named trap species</span>\n'
TITLE = ('<summary><span class="t">NBME blueprint: coverage by system and how questions are worded</span>',
         '<summary><span class="t">NBME questions: physician tasks, wording, presentations</span>')
NOTE = ('<p class="bpnote">Counts and ranges follow the shelf you are viewing: each clerkship shows its own NBME subject '
        'exam outline, and Step 2 shows the USMLE Step 2 CK outline. A low NBME count means not yet seen on a form you '
        'have logged, not untested.</p>',
        '<p class="bpnote">Ranges follow the shelf in view. Clerkship shelf: its NBME subject exam outline. Step 2: the '
        'USMLE Step 2 CK outline.</p>')


def expected(s):
    """the pilot's direct edits (page_edits.py, pilot r3 and r4)"""
    a = s.index(GUIDE[0]); b = s.index(GUIDE[1], a) + len(GUIDE[1]); s = s[:a] + s[b:]
    s = s.replace(STRATEGY, '')
    s, n1 = re.subn(r'(<div class="trapline">)' + PILL, r'\1', s)
    s, n2 = re.subn(ROW, '', s)
    s = s.replace(COUNT, '').replace(*TITLE).replace(*NOTE)
    return s, n1, n2


def unique(inner, at, end):
    """the shortest find string starting at `at` that covers inner[at:end] and occurs once in the brief"""
    stop = end
    while inner.count(inner[at:stop]) != 1:
        stop += 1
        if stop > len(inner):
            raise SystemExit('gen_edits: no unique anchor at offset %d' % at)
    return inner[at:stop], inner[end:stop]


def main():
    s = read_page(PAGE)
    for snip in (GUIDE[0], STRATEGY, COUNT, TITLE[0], NOTE[0]):
        assert s.count(snip) == 1, snip[:60]
    a = s.index(GUIDE[0]); guide = s[a:s.index(GUIDE[1], a) + len(GUIDE[1])]
    ops = [{'op': 'replace_global', 'find': guide, 'with': '', 'note': 'the method guide card leaves the page'},
           {'op': 'replace_global', 'find': STRATEGY, 'with': '', 'note': 'the "How to Use This" header and note leave the page'},
           {'op': 'replace_global', 'find': COUNT, 'with': '', 'note': 'the species count leaves the page header'},
           {'op': 'replace_global', 'find': TITLE[0], 'with': TITLE[1], 'note': 'NBME card title'},
           {'op': 'replace_global', 'find': NOTE[0], 'with': NOTE[1], 'note': 'NBME card note'}]
    n_line = n_row = 0
    touched = []
    for b in briefs(s):
        inner = b.inner
        cuts = [(m.start(), m.end()) for m in re.finditer(ROW, inner)]
        cuts += [(m.start(1), m.end(1)) for m in re.finditer(r'<div class="trapline">(' + PILL + ')', inner)]
        if not cuts:
            continue
        touched.append(b.id)
        work = inner
        for st, en in sorted(cuts, reverse=True):   # last first, so earlier offsets hold; each op sees the result so far
            find, tail = unique(work, st, en)
            row = work[st:en].startswith('<div class="traps">')
            ops.append({'op': 'replace', 'brief': b.id, 'find': find, 'with': tail,
                        'note': 'W-20261116-1: ' + ('a traps row of labels only leaves' if row else 'trap species label leaves the trap line')})
            work = work[:st] + work[en:]
            n_row += row; n_line += not row
    spec = {'_doc': 's176h page text edits, written by repair/s176h/gen_edits.py; waiver W-20261116-1 covers the brief edits',
            'edits': ops}
    want, n1, n2 = expected(s)
    print('gen_edits: %d ops; trap line labels %d (direct %d), label-only rows %d (direct %d), briefs %d'
          % (len(ops), n_line, n1, n_row, n2, len(touched)))
    assert (n_line, n_row) == (n1, n2)
    json.dump(spec, open(OUT, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    open(OUT, 'a').write('\n')
    return want


if __name__ == '__main__':
    want = main()
    tmp = os.path.join(WS, 'local', 's176h'); os.makedirs(tmp, exist_ok=True)
    open(os.path.join(tmp, 'expected_page.html'), 'w', encoding='utf-8').write(want)
