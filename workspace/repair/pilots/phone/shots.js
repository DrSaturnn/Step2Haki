// Phone pilot screenshots and checks: node shots.js PAGE OUTDIR [--dark] [--long] [--hide]
const { chromium, devices } = require('playwright');
const { serve } = require('../../../tools/serve_page.js');
(async () => {
  const [page, out] = process.argv.slice(2); const flags = process.argv.slice(4);
  const srv = await serve(page);
  const b = await chromium.launch();
  const ctx = await b.newContext({ ...devices['iPhone 14'], serviceWorkers: 'block' });
  const init = [];
  if (flags.includes('--dark')) init.push("localStorage.setItem('ax-theme','dark');");
  if (flags.includes('--long')) init.push("document.documentElement.setAttribute('data-ph-layout','long');");
  if (flags.includes('--hide')) init.push("document.documentElement.setAttribute('data-ph-bars','hide');");
  if (init.length) await ctx.addInitScript(init.join(''));
  const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  const shot = async (n) => { await p.waitForTimeout(650); await p.screenshot({ path: `${out}/${n}.png` }); };
  const log = (k, v) => console.log(k, JSON.stringify(v));
  await p.goto(srv.url, { waitUntil: 'load' }); await p.waitForTimeout(2500);
  await shot('01_home');
  await p.mouse.move(195, 400); await p.mouse.wheel(0, 900); await shot('02_home_scroll');
  // a Presentations group row on Home opens Browse at its group
  const row = await p.$('main .wrap > .psub'); if (row) { await row.click(); await shot('03_browse_from_home'); }
  log('navopen', await p.evaluate(() => document.body.classList.contains('navopen')));
  // pick the first visible brief tile in the open group
  const tile = await p.$('#axn .axn-dz.on a.axn-b:not([hidden])'); const tid = tile && await tile.getAttribute('data-id');
  if (tile) { await tile.click(); await p.waitForTimeout(1500); await shot('04_brief_top'); }
  log('solo', await p.evaluate(() => ({ open: document.documentElement.classList.contains('ph-open'), hash: location.hash, cur: (document.querySelector('.ph-cur') || {}).id, vis: [...document.querySelectorAll('main .wrap > *')].filter(e => e.offsetParent).length })));
  await p.mouse.wheel(0, 1200); await shot('05_brief_scroll');
  await p.mouse.wheel(0, 1800); await shot('06_brief_scroll2');
  log('head', await p.evaluate(() => { const h = document.getElementById('phead'); return { on: h.classList.contains('on'), t: h.querySelector('.ph-ti').innerText, cur: (h.querySelector('[aria-current=step]') || {}).textContent }; }));
  // tap step 4 in the header
  const c4 = await p.$('#phead .ph-steps button:nth-child(4):not(.off)'); if (c4) { await c4.click(); await p.waitForTimeout(1200); await shot('07_step4'); }
  log('after step', await p.evaluate(() => (document.querySelector('#phead [aria-current=step]') || {}).textContent));
  await p.click('#phead .ph-rec'); await shot('08_recall'); await p.click('#phead .ph-rec');
  // end of the brief
  await p.evaluate(() => window.scrollTo(0, document.documentElement.scrollHeight)); await shot('09_brief_end');
  await p.click('#mbar [data-act=index]'); await shot('10_browse_reading');
  await p.click('#mbar [data-act=settings]'); await shot('11_settings');
  await p.click('#mbar [data-act=index]'); await shot('12_browse_again');
  await p.fill('#search', 'lithium'); await p.waitForTimeout(1500); await shot('13_search');
  await p.fill('#search', ''); await p.click('#mbar [data-act=home]'); await shot('14_back_reading');
  await p.click('#phead .ph-back'); await shot('15_home_restored');
  log('home', await p.evaluate(() => ({ open: document.documentElement.classList.contains('ph-open'), y: Math.round(scrollY), hash: location.hash })));
  await p.click('#mbar [data-act=review]'); await shot('16_review');
  await p.goto(srv.url + '#mdd', { waitUntil: 'load' }); await p.waitForTimeout(2500); await shot('17_deeplink_mdd');
  log('deeplink', await p.evaluate(() => ({ cur: (document.querySelector('.ph-cur') || {}).id, top: Math.round(document.getElementById('mdd').getBoundingClientRect().top) })));
  log('errors', errs);
  await b.close(); srv.close();
})();
