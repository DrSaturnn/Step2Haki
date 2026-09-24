#!/usr/bin/env python3
"""gate.py: mechanical invariants of the AxBx page (study-page-builder + board-brief contract).

Usage
  python3 tools/gate.py [page] [--base REF|FILE] [--attr-only REF|FILE] [--allow FILE] [--list]
    page         default: <repo>/index.html
    --base       comparison for never-delete / id-immutability / version-bump checks (default HEAD;
                 'none' skips). A git ref resolves to REF:index.html; an existing path is read as a file.
    --attr-only  additionally assert that only attributes changed vs REF (text and tag structure identical,
                 identity/option attributes untouched). Implies --base REF unless --base is given.
    --allow      allowlist of pre-existing findings (default tools/gate_allowlist.txt)
    --list       print the check catalogue and exit
Prints one summary line, then each failure with its fix. Exit 0 pass, 1 fail.
Judgment (clinical truth, scope, voice, cue review) is never approved by this script.
"""
import csv
import html as H
import json
import os
import re
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pagelib import (ITEM_ATTRS, OID_RE, QID_RE, STATUSES, TYPES, attrs, briefs, items,  # noqa: E402
                     read_page, text)

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHELVES = {'fm', 'peds'}
PROTECTED_ATTR_ONLY = {'id', 'data-item-id', 'data-item-version', 'data-key-id', 'data-d1-id', 'data-d2-id',
                       'data-d1', 'data-d2', 'data-label-answer', 'data-label-d1', 'data-label-d2', 'class'}
VERDICT_OK_MASK = re.compile(r'^(last|none|\d+)$')

CATALOG = {
    'brief-id': ('every .brief has a unique, lowercase [a-z0-9-] id; bs briefs start bs-, aq briefs aq-',
                 'restore the original id (ids are permanent: review progress is keyed on them); new ids: short, lowercase, grep first'),
    'brief-shelf': ('every brief has data-shelf with tokens from fm/peds', 'add data-shelf="fm", "peds" or "fm peds"'),
    'brief-bp': ('every brief has data-bp; every token is an NBME code from the page OUT.codes map',
                 'add data-bp="<primary> [secondary]" using codes from the NBME script (gen immune heme ...)'),
    'brief-h4': ('every brief has exactly one <h4> title', 'add a short <h4> topic name as the first child'),
    'dup-id': ('element ids are unique in the static page', 'rename the NEW element id; never rename an existing brief id'),
    'nav-link': ('every brief has exactly one #navlinks link, class bs (Part II), aq (Aquifer source) or none (topic)',
                 'add/fix <a href="#id"> under the right .sect group; Part II class="bs", Aquifer-source class="aq"'),
    'nav-count': ('each .sect .count equals its number of topic (unclassed) links', 'update the hand-maintained <span class="count">'),
    'item-attrs': ('every bank <li> carries ' + ' '.join(ITEM_ATTRS), 'add the missing attributes; new ids from tools/idgen.py'),
    'item-ids': ('data-item-id is q_+20hex, option ids o_+20hex, all unique page-wide',
                 'use tools/idgen.py; never reuse or edit an existing id'),
    'item-values': ('data-type in the enum, data-item-status in ready/needs_source/needs_repair, version a positive integer',
                    'fix the attribute value'),
    'item-typed-no-id': ('every <li data-type> has a data-item-id', 'assign ids with tools/idgen.py (prose notes carry no data-type)'),
    'item-outside-bank': ('every identified item sits inside an ol.bank of a .brief', 'move it into the owning brief\'s ol.bank'),
    'item-chain': ('every item has a direct-child arrow, non-empty stem and keyed segment 2',
                   'write "stem → answer [→ companion]" with the arrows outside nested tags'),
    'item-options': ('key, data-d1, data-d2 (or data-label-*) are non-empty and distinct', 'author two distinct same-task distractors'),
    'item-leadin': ('data-lead-in, when present, is non-empty', 'remove the empty attribute or write the exact lead-in'),
    'table-title': ('every brief table has exactly one title: <caption> first child XOR <h5> immediately above',
                    'keep one: a caption as first child, or an h5 directly above'),
    'table-mask': ('no data-mask on a Tier table; data-mask values are last|none|N; no rowspan/colspan in brief tables',
                   'remove data-mask from Tier tables; group rows with <tbody>, never rowspan'),
    'bs-vignette': ('every Part II brief has a .vignette before its .dp with a <b>Q</b> line',
                    'add the paraphrased source vignette (Pt · Labs · Imaging · Q) between p.sub and .dp'),
    'no-letters-pct': ('no option letters or vendor selection percentages in .vignette Q lines or .trapline',
                       'drop "(A)", "choice C", "22% chose"; keep labeled clinical probabilities only'),
    'anchor': ('every static href="#x" and .scaleref data-scale resolves to an id', 'point it at an existing id'),
    'pairs-with': ('each <b> in a "Pairs with" block matches a brief <h4> (quoted/question discriminators exempt)',
                   'use the exact partner <h4> text in <b>, or <i> for a partner that does not exist yet'),
    'vendor-image': ('no <img>/<image>/<picture>/<object>/<embed> and no raster data: URI (figures are redrawn inline SVG)',
                     'redraw as inline svg.axfig, a table or a decision spine'),
    'residue': ('no raw markdown (**), escaped tag markup (&lt;b&gt;), bare pills, or emoji in briefs',
                'convert markdown to <b>, unescape allowlisted tags, map bare pills to a named species, remove emoji'),
    'trap-count': ('"<b>N</b> named trap species" appears at least twice (static + transform) with one N',
                   'update both copies together'),
    'scripts': ('every executable inline <script> passes node --check; JSON blocks skipped', 'fix the syntax error'),
    'div-balance': ('static body has equal <div> opens and closes', 'close the div the edit opened (or remove the extra </div>)'),
    'nbme-coverage': ('every data-nbme id has a row in repair/nbme/coverage.csv and every coverage row id is on the page',
                      'add the coverage row (nbme-intake step 5), or the data-nbme link'),
    'never-delete': ('no brief id or item id present at base is missing now', 'restore it; questions and briefs are never deleted'),
    'id-immutable': ('an item keeps its data-key-id/d1-id/d2-id and its owning brief id', 'restore the original ids'),
    'version-bump': ('data-item-version never decreases and increases when the key or a distractor label changed vs base',
                     'increment data-item-version by 1 on the edited item'),
    'attr-only': ('(--attr-only) text and tag structure identical to REF; identity/option attributes untouched',
                  'revert the non-attribute change, or ship it as a content edit without --attr-only'),
}


