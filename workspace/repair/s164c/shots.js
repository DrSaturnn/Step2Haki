// s164c chunk 4c: screenshots of before and cand at desk 1512 and phone 390: masthead, one built brief, the search
// results list, a drawer. Pages are served over local HTTP (the cand fetches search.json beside it).
//   node repair/s164c/shots.js local/s164c/before.html local/s164c/cand.html local/s164c/shots
'use strict';
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');
const { serve } = require('../../tools/serve_page');
const [before, cand, out] = process.argv.slice(2);
const VIEWS = { desk: { viewport: { width: 1512, height: 945 } }, phone: { viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 } };
const BRIEF = 'delirium', QUERY = 'lithium';

(async () => {
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch();
  for (const [tag, page] of [['before', before], ['cand', cand]]) {
    const srv = await serve(page);
    for (const [vname, opts] of Object.entries(VIEWS)) {
      const phone = vname === 'phone', shot = n => p.screenshot({ path: path.join(out, `${vname}_${n}_${tag}.png`) });
      const ctx = await browser.newContext(opts); const p = await ctx.newPage(); const errors = [];
      p.on('pageerror', e => errors.push(String(e)));
      await p.goto(srv.url, { waitUntil: 'load' }); await p.waitForTimeout(3500);
      await shot('1-masthead');
      await p.goto(srv.url + '#' + BRIEF, { waitUntil: 'load' }); await p.waitForTimeout(4000);
      await shot('2-brief');
      if (phone && !(await p.isVisible('#search'))) { await p.click('#navtab'); await p.waitForTimeout(700); }
      await p.fill('#search', QUERY); await p.waitForTimeout(2500);
      await shot('3-search');
      await p.goto(srv.url + '#' + BRIEF, { waitUntil: 'load' }); await p.waitForTimeout(4000);
      const to = await p.evaluate(id => {
        const b = document.getElementById(id); if (window.AX && AX.brief) AX.brief.ensure(b);
        const d = Array.from(b.querySelectorAll('.sp-drw')).find(d => d.offsetParent !== null);
        if (!d) return null; d.setAttribute('data-sh', '1'); d.scrollIntoView({ block: 'center', behavior: 'instant' }); return d.getAttribute('data-brief');
      }, BRIEF);
      if (to) {
        await p.waitForTimeout(1200); await p.click('[data-sh="1"]'); await p.waitForTimeout(1200);
        if (!(await p.$('.sp-drawer'))) { await p.click('[data-sh="1"]'); await p.waitForTimeout(1200); }
        await shot('4-drawer');
      }
      console.log(tag, vname, 'drawer to', to, 'errors', errors.length, errors.slice(0, 2).join(' | '));
      await ctx.close();
    }
    srv.close();
  }
  await browser.close();
})();
