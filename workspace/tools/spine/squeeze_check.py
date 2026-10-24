#!/usr/bin/env python3
"""squeeze_check (Jonathan 2026-10-24, no screenshots): find text squeezed into a narrow column on a phone, from the
rendered DOM, with no images. Replaces the screenshot reading for the runbook's "widen, never shorten" rule.

A text block is flagged when, at a 390 px phone width, it wraps to 3 or more lines with 2.5 words per line or fewer and
its box is under 180 px wide. Blocks inside the Practice bank and hidden elements are skipped. Study mode is not needed:
masks blur text but do not change its layout.

  python3 tools/spine/squeeze_check.py <page.html> <brief-id>[,<brief-id>...] [--width 390] [--timeout 240]
Exit 0 when nothing is squeezed, 1 otherwise (one line per block: brief, words, lines, width, the text).
"""
import os
import sys

JS = r"""
(ids) => {
  const out = [];
  const SEL = 'td, th, p, li, dd, dt, .sp-f, .sp-src, .sp-commit, figcaption, caption, .wh, .why';
  for (const id of ids) {
    const br = document.getElementById(id);
    if (!br) { out.push([id, -1, 0, 0, 'brief not found']); continue; }
    for (const el of br.querySelectorAll(SEL)) {
      if (el.closest('ol.bank, .bankwrap, .sp-drawer, .qx-pv')) continue;
      const r = el.getBoundingClientRect();
      if (!r.width || !r.height || getComputedStyle(el).visibility === 'hidden') continue;
      if (el.querySelector(SEL)) continue;               // judge the innermost block only
      const txt = (el.innerText || '').replace(/\s+/g, ' ').trim();
      const nw = txt ? txt.split(' ').length : 0;
      if (nw < 6) continue;
      const range = document.createRange(); range.selectNodeContents(el);
      const tops = new Set(Array.from(range.getClientRects()).filter(q => q.width > 1).map(q => Math.round(q.top)));
      const lines = tops.size;
      if (lines >= 3 && nw / lines <= 2.5 && r.width < 180) out.push([id, nw, lines, Math.round(r.width), txt.slice(0, 70)]);
    }
  }
  return out;
}
"""


def main(argv):
    if len(argv) < 2:
        sys.exit(__doc__.strip().splitlines()[-2].strip())
    page, ids = os.path.abspath(argv[0]), argv[1].split(',')
    width = int(argv[argv.index('--width') + 1]) if '--width' in argv else 390
    tmo = int(argv[argv.index('--timeout') + 1]) if '--timeout' in argv else 240
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': width, 'height': 844})
        pg.set_default_timeout(tmo * 1000)
        pg.goto('file://' + page)
        pg.wait_for_timeout(2500)
        rows = pg.evaluate(JS, ids)
        b.close()
    for bid, nw, lines, w, t in rows:
        print('squeeze %s: %s' % (bid, t) if nw < 0 else 'squeeze %s: %d words on %d lines in %d px: %s' % (bid, nw, lines, w, t))
    print('squeeze_check: %d squeezed block(s) in %d brief(s) at %d px' % (len(rows), len(ids), width))
    return 1 if rows else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
