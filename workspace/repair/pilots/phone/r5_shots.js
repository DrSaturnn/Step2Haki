// r5: node r5_shots.js PAGE OUTDIR. Drawer and push opening (tab, swipe open, swipe close, scrim tap), table swipe left alone.
const { chromium, devices } = require('playwright');
const { serve } = require('../../../tools/serve_page.js');
(async () => {
  const [page, out] = process.argv.slice(2);
  const srv = await serve(page); const b = await chromium.launch(); const errs = [];
  async function run(tag, q) {
    const ctx = await b.newContext({ ...devices['iPhone 14'], serviceWorkers: 'block' });
    const p = await ctx.newPage(); p.on('pageerror', e => errs.push(tag + ': ' + e.message));
    const cdp = await ctx.newCDPSession(p);
    const shot = async n => { await p.waitForTimeout(700); await p.screenshot({ path: `${out}/${tag}_${n}.png` }); };
    const open = () => p.evaluate(() => document.body.classList.contains('navopen'));
    const swipe = async (x0, x1, y, mid) => {
      await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: x0, y }] });
      for (let i = 1; i <= 8; i++) { await cdp.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: x0 + (x1 - x0) * i / 8, y }] }); await p.waitForTimeout(16); if (mid && i === 5) await p.screenshot({ path: `${out}/${tag}_${mid}.png` }); }
      await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] }); await p.waitForTimeout(700);
    };
    await p.goto(srv.url + q, { waitUntil: 'load' }); await p.waitForTimeout(2600);
    await shot('1home');
    await p.tap('#mbar [data-act="index"]'); await shot('2tab_open'); const a = await open();
    await p.touchscreen.tap(370, 300); await p.waitForTimeout(600); const c = await open();
    await p.goto(srv.url + q + '#mdd', { waitUntil: 'load' }); await p.waitForTimeout(2600);
    await p.evaluate(() => scrollTo(0, 1500)); await p.waitForTimeout(500);
    await swipe(120, 330, 420, '3mid'); const d = await open(); await shot('4swipe_open');
    await swipe(300, 60, 420); const e = await open();
    await swipe(8, 300, 420); const f = await open();
    const y = await p.evaluate(() => scrollY);
    console.log(tag, JSON.stringify({ tab_open: a, scrim_tap_closes: !c, swipe_opens: d, swipe_closes: !e, edge_swipe_ignored: !f, scroll_kept: y }));
    await ctx.close();
  }
  await run('drawer', '?phnav=drawer'); await run('push', '?phnav=push'); await run('screen', '?phnav=screen&phsurf=now');
  console.log('errors', JSON.stringify(errs)); await b.close(); process.exit(0);
})();