class Gate:
    def __init__(self, allow):
        self.fails, self.allowed, self.allow = [], [], allow
        self.used = set()

    def fail(self, code, key, msg):
        k = '%s %s' % (code, key)
        if k in self.allow:
            self.allowed.append(k)
            self.used.add(k)
        else:
            self.fails.append((code, key, msg))


def load_allow(path):
    out = {}
    if path and os.path.exists(path):
        for line in open(path, encoding='utf-8'):
            body = line.split('#', 1)[0].strip()
            if body:
                parts = body.split(None, 1)
                out['%s %s' % (parts[0], parts[1].strip() if len(parts) > 1 else '')] = line.strip()
    return out


def load_ref(ref):
    if ref is None or ref == 'none':
        return None
    if os.path.isfile(ref):
        return read_page(ref)
    r = subprocess.run(['git', '-C', REPO, 'show', '%s:index.html' % ref], capture_output=True)
    if r.returncode != 0:
        raise SystemExit('gate: cannot read base %r: %s' % (ref, r.stderr.decode().strip()))
    return r.stdout.decode('utf-8')


def norm(s):
    return re.sub(r'\s+', ' ', H.unescape(s or '')).strip()


def nkey(s):
    return re.sub(r'[^a-z0-9 ]', '', norm(s).lower())


def bp_codes(page):
    m = re.search(r'var OUT=(\{.*?\});\n', page)
    if not m:
        return None
    try:
        return set(json.loads(m.group(1))['codes'])
    except Exception:
        return None


def labels(it):
    a = it.attrs
    return (norm(a.get('data-label-answer') or it.key).lower(),
            norm(a.get('data-label-d1') or a.get('data-d1')).lower(),
            norm(a.get('data-label-d2') or a.get('data-d2')).lower())


