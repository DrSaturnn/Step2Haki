// Desktop parity: node desk_parity.js BEFORE AFTER OUTDIR; screenshots at 1512x945 (a_* before, b_* after); diff with diff.py
const { chromium } = require('playwright');
const { serve } = require('../../../tools/serve_page.js');
(async () => {
  const [A, Bp, out] = process.argv.slice(2);
  const b = await chromium.launch();
  async function run(page, tag) {
    const srv = await serve(page);
    const ctx = await b.newContext({ viewport: { width: 1512, height: 945 }, serviceWorkers: 'block' });
    const p = await ctx.newPage();
    const st = [['home', ''], ['mdd', '#mdd'], ['scaphoid', '#scaphoid-s4'], ['lith', '#lithium-effects']];
    for (const [n, h] of st) {
      await p.goto(srv.url + h, { waitUntil: 'load' }); await p.waitForTimeout(3000);
      await p.evaluate(() => { document.querySelectorAll('.bb-next b, .axbuild, .axlogbtn').forEach(e => e.style.visibility = 'hidden'); });
      await p.screenshot({ path: `${out}/${tag}_${n}.png` });
    }
    await p.goto(srv.url, { waitUntil: 'load' }); await p.waitForTimeout(2500);
    await p.click('#axcfg'); await p.waitForTimeout(800);
    await p.evaluate(() => { document.querySelectorAll('.axbuild, .axlogbtn').forEach(e => e.style.visibility = 'hidden'); });
    await p.screenshot({ path: `${out}/${tag}_settings.png` });
    await ctx.close(); srv.close();
  }
  await run(A, 'a'); await run(Bp, 'b');
  await b.close();
})();
