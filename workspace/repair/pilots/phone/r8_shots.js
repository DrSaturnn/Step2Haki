// r8: node r8_shots.js PAGE OUTDIR. The study-desk Home: first visit, after reading two briefs, By complaint, a row opening the drawer, search.
const { chromium, devices } = require('playwright');
const { serve } = require('../../../tools/serve_page.js');
(async () => {
  const [page, out] = process.argv.slice(2);
  const srv = await serve(page); const b = await chromium.launch(); const errs = [];
  async function run(tag, dark) {
    const ctx = await b.newContext({ ...devices['iPhone 14'], serviceWorkers: 'block' });
    if (dark) await ctx.addInitScript("localStorage.setItem('ax-theme','dark');");
    const p = await ctx.newPage(); p.on('pageerror', e => errs.push(tag + ': ' + e.message));
    const shot = async n => { await p.waitForTimeout(700); await p.screenshot({ path: `${out}/${tag}_${n}.png` }); };
    await p.goto(srv.url, { waitUntil: 'load' }); await p.waitForTimeout(2600); await shot('1first');
    for (const id of ['scaphoid', 'lithium-effects', 'mdd']) { await p.evaluate(h => { location.hash = '#' + h; }, id); await p.waitForTimeout(1500); await p.mouse.move(195, 400); await p.mouse.wheel(0, 2400); await p.waitForTimeout(900); }
    await p.tap('#mbar [data-act="home"]'); await p.waitForTimeout(600); await p.evaluate(() => scrollTo(0, 0)); await shot('2home');
    console.log(tag, JSON.stringify(await p.evaluate(() => ({ recent: JSON.parse(localStorage.getItem('ph-recent') || '[]').map(r => r.id + ':' + r.n), rows: document.querySelectorAll('#phhome .hh-r').length, h: document.documentElement.scrollHeight }))));
    await p.mouse.move(195, 400); await p.mouse.wheel(0, 620); await shot('3scroll');
    await p.mouse.wheel(0, 900); await shot('4end');
    await p.evaluate(() => scrollTo(0, 300)); await p.tap('#phhome .hh-seg [data-v="cc"]'); await shot('5complaint');
    await p.tap('#phhome .hh-seg ~ .hh-r'); await shot('6row_drawer'); const o1 = await p.evaluate(() => document.body.classList.contains('navopen'));
    await p.tap('#mbar [data-act="index"]'); await p.waitForTimeout(500); await p.evaluate(() => scrollTo(0, 0));
    await p.tap('#phhome .hh-s'); await shot('7search'); const f = await p.evaluate(() => (document.activeElement || {}).tagName);
    await p.tap('#mbar [data-act="index"]'); await p.waitForTimeout(500);
    await p.tap('#phhome .hh-c'); await p.waitForTimeout(1500); await shot('8continue');
    console.log(tag, JSON.stringify({ row_opens_drawer: o1, search_focus: f, continue_hash: await p.evaluate(() => location.hash) }));
    await ctx.close();
  }
  await run('desk'); await run('deskdark', true);
  console.log('errors', JSON.stringify(errs)); await b.close(); process.exit(0);
})();
