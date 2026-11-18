// Before and after screenshots for the audit changes to the Two-pane fixes: the build before the audit (BEFORE)
// against the candidate (AFTER).
//   node repair/s172b/shots_audit.js BEFORE_PAGE AFTER_PAGE OUT_DIR
'use strict';
const path = require('path');
const WS = path.resolve(__dirname, '..', '..');
const { chromium } = require('playwright');
const { serve } = require(WS + '/tools/serve_page');
const [BEFORE, AFTER, OUT] = process.argv.slice(2);
const SHOTS = [
  // name, width, height, brief, steps
  // an answer made while the window sits between two pages
  ['between', 1512, 945, 'chf', async p => {
    await p.evaluate(() => { const pg = document.querySelector('.brief.ax2-cur .mcq.sk-cur').closest('.ax2-page'); window.scrollTo({ top: scrollY + pg.getBoundingClientRect().top - innerHeight * 0.45, behavior: 'instant' }); });
    await p.waitForTimeout(300);
    await p.locator('.brief.ax2-cur .mcq.sk-cur .opts button').first().click(); await p.waitForTimeout(900); }],
  // the term list that squeezed its text column
  ['grid', 1512, 945, 'hpv', async p => {
    await p.evaluate(() => { const d = [...document.querySelectorAll('.brief.ax2-cur dl.rows')].find(x => /meningococcal/i.test((x.previousElementSibling || {}).textContent || ''));
      const pg = d.closest('.ax2-page'); window.scrollTo({ top: scrollY + pg.getBoundingClientRect().top - 108, behavior: 'instant' }); });
    await p.waitForTimeout(500); }],
  ['grid2', 1512, 945, 'teratogens', async p => {
    await p.evaluate(() => { const d = document.querySelector('.brief.ax2-cur .ax2-cols dl.rows:not(.rows-short):not(.mnem)');
      const pg = d.closest('.ax2-page'); window.scrollTo({ top: scrollY + pg.getBoundingClientRect().top - 108, behavior: 'instant' }); });
    await p.waitForTimeout(500); }],
  // a short window: the rail and its Display settings tile
  ['rail680', 1280, 680, 'mdd', async p => { await p.waitForTimeout(200); }],
];
(async () => {
  const b = await chromium.launch();
  for (const [tag, page] of [['before', BEFORE], ['after', AFTER]]) {
    const srv = await serve(page);
    for (const [name, W, H, id, act] of SHOTS) {
      const p = await b.newPage({ viewport: { width: W, height: H } });
      await p.addInitScript(() => localStorage.setItem('ax-settings', JSON.stringify({ v: 1, s: { tour: '1' } })));
      await p.goto(srv.url + '#' + id, { waitUntil: 'load' }); await p.waitForTimeout(1800);
      await p.evaluate(() => document.querySelector('#modes .layout button[data-v="two"]').click()); await p.waitForTimeout(1500);
      try { await act(p); } catch (e) { console.log(tag, name, 'step failed:', e.message.split('\n')[0]); }
      await p.screenshot({ path: path.join(OUT, `${name}_${tag}.png`) });
      await p.close();
    }
    srv.close();
  }
  await b.close();
  console.log('shots written to', OUT);
})();
