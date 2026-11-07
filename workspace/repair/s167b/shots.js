const { chromium, devices } = require('playwright');
const page = process.argv[2], out = process.argv[3];
(async () => {
  const b = await chromium.launch();
  for (const [name, opt] of [['desk', { viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 }], ['phone', { ...devices['iPhone 13'] }]]) {
    const ctx = await b.newContext(opt); const pg = await ctx.newPage();
    await pg.goto('file://' + page + '?shelf=step2'); await pg.waitForTimeout(3000);
    await pg.screenshot({ path: out + '/' + name + '_default.png' });
    const ms = await pg.evaluate(async () => { const t0 = performance.now(); document.querySelector('#modes button.dark:not(.tint)').click();
      await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))); return Math.round(performance.now() - t0); });
    await pg.screenshot({ path: out + '/' + name + '_dark_2frames.png' });
    console.log(name, 'dark in', ms, 'ms; flat class', await pg.evaluate(() => document.body.classList.contains('flat')));
    await ctx.close();
  }
  await b.close();
})();
