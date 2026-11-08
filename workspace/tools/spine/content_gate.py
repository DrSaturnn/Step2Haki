#!/usr/bin/env python3
"""content_gate.py (s170 T6, CONTENT_BATCHES_S170 T6): structural content checks the content batches (s170 to s180)
ship under. Read-only helpers; tools/gate.py check_lints calls check() for three gate checks:

  nbme-block    a brief's count of NBME blocks outside the bank and outside pause points cannot rise against the base;
                a brief whose text changed has none, unless the block's hash is listed in repair/*/nbme_keep.json
  step2-workup  a brief whose text changed has no workup ladder (figure.w5a or div.w5t) inside step 2 (criteria)
  step-moves    a top-level block whose text sits in step X on the base and in step Y on the page needs a row in
                repair/*/step_moves.json

  python3 tools/spine/content_gate.py PAGE.html [--base BASE.html]   prints each brief's blocks, step 2 ladders and moves

nbme_keep.json:   [{"brief": "mdd", "hash": "0123456789", "reason": "..."}]
step_moves.json:  [{"brief": "mdd", "hash": "0123456789", "from": 6, "to": 2, "class": "criteria", "reason": "..."}]
Hashes are h8() of the block's whitespace-normalized text (the same hash content_audit.py writes in nbme_blocks.csv).
"""
import glob
import hashlib
import json
import os
import re
import sys

from bs4 import BeautifulSoup

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(HERE)
WS = os.path.dirname(TOOLS)
for p in (TOOLS, HERE):
    if p not in sys.path:
        sys.path.insert(0, p)
from pagelib import briefs, read_page  # noqa: E402

STEP_HEAD = re.compile(r'<h5 class="tsec sp-h" id="[^"]*"><b class="sp-n">(\d)</b>([^<]*)</h5>')
MIN_MOVE_WORDS = 4   # blocks shorter than this (a lone label, an empty wrapper) are not tracked as moves


def norm(t):
    return re.sub(r'\s+', ' ', t or '').strip()


def h8(t):
    return hashlib.sha1(norm(t).encode()).hexdigest()[:10]


def step_regions(inner):
    """{step number: (step name, html of that step)} for spine briefs; the bank (authored-hdr) ends the last step."""
    heads = list(STEP_HEAD.finditer(inner))
    end_bank = inner.find('class="authored-hdr"')
    out = {}
    for i, m in enumerate(heads):
        stop = heads[i + 1].start() if i + 1 < len(heads) else (end_bank if end_bank > m.end() else len(inner))
        out[int(m.group(1))] = (m.group(2).strip(), inner[m.end():stop])
    return out


def _soup(html):
    s = BeautifulSoup(html, 'lxml')
    return s.body or s


def nbme_blocks(inner):
    """NBME blocks outside the question bank and outside pause points (div.sp-pause, .pp-b), outermost only:
    [{kind, label, data_nbme, hash, words, text}] (content_audit.py section 6 detector)."""
    soup = _soup(inner)
    for bank in soup.select('ol.bank'):
        bank.decompose()
    out, seen = [], set()
    for el in soup.find_all(True):
        cl = el.get('class') or []
        lab = el.find('span', class_=['lbl', 'sp-ct', 'ex'], recursive=False)
        labt = norm(lab.get_text(' ')) if lab else ''
        is_nb = ('nbq' in cl or 'pc-nbq' in cl or 'pc-nbi' in cl
                 or (el.name == 'div' and el.get('data-nbme') is not None)
                 or (el.name == 'div' and 'NBME' in labt))
        if not is_nb or any(id(p) in seen for p in el.parents):
            continue
        seen.add(id(el))
        if el.find_parent('div', class_='sp-pause') or 'pp-b' in cl or el.find_parent(class_='pp-b'):
            continue
        t = norm(el.get_text(' '))
        out.append({'kind': el.name + '.' + '.'.join(cl), 'label': labt[:40], 'data_nbme': el.get('data-nbme', ''),
                    'hash': h8(t), 'words': len(t.split()), 'text': t[:160]})
    return out


def workup_in_step2(inner):
    """Workup ladders (figure.w5a, div.w5t) inside step 2: [text of each, first 120 chars]; outermost only."""
    st = step_regions(inner)
    if 2 not in st:
        return []
    soup = _soup(st[2][1])
    out, seen = [], set()
    for el in soup.find_all(True):
        cl = el.get('class') or []
        if ('w5a' in cl or 'w5t' in cl) and not any(id(p) in seen for p in el.parents):
            seen.add(id(el))
            out.append(norm(el.get_text(' '))[:120])
    return out


