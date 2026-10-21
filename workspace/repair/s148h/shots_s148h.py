#!/usr/bin/env python3
"""s148h display-lane images (S4 plan in S148H.md): answered practice cards with their per-choice reasons, and the split
First step bands, from the batch page; then packed into contact sheets for the display reviewer.

  python3 repair/s148h/shots_s148h.py <page.html> <out dir> --cards b1,b2,... --bands b1,b2,... [--n 3]

cards  per brief, at 390 px phone, normal mode: the default Stack view's current card answered with its keyed choice
       (reasons under every choice; <brief>_card0_stack_phone.png), then in the List view the n items whose three
       reasons are longest, each answered with its keyed choice (<brief>_card<k>_phone.png); an item already answered
       in the Stack view shows answered
bands  per brief, the First step panel (.w5t.first) at 390 px phone, phone study mode, and 1280 desktop;
       file <brief>_first_<phone|phone-study|desktop>.png
sheets the images packed into columns of at most 1,500 px height, at most 3 columns per sheet:
       sheets/cards_sheet<N>.png and sheets/bands_<phone|phone-study|desktop>_sheet<N>.png, each column headed by its
       brief id.
Playwright timeouts are 240000 ms (two-core container; handoff session notes).
"""
import json
import os
import sys

from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
NO_LAZY = ("()=>{const s=document.createElement('style');s.textContent='*{content-visibility:visible!important}"
           "html,body{scroll-behavior:auto!important}';document.head.appendChild(s)}")
HIDE_FIXED = ("()=>{for(const e of document.querySelectorAll('body *')){if(getComputedStyle(e).position==='fixed'"
              "&&!e.closest('.brief'))e.style.setProperty('visibility','hidden','important')}}")


def opt(argv, k, d=None):
    return argv[argv.index(k) + 1] if k in argv else d


def longest(bid, n):
    r = json.load(open(os.path.join(HERE, 'data', 'reasons.json'), encoding='utf-8'))[bid]
    its = [(sum(len(x) for x in v), k) for k, v in r.items() if not k.startswith('_')]
    return [k for _, k in sorted(its, reverse=True)[:n]]


def page_ctx(b, width, study, page):
    c = b.new_context(viewport={'width': width, 'height': 1400}, device_scale_factor=1)
    c.add_init_script("try{localStorage.setItem('ax-flat','0');localStorage.setItem('ax-study','%s')}catch(e){}"
                      % ('1' if study else '0'))
    p = c.new_page()
    p.set_default_timeout(240000)
    p.goto('file://' + page)
    p.wait_for_timeout(2500)
    p.evaluate(NO_LAZY)
    p.wait_for_timeout(400)
    p.evaluate(HIDE_FIXED)
    return c, p


def pack(files, out, label_of, maxh=1500, cols=3):
    """Columns of images stacked down to maxh, cols per sheet, each image headed by its label."""
    ims = [(label_of(f), Image.open(f)) for f in files]
    columns, cur, h = [], [], 0
    for lab, im in ims:
        if im.height > maxh:                 # tall image: scale to fit one column
            im = im.resize((int(im.width * maxh / im.height), maxh))
        if cur and h + im.height + 22 > maxh:
            columns.append(cur)
            cur, h = [], 0
        cur.append((lab, im))
        h += im.height + 22
    if cur:
        columns.append(cur)
    written = []
    for s in range(0, len(columns), cols):
        cs = columns[s:s + cols]
        w = sum(max(im.width for _, im in c) for c in cs) + 24 * (len(cs) + 1)
        sheet = Image.new('RGB', (w, maxh + 30), (200, 200, 200))
        d = ImageDraw.Draw(sheet)
        x = 24
        for c in cs:
            y = 6
            for lab, im in c:
                d.text((x, y), lab, fill=(150, 0, 0))
                sheet.paste(im, (x, y + 16))
                y += im.height + 22
            x += max(im.width for _, im in c) + 24
        f = '%s%d.png' % (out, s // cols + 1)
        sheet.save(f)
        written.append(f)
    return written


def main(argv):
    page, out = os.path.abspath(argv[0]), argv[1]
    cards = [x for x in (opt(argv, '--cards', '') or '').split(',') if x]
    bands = [x for x in (opt(argv, '--bands', '') or '').split(',') if x]
    n = int(opt(argv, '--n', '3'))
    os.makedirs(os.path.join(out, 'sheets'), exist_ok=True)
    cfiles, bfiles = [], {'phone': [], 'phone-study': [], 'desktop': []}
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        if cards:
            c, p = page_ctx(b, 390, False, page)
            for bid in cards:
                # the default Stack view: the current card, answered
                cur = p.locator('#%s .mcq.sk-cur' % bid)
                if cur.count():
                    cur.first.scroll_into_view_if_needed()
                    p.wait_for_timeout(300)
                    cur.first.locator('button[data-correct="1"]').click()
                    p.wait_for_timeout(700)
                    f = os.path.join(out, '%s_card0_stack_phone.png' % bid)
                    p.locator('#%s .bankwrap' % bid).first.screenshot(path=f)
                    cfiles.append(f)
                    print(f)
                # then the List view, so the chosen items are all on the page
                p.locator('#%s button' % bid, has_text='List').first.click()
                p.wait_for_timeout(800)
                for k, iid in enumerate(longest(bid, n), 1):
                    sel = '#%s .mcq[data-item-id="%s"]' % (bid, iid)
                    el = p.locator(sel)
                    if el.count() == 0:
                        print('no card', bid, iid)
                        continue
                    el.first.scroll_into_view_if_needed()
                    p.wait_for_timeout(300)
                    try:
                        el.first.locator('button[data-correct="1"]').click(timeout=8000)
                    except Exception as e:  # noqa: BLE001 (already answered in the Stack view)
                        print('no click', bid, iid, str(e)[:60])
                    p.wait_for_timeout(700)
                    el.first.scroll_into_view_if_needed()
                    f = os.path.join(out, '%s_card%d_phone.png' % (bid, k))
                    el.first.screenshot(path=f)
                    cfiles.append(f)
                    print(f)
            c.close()
        for mode, width, study in (('phone', 390, False), ('phone-study', 390, True), ('desktop', 1280, False)):
            if not bands:
                break
            c, p = page_ctx(b, width, study, page)
            for bid in bands:
                el = p.locator('#%s .w5t.first' % bid)
                if el.count() == 0:
                    print('no first step', bid)
                    continue
                el.first.scroll_into_view_if_needed()
                p.wait_for_timeout(600)
                f = os.path.join(out, '%s_first_%s.png' % (bid, mode))
                el.first.screenshot(path=f)
                bfiles[mode].append(f)
                print(f)
            c.close()
        b.close()
    lab = lambda f: os.path.basename(f)[:-4]  # noqa: E731
    sh = pack(cfiles, os.path.join(out, 'sheets', 'cards_sheet'), lab) if cfiles else []
    for mode, fs in bfiles.items():
        if fs:
            sh += pack(fs, os.path.join(out, 'sheets', 'bands_%s_sheet' % mode), lab,
                       maxh=1500, cols=2 if mode == 'desktop' else 3)
    for f in sh:
        print('sheet', f, Image.open(f).size)


if __name__ == '__main__':
    main(sys.argv[1:])
