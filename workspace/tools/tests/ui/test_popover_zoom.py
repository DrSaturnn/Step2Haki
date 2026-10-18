#!/usr/bin/env python3
"""s147: popover cards, the review panel and the profile sheet must open next to their buttons at every desktop width,
including 1500 px and wider, where the page is scaled to 110% (html zoom, s146c). Before the fix the card opened
tens of thousands of px below its button there (getBoundingClientRect and scrollY are zoomed px; CSS lengths are not).

  python3 tools/tests/ui/test_popover_zoom.py <page.html>     exit 0 when every check passes
"""
import sys
from playwright.sync_api import sync_playwright

page, bad = sys.argv[1], []
with sync_playwright() as p:
    b = p.chromium.launch()
    for w in (1280, 1600, 1920):
        pg = b.new_page(viewport={'width': w, 'height': 1000}); pg.goto('file://' + page); pg.wait_for_timeout(1200)
        for bid in ('pyelo', 'copd', 'hypercalcemia'):
            btn = pg.locator('#%s button.sp-pop' % bid).first
            btn.scroll_into_view_if_needed(); pg.wait_for_timeout(200); btn.hover(); pg.wait_for_timeout(300)
            r = pg.evaluate("""() => { const c = document.querySelector('.sp-card'), o = document.querySelector('.sp-pop[aria-expanded="true"]');
                if(!c || !o) return null; const a = c.getBoundingClientRect(), q = o.getBoundingClientRect();
                return {gap: a.top - q.bottom, flip: q.top - a.bottom, left: a.left, right: a.right, vw: innerWidth}; }""")
            ok = r and (0 <= r['gap'] <= 30 or 0 <= r['flip'] <= 30) and r['left'] >= 0 and r['right'] <= r['vw']
            print('%s %d %s: %s' % ('ok ' if ok else 'BAD', w, bid, r)); bad += [] if ok else [(w, bid)]
            pg.mouse.move(0, 0); pg.wait_for_timeout(300)
        s = pg.evaluate("""() => { const q = [...document.querySelectorAll('button')].find(e => /axrv/i.test(e.id + ' ' + e.className + ' ' + (e.getAttribute('aria-controls') || '')));
            if(!q) return 'no pill'; q.click(); const s = document.getElementById('axrv'); if(!s || s.hidden) return 'closed';
            const a = s.getBoundingClientRect(); return {right: a.right, left: a.left, vw: innerWidth}; }""")
        ok = isinstance(s, dict) and s['left'] >= 0 and s['right'] <= s['vw']
        print('%s %d profile sheet: %s' % ('ok ' if ok else 'BAD', w, s)); bad += [] if ok else [(w, 'sheet')]
        pg.close()
    b.close()
print('test_popover_zoom: %d failure(s)' % len(bad)); sys.exit(1 if bad else 0)