def check_page(page, g, page_path):
    body_end = page.find('<script')
    body = page[:body_end if body_end >= 0 else len(page)]
    bl = briefs(page)
    it = items(page)
    stats = {'briefs': len(bl), 'items': len(it)}

    # ---- briefs
    idc = Counter(b.id for b in bl)
    seen_dup = set()
    codes = bp_codes(page)
    if codes is None:
        g.fail('brief-bp', 'OUT', 'cannot read the NBME OUT.codes map from the page script')
        codes = set()
    for b in bl:
        if not b.id:
            g.fail('brief-id', 'offset%d' % b.start, 'brief at offset %d has no id' % b.start)
            continue
        if idc[b.id] > 1:
            if b.id in seen_dup:
                continue
            seen_dup.add(b.id)
            g.fail('brief-id', b.id, 'brief id %s occurs %d times' % (b.id, idc[b.id]))
        if not re.match(r'^[a-z0-9][a-z0-9-]*$', b.id):
            g.fail('brief-id', b.id, 'brief id %r is not lowercase [a-z0-9-]' % b.id)
        if b.kind == 'bs' and not b.id.startswith('bs-'):
            g.fail('brief-id', b.id, 'Part II brief %s lacks the bs- prefix' % b.id)
        if b.kind == 'aq' and not b.id.startswith('aq-'):
            g.fail('brief-id', b.id, 'Aquifer brief %s lacks the aq- prefix' % b.id)
        sh = b.attrs.get('data-shelf')
        if sh is None or not sh.split() or not set(sh.split()) <= SHELVES:
            g.fail('brief-shelf', b.id, '%s data-shelf=%r' % (b.id, sh))
        bp = b.attrs.get('data-bp')
        if bp is None or not bp.split():
            g.fail('brief-bp', b.id, '%s has no data-bp' % b.id)
        elif codes and not set(bp.split()) <= codes:
            g.fail('brief-bp', b.id, '%s data-bp=%r has unknown code(s) %s' % (b.id, bp, sorted(set(bp.split()) - codes)))
        if len(re.findall(r'<h4\b', b.inner)) != 1:
            g.fail('brief-h4', b.id, '%s has %d <h4>' % (b.id, len(re.findall(r'<h4\b', b.inner))))

    # ---- page-wide ids and anchors
    ids = re.findall(r'\sid="([^"]*)"', body)
    for k, v in Counter(ids).items():
        if v > 1:
            g.fail('dup-id', k, 'id %s occurs %d times' % (k, v))
    idset = set(ids)
    for x in sorted(set(re.findall(r'href="#([^"]+)"', body))):
        if H.unescape(x) not in idset:
            g.fail('anchor', x, 'href="#%s" has no target' % x)
    for x in sorted(set(re.findall(r'data-scale="([^"]+)"', body))):
        if x not in idset:
            g.fail('anchor', 'scale:' + x, 'scaleref data-scale="%s" has no target' % x)

    # ---- nav
    ns = body.find('<div id="navlinks">')
    if ns < 0:
        g.fail('nav-link', 'navlinks', 'no <div id="navlinks">')
    else:
        ne = body.find('</aside>', ns)
        nav = body[ns:ne if ne > 0 else ns + 200000]
        links = defaultdict(list)
        for m in re.finditer(r'<a\b([^>]*)>', nav):
            a = attrs(m.group(0))
            if a.get('href', '').startswith('#'):
                links[a['href'][1:]].append(a.get('class', ''))
        for b in bl:
            want = 'aq' if (b.kind == 'aq' or b.attrs.get('data-src') == 'aquifer') else ('bs' if b.kind == 'bs' else '')
            got = links.get(b.id, [])
            if len(got) != 1:
                g.fail('nav-link', b.id, '%s has %d nav links' % (b.id, len(got)))
            elif got[0] != want:
                g.fail('nav-link', b.id, '%s nav link class=%r, expected %r' % (b.id, got[0], want))
        for sec in re.split(r'<div class="sect">', nav)[1:]:
            m = re.match(r'(.*?)\s*<span class="count">(\d+)</span>', sec, re.S)
            if not m:
                continue
            plain = len([1 for t in re.findall(r'<a\b[^>]*>', sec) if 'class=' not in t])
            if int(m.group(2)) != plain:
                g.fail('nav-count', text(m.group(1)), '.sect "%s" count %s but %d topic links' % (text(m.group(1)), m.group(2), plain))

    # ---- items
    banks = []
    for m in re.finditer(r'<ol\b[^>]*class="bank\b[^"]*"[^>]*>', body):
        banks.append((m.start(), body.find('</ol>', m.end())))
    qc = Counter(i.id for i in it)
    oc = Counter(i.attrs.get(k) for i in it for k in ('data-key-id', 'data-d1-id', 'data-d2-id'))
    for i in it:
        a, iid = i.attrs, i.id or 'offset%d' % i.start
        miss = [k for k in ITEM_ATTRS if k not in a]
        if miss:
            g.fail('item-attrs', iid, '%s (%s) missing %s' % (iid, i.brief_id, ' '.join(miss)))
        if not QID_RE.match(a.get('data-item-id', '')):
            g.fail('item-ids', iid, '%s: malformed data-item-id' % iid)
        elif qc[i.id] > 1:
            g.fail('item-ids', iid, '%s occurs %d times' % (iid, qc[i.id]))
        for k in ('data-key-id', 'data-d1-id', 'data-d2-id'):
            v = a.get(k, '')
            if k in a and not OID_RE.match(v):
                g.fail('item-ids', iid + ':' + k, '%s: malformed %s=%r' % (iid, k, v))
            elif v and oc[v] > 1:
                g.fail('item-ids', iid + ':' + k, '%s: %s %s is not unique' % (iid, k, v))
        if 'data-type' in a and a['data-type'] not in TYPES:
            g.fail('item-values', iid, '%s data-type=%r' % (iid, a['data-type']))
        if 'data-item-status' in a and a['data-item-status'] not in STATUSES:
            g.fail('item-values', iid, '%s data-item-status=%r' % (iid, a['data-item-status']))
        if 'data-item-version' in a and not re.match(r'^[1-9]\d*$', a['data-item-version']):
            g.fail('item-values', iid, '%s data-item-version=%r' % (iid, a['data-item-version']))
        if not i.brief_id or not any(s < i.start < e for s, e in banks):
            g.fail('item-outside-bank', iid, '%s is not inside a .brief ol.bank' % iid)
        if len(i.segments) < 2 or not text(i.segments[0]) or not i.key:
            g.fail('item-chain', iid, '%s (%s): no direct-child "stem → answer" chain' % (iid, i.brief_id))
        else:
            k, d1, d2 = labels(i)
            if not (k and d1 and d2) or len({k, d1, d2}) < 3:
                g.fail('item-options', iid, '%s (%s): key/d1/d2 empty or not distinct: %r / %r / %r' % (iid, i.brief_id, k, d1, d2))
        if 'data-lead-in' in a and not norm(a['data-lead-in']):
            g.fail('item-leadin', iid, '%s has an empty data-lead-in' % iid)
    for m in re.finditer(r'<li\b[^>]*\bdata-type="[^"]*"[^>]*>', body):
        if 'data-item-id=' not in m.group(0):
            g.fail('item-typed-no-id', 'offset%d' % m.start(), 'typed <li> without data-item-id at offset %d: %s' % (m.start(), m.group(0)[:90]))

    # ---- per-brief content rules
    h4map = {nkey(b.title): b.id for b in bl}
    for b in bl:
        inn = b.inner
        for m in re.finditer(r'<table\b[^>]*>', inn):
            cap = inn[m.end():].lstrip().startswith('<caption')
            pre = re.sub(r'<div class="tw[^"]*">\s*$', '', inn[:m.start()].rstrip()).rstrip()
            h5 = pre.endswith('</h5>')
            tno = len(re.findall(r'<table\b', inn[:m.start()])) + 1
            if cap == h5:
                g.fail('table-title', '%s:t%d' % (b.id, tno), '%s table %d has %s' % (b.id, tno, 'both a caption and an h5' if cap else 'no title'))
            tend = inn.find('</table>', m.start())
            t = inn[m.start():tend]
            ta = attrs(m.group(0))
            th = re.search(r'<th\b[^>]*>(.*?)</th>', t, re.S)
            if 'data-mask' in ta:
                if th and text(th.group(1)).lower().startswith('tier'):
                    g.fail('table-mask', '%s:t%d' % (b.id, tno), '%s table %d: data-mask on a Tier table disables its auto-mask' % (b.id, tno))
                if not VERDICT_OK_MASK.match(ta['data-mask']):
                    g.fail('table-mask', '%s:t%d' % (b.id, tno), '%s table %d: data-mask=%r' % (b.id, tno, ta['data-mask']))
            if re.search(r'\b(rowspan|colspan)\s*=', t):
                g.fail('table-mask', '%s:t%d:span' % (b.id, tno), '%s table %d uses rowspan/colspan (breaks column masking)' % (b.id, tno))
        vm = re.search(r'<div class="vignette"[^>]*>(.*?)</div>', inn, re.S)
        if b.kind == 'bs':
            dp = inn.find('<div class="dp"')
            if not vm:
                g.fail('bs-vignette', b.id, 'Part II brief %s has no .vignette' % b.id)
            elif (dp >= 0 and vm.start() > dp) or '<b>Q</b>' not in vm.group(1):
                g.fail('bs-vignette', b.id, 'Part II brief %s: vignette after .dp or without a <b>Q</b> line' % b.id)
        letters = re.compile(r'\(\s*[A-H]\s*\)|(?<![\w/])[A-H]\)\s|\b(?:option|choice|answer)\s+[A-H]\b|'
                             r'\d+(?:\.\d+)?\s*%\s*(?:of\s+(?:users|students|test-?takers|examinees|respondents)|chose|picked|selected|answered)|'
                             r'\((?:\d+(?:\.\d+)?)\s*%\)')
        if vm and '<b>Q</b>' in vm.group(1):
            q = text(vm.group(1).split('<b>Q</b>', 1)[1])
            if letters.search(q):
                g.fail('no-letters-pct', b.id + ':Q', '%s Q line: %r' % (b.id, letters.search(q).group(0)))
        for n, m in enumerate(re.finditer(r'<div class="trapline">(.*?)</div>', inn, re.S)):
            t = text(m.group(1))
            if letters.search(t):
                g.fail('no-letters-pct', '%s:trap%d' % (b.id, n + 1), '%s trapline %d: %r' % (b.id, n + 1, letters.search(t).group(0)))
        for m in re.finditer(r'<div class="pearls"[^>]*>\s*<span class="lbl">Pairs with</span>(.*?)</div>', inn, re.S):
            for bb in re.findall(r'<b>(.*?)</b>', m.group(1), re.S):
                t = text(bb)
                if not t or t[0] in '"\'“‘' or t.endswith('?') or t.endswith('?"') or t.endswith('?”'):
                    continue
                if nkey(t) not in h4map:
                    g.fail('pairs-with', '%s:%s' % (b.id, nkey(t).replace(' ', '_')[:60]), '%s Pairs-with <b>%s</b> matches no <h4>' % (b.id, t))
        if '**' in inn:
            g.fail('residue', b.id + ':md', '%s contains raw markdown **' % b.id)
        if re.search(r'&lt;/?(?:b|i|span|sup|sub|div|p|br|em|strong)\b', inn):
            g.fail('residue', b.id + ':esc', '%s contains escaped tag markup' % b.id)
        if re.search(r'<span class="pill">', inn):
            g.fail('residue', b.id + ':pill', '%s has a bare pill (no p-* species class)' % b.id)
        emo = [c for c in H.unescape(re.sub(r'<[^>]+>', '', inn)) if ord(c) >= 0x1F000 or c == '️']
        if emo:
            g.fail('residue', b.id + ':emoji', '%s contains emoji %r' % (b.id, ''.join(sorted(set(emo)))))

    # ---- images
    for pat, what in ((r'<img\b', '<img>'), (r'<image\b', 'svg <image>'), (r'<picture\b', '<picture>'),
                      (r'<object\b', '<object>'), (r'<embed\b', '<embed>')):
        for m in re.finditer(pat, body, re.I):
            g.fail('vendor-image', 'offset%d' % m.start(), '%s at offset %d' % (what, m.start()))
    for m in re.finditer(r'data:image/(?!svg\+xml)[a-z]+', page, re.I):
        g.fail('vendor-image', 'offset%d' % m.start(), 'raster data URI at offset %d' % m.start())

    # ---- trap species count
    tc = re.findall(r'<b>(\d+)</b> named trap species', page)
    if len(tc) < 2 or len(set(tc)) != 1:
        g.fail('trap-count', '*', '"named trap species" counts %r (need >= 2 copies, one value)' % tc)

    # ---- div balance
    op, cl = len(re.findall(r'<div\b', body)), len(re.findall(r'</div\s*>', body))
    if op != cl:
        g.fail('div-balance', '*', 'static body has %d <div> and %d </div>' % (op, cl))

    # ---- scripts
    ns = 0
    for m in re.finditer(r'<script\b([^>]*)>(.*?)</script>', page, re.S):
        a = attrs('<script' + m.group(1) + '>')
        typ = a.get('type', '').lower()
        if 'src' in a or (typ and typ not in ('text/javascript', 'module', 'application/javascript')):
            continue
        ns += 1
        with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False, encoding='utf-8') as f:
            f.write(m.group(2))
            fn = f.name
        try:
            r = subprocess.run(['node', '--check', fn], capture_output=True, text=True)
        finally:
            os.unlink(fn)
        if r.returncode != 0:
            err = [l for l in r.stderr.splitlines() if l.strip()]
            g.fail('scripts', 's%d' % ns, 'script %d fails node --check: %s' % (ns, ' | '.join(err[1:4])[:200]))
    stats['scripts'] = ns

    # ---- nbme coverage
    cov = os.path.join(os.path.dirname(os.path.abspath(page_path)), 'repair', 'nbme', 'coverage.csv')
    if not os.path.exists(cov):
        cov = os.path.join(REPO, 'repair', 'nbme', 'coverage.csv')
    page_n = set()
    for v in re.findall(r'data-nbme="([^"]*)"', body):
        page_n.update(v.split())
    rows = []
    if os.path.exists(cov):
        rows = list(csv.DictReader(open(cov, encoding='utf-8')))
    cov_n = {r.get('nbme_id', '').strip() for r in rows if r.get('nbme_id', '').strip()}
    for n in sorted(page_n - cov_n):
        g.fail('nbme-coverage', n, 'data-nbme="%s" has no row in repair/nbme/coverage.csv' % n)
    for n in sorted(cov_n - page_n):
        linked = [r for r in rows if r.get('nbme_id') == n and r.get('sort', '').strip() in ('covered', 'new angle', 'conflict', 'new')]
        if linked:
            g.fail('nbme-coverage', n, 'coverage row %s has no data-nbme link on the page' % n)
    fp = Counter(r.get('fingerprint', '') for r in rows if r.get('fingerprint') and not r.get('same_as'))
    for k, v in fp.items():
        if v > 1:
            g.fail('nbme-coverage', 'fp:' + k, 'fingerprint %s repeated without same_as' % k)
    return bl, it, stats


