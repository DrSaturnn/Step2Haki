#!/usr/bin/env python3
"""basepage (s148e): the page a spine brief folder is built and checked against.

A brief that is new in its batch has no place on the working page yet. Its folder then holds one shell edit,
05_<id>_new.json: a single new_brief op whose brief is the plain shell (title, subtitle, Practice header, bank,
Pairs with, rule), carrying no data-spine="2". The batch applies the shell first (repair/sNN/05_<id>_new.json) and the
spine build second (10_<id>_spine.json, replace_brief), so the READY gate (tools/hooks/ready_gate.py) still covers the
spine body. The shell copy in the folder is what lets verify, the card checklist, the review packet and spinelib build
and check the new brief exactly as they do a shipped one.

  base_page(folder)            the working page (index.html) with every pending shell applied: the folder's own, and
                               any other brief folder's shell whose brief is not on the working page yet (the batch's
                               other new briefs, so drawers between new briefs resolve); after the ship the briefs are
                               on the page and their shells are skipped; unchanged when nothing is pending
  base_page_path(folder, tmp)  the same page written to <tmp>/base.html (the working page path when there is no shell)
  shells(folder)               the folder's 05_*_new.json files
  check_shell(spec)            errors for a shell spec: one new_brief op, no data-spine="2" in its html

s159 (psych pharm cards) adds two pending kinds around the shells, both skipped once the page has them:
  site layer   repair/<open wave>/0[0-4]_*.json with a top-level "marker" string (eg 'id="psych-pharm"') not yet on the
               working page, applied before the shells (a new page section the shells anchor to)
  retirements  any migration folder's 06_*_retire.json (one retire_brief op) whose brief is still on the page, applied
               after every shell (the shells carry the retired brief's items, ids unchanged)
"""
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(WS, 'tools'))
import pagelib as P  # noqa: E402

PAGE = os.path.join(WS, 'index.html')


def shells(folder):
    return sorted(glob.glob(os.path.join(folder, '05_*_new.json'))) if folder else []


def _new_id(spec):
    import re
    m = re.search(r'id="([^"]+)"', (spec.get('edits') or [{}])[0].get('html') or '')
    return m.group(1) if m else None


def pending(folder=None, page=None):
    """shell files to apply: the folder's own plus every migration folder's shell whose brief is not on the page"""
    page = P.read_page(PAGE) if page is None else page
    on = {b.id for b in P.briefs(page)}
    found = glob.glob(os.path.join(WS, 'repair', 'migration', '**', 'spine', '05_*_new.json'), recursive=True)
    out, seen = [], set()
    for f in shells(folder) + sorted(found):
        try:
            bid = _new_id(json.load(open(f, encoding='utf-8')))
        except (OSError, ValueError):
            continue
        # an id already on the page in any form (a retired brief's alias span, s159) is not a pending shell
        if bid and bid not in on and bid not in seen and ('id="%s"' % bid) not in page:
            seen.add(bid)
            out.append(f)
    return out


def _wave():
    w = os.environ.get('AX_BATCH')
    if w:
        return w
    try:
        d = json.load(open(os.path.join(WS, 'repair', 'efficiency', 'WAVE.json'), encoding='utf-8'))
        return d['id'] if d.get('open') else None
    except (OSError, ValueError, KeyError):
        return None


def site_pre(page):
    w = _wave()
    out = []
    for f in sorted(glob.glob(os.path.join(WS, 'repair', w, '0[0-4]_*.json'))) if w else []:
        try:
            m = json.load(open(f, encoding='utf-8')).get('marker')
        except (OSError, ValueError):
            continue
        if m and m not in page:
            out.append(f)
    return out


def retirements(page):
    on = {b.id for b in P.briefs(page)}
    out = []
    for f in sorted(glob.glob(os.path.join(WS, 'repair', 'migration', '**', 'spine', '06_*_retire.json'), recursive=True)):
        try:
            e = json.load(open(f, encoding='utf-8'))['edits'][0]
        except (OSError, ValueError, KeyError, IndexError):
            continue
        if e.get('op') == 'retire_brief' and e.get('brief') in on and f not in out:
            out.append(f)
    return out


def check_shell(spec):
    errs = []
    eds = spec.get('edits', [])
    if len(eds) != 1 or eds[0].get('op') != 'new_brief':
        errs.append('a shell file holds exactly one new_brief op')
    for e in eds:
        if 'data-spine="2"' in (e.get('html') or ''):
            errs.append('a shell carries no data-spine="2": the spine body arrives by replace_brief, under the READY gate')
    return errs


def base_page(folder=None, page_path=PAGE):
    page = P.read_page(page_path)
    pre = site_pre(page)
    sh = pending(folder, page)
    ret = retirements(page)
    if not (pre or sh or ret):
        return page
    import apply_edits
    for f in pre:
        page, _ = apply_edits.apply(page, json.load(open(f, encoding='utf-8')))
    for f in sh:
        spec = json.load(open(f, encoding='utf-8'))
        errs = check_shell(spec)
        if errs:
            raise ValueError('%s: %s' % (os.path.basename(f), '; '.join(errs)))
        page, _ = apply_edits.apply(page, spec)
    for f in ret:
        page, _ = apply_edits.apply(page, json.load(open(f, encoding='utf-8')))
    return page


def base_page_path(folder, tmp):
    page = P.read_page(PAGE)
    if not (pending(folder, page) or site_pre(page) or retirements(page)):
        return PAGE
    os.makedirs(tmp, exist_ok=True)
    p = os.path.join(tmp, 'base.html')
    P.write_page(p, base_page(folder))
    return p


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit('usage: basepage.py <brief folder> <out.html>')
    P.write_page(sys.argv[2], base_page(os.path.abspath(sys.argv[1])))
    print('base page written: %s (%d shell edit file(s))' % (sys.argv[2], len(shells(os.path.abspath(sys.argv[1])))))
