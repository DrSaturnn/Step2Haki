#!/usr/bin/env python3
"""s163 generator (CRITERIA_STEP2.md Part E; 2026-11-04, D1 and D5: "would the prototype then simply be what
is shipped?"). Built from the prototype claude/pending/criteria_step2/move_criteria.py. Reads the live page and writes
repair/s163/*.json as small brief-scoped edits (never replace_brief, so the READY gate is not involved):

  10_steps.json    E1, E2, E5: every spine rail in the new order (1 Script or Presentation, 2 Criteria, 3 Urgent,
                   4 Differential, 5 Workup, 6 Severity, 7 Treatment, 8 Follow-up), the Criteria block moved to right
                   after step 1, the step discs renumbered, numbered section ids renamed once (B2: -s2 to -s3, -s3 to
                   -s4, -s4 to -s5, -s5 to -s2; named ids such as -dx, -mx, -care stay), an empty Criteria tile greyed
                   (B1: it already is; it now sits second), and the heading glow CSS keyed to the new ids.
  20_wording.json  E3, E4: the hand rewrites of rewrites.txt (numeric step references, ownership and figurative
                   placement wording, D4 and D6), applied after the move; bank items through replace_item_text.

  python3 repair/pilots/criteria-step2/make_batch.py [--page index.html] [--survey]
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(WS, 'tools'))
from pagelib import briefs, read_page  # noqa: E402

NEW = {1: 1, 5: 2, 2: 3, 3: 4, 4: 5, 6: 6, 7: 7, 8: 8}      # old step number -> new
ORDER = [1, 5, 2, 3, 4, 6, 7, 8]                             # old numbers in the new display order
NAV = re.compile(r'<nav class="sp-step"[^>]*>(.*?)</nav>', re.S)
LINK = re.compile(r'<a((?: href="#[^"]+")?[^>]*)><b>(\d)</b><span>([^<]*)</span></a>')
HEAD = re.compile(r'<h5 class="tsec sp-h" id="([^"]+)"><b class="sp-n">(\d)</b>([^<]*)</h5>')


def new_id(i):
    m = re.match(r'^(.*-s)([2-5])$', i)
    return m.group(1) + str(NEW[int(m.group(2))]) if m else i


def balanced(s):
    for t in ('div', 'table', 'ul', 'ol', 'details', 'section', 'p'):
        if len(re.findall(r'<%s\b' % t, s)) != len(re.findall(r'</%s>' % t, s)):
            return t
    return None


def plan_brief(h, b, log):
    """Edits for one brief with a spine rail; returns a list of ops."""
    seg = h[b.start:b.end]
    m = NAV.search(seg)
    if not m:
        return []
    links = {}
    for attrs, n, lab in LINK.findall(m.group(1)):
        href = re.search(r'href="#([^"]+)"', attrs)
        links[int(n)] = (attrs, href.group(1) if href else None, lab)
    if sorted(links) != list(range(1, 9)):
        log['skipped'].append(b.id + ' (rail)')
        return []
    prac = re.search(r'<a [^>]*class="sp-prac"[^>]*>.*?</a>', m.group(1), re.S)
    rail = ''
    for old in ORDER:
        attrs, href, lab = links[old]
        if href:
            attrs = attrs.replace('href="#%s"' % href, 'href="#%s"' % new_id(href))
        rail += '<a%s><b>%d</b><span>%s</span></a>' % (attrs, NEW[old], lab)
    nav_new = m.group(0).replace(m.group(1), rail + (prac.group(0) if prac else ''))
    ops = [{'op': 'replace', 'brief': b.id, 'find': m.group(0), 'with': nav_new,
            'note': 's163 E1: rail in the new step order, ids renamed (B2)'}]
    heads = [(x.start(), x.group(1), int(x.group(2)), x.group(3)) for x in HEAD.finditer(seg)]
    discs = {n: i for _, i, n, _ in heads}
    for n, (attrs, href, lab) in links.items():
        if href and not href.endswith('-bank') and discs.get(n) != href:
            log['skipped'].append('%s (heading %d is %s, rail says %s)' % (b.id, n, discs.get(n), href))
            return []
    # the Criteria block: its heading to the next spine heading (or the bank); moved to right before the first spine
    # heading after step 1's
    crit = links[5][1]
    order = [n for _, _, n, _ in heads]
    if crit:
        cs = seg.find('<h5 class="tsec sp-h" id="%s"' % crit)
        later = [p for p, _, n, _ in heads if p > cs]
        bank = seg.find('<ol class="bank')
        ce = later[0] if later else None
        if ce is None:
            log['skipped'].append(b.id + ' (criteria is the last section)')
            return []
        if bank > 0 and ce > bank:
            log['skipped'].append(b.id + ' (criteria runs into the bank)')
            return []
        block = seg[cs:ce]
        bad = balanced(block)
        if bad:
            log['skipped'].append('%s (criteria block unbalanced <%s>)' % (b.id, bad))
            return []
        if 'pause' in block.lower():
            log['pause_in_criteria'].append(b.id)
        s1 = [p for p, _, n, _ in heads if n == 1][0]
        after1 = [p for p, _, n, _ in heads if p > s1]
        if after1[0] != cs:
            anchor_m = HEAD.match(seg, after1[0])
            ops.append({'op': 'replace', 'brief': b.id, 'find': block, 'with': '',
                        'note': 's163 E1: Criteria block lifted from after Workup'})
            ops.append({'op': 'insert_before', 'brief': b.id, 'anchor': anchor_m.group(0), 'html': block,
                        'note': 's163 E1: Criteria block placed right after step 1 (D1)'})
            log['moved'] += 1
    # headings: renumber the discs and rename the ids
    # the title is in the anchor, so a renamed heading never collides with the one it replaces (ids rotate 5-2-3-4)
    for p, i, n, t in heads:
        if NEW[n] != n or new_id(i) != i:
            old = '<h5 class="tsec sp-h" id="%s"><b class="sp-n">%d</b>%s</h5>' % (i, n, t)
            ops.append({'op': 'replace', 'brief': b.id, 'find': old,
                        'with': '<h5 class="tsec sp-h" id="%s"><b class="sp-n">%d</b>%s</h5>' % (new_id(i), NEW[n], t),
                        'note': 's163 E1/E2: step disc renumbered, id renamed'})
            log['headings'] += 1
    log['ids'] |= {i for _, i, _, _ in heads if new_id(i) != i}
    log['order'][tuple(order)] = log['order'].get(tuple(order), 0) + 1
    return ops


GLOW_OLD = ['.brief.sp h5.sp-h[id$="-s2"]{--glow:rgba(142,90,22,.11)}',
            '.brief.sp h5.sp-h[id$="-s3"],.brief.sp h5.sp-h[id$="-s5"]{--glow:rgba(10,84,97,.10)}',
            '.brief.sp h5.sp-h[id$="-s4"]{--glow:rgba(var(--acc-rgb),.14)}',
            '[data-theme="dark"] .brief.sp h5.sp-h[id$="-s2"]{--glow:rgba(237,195,139,0.11)}',
            '[data-theme="dark"] .brief.sp h5.sp-h[id$="-s3"],[data-theme="dark"] .brief.sp h5.sp-h[id$="-s5"]{--glow:rgba(186,239,248,0.1)}']


def glow_new(s):
    # Urgent was -s2 and is now -s3; Differential -s3 now -s4; Workup -s4 now -s5; Criteria -s5 now -s2
    return re.sub(r'id\$="-s([2-5])"', lambda mm: 'id$="-s%d"' % NEW[int(mm.group(1))], s)


# 30_chrome.json (chunk 4): page text outside the briefs (NBME page, Shelf intros, sidebar notes) and the NBME
# presentations panel script. Changelog entries are history and stay. The panel's step() fallback maps a named -dx id
# to Differential, which is now step 4 (was 3); -mx stays 7.
CHROME = [
    ('the deciding fact lives in the <b>background</b>', 'the deciding fact is in the <b>background</b>'),
    ('and mosquito bites sit in a spotted fever stem', 'and mosquito bites appear in a spotted fever stem'),
    ('<b>The clue sits in a relative.</b>', '<b>The clue is in a relative.</b>'),
    ('Each option sits in one cell of potassium', 'Each option fills one cell of potassium'),
    ('Each entry links to the brief that owns it.', 'Each entry links to the brief that teaches it.'),
    ('board questions that belong to no single organ', 'board questions that fit no single organ'),
    ("var STEPS={1:'Illness script',2:'Urgent risks',3:'Differential',4:'Workup',5:'Diagnostic criteria',",
     "var STEPS={1:'Illness script',2:'Diagnostic criteria',3:'Urgent risks',4:'Differential',5:'Workup',"),
    ("m[2]||(m[1]==='dx'?'3':'7')", "m[2]||(m[1]==='dx'?'4':'7')"),
    ("['frame','Framings']", "['frame','NBME framing']"),
    ("frame:'How NBME framed it',linked:", "frame:'NBME framing',linked:"),
]


# 60_site.json (chunk 8, E6 / plan C4): a Differential row's linked-brief preview (hover on desktop, first tap on a
# phone) adds that brief's diagnostic criteria (its step 2), cloned from the brief when the preview opens, so no copy
# exists to drift. Shown only when the row names the linked brief's diagnosis (title words) or one of its criteria
# blocks (block label words); a row whose drawer opens a broader brief (a VSD row to Congenital Heart Disease) gets
# none. The clone sits in an id-less .brief.sp wrapper, as the drawer's clone does, so the criteria keep their own
# styling and Recall masks; controls inside it become plain text.
PV_CSS = r'''
/* s163 C4: the linked brief's diagnostic criteria in a Differential row's preview */
html body .qx-pv > .brief.sp.qx-pc{display:block;box-sizing:border-box;margin:12px 0 0;padding:10px 0 2px;border:0!important;border-top:1px solid var(--hair)!important;border-radius:0;background:none!important;box-shadow:none!important;zoom:1;isolation:auto;content-visibility:visible;contain-intrinsic-size:none;max-height:min(300px,45vh);overflow:auto;overscroll-behavior:contain;scroll-margin-top:0}
html body .qx-pv > .brief.sp.qx-pc > .qx-pk{margin:0 0 6px}
html body .qx-pv > .brief.sp.qx-pc > :is(.crit,.sp-dx){margin:0;max-width:none}
/* a wide criteria table restacks one row per card in the 340px preview, as the phone page does, so no column hides to the right */
@media (min-width:641px){html body .qx-pv > .brief.sp.qx-pc .tw{overflow:visible;background:none;box-shadow:none;padding:0;margin:0}
html body .qx-pv > .brief.sp.qx-pc .tw :is(table,tbody,tr,td){display:block;width:100%;max-width:100%;box-sizing:border-box}
html body .qx-pv > .brief.sp.qx-pc .tw thead{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
html body .qx-pv > .brief.sp.qx-pc .tw caption{display:block;padding:0 0 6px;text-align:left}
html body .qx-pv > .brief.sp.qx-pc .tw tbody tr{padding:8px 0;border-top:1px solid var(--hair);background:none;box-shadow:none}
html body .qx-pv > .brief.sp.qx-pc .tw tbody td{border:0;padding:2px 0}
html body .qx-pv > .brief.sp.qx-pc .tw tbody td:first-child{font-weight:650;color:var(--ink);padding-bottom:4px}
html body .qx-pv > .brief.sp.qx-pc .tw tbody td:not(:first-child)[data-label]::before{content:attr(data-label);display:block;font:650 11px/15px var(--sans);letter-spacing:.04em;text-transform:uppercase;color:var(--muted)}}'''
PV_JS = r'''  /* s163 C4: in a Differential row, the preview adds the linked brief's diagnostic criteria (its step 2), cloned from
     that brief when the preview opens, so no copy exists to drift. Only when the row names that brief's diagnosis or
     one of its criteria blocks; a row whose drawer opens a broader brief gets none. */
  var PV_STOP = /^(a|an|the|of|in|and|or|with|for|to|on|at|by|vs|child|children|adult|adults|disease|disorder|syndrome|criteria|criterion|defining|diagnostic|diagnosis|classic|test)$/;
  function pvToks(s){
    var o = [];
    norm(s).toLowerCase().replace(/[^a-z0-9]+/g, ' ').split(' ').forEach(function(w){
      if(w.length > 4 && /[^s]s$/.test(w)) w = w.slice(0, -1);
      if(w && !PV_STOP.test(w) && o.indexOf(w) < 0) o.push(w);
    });
    return o;
  }
  function pvIn(a, b){ return a.length > 0 && a.every(function(w){ return b.indexOf(w) >= 0; }); }
  function pvInDx(link){
    var b = link.closest('.brief'), h = null; if(!b) return false;
    Array.prototype.forEach.call(b.querySelectorAll('h5.sp-h'), function(x){ if(x.compareDocumentPosition(link) & 4) h = x; });
    return !!h && /differential/i.test(h.textContent);
  }
  function pvLabel(n){ var l = n.querySelector(':scope > .lbl, caption'); return l ? norm(l.textContent) : ''; }
  function pvCrit(link, t){
    if(!pvInDx(link)) return null;
    var h = t.querySelector('h5.sp-h[id$="-s2"]'); if(!h || !/criteria/i.test(h.textContent)) return null;
    var on = false, bl = [];
    Array.prototype.forEach.call(t.querySelectorAll('h5.tsec, div.crit, div.sp-dx'), function(n){
      if(n.tagName === 'H5') on = n === h; else if(on && !n.parentElement.closest('div.crit, div.sp-dx')) bl.push(n);
    });
    if(!bl.length) return null;
    var c = link.closest('tr'), all = '';
    c = c && c.cells[0];
    if(c){ c = c.cloneNode(true); c.querySelectorAll('.sp-drw').forEach(function(d){ d.remove(); }); all = norm(c.textContent); }
    if(!all) all = norm(link.textContent);
    var core = pvToks(all.replace(/\([^)]*\)/g, ' '));
    all = pvToks(all);
    for(var i = 0; i < bl.length; i++){
      var lab = pvLabel(bl[i]), k = lab.indexOf(':');
      var lc = k < 0 ? [] : pvToks(/^defining/i.test(lab) ? lab.slice(k + 1) : lab.slice(0, k));
      if(pvIn(core, pvToks(lab)) || pvIn(lc, all) || pvIn(pvToks(lab), all)) return bl[i];
    }
    var tt = pvToks((t.querySelector('h4') || {}).textContent || '');
    return pvIn(tt, all) || pvIn(core, tt) ? bl[0] : null;
  }
  function pvTile(n){
    var w = document.createElement('div'); w.className = 'brief sp qx-pc';
    ['study', 'flat'].forEach(function(m){ if(document.body.classList.contains(m)) w.classList.add('axm-' + m); });
    var k = document.createElement('span'); k.className = 'qx-pk'; k.textContent = 'Diagnostic criteria'; w.appendChild(k);
    var c = n.cloneNode(true);
    c.querySelectorAll('.mask-toggle').forEach(function(x){ x.remove(); });
    c.querySelectorAll('button, a').forEach(function(x){ var s = document.createElement('span'); while(x.firstChild) s.appendChild(x.firstChild); x.replaceWith(s); });
    c.querySelectorAll('[id]').forEach(function(x){ x.removeAttribute('id'); }); c.removeAttribute('id');
    w.appendChild(c); return w;
  }
'''
PV_CALL = "    if(q) pv.querySelector('.qx-pq').textContent = norm(q.textContent);\n"
SITE = [
    ('.qx-pv .qx-po:focus-visible{outline:2px solid var(--accent);outline-offset:2px}',
     '.qx-pv .qx-po:focus-visible{outline:2px solid var(--accent);outline-offset:2px}' + PV_CSS),
    ('  function openPv(link){\n', PV_JS + '  function openPv(link){\n'),
    (PV_CALL, PV_CALL + '    var cr = pvCrit(link, t); if(cr) pv.appendChild(pvTile(cr));\n'),
]


def site_ops(h, log):
    ops = []
    for find, w in SITE:
        if h.count(find) != 1:
            log['skipped'].append('site %r found %d times' % (find[:40], h.count(find)))
            continue
        ops.append({'op': 'replace_global', 'find': find, 'with': w, 'note': 's163 E6: drawer-preview criteria (C4)'})
        h = h.replace(find, w)
    return ops


# 40_labels.json (chunk 5, D8): NBME block labels. A trimmed board question (div.pearls.nbq, div.pc-nbq) reads
# "NBME question N"; commentary (div.pearls without nbq) and inline mentions read "NBME framing". Matched by markup.
OLD_LBL = 'How NBME framed it'


def label_rows(h, log):
    rows = []
    for b in briefs(h):
        seg = h[b.start:b.end]
        for mm in re.finditer(re.escape(OLD_LBL), seg):
            i = mm.start()
            pre, post = seg[max(0, i - 200):i], seg[mm.end():mm.end() + 40]
            q = re.match(r': question (\d+)</span>', post)
            if q and re.search(r'<div class="pearls nbq"[^>]*><span class="lbl">$', pre):
                rows.append((b.id, OLD_LBL + q.group(0), 'NBME question %s</span>' % q.group(1), 1, 's163 D8 a: nbq'))
            elif post.startswith('</span>') and re.search(r'<div class="pearls nbq"[^>]*><span class="lbl">$', pre):
                rows.append((b.id, pre[pre.rfind('<div'):] + OLD_LBL + '</span>',
                             pre[pre.rfind('<div'):] + 'NBME question 1</span>', 1, 's163 D8 b: plain nbq'))
            elif post.startswith('</span>') and pre.endswith('<div class="pc-nbq"><span class="lbl">'):
                rows.append((b.id, '<div class="pc-nbq"><span class="lbl">' + OLD_LBL + '</span>',
                             '<div class="pc-nbq"><span class="lbl">NBME question</span>', 1, 's163 D8 c: pc-nbq'))
            elif post.startswith('</span>') and pre.endswith('<div class="pearls"><span class="lbl">'):
                rows.append((b.id, '<div class="pearls"><span class="lbl">' + OLD_LBL + '</span>',
                             '<div class="pearls"><span class="lbl">NBME framing</span>', 1, 's163 D8 d: commentary'))
            elif post.startswith(':'):
                rows.append((b.id, OLD_LBL + ':', 'NBME framing:', 1, 's163 D8 e: inline'))
            else:
                log['skipped'].append('label %s unclassified %r' % (b.id, post[:30]))
    return rows


def chrome_ops(h, log):
    ops = []
    for find, w in CHROME:
        if h.count(find) != 1:
            log['skipped'].append('chrome %r found %d times' % (find[:40], h.count(find)))
            continue
        ops.append({'op': 'replace_global', 'find': find, 'with': w, 'note': 's163 E3: chrome wording and NBME panel'})
        h = h.replace(find, w)
    return ops


def in_body_links(h, ids, log):
    """hrefs to a renamed id outside the rails (survey 2026-11-04: one, angina's Diagnostic workup link)."""
    ops = []
    navs = [(x.start(), x.end()) for x in NAV.finditer(h)]
    bl = list(briefs(h))
    for mm in re.finditer(r'href="#([^"]+)"', h):
        if mm.group(1) in ids and not any(s <= mm.start() < e for s, e in navs):
            b = [x for x in bl if x.start <= mm.start() < x.end]
            log['body_links'].append('%s %s' % (b[0].id if b else '(chrome)', mm.group(1)))
            ctx = h[mm.start():mm.end() + 60]
            ops.append({'op': 'replace', 'brief': b[0].id, 'find': ctx,
                        'with': 'href="#%s"' % new_id(mm.group(1)) + ctx[len(mm.group(0)):], 'note': 's163 E2: in-body link to a renamed id'})
    return ops


def read_rows(path, note):
    """brief ||| old ||| new ||| count ||| class rows (rewrites.txt format) as apply_rows tuples."""
    rows = []
    if not os.path.exists(path):
        return rows
    for ln in open(path, encoding='utf-8'):
        if not ln.strip() or ln.startswith('#'):
            continue
        f = ln.rstrip('\n').split('|||')
        f = [x[1:] if x.startswith(' ') else x for x in f]
        f = [x[:-1] if x.endswith(' ') else x for x in f]
        rows.append((f[0].strip(), f[1], f[2], int(f[3]) if len(f) > 3 and f[3].strip() else 1,
                     note % (f[4].strip() if len(f) > 4 else '')))
    return rows


def rewrite_ops(h, path, log):
    """rewrites.txt rows (brief ||| old ||| new ||| count ||| class), applied in order to h (the page after
    10_steps.json). Each occurrence becomes one op whose anchor is widened, away from any bank boundary, until it is
    unique in its scope: the brief (replace) or the bank item that holds it (replace_item_text). Returns (ops, h)."""
    rows = []
    if not os.path.exists(path):
        return [], h
    for ln in open(path, encoding='utf-8'):
        if not ln.strip() or ln.startswith('#'):
            continue
        f = ln.rstrip('\n').split('|||')
        f = [x[1:] if x.startswith(' ') else x for x in f]
        f = [x[:-1] if x.endswith(' ') else x for x in f]
        rows.append((f[0].strip(), f[1], f[2], int(f[3]) if len(f) > 3 and f[3].strip() else 1,
                     's163 E3 %s (D4/D6)' % (f[4].strip() if len(f) > 4 else '')))
    return apply_rows(h, rows, log)


def apply_rows(h, rows, log):
    """(brief, old, new, count, note) rows as widened brief- or item-scoped ops, applied in order. Returns (ops, h)."""
    import apply_edits
    from pagelib import items
    ops = []
    for bid, old, new, want, note in rows:
        b = [x for x in briefs(h) if x.id == bid]
        if len(b) != 1:
            log['rw_fail'].append('%s: brief not found' % bid)
            continue
        b = b[0]
        seg = h[b.start:b.end]
        got = seg.count(old)
        if got != want:
            log['rw_fail'].append('%s: %r found %d, expected %d' % (bid, old[:60], got, want))
            continue
        for _ in range(want):
            seg = h[b.start:b.end]
            at = b.start + seg.find(old)
            its = [i for i in items(h) if b.start <= i.start < b.end]
            it = [i for i in its if i.start <= at < i.end]
            banks = apply_edits._bank_ranges(h, b)
            if it:
                lo, hi, op = it[0].start, it[0].end, {'op': 'replace_item_text', 'brief': bid, 'item': it[0].id}
            else:
                lo, hi, op = b.start, b.end, {'op': 'replace', 'brief': bid}
                for bs, be in banks:          # the anchor may widen up to, never into, a bank
                    if be <= at:
                        lo = max(lo, be)
                    elif bs >= at + len(old):
                        hi = min(hi, bs)
            a, z = at, at + len(old)
            while h[lo:hi].count(h[a:z]) != 1:
                if a > lo:
                    a = max(lo, a - 20)
                if z < hi:
                    z = min(hi, z + 20)
                if a == lo and z == hi:
                    break
            find = h[a:z]
            repl = h[a:at] + new + h[at + len(old):z]
            op.update({'find': find, 'with': repl, 'note': note})
            h, _ = apply_edits.apply(h, {'edits': [op]})
            ops.append(op)
            b = [x for x in briefs(h) if x.id == bid][0]
            log['rw'] += 1
    return ops, h


def main(argv):
    page = os.path.join(WS, 'index.html')
    if '--page' in argv:
        page = argv[argv.index('--page') + 1]
    h = read_page(page)
    log = {'moved': 0, 'headings': 0, 'skipped': [], 'pause_in_criteria': [], 'ids': set(), 'order': {},
           'body_links': []}
    ops = []
    for b in briefs(h):
        ops += plan_brief(h, b, log)
    ops += in_body_links(h, log['ids'], log)
    for s in GLOW_OLD:
        if h.count(s) != 1:
            log['skipped'].append('glow css %r found %d times' % (s[:40], h.count(s)))
        else:
            ops.append({'op': 'replace_global', 'find': s, 'with': glow_new(s),
                        'note': 's163 E2: heading glow keyed to the renamed ids'})
    rails = len([1 for o in ops if o['note'].startswith('s163 E1: rail')])
    print('make_batch: %d rails, %d criteria moved, %d headings, %d ids renamed, %d body links, %d skipped %s, '
          'pause in criteria %s' % (rails, log['moved'], log['headings'], len(log['ids']), len(log['body_links']),
                                    len(log['skipped']), log['skipped'][:4], log['pause_in_criteria']))
    if '--survey' in argv:
        for k, v in sorted(log['order'].items(), key=lambda kv: -kv[1]):
            print('  heading order', k, v)
        return 0
    out = os.path.join(WS, 'repair', 's163')
    os.makedirs(out, exist_ok=True)
    json.dump({'edits': ops}, open(os.path.join(out, '10_steps.json'), 'w', encoding='utf-8'), indent=1,
              ensure_ascii=False)
    import apply_edits
    after, _ = apply_edits.apply(h, {'edits': ops})
    log['rw'], log['rw_fail'] = 0, []
    rw, _ = rewrite_ops(after, os.path.join(HERE, 'rewrites.txt'), log)
    print('make_batch: %d rewrites, %d failed' % (log['rw'], len(log['rw_fail'])))
    for x in log['rw_fail']:
        print('  FAIL', x)
    if rw:
        json.dump({'edits': rw}, open(os.path.join(out, '20_wording.json'), 'w', encoding='utf-8'), indent=1,
                  ensure_ascii=False)
    print('make_batch: wrote 10_steps.json (%d ops)%s' % (len(ops), ', 20_wording.json (%d ops)' % len(rw) if rw else ''))
    after2, _ = apply_edits.apply(after, {'edits': rw}) if rw else (after, None)
    ch = chrome_ops(after2, log)
    json.dump({'edits': ch}, open(os.path.join(out, '30_chrome.json'), 'w', encoding='utf-8'), indent=1,
              ensure_ascii=False)
    print('make_batch: wrote 30_chrome.json (%d of %d ops)' % (len(ch), len(CHROME)))
    after3, _ = apply_edits.apply(after2, {'edits': ch})
    rows = label_rows(after3, log)
    n0 = log['rw']
    lb, _ = apply_rows(after3, rows, log)
    kinds = {}
    for r in rows:
        kinds[r[4][8]] = kinds.get(r[4][8], 0) + 1
    json.dump({'edits': lb}, open(os.path.join(out, '40_labels.json'), 'w', encoding='utf-8'), indent=1,
              ensure_ascii=False)
    print('make_batch: wrote 40_labels.json (%d ops of %d rows; by kind %s; %d failed)' % (
        len(lb), len(rows), sorted(kinds.items()), len(log['rw_fail'])))
    # 50_masks.json (chunk 6, E4): B4 Recall masks on a criteria cutoff that a masked answer elsewhere repeats, and
    # the first-use abbreviation spell-outs now that Criteria is step 2 (masks.txt, by hand).
    after4, _ = apply_edits.apply(after3, {'edits': lb})
    mrows = read_rows(os.path.join(HERE, 'masks.txt'), 's163 E4 %s (B4)')
    n1 = len(log['rw_fail'])
    mk, _ = apply_rows(after4, mrows, log)
    json.dump({'edits': mk}, open(os.path.join(out, '50_masks.json'), 'w', encoding='utf-8'), indent=1,
              ensure_ascii=False)
    print('make_batch: wrote 50_masks.json (%d ops of %d rows; %d failed)' % (len(mk), len(mrows), len(log['rw_fail']) - n1))
    after5, _ = apply_edits.apply(after4, {'edits': mk})
    st = site_ops(after5, log)
    json.dump({'edits': st}, open(os.path.join(out, '60_site.json'), 'w', encoding='utf-8'), indent=1,
              ensure_ascii=False)
    print('make_batch: wrote 60_site.json (%d of %d ops)' % (len(st), len(SITE)))
    for x in log['rw_fail'] + log['skipped']:
        print('  FAIL', x)
    return 0 if not log['skipped'] and not log['rw_fail'] else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