def check_base(page, ref_html, bl, it, g):
    rb, ri = briefs(ref_html), items(ref_html)
    cur_b = {b.id for b in bl}
    for b in rb:
        if b.id and b.id not in cur_b:
            g.fail('never-delete', b.id, 'brief %s existed at base and is missing now' % b.id)
    cur = {i.id: i for i in it}
    for r in ri:
        c = cur.get(r.id)
        if c is None:
            g.fail('never-delete', r.id, 'item %s (%s) existed at base and is missing now' % (r.id, r.brief_id))
            continue
        for k in ('data-key-id', 'data-d1-id', 'data-d2-id'):
            if c.attrs.get(k) != r.attrs.get(k):
                g.fail('id-immutable', r.id + ':' + k, '%s %s changed %s -> %s' % (r.id, k, r.attrs.get(k), c.attrs.get(k)))
        if c.brief_id != r.brief_id:
            g.fail('id-immutable', r.id + ':brief', '%s moved from brief %s to %s' % (r.id, r.brief_id, c.brief_id))
        try:
            rv, cv = int(r.attrs.get('data-item-version', '0')), int(c.attrs.get('data-item-version', '0'))
        except ValueError:
            continue
        if cv < rv:
            g.fail('version-bump', r.id, '%s version decreased %d -> %d' % (r.id, rv, cv))
        elif labels(c) != labels(r) and cv == rv:
            g.fail('version-bump', r.id, '%s (%s) key/distractor label changed but data-item-version is still %d' % (r.id, c.brief_id, cv))


