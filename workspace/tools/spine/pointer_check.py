#!/usr/bin/env python3
"""pointer_check (s150c S8 audit class "pointer not actionable"; Jonathan 2026-10-24, fewer lead calls): in a running
page, click every drawer button (.sp-drw) of the named briefs through the page script and confirm the drawer shows the
target brief (its <h4> title); and confirm every "Pairs with" block rendered as an owner list with no unlinked rows.

  python3 tools/spine/pointer_check.py <page.html> <brief-id>[,<brief-id>...] [--timeout 240]
Exit 0 when every pointer opens the right brief and every Pairs with block links; 1 otherwise, one line per problem.
"""
import os
import sys

CLICK = r"""
async (ids) => {
  const out = [], sleep = ms => new Promise(r => setTimeout(r, ms));
  const title = t => { const e = document.getElementById(t); const h = e && e.querySelector('h4'); return h ? h.textContent.trim() : null; };
  for (const id of ids) {
    const el = document.getElementById(id);
    if (!el) { out.push([id, '', 'brief not found']); continue; }
    const seen = new Set();
    for (const bt of el.querySelectorAll('.sp-drw[data-brief]')) {
      const t = bt.getAttribute('data-brief'); if (seen.has(t)) continue; seen.add(t);
      if (!document.getElementById(t)) { out.push([id, t, 'target brief missing']); continue; }
      bt.click(); await sleep(500);
      const dr = [...document.querySelectorAll('.sp-drawer')].find(d => d.offsetParent !== null || getComputedStyle(d).display !== 'none');
      const want = title(t), txt = dr ? dr.textContent.replace(/\s+/g, ' ') : '';
      if (!dr) out.push([id, t, 'no drawer opened']);
      else if (want && !txt.includes(want.slice(0, 25))) out.push([id, t, 'drawer shows another brief']);
      else out.push([id, t, 'ok']);
      document.dispatchEvent(new KeyboardEvent('keydown', {key: 'Escape'})); await sleep(150);
    }
    for (const l of el.querySelectorAll('.lbl')) {
      if (!/^pairs with$/i.test(l.textContent.trim())) continue;
      const pb = l.parentElement;
      if (!pb.querySelector('.qx-pl')) out.push([id, 'Pairs with', 'not rendered as an owner list (leading text before the first title?)']);
      else if (pb.querySelectorAll('.qx-nolink').length) out.push([id, 'Pairs with', pb.querySelectorAll('.qx-nolink').length + ' row(s) name no live brief title']);
    }
  }
  return out;
}
"""


def main(argv):
    if len(argv) < 2:
        sys.exit(__doc__.strip().splitlines()[4].strip())
    page, ids = os.path.abspath(argv[0]), argv[1].split(',')
    tmo = int(argv[argv.index('--timeout') + 1]) if '--timeout' in argv else 240
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 1280, 'height': 900})
        pg.set_default_timeout(tmo * 1000)
        pg.goto('file://' + page)
        pg.wait_for_timeout(2500)
        rows = pg.evaluate(CLICK, ids)
        b.close()
    bad = [r for r in rows if r[2] != 'ok']
    for bid, t, why in bad:
        print('pointer %s -> %s: %s' % (bid, t, why))
    print('pointer_check: %d pointer(s) checked in %d brief(s); %d problem(s)' % (sum(1 for r in rows if r[2] == 'ok'), len(ids), len(bad)))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
