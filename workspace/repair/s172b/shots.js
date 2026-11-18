// Before and after screenshots for the Two-pane fixes: live page (BEFORE) against the candidate (AFTER).
//   node repair/s172b/shots.js BEFORE_PAGE AFTER_PAGE OUT_DIR
'use strict';
const path = require('path');
const WS = path.resolve(__dirname, '..', '..');
const { chromium } = require('playwright');
const { serve } = require(WS + '/tools/serve_page');
const [BEFORE, AFTER, OUT] = process.argv.slice(2);
const SHOTS = [
  // name, width, height, brief, steps
  ['shelf', 1512, 945, 'chf', async p => { await p.evaluate(() => document.querySelector('.shelfpick button[data-shelf="psych"]').click()); await p.waitForTimeout(1500); }],
  ['answer', 1512, 945, 'chf', async p => {
    await p.evaluate(() => { const q = document.querySelector('.brief.ax2-cur .mcq.sk-cur'); q.querySelector('.opts button').click(); });
    await p.waitForTimeout(900);
    await p.evaluate(() => { const q = document.querySelector('.brief.ax2-cur .mcq.sk-cur'); q.closest('.ax2-page').scrollIntoView(); }); await p.waitForTimeout(500); }],
  ['sidebar', 1512, 945, 'chf', async p => { await p.evaluate(() => document.querySelector('#ax2rail .ex').click()); await p.waitForTimeout(1500); }],
  ['rail', 1512, 945, 'mdd', async p => { await p.evaluate(() => scrollBy(0, innerHeight * 1.2)); await p.waitForTimeout(600); }],
  ['rail800', 1280, 800, 'mdd', async p => { await p.evaluate(() => scrollBy(0, innerHeight * 1.2)); await p.waitForTimeout(600); }],
  ['ladder', 1440, 900, 'chf', async p => {
    await p.evaluate(() => { const r = document.querySelector('.brief.ax2-cur .sp-rung'); r.closest('.ax2-page').scrollIntoView(); }); await p.waitForTimeout(600); }],
  ['hpv', 1512, 945, 'hpv', async p => {
    await p.evaluate(() => { const h = [...document.querySelectorAll('.brief.ax2-cur .ax2-u')].find(u => u.dataset.name === 'Platform and gates'); if (h) h.closest('.ax2-page').scrollIntoView(); }); await p.waitForTimeout(600); }],
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
