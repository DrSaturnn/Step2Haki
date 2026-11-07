// Pilot option screenshots: node variant_shots.js PAGE OUTDIR
const { chromium, devices } = require('playwright');
const { serve } = require('../../../tools/serve_page.js');
(async () => {
  const [page, out] = process.argv.slice(2);
  const srv = await serve(page); const b = await chromium.launch();
  const runs = [
    ['rail', { rail: 'on' }, '#pmr', async p => { await p.mouse.move(195, 400); await p.mouse.wheel(0, 2200); await p.waitForTimeout(500); }],
    ['dxb', { dx: 'b' }, '#pmr', async p => { await p.evaluate(() => { const d = document.querySelector('#pmr .sp-dx'); if (d) d.scrollIntoView(); }); await p.waitForTimeout(800); await p.mouse.wheel(0, -40); }],
    ['dxa', { dx: 'a' }, '#pmr', async p => { await p.evaluate(() => { const d = document.querySelector('#pmr .sp-dx'); if (d) d.scrollIntoView(); }); await p.waitForTimeout(800); await p.mouse.wheel(0, -40); }],
    ['long', { layout: 'long' }, '', async p => { await p.mouse.move(195, 400); await p.mouse.wheel(0, 4200); await p.waitForTimeout(600); }],
    ['hide', { bars: 'hide' }, '#mdd', async p => { await p.mouse.move(195, 400); await p.mouse.wheel(0, 1500); await p.waitForTimeout(600); }],
    ['dark', { dark: 1 }, '#mdd', async p => { await p.mouse.move(195, 400); await p.mouse.wheel(0, 900); }],
    ['darkhome', { dark: 1 }, '', async p => {}],
    ['pilotset', {}, '', async p => { await p.click('#mbar [data-act=settings]'); await p.waitForTimeout(700); await p.evaluate(() => { const s = document.getElementById('axdisp'); s.scrollTop = s.scrollHeight; }); }],
  ];
  for (const [n, o, h, fn] of runs) {
    const ctx = await b.newContext({ ...devices['iPhone 14'], serviceWorkers: 'block' });
    await ctx.addInitScript(`try{localStorage.setItem('ph-pilot', ${JSON.stringify(JSON.stringify(o))}); ${o.dark ? "localStorage.setItem('ax-dark','1');" : ''}}catch(e){}`);
    const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
    await p.goto(srv.url + h, { waitUntil: 'load' }); await p.waitForTimeout(2500);
    if (o.dark) { const dk = await p.evaluate(() => document.documentElement.getAttribute('data-theme')); if (dk !== 'dark') { await p.evaluate(() => { const b = document.querySelector('#modes button.dark'); if (b) b.click(); }); await p.waitForTimeout(500); } }
    await fn(p); await p.waitForTimeout(700);
    await p.screenshot({ path: `${out}/v_${n}.png` });
    console.log(n, errs);
    await ctx.close();
  }
  await b.close(); srv.close();
})();
