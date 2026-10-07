#!/usr/bin/env python3
"""legib_audit.py: legibility measurements for the AxBx study page (s112 plan, claude/S112_LEGIBILITY_PLAN.md).

  python3 tools/legib_audit.py PAGE --briefs a,b,c [--label before] [--out local/legib] [--views phone,desk] [--modes sculpted,flat,study]

For every text node in each sampled brief, in every view and mode:
  contrast  pixel-true: the brief is screenshotted with its text made transparent (fixed chrome hidden), and the text
            color (with alpha and ancestor opacity) is compared with every background pixel under the text's line boxes.
            Reported as the 20th percentile, so gradients and inset shadows count but a thin line crossing the box does
            not; a clash is p5 below need while p20 passes. Need 4.5:1, or 3:1 at large size
            (24 px, or 18.66 px bold). SVG text is skipped.
  size      computed font size; floors 10.5 px (any text) and 11 px (labels).
  depth     how many boxes with a soft shadow (blur above 0) or a gradient background enclose the text, the brief card
            included; spread-only rings count as borders.
  frames    how many enclosing boxes show any edge (border on 3+ sides, any shadow or ring, gradient, or a fill).
Writes <out>/<label>.json (every node) and <out>/<label>.md (summary by component and by element). Prints totals.
"""
import argparse, io, json, os, statistics, sys
from collections import defaultdict

import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

VIEWS = {'phone': 390, 'desk': 1180}
COMPONENTS = ['dp', 'pearls', 'danger', 'rule', 'crit', 'vignette', 'lcp', 'lcw', 'lcc', 'mcq', 'bank', 'trapline', 'traps',
              'chain', 'figcap', 'figbody', 'bsband', 'aqband', 'jump', 'sub', 'tsec', 'authored-hdr']

COLLECT = r"""
(bid) => {
  const parse = c => { const m = c && c.match(/rgba?\(([^)]+)\)/); if (!m) return null;
    const v = m[1].split(',').map(Number); return [v[0], v[1], v[2], v.length > 3 ? v[3] : 1]; };
  const br = document.getElementById(bid); if (!br) return null;
  const R = br.getBoundingClientRect();
  const comps = %s;
  // a depth level = a soft shadow (any blur) or a gradient surface; spread-only rings are borders, not depth
  const soft = bs => bs && bs !== 'none' && bs.split(/,(?![^()]*\))/).some(s => {
    const n = s.replace(/rgba?\([^)]*\)/, '').match(/-?[\d.]+px/g) || []; return parseFloat(n[2] || '0') > 0; });
  const deco = e => { const cs = getComputedStyle(e); return soft(cs.boxShadow) || /gradient/.test(cs.backgroundImage); };
  // a frame = any visible box edge: border, ring or soft shadow, gradient, or a fill (the eye reads each as one more box)
  const frame = e => { const cs = getComputedStyle(e);
    const bd = ['Top', 'Right', 'Bottom', 'Left'].filter(sd => parseFloat(cs['border' + sd + 'Width']) > 0 && cs['border' + sd + 'Style'] !== 'none'
      && !/rgba\([^)]*,\s*0\)/.test(cs['border' + sd + 'Color'])).length >= 3;
    const fill = cs.backgroundColor && !/rgba\([^)]*,\s*0\)/.test(cs.backgroundColor) && cs.backgroundColor !== 'transparent';
    return bd || (cs.boxShadow && cs.boxShadow !== 'none') || /gradient/.test(cs.backgroundImage) || fill; };
  const items = [];
  const w = document.createTreeWalker(br, NodeFilter.SHOW_TEXT);
  let n;
  while ((n = w.nextNode())) {
    const t = n.textContent.trim(); if (t.length < 2) continue;
    const el = n.parentElement; if (!el || el.closest('svg')) continue;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') continue;
    let op = 1, depth = 0, frames = 0, comp = '';
    for (let e = el; e; e = e.parentElement) {
      const s = getComputedStyle(e); op *= parseFloat(s.opacity || '1');
      if (deco(e)) depth++;
      if (frame(e)) frames++;
      if (!comp && e.classList) { for (const c of comps) if (e.classList.contains(c)) { comp = c; break; } }
      if (e === br) break;
    }
    const col = parse(cs.color); if (!col) continue; col[3] *= op; if (col[3] < 0.05) continue;
    const rg = document.createRange(); rg.selectNodeContents(n);
    const rects = [...rg.getClientRects()].filter(r => r.width > 2 && r.height > 4)
      .map(r => [r.left - R.left, r.top - R.top, r.width, r.height]);
    if (!rects.length) continue;
    const cls = (typeof el.className === 'string' && el.className.trim()) ? '.' + el.className.trim().split(/\s+/).join('.') : '';
    const pc = el.parentElement, pcls = pc && typeof pc.className === 'string' && pc.className.trim() ? '.' + pc.className.trim().split(/\s+/)[0] : (pc ? pc.tagName.toLowerCase() : '');
    items.push({key: el.tagName.toLowerCase() + cls + ' < ' + pcls, comp: comp || '(card)', fs: parseFloat(cs.fontSize),
                fw: parseInt(cs.fontWeight) || 400, upper: cs.textTransform === 'uppercase', color: col, depth, frames, rects, text: t.slice(0, 48)});
  }
  return {w: R.width, h: R.height, items};
}
""" % json.dumps(COMPONENTS)

