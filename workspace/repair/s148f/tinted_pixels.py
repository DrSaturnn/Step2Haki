#!/usr/bin/env python3
"""s148f: contrast in the tinted theme from real pixels. contrast_computed.py composites a node's text color on its
ancestors' fills, but the tinted canvas is a color-mix gradient behind translucent glass, which that method cannot
composite (s148b note), so its tinted results are not valid. Here each text element is shot with its text hidden
(color: transparent), the median pixel is the background it actually sits on, and the ratio is taken against its
computed text color. Need 4.5:1 (3:1 at 24 px, or 18.66 px bold).

  python3 repair/s148f/tinted_pixels.py <page.html> <brief,...> [--sel 'css,css'] [--width 1180]
"""
import io, sys
from statistics import median
from playwright.sync_api import sync_playwright
from PIL import Image
SEL = 'p.sub,span.mask-region,.bkmode,.bkfilter button,.bknav button,.bkn,.qx-chip,.qx-no,.qx-top .rv,.stem .sd,.lbl,th,td,.sp-commit,.sp-f'


def lum(c):
    f = lambda x: (x / 255 / 12.92) if x / 255 <= .03928 else ((x / 255 + .055) / 1.055) ** 2.4
    return .2126 * f(c[0]) + .7152 * f(c[1]) + .0722 * f(c[2])


def main(a):
    page, bids = a[0], a[1].split(',')
    sel = a[a.index('--sel') + 1] if '--sel' in a else SEL
    w = int(a[a.index('--width') + 1]) if '--width' in a else 1180
    below = 0; n = 0
    with sync_playwright() as pw:
        b = pw.chromium.launch(); c = b.new_context(viewport={'width': w, 'height': 1000})
        c.add_init_script("try{localStorage.setItem('ax-theme','tinted')}catch(e){}")
        p = c.new_page(); p.goto('file://' + page); p.wait_for_timeout(2500)
        p.add_style_tag(content='*{content-visibility:visible!important;transition:none!important;animation:none!important}')
        for bid in bids:
            els = p.locator('#%s :is(%s)' % (bid, sel))
            k = els.count()
            for i in range(k):
                el = els.nth(i)
                info = el.evaluate("e=>{const s=getComputedStyle(e);const r=e.getBoundingClientRect();if(!e.offsetParent||r.width<4||r.height<4||!e.textContent.trim())return null;"
                                   "const m=s.color.match(/[\\d.]+/g).map(Number);return {c:m,fs:parseFloat(s.fontSize),fw:parseInt(s.fontWeight),t:e.textContent.trim().slice(0,40),tag:e.tagName.toLowerCase()+'.'+(e.className||'')}}")
                if not info:
                    continue
                el.scroll_into_view_if_needed()
                el.evaluate("e=>{e.dataset.qxc=e.style.color;e.style.setProperty('color','transparent','important');e.querySelectorAll('*').forEach(x=>x.style.setProperty('color','transparent','important'))}")
                img = Image.open(io.BytesIO(el.screenshot())).convert('RGB')
                el.evaluate("e=>{e.style.color=e.dataset.qxc;e.querySelectorAll('*').forEach(x=>x.style.removeProperty('color'))}")
                px = list(img.getdata())
                bg = tuple(median(ch) for ch in zip(*px))
                tc = info['c'][:3]; al = info['c'][3] if len(info['c']) > 3 else 1
                tc = [tc[j] * al + bg[j] * (1 - al) for j in range(3)]
                l1, l2 = lum(tc), lum(bg); r = (max(l1, l2) + .05) / (min(l1, l2) + .05)
                need = 3 if info['fs'] >= 24 or (info['fs'] >= 18.66 and info['fw'] >= 700) else 4.5
                n += 1
                if r < need:
                    below += 1
                    print('below %-28s %.2f (need %.1f) "%s"' % (info['tag'][:28], r, need, info['t']))
    print('tinted_pixels: %d element(s), %d below' % (n, below))
    return 1 if below else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
