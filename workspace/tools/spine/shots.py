"""shots: review screenshots of spine briefs from a built page (replaces /tmp shootgen.py and shotcharts.py).

  python3 tools/spine/shots.py <page.html> <out-dir> <brief-id>[,<brief-id>...] [--mode steps|charts|both]
                               [--width 1280] [--phone] [--dark]

steps   one image per spine section (Script ... Follow-up, then Practice), in a tall viewport: a short viewport
        leaves content-visibility sections blank (s125).
charts  one image per timeline, chart or workup panel at 2x scale (the full-resolution crops the audit and the
        Lead review; contact sheets are too small for legibility checks).
--phone uses a 390 px viewport; --dark sets the dark theme. Fixed bars are hidden so they do not cover content.
Prints one line per file written.
"""
import os
import sys

from playwright.sync_api import sync_playwright

HIDE_FIXED = ("()=>{for(const e of document.querySelectorAll('body *')){if(getComputedStyle(e).position==='fixed'"
              "&&!e.closest('.brief'))e.style.setProperty('visibility','hidden','important')}}")


def opt(argv, k, d=None):
    return argv[argv.index(k) + 1] if k in argv else d


def main(argv):
    if len(argv) < 3:
        sys.exit(__doc__.strip().splitlines()[2].strip())
    page, out, ids = os.path.abspath(argv[0]), argv[1], argv[2].split(',')
    mode = opt(argv, '--mode', 'both')
    phone, dark = '--phone' in argv, '--dark' in argv
    width = 390 if phone else int(opt(argv, '--width', '1280'))
    tag = ('phone' if phone else str(width)) + ('-dark' if dark else '')
    os.makedirs(out, exist_ok=True)
    init = "try{localStorage.setItem('ax-flat','0');localStorage.setItem('ax-study','0')%s}catch(e){}" % (
        ";localStorage.setItem('ax-theme','dark')" if dark else '')
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        if mode in ('steps', 'both'):
            c = b.new_context(viewport={'width': width, 'height': 3000}, color_scheme='dark' if dark else 'light')
            c.add_init_script(init)
            p = c.new_page()
            p.goto('file://' + page)
            p.wait_for_timeout(2500)
            p.evaluate(HIDE_FIXED)
            for bid in ids:
                hs = p.evaluate("id=>[...document.querySelectorAll('#'+id+' h5.sp-h, #'+id+' h5.authored-hdr')].map(h=>h.id)", bid)
                if not hs:
                    print('no spine headers in', bid)
                    continue
                for k, (a, z) in enumerate([(bid, hs[0])] + list(zip(hs, hs[1:]))):
                    for _ in range(2):
                        p.evaluate("id=>document.getElementById(id).scrollIntoView()", a)
                        p.wait_for_timeout(600)
                    r = p.evaluate("([a,z,bid])=>{const A=document.getElementById(a).getBoundingClientRect();"
                                   "const Z=document.getElementById(z).getBoundingClientRect();"
                                   "const B=document.getElementById(bid).getBoundingClientRect();"
                                   "return {x:B.left,y:Math.max(0,A.top-6),width:B.width,height:Math.min(2990,Z.top-A.top+6)}}",
                                   [a, z, bid])
                    r['height'] = min(r['height'], 2995 - r['y'])   # keep the clip inside the viewport
                    if r['height'] > 20:
                        f = '%s/%s_%s_step%d.png' % (out, bid, tag, k)
                        try:
                            p.screenshot(path=f, clip=r)
                            print(f)
                        except Exception as e:  # noqa: BLE001
                            print('skip', bid, k, str(e)[:80])
            c.close()
        if mode in ('charts', 'both'):
            c = b.new_context(viewport={'width': width, 'height': 1200}, device_scale_factor=2,
                              color_scheme='dark' if dark else 'light')
            c.add_init_script(init)
            p = c.new_page()
            p.goto('file://' + page)
            p.wait_for_timeout(2500)
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
