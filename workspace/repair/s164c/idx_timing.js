const { chromium } = require('playwright'); const { serve } = require('../../tools/serve_page');
(async () => {
  const srv = await serve('local/s164c/cand.html'); const b = await chromium.launch();
  for (const phone of [false, true]) {
    const ctx = await b.newContext(phone ? { viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true } : { viewport: { width: 1512, height: 945 } });
    await ctx.addInitScript(() => { window.__lt = []; new PerformanceObserver(l => { for (const e of l.getEntries()) __lt.push([Math.round(e.startTime), Math.round(e.duration)]); }).observe({ type: 'longtask', buffered: true }); });
    const p = await ctx.newPage(); const cdp = await ctx.newCDPSession(p);
    if (phone) await cdp.send('Emulation.setCPUThrottlingRate', { rate: 4 });
    await p.goto(srv.url, { waitUntil: 'load' });
    await p.waitForFunction(() => window.__axSearch && __axSearch.stats().built, null, { timeout: 60000 });
    await p.waitForTimeout(2000);
    const r = await p.evaluate(() => ({ s: __axSearch.stats(), lt: __lt, res: performance.getEntriesByType('resource').filter(e => /search\.json/.test(e.name)).map(e => [Math.round(e.startTime), Math.round(e.responseEnd)]) }));
    console.log(phone ? 'phone' : 'desk', JSON.stringify(r));
    await ctx.close();
  }
  await b.close(); srv.close();
})();