def top_blocks(region_html):
    """[(hash, text)] of the top-level elements of one step region, skipping blocks under MIN_MOVE_WORDS words."""
    soup = _soup(region_html)
    out = []
    for c in soup.children:
        if not getattr(c, 'name', None):
            continue
        t = norm(c.get_text(' '))
        if len(t.split()) >= MIN_MOVE_WORDS:
            out.append((h8(t), t))
    return out


def moves(ref_inner, inner):
    """Top-level blocks whose text sits in a step on the page that held no copy of it on the base:
    [{hash, from: [steps on base], to: [new steps on page], text}]. A block new to the brief is not a move."""
    def where(html):
        d = {}
        for n, (_, reg) in step_regions(html).items():
            for hsh, t in top_blocks(reg):
                d.setdefault(hsh, [set(), t])[0].add(n)
        return d
    was, now = where(ref_inner), where(inner)
    out = []
    for hsh, (steps, t) in now.items():
        if hsh not in was:
            continue
        new = steps - was[hsh][0]
        if new:
            out.append({'hash': hsh, 'from': sorted(was[hsh][0]), 'to': sorted(new), 'text': t[:120]})
    return out


def load_rows(name, root=None):
    """Rows from every repair/*/<name> (nbme_keep.json, step_moves.json) under workspace/."""
    rows = []
    for p in sorted(glob.glob(os.path.join(root or WS, 'repair', '*', name))):
        try:
            data = json.load(open(p, encoding='utf-8'))
        except ValueError as e:
            raise ValueError('%s: %s' % (os.path.relpath(p, root or WS), e))
        for r in data if isinstance(data, list) else data.get('rows', []):
            r = dict(r)
            r['_file'] = os.path.relpath(p, root or WS)
            rows.append(r)
    return rows


def check(ref_html, page_html, changed_ids, root=None):
    """[(code, key, message)] for the three gate checks. changed_ids: ids of briefs whose text changed (prose_lint)."""
    fails = []
    keep = {(r.get('brief'), r.get('hash')) for r in load_rows('nbme_keep.json', root)}
    mv_rows = {(r.get('brief'), r.get('hash')): r for r in load_rows('step_moves.json', root)}
    ref = {}
    if ref_html is not None:
        for b in briefs(ref_html):
            ref[b.id] = ref.get(b.id, '') + b.inner
    cur = {}
    for b in briefs(page_html):
        cur[b.id] = cur.get(b.id, '') + b.inner
    for bid, inner in cur.items():
        nb = nbme_blocks(inner)
        if bid in ref:
            was = len(nbme_blocks(ref[bid]))
            if len(nb) > was:
                fails.append(('nbme-block', bid + ' count', '%s: %d NBME blocks outside pause points (base %d)' % (bid, len(nb), was)))
        if bid in changed_ids:
            for blk in nb:
                if (bid, blk['hash']) not in keep:
                    fails.append(('nbme-block', '%s %s' % (bid, blk['hash']),
                                  '%s changed and keeps an NBME block outside a pause point (%s, hash %s): "%s"'
                                  % (bid, blk['kind'], blk['hash'], blk['text'][:60])))
            for t in workup_in_step2(inner):
                fails.append(('step2-workup', '%s %s' % (bid, h8(t)),
                              '%s changed and holds a workup ladder in step 2: "%s"' % (bid, t[:60])))
        if bid in ref:
            for m in moves(ref[bid], inner):
                row = mv_rows.get((bid, m['hash']))
                if row is None:
                    fails.append(('step-moves', '%s %s' % (bid, m['hash']),
                                  '%s: block moved from step %s to step %s with no step_moves.json row (hash %s): "%s"'
                                  % (bid, '/'.join(map(str, m['from'])), '/'.join(map(str, m['to'])), m['hash'], m['text'][:60])))
                elif not all(row.get(k) not in (None, '') for k in ('from', 'to', 'class', 'reason')):
                    fails.append(('step-moves', '%s %s' % (bid, m['hash']),
                                  '%s: step_moves.json row for hash %s lacks from, to, class or reason (%s)' % (bid, m['hash'], row['_file'])))
    return fails


def main(argv):
    page = read_page(argv[0])
    base = read_page(argv[argv.index('--base') + 1]) if '--base' in argv else None
    ref = {b.id: b.inner for b in briefs(base)} if base else {}
    for b in briefs(page):
        nb, w2 = nbme_blocks(b.inner), workup_in_step2(b.inner)
        mv = moves(ref[b.id], b.inner) if b.id in ref else []
        if nb or w2 or mv:
            print('%s: nbme %d, step2 ladders %d, moves %d' % (b.id, len(nb), len(w2), len(mv)))
            for x in nb:
                print('   nbme %s %s "%s"' % (x['hash'], x['kind'], x['text'][:70]))
            for x in w2:
                print('   step2 "%s"' % x[:70])
            for x in mv:
                print('   move %s %s->%s "%s"' % (x['hash'], x['from'], x['to'], x['text'][:70]))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
