#!/usr/bin/env python3
"""Close-up screenshots of hover triggers: python3 repair/s172e/hover_shots.py PAGE OUT POP[,POP...] [--phone] [--dark] [--study] [--open]

One image per pop id: the table row or line holding the trigger, at 2x. --open hovers (desktop) or taps (phone) the
trigger first, so the card shows.
"""
import os
import sys

from playwright.sync_api import sync_playwright


def main(a):
    page, out, pops = os.path.abspath(a[0]), a[1], a[2].split(',')
    phone, dark, study, opn = '--phone' in a, '--dark' in a, '--study' in a, '--open' in a
    os.makedirs(out, exist_ok=True)
    tag = ('phone' if phone else 'desk') + ('_dark' if dark else '') + ('_study' if study else '') + ('_open' if opn else '')
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        ctx = b.new_context(viewport={'width': 390 if phone else 1280, 'height': 900}, device_scale_factor=2,
                            color_scheme='dark' if dark else 'light',
                            has_touch=phone, is_mobile=phone)
        ctx.add_init_script("try{localStorage.setItem('ax-flat','0');localStorage.setItem('ax-study','%s')%s}catch(e){}" % (
            '1' if study else '0', ";localStorage.setItem('ax-theme','dark')" if dark else ''))
        p = ctx.new_page()
        p.goto('file://' + page + '?axall')
        p.wait_for_selector('button.sp-pop', state='attached', timeout=120000) if False else p.wait_for_selector('.sp-pop', state='attached', timeout=120000)
        p.evaluate("()=>{const s=document.createElement('style');s.textContent='*{content-visibility:visible!important}"
                   "html,body{scroll-behavior:auto!important}';document.head.appendChild(s)}")
        p.wait_for_timeout(1500)
        for pid in pops:
            btn = p.locator('.sp-pop[aria-controls="%s"]' % pid).first
            try:
                p.wait_for_selector('.sp-pop[aria-controls="%s"]' % pid, state='attached', timeout=60000)
            except Exception:
                print('missing ' + pid)
                continue
            btn.scroll_into_view_if_needed()
            p.wait_for_timeout(300)
            if opn:
                (btn.tap() if phone else btn.hover())
                p.wait_for_timeout(500)
            box = btn.evaluate("e=>{const r=(e.closest('tr')||e.closest('li,p,div')).getBoundingClientRect();"
                               "return {x:Math.max(0,r.x-8),y:Math.max(0,r.y-12),w:r.width+16,h:r.height+(%d)}}" % (260 if opn else 24))
            vp = p.viewport_size
            clip = {'x': box['x'], 'y': box['y'], 'width': min(box['w'], vp['width'] - box['x']),
                    'height': min(box['h'], vp['height'] - box['y'])}
            f = os.path.join(out, '%s_%s.png' % (pid, tag))
            p.screenshot(path=f, clip=clip)
            print(f)
        b.close()


if __name__ == '__main__':
    main(sys.argv[1:])
