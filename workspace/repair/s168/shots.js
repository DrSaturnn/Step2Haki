// s168 report screenshots: node repair/s168/shots.js PAGE OUTDIR
'use strict';
const { chromium } = require('playwright');
const { serve } = require('../../tools/serve_page');
const fs = require('fs');
const [page, out] = process.argv.slice(2);
fs.mkdirSync(out, { recursive: true });
const rec = s => JSON.stringify({ v: 1, s });
(async () => {
  const srv = await serve(page);
  const b = await chromium.launch();
  async function open(W, H, s, hash, dpr) {
    const p = await b.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: dpr || 1 });
    p.on('pageerror', e => console.log('PAGEERR', e.message));
    await p.addInitScript(r => { try { localStorage.setItem('ax-settings', r); } catch (e) {} }, rec(s));
    await p.goto(srv.url + '#' + hash, { waitUntil: 'load' }); await p.waitForTimeout(2800);
    return p;
  }
  async function pageAt(p, i) {
    await p.evaluate(i => { const pg = document.querySelectorAll('.ax2-page')[i]; const bb = document.getElementById('axbar').getBoundingClientRect().bottom;
      window.scrollTo({ top: i ? scrollY + pg.getBoundingClientRect().top - bb - 12 : 0, behavior: 'instant' }); }, i);
    await p.waitForTimeout(400);
  }
  const bgOf = p => p.evaluate(() => getComputedStyle(document.body).backgroundImage + ' / ' + getComputedStyle(document.body).backgroundColor);
  let p = await open(1512, 945, {}, 'chf', 2);
  await p.screenshot({ path: out + '/01_desk_scrolling.png' });
  const bgScroll = await bgOf(p);
  await p.click('#axcfg'); await p.waitForTimeout(500); await p.screenshot({ path: out + '/02_desk_display_settings.png', clip: { x: 0, y: 0, width: 420, height: 720 } });
  await p.close();
  for (const [name, s] of [['light', {}], ['dark', { theme: 'dark' }], ['tinted', { theme: 'tinted' }], ['flat', { flat: '1' }]]) {
    p = await open(1512, 945, Object.assign({ layout: 'two' }, s), 'chf', 2);
    if (name === 'light') { console.log('background scrolling: ' + bgScroll); console.log('background two-pane: ' + await bgOf(p)); }
    await pageAt(p, 0); await p.screenshot({ path: `${out}/03_two_${name}_p1.png` });
    if (name === 'light') { await pageAt(p, 1); await p.screenshot({ path: `${out}/04_two_light_p2.png` }); }
    await p.close();
  }
  p = await open(1512, 945, { layout: 'two' }, 'scaphoid', 2);
  await p.evaluate(() => { const w = document.querySelector('#scaphoid figure.w5a'); window.scrollTo({ top: w.getBoundingClientRect().top + scrollY - 160, behavior: 'instant' }); });
  await p.waitForTimeout(400); await p.screenshot({ path: out + '/05_two_workup_continued.png' });
  await p.click('#ax2rail .sec:nth-of-type(4)'); await p.waitForTimeout(400); await p.screenshot({ path: out + '/06_two_rail_section.png' });
  await p.keyboard.press('Escape'); await p.click('#ax2rail .ex'); await p.waitForTimeout(900); await pageAt(p, 0);
  await p.screenshot({ path: out + '/07_two_sidebar_expanded.png' });
  await p.close();
  p = await open(1920, 1080, { layout: 'two' }, 'psychosis-duration', 1);
  await pageAt(p, 0); await p.screenshot({ path: out + '/08_two_1920_psychosis.png' });
  await p.close();
  p = await open(390, 844, { layout: 'two' }, 'chf', 2);
  console.log('phone layout attribute: ' + await p.evaluate(() => document.documentElement.getAttribute('data-layout')));
  await p.screenshot({ path: out + '/09_phone_scrolling.png' });
  await p.close();
  await b.close(); process.exit(0);
})();
