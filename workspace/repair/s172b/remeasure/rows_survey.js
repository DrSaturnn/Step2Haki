// Term-and-text lists (dl.rows) in Two-pane over every brief: how many squeeze the text column, with and without the
// Two-pane cap on the term column. OLD=1 puts the page's general rule (auto 1fr) back for the comparison.
//   node repair/s172b/remeasure/rows_survey.js PAGE [WxH] [open]
'use strict';
const path = require('path');
const WS = path.resolve(__dirname, '..', '..', '..');
const { chromium } = require('playwright');
const { serve } = require(WS + '/tools/serve_page');
const PAGE = process.argv[2], [W, H] = (process.argv[3] || '1512x945').split('x').map(Number), nav = process.argv[4] === 'open';
(async () => {
  const b = await chromium.launch(), srv = await serve(PAGE);
  const pass = async old => {
    const p = await b.newPage({ viewport: { width: W, height: H } });
    await p.addInitScript(() => localStorage.setItem('ax-settings', JSON.stringify({ v: 1, s: { tour: '1' } })));
    await p.goto(srv.url + '#chf', { waitUntil: 'load' }); await p.waitForTimeout(1800);
    if (old) await p.addStyleTag({ content: 'html[data-layout="two"] .ax2-cols dl.rows:not(.rows-short,.mnem){grid-template-columns:auto 1fr !important}' });
    await p.evaluate(() => document.querySelector('#modes .layout button[data-v="two"]').click()); await p.waitForTimeout(1500);
    if (nav) { await p.evaluate(() => document.querySelector('#ax2rail .ex').click()); await p.waitForTimeout(1200); }
    const ids = await p.evaluate(() => [...document.querySelectorAll('main .wrap > .brief[id]')].map(x => x.id));
    const t = { briefs: ids.length, lists: 0, squeezed: 0, squeezedIn: [], wideTerm: 0, pages: 0 };
    for (const id of ids) {
      await p.evaluate(id => { location.hash = id; }, id); await p.waitForTimeout(900);
      const r = await p.evaluate(() => { const B = document.querySelector('.brief.ax2-cur'), o = { lists: 0, squeezed: 0, wide: 0, pages: B.querySelectorAll('.ax2-page').length };
        B.querySelectorAll('.ax2-cols dl.rows:not(.rows-short):not(.mnem)').forEach(d => { if (getComputedStyle(d).display !== 'grid' || !d.querySelector(':scope > dd')) return;
          o.lists++; const w = d.getBoundingClientRect().width, dd = [...d.querySelectorAll(':scope > dd')], dt = [...d.querySelectorAll(':scope > dt')];
          if (dd.some(x => x.getBoundingClientRect().width < 110 && x.textContent.trim().length > 20)) o.squeezed++;
          if (dt.some(x => x.getBoundingClientRect().width > w * 0.401)) o.wide++; });
        return o; });
      t.lists += r.lists; t.squeezed += r.squeezed; t.wideTerm += r.wide; t.pages += r.pages; if (r.squeezed) t.squeezedIn.push(id);
    }
    await p.close(); return t;
  };
  const [o, n] = await Promise.all([pass(true), pass(false)]);
  console.log(`${W}x${H} ${nav ? 'sidebar open' : 'rail'}`);
  console.log('  general rule (auto 1fr):', JSON.stringify(o));
  console.log('  term column capped at 40%:', JSON.stringify(n));
  await b.close(); srv.close();
})();
