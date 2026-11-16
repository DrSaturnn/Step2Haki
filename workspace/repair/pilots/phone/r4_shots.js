const { chromium, devices } = require('playwright');
const { serve } = require('../../../tools/serve_page.js');
(async () => {
  const [page, out] = process.argv.slice(2);
  const srv = await serve(page); const b = await chromium.launch();
  const errs = [];
  async function run(tag, q, dark) {
    const ctx = await b.newContext({ ...devices['iPhone 14'], serviceWorkers: 'block' });
    if (dark) await ctx.addInitScript("localStorage.setItem('ax-theme','dark');");
    const p = await ctx.newPage(); p.on('pageerror', e => errs.push(tag + ': ' + e.message));
    const shot = async n => { await p.waitForTimeout(700); await p.screenshot({ path: `${out}/${tag}_${n}.png` }); };
    await p.goto(srv.url + q, { waitUntil: 'load' }); await p.waitForTimeout(2600);
    await shot('1home');
    await p.mouse.move(195, 400); await p.mouse.wheel(0, 620); await shot('2home2');
    const t = await p.$('#phhome .hh-t'); if (t) { await t.click(); await shot('3browse'); }
    else { const r = await p.$('main .wrap > .sectwrap:nth-of-type(3)'); }
    console.log(tag, 'navopen', await p.evaluate(() => document.body.classList.contains('navopen')), 'tiles', await p.evaluate(() => document.querySelectorAll('#phhome .hh-t').length), 'groups', await p.evaluate(() => document.querySelectorAll('#phhome .hh-g').length));
    await p.goto(srv.url + q + '#mdd', { waitUntil: 'load' }); await p.waitForTimeout(2600); await p.mouse.move(195, 400); await p.mouse.wheel(0, 1500); await shot('4brief');
    await p.mouse.wheel(0, 2600); await shot('5brief2');
    await ctx.close();
  }
  await run('A', '?phhome=tiles&phtabs=float&phsurf=now');
  await run('B', '?phhome=tiles&phtabs=float&phsurf=axbx');
  await run('C', '?phhome=list&phtabs=dock&phsurf=now');
  await run('D', '?phhome=tiles&phtabs=float&phsurf=now', true);
  console.log('errors', JSON.stringify(errs)); await b.close(); process.exit(0);
})();