HIDE = "#%s, #%s *, #%s *::before, #%s *::after{color:transparent!important;-webkit-text-fill-color:transparent!important;text-shadow:none!important}"


def lum(rgb):
    c = rgb / 255.0
    c = np.where(c <= 0.03928, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


def measure(img, it):
    """(p20, p5) contrast of the text color against the pixels under its line boxes. p20 is the reported ratio: it
    follows gradients and inset shadows but ignores a thin line crossing the box; p5 below need while p20 passes marks
    a clash (a tick, border or edge running through the text)."""
    H, W = img.shape[:2]
    px = []
    for x, y, w, h in it['rects']:
        x0, y0, x1, y1 = max(0, int(x)), max(0, int(y)), min(W, int(x + w)), min(H, int(y + h))
        if x1 > x0 and y1 > y0:
            px.append(img[y0:y1, x0:x1].reshape(-1, 3))
    if not px:
        return None
    bg = np.concatenate(px).astype(float)
    r, g, b, a = it['color']
    fg = np.array([r, g, b], float) * a + bg * (1 - a)
    lf, lb = lum(fg), lum(bg)
    cr = (np.maximum(lf, lb) + 0.05) / (np.minimum(lf, lb) + 0.05)
    return float(np.percentile(cr, 20)), float(np.percentile(cr, 5))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('page'); ap.add_argument('--briefs', required=True); ap.add_argument('--label', default='run')
    ap.add_argument('--out', default=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'local', 'legib'))
    ap.add_argument('--views', default='phone,desk'); ap.add_argument('--modes', default='sculpted,flat,study')
    ap.add_argument('--shots', action='store_true', help='also save a normal screenshot of each brief')
    ap.add_argument('--css', default='', help='a CSS file injected after load, to measure a candidate restyle before it ships')
    a = ap.parse_args()
    bids = a.briefs.split(','); os.makedirs(a.out, exist_ok=True)
    rows = []
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium')
        for view in a.views.split(','):
            for mode in a.modes.split(','):
                ctx = b.new_context(viewport={'width': VIEWS[view], 'height': 900}, device_scale_factor=1)
                ctx.add_init_script("try{localStorage.setItem('ax-flat','%s');localStorage.setItem('ax-study','%s')}catch(e){}"
                                    % ('1' if mode == 'flat' else '0', '1' if mode == 'study' else '0'))
                pg = ctx.new_page()
                pg.goto('file://' + os.path.abspath(a.page) + '#' + bids[0]); pg.wait_for_timeout(2500)
                if a.css:
                    pg.add_style_tag(content=open(a.css, encoding='utf-8').read()); pg.wait_for_timeout(300)
                # fixed and sticky chrome (bottom bar, Index pill, update bar) would be painted into tall element screenshots
                pg.evaluate("() => { for (const e of document.querySelectorAll('body *')) { const p = getComputedStyle(e).position;"
                            " if ((p === 'fixed' || p === 'sticky') && !e.closest('.brief')) e.style.setProperty('visibility', 'hidden', 'important'); } }")
                for bid in bids:
                    pg.evaluate("h => { location.hash = h }", bid); pg.wait_for_timeout(900)
                    el = pg.locator('#' + bid)
                    if a.shots:
                        el.screenshot(path=os.path.join(a.out, '%s_%s_%s_%s.png' % (a.label, bid, view, mode)))
                    data = pg.evaluate(COLLECT, bid)
                    if not data:
                        print('missing brief', bid, file=sys.stderr); continue
                    tag = pg.add_style_tag(content=HIDE % (bid, bid, bid, bid))
                    img = np.array(Image.open(io.BytesIO(el.screenshot())).convert('RGB'))
                    tag.evaluate("e => e.remove()")
                    for it in data['items']:
                        m = measure(img, it)
                        if m is None:
                            continue
                        c, c5 = m
                        large = it['fs'] >= 24 or (it['fw'] >= 700 and it['fs'] >= 18.66)
                        rows.append(dict(view=view, mode=mode, brief=bid, key=it['key'], comp=it['comp'], fs=it['fs'], fw=it['fw'],
                                         upper=it['upper'], depth=it['depth'], frames=it['frames'], cr=round(c, 2), cr5=round(c5, 2), need=3.0 if large else 4.5, text=it['text']))
                ctx.close()
        b.close()
    json.dump(rows, open(os.path.join(a.out, a.label + '.json'), 'w'), ensure_ascii=False)
    report(rows, a)