TOKEN = re.compile(r'<!--.*?-->|<[^>]+>|[^<]+', re.S)


def check_attr_only(page, ref_html, g):
    a, b = TOKEN.findall(ref_html), TOKEN.findall(page)
    n_attr = 0
    if len(a) != len(b):
        g.fail('attr-only', 'tokens', 'token count differs from REF (%d vs %d): text or tags were added/removed' % (len(a), len(b)))
        return 0
    for x, y in zip(a, b):
        if x == y:
            continue
        if not (x.startswith('<') and y.startswith('<')) or x.startswith('<!--'):
            g.fail('attr-only', 'text', 'text changed: %r -> %r' % (x[:60], y[:60]))
            continue
        nx, ny = re.match(r'</?\s*([A-Za-z0-9]+)', x), re.match(r'</?\s*([A-Za-z0-9]+)', y)
        if not nx or not ny or nx.group(0) != ny.group(0):
            g.fail('attr-only', 'tag', 'tag changed: %r -> %r' % (x[:60], y[:60]))
            continue
        ax, ay = attrs(x), attrs(y)
        n_attr += 1
        for k in PROTECTED_ATTR_ONLY:
            if ax.get(k) != ay.get(k):
                g.fail('attr-only', '%s:%s' % (ax.get('data-item-id') or ax.get('id') or '?', k),
                       'protected attribute %s changed on %s' % (k, ax.get('data-item-id') or ax.get('id') or x[:40]))
    return n_attr


