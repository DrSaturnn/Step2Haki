const { chromium, devices } = require('playwright');
(async () => {
  const b = await chromium.launch();
  for (const [name, opt] of [['desk', { viewport: { width: 1440, height: 900 } }], ['phone', devices['iPhone 13']]]) {
    const ctx = await b.newContext(opt); const pg = await ctx.newPage();
    const cdp = await ctx.newCDPSession(pg); if (name === 'phone') await cdp.send('Emulation.setCPUThrottlingRate', { rate: 4 });
    await pg.goto('file://' + process.argv[2] + '?shelf=step2'); await pg.waitForTimeout(3000);
    for (const deep of [false, true]) {
      if (deep) { await pg.evaluate(() => { location.hash = '#voices'; }); await pg.waitForTimeout(2500); }
      const r = await pg.evaluate(async () => {
        const out = [];
        for (const on of [true, false, true, false]) {
          const t0 = performance.now();
          if (on) document.documentElement.setAttribute('data-theme', 'dark'); else document.documentElement.removeAttribute('data-theme');
          void getComputedStyle(document.body).backgroundColor; document.body.offsetHeight;
          await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
          out.push(Math.round(performance.now() - t0));
        }
        return out.join(' ') + ' ms; built briefs ' + document.querySelectorAll('.brief:not(:has(> template.axl))').length + ', elements ' + document.getElementsByTagName('*').length;
      });
      console.log(name, deep ? 'after opening #voices' : 'home', r);
    }
    await ctx.close();
  }
  await b.close();
})();