def report(rows, a):
    def summ(group):
        out = []
        for k, rs in sorted(group.items(), key=lambda kv: -sum(r['cr'] < r['need'] for r in kv[1])):
            f = [r for r in rs if r['cr'] < r['need']]
            out.append('| %s | %d | %d | %.2f | %.1f | %d | %d | %s |' % (k, len(rs), len(f), min(r['cr'] for r in rs), min(r['fs'] for r in rs),
                                                             max(r['depth'] for r in rs), max(r['frames'] for r in rs), (min(f, key=lambda r: r['cr'])['text'] if f else '').replace('|', '/')))
        return out
    L = ['# Legibility audit: %s' % a.label, '', 'Page: %s. Briefs: %s.' % (a.page, a.briefs), '']
    L += ['## Totals by view and mode', '', '| view | mode | text nodes | below contrast | clashes | under 10.5 px | under 11 px | depth 3+ | max depth | frames 4+ | max frames |', '|---|---|---|---|---|---|---|---|---|---|---|']
    vm = defaultdict(list)
    for r in rows:
        vm[(r['view'], r['mode'])].append(r)
    for (v, m), rs in vm.items():
        L.append('| %s | %s | %d | %d | %d | %d | %d | %d | %d | %d | %d |' % (v, m, len(rs), sum(r['cr'] < r['need'] for r in rs),
                                                         sum(r['cr'] >= r['need'] > r['cr5'] for r in rs), sum(r['fs'] < 10.5 for r in rs),
                                                         sum(r['fs'] < 11 for r in rs), sum(r['depth'] >= 3 for r in rs), max(r['depth'] for r in rs),
                                                         sum(r['frames'] >= 4 for r in rs), max(r['frames'] for r in rs)))
    hd = ['', '| %s | nodes | below | worst ratio | min px | max depth | max frames | worst sample |', '|---|---|---|---|---|---|---|---|']
    ph = [r for r in rows if r['view'] == 'phone' and r['mode'] == 'sculpted'] or rows
    by = defaultdict(list)
    for r in ph:
        by[r['comp']].append(r)
    L += ['', '## By component (phone, sculpted)'] + [hd[0], hd[1] % 'component', hd[2]] + summ(by)
    by = defaultdict(list)
    for r in ph:
        by[r['key']].append(r)
    L += ['', '## By element (phone, sculpted), worst 40'] + [hd[0], hd[1] % 'element', hd[2]] + summ(by)[:40]
    open(os.path.join(a.out, a.label + '.md'), 'w').write('\n'.join(L) + '\n')
    print('\n'.join(L[:6 + len(vm) + 2]))


if __name__ == '__main__':
    main()
