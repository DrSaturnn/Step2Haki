#!/usr/bin/env python3
"""offline check (the link sits on a tinted box, p20 about 7.5 as the live
Pairs with links did in s146, where b < .xref clashed at p5 about 4.1; the container's fallback font sets the underline
lower, so the test uses a 1 px offset and 2 px thickness to put it inside the line box as the live page's font does)
 for legib_audit's pointer-link underline (s147): a dotted .xref underline in its own decoration color
must not count as a clash, while a real edge through text (a border line) still does.

  python3 tools/tests/legib/test_legib_xref.py
"""
import io, os, sys, tempfile
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
import legib_audit as L  # noqa: E402

PAGE = """<!doctype html><html><head><style>
body{margin:0;background:#fff;color:rgb(21,21,27);font:15px/25.2px -apple-system, BlinkMacSystemFont, "Segoe UI", Inter, Roboto, system-ui, sans-serif}
.xref{color:inherit;text-decoration:underline;text-decoration-style:dotted;text-decoration-color:rgba(59,91,140,.55);text-underline-offset:1px;text-decoration-thickness:2px}
.edge{background:linear-gradient(#fff 45%,#3B5B8C 45%,#3B5B8C 60%,#fff 60%)}
</style></head><body><div id="b" style="padding:20px;width:600px">
<p id="t1" style="background:rgb(160,172,192)">See <a class="xref" href="#x"><b>Workup of hematuria in a child</b></a></p>
<p id="t2"><span class="edge">Line through this text here</span></p>
</div></body></html>"""


def run(css):
    d = tempfile.mkdtemp(); f = os.path.join(d, 'p.html'); open(f, 'w').write(PAGE)
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium')
        pg = b.new_page(viewport={'width': 700, 'height': 300}); pg.goto('file://' + f)
        data = pg.evaluate(L.COLLECT, 'b')
        el = pg.locator('#b')
        tag = pg.add_style_tag(content=css)
        img = np.array(Image.open(io.BytesIO(el.screenshot())).convert('RGB'))
        tag.evaluate('e => e.remove()'); b.close()
    out = {}
    for it in data['items']:
        c, c5 = L.measure(img, it)
        out[it["text"][:10]] = (c >= 4.5 > c5)        # True = counted as a clash
        if os.environ.get("DBG"): print(it["text"][:12], it["fw"], round(c, 2), round(c5, 2))
    return out


ok = fail = 0
def expect(name, cond):
    global ok, fail
    print(('ok   ' if cond else 'FAIL ') + name); ok += cond; fail += (not cond)

old = run(L.HIDE % ('b', 'b', 'b', 'b'))
new = run(L.hide_css('b'))
expect('before the fix the .xref underline counted as a clash (the bug this fixes)', old.get('Workup of ') is True)
expect('after the fix the .xref underline is not a clash', new.get('Workup of ') is False)
expect('a real edge through text is still a clash', new.get('Line throu') is True)
print('test_legib_xref: %d passed, %d failed' % (ok, fail)); sys.exit(1 if fail else 0)
