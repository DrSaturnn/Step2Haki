"""shots: review screenshots of spine briefs from a built page (replaces /tmp shootgen.py and shotcharts.py).

  python3 tools/spine/shots.py <page.html> <out-dir> <brief-id>[,<brief-id>...] [--mode steps|charts|both]
                               [--width 1280] [--phone] [--dark] [--study]

steps   one image per spine section (Script ... Follow-up), then the Practice section to the end of the brief, in a
        tall viewport (a short one leaves content-visibility sections blank, s125); a section taller than one image is
        tiled (step3a, step3b...); a brief without step headers is tiled whole. Nothing on the brief is skipped.
charts  one image per timeline, chart or workup panel at 2x scale (the full-resolution crops the audit and the
        Lead review; contact sheets are too small for legibility checks).
--phone uses a 390 px viewport; --dark sets the dark theme; --study turns study mode on (masks hidden answers). Fixed bars are hidden so they do not cover content.
Prints one line per file written.
"""
import os
import sys

from playwright.sync_api import sync_playwright

# lazy sections (content-visibility: auto) change height as they render, which moved step bounds between measuring and
# shooting (COPD review, 2026-10-10): render everything up front so every measurement is final
NO_LAZY = ("()=>{const s=document.createElement('style');s.textContent='*{content-visibility:visible!important}html,body{scroll-behavior:auto!important}';"
           "document.head.appendChild(s)}")
HIDE_FIXED = ("()=>{for(const e of document.querySelectorAll('body *')){if(getComputedStyle(e).position==='fixed'"
              "&&!e.closest('.brief'))e.style.setProperty('visibility','hidden','important')}}")


def opt(argv, k, d=None):
    return argv[argv.index(k) + 1] if k in argv else d


def main(argv):
    if len(argv) < 3:
        sys.exit(__doc__.strip().splitlines()[2].strip())
    page, out, ids = os.path.abspath(argv[0]), argv[1], argv[2].split(',')
    mode = opt(argv, '--mode', 'both')
    phone, dark, study = '--phone' in argv, '--dark' in argv, '--study' in argv
    width = 390 if phone else int(opt(argv, '--width', '1280'))
    tag = ('phone' if phone else str(width)) + ('-dark' if dark else '') + ('-study' if study else '')
    os.makedirs(out, exist_ok=True)
    init = "try{localStorage.setItem('ax-flat','0');localStorage.setItem('ax-study','%s')%s}catch(e){}" % (
        '1' if study else '0', ";localStorage.setItem('ax-theme','dark')" if dark else '')
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        if mode in ('steps', 'both'):
            c = b.new_context(viewport={'width': width, 'height': 3000}, color_scheme='dark' if dark else 'light')
            c.add_init_script(init)
            p = c.new_page()
            p.goto('file://' + page)
            p.wait_for_timeout(2500)
            p.evaluate(NO_LAZY)
            p.wait_for_timeout(400)
            p.evaluate(HIDE_FIXED)
            for bid in ids:                     # visit every brief once so lazy sections lay out
                p.evaluate("id=>{const e=document.getElementById(id);if(e)e.scrollIntoView()}", bid)
                p.wait_for_timeout(800)
            for bid in ids:
                # segment bounds in page coordinates: brief top, each step header, the Practice header, brief bottom.
                # A segment taller than one slice is tiled, so long steps (and the bank, on phone) are never cut off.
                def bounds():
                    return p.evaluate("id=>{const B=document.getElementById(id);if(!B)return null;const y=window.scrollY;"
                                      "const hs=[...B.querySelectorAll('h5.sp-h, h5.authored-hdr')].map(h=>h.getBoundingClientRect().top+y-6);"
                                      "const r=B.getBoundingClientRect();return {x:r.left,w:r.width,top:r.top+y,bottom:r.bottom+y,hs:hs}}", bid)
                bd = bounds()
                if not bd:
                    print('no brief', bid)
                    continue
                for _ in range(3):              # let lazy sections lay out, then measure again
                    for y in range(int(bd['top']), int(bd['bottom']), 2400):
                        p.evaluate("y=>window.scrollTo({top:y,behavior:'instant'})", y)
                        p.wait_for_timeout(250)
                    nb = bounds()
                    if abs(nb['bottom'] - bd['bottom']) < 2:
                        break
                    bd = nb
                edges = [bd['top']] + [h for h in bd['hs'] if bd['top'] < h < bd['bottom']] + [bd['bottom']]
                n = 0
                for k, (y0, y1) in enumerate(zip(edges, edges[1:])):
                    part = 0
                    y = y0
                    while y1 - y > 20:
                        h = min(2900, y1 - y)
                        p.evaluate("y=>window.scrollTo({top:y,behavior:'instant'})", y)
                        p.wait_for_timeout(500)
                        off = p.evaluate("y=>y-window.scrollY", y)     # the page may not scroll all the way at the end
                        vb = p.evaluate("id=>document.getElementById(id).getBoundingClientRect().bottom", bid)
                        h = max(0, min(h, vb - max(0, off)))           # never past the brief's own end
                        f = '%s/%s_%s_step%d%s.png' % (out, bid, tag, k, '' if y1 - y0 <= 2900 else chr(97 + part))
                        try:
                            h = min(h, 2995 - max(0, off))             # what fits below the slice's top; the next slice starts there
                            if h <= 20:
                                break
                            p.screenshot(path=f, clip={'x': bd['x'], 'y': max(0, off), 'width': bd['w'], 'height': h})
                            print(f)
                            n += 1
                        except Exception as e:  # noqa: BLE001
                            print('skip', bid, k, str(e)[:80])
                        y += h
                        part += 1
                print('%s: %d image(s), %d segment(s) (steps, then Practice to the end of the brief)' % (bid, n, len(edges) - 1))
            c.close()
        if mode in ('charts', 'both'):
            c = b.new_context(viewport={'width': width, 'height': 1200}, device_scale_factor=2,
                              color_scheme='dark' if dark else 'light')
            c.add_init_script(init)
            p = c.new_page()
            p.goto('file://' + page)
            p.wait_for_timeout(2500)
            p.evaluate(NO_LAZY)
            p.wait_for_timeout(400)
            p.evaluate(HIDE_FIXED)
            n = p.evaluate("ids=>{const L=[];for(const id of ids){const B=document.getElementById(id);if(!B)continue;"
                           "B.querySelectorAll('.lcw, .lcp, .sw-wheel, figure').forEach(e=>{const t=e.closest('.lcw')||e;"
                           "if(!L.includes(t))L.push(t)})}L.forEach((e,i)=>e.setAttribute('data-shot',i));"
                           "return L.map(e=>e.closest('.brief').id)}", ids)
            for i, bid in enumerate(n):
                el = p.locator('[data-shot="%d"]' % i)
                for _ in range(2):
                    el.scroll_into_view_if_needed()
                    p.wait_for_timeout(350)
                f = '%s/%s_%s_chart%d.png' % (out, bid, tag, i)
                try:
                    el.screenshot(path=f)
                    print(f)
                except Exception as e:  # noqa: BLE001 (a hidden or zero-size element)
                    print('skip', bid, i, str(e)[:80])
            c.close()
        b.close()


if __name__ == '__main__':
    main(sys.argv[1:])