def main(argv):
    args, page_path, base, attr_ref = list(argv), None, 'HEAD', None
    allow_path = os.path.join(REPO, 'tools', 'gate_allowlist.txt')
    base_given = False
    if '--list' in args:
        for k, (d, fx) in CATALOG.items():
            print('%-18s %s\n%-18s fix: %s' % (k, d, '', fx))
        return 0
    i = 0
    while i < len(args):
        a = args[i]
        if a == '--base':
            base, base_given = args[i + 1], True
            i += 2
        elif a == '--attr-only':
            attr_ref = args[i + 1]
            i += 2
        elif a == '--allow':
            allow_path = args[i + 1]
            i += 2
        else:
            page_path = a
            i += 1
    if attr_ref and not base_given:
        base = attr_ref
    page_path = page_path or os.path.join(REPO, 'index.html')
    page = read_page(page_path)
    g = Gate(load_allow(allow_path))
    bl, it, st = check_page(page, g, page_path)
    ref_html = load_ref(base)
    if ref_html is not None:
        check_base(page, ref_html, bl, it, g)
    n_attr = None
    if attr_ref:
        n_attr = check_attr_only(page, load_ref(attr_ref), g)
    stale = sorted(set(g.allow) - g.used)
    summary = 'gate: %s %d briefs, %d items, %d scripts, %d checks, base %s%s | allowlisted %d%s | %d failure(s)' % (
        'FAIL' if g.fails else 'PASS', st['briefs'], st['items'], st['scripts'], len(CATALOG),
        base if ref_html is not None else 'none',
        (' | attr-only vs %s: %d tag(s) changed' % (attr_ref, n_attr)) if attr_ref else '',
        len(g.allowed), (' (%d stale allowlist line(s): %s)' % (len(stale), '; '.join(stale)[:200])) if stale else '',
        len(g.fails))
    print(summary)
    for code, key, msg in g.fails[:80]:
        print('  [%s] %s\n      fix: %s' % (code, msg, CATALOG[code][1]))
    if len(g.fails) > 80:
        print('  ... %d more' % (len(g.fails) - 80))
    return 1 if g.fails else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
