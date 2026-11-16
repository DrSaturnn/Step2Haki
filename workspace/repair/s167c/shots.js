// s167c screenshots: desk and phone, the sidebar (Presentations sub headers, Preventive), a brief with anchored hovers
// and visible lines (substance), an open hover card, and a shared-axis timeline (sud-meds).
//   node repair/s167c/shots.js PAGE OUTDIR
const { chromium, devices } = require('playwright');
const path = require('path');
const { serve } = require('../../tools/serve_page');
const page = path.resolve(process.argv[2]), out = path.resolve(process.argv[3]);
(async () => {
  const srv = await serve(page);
  const b = await chromium.launch();
  for (const [name, opt] of [['desk', { viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2 }],
                             ['phone', { ...devices['iPhone 13'] }]]) {
    const ctx = await b.newContext(opt); const pg = await ctx.newPage();
    const go = async (hash) => { await pg.goto(srv.url + '?shelf=step2' + hash); await pg.waitForTimeout(3500); };
    await go('');
    if (name === 'desk') {
      await pg.evaluate(() => { const n = document.querySelector('#navlinks'); n.scrollTop = 0; });
      await pg.screenshot({ path: out + '/desk_sidebar_top.png' });
      await pg.evaluate(() => { const a = document.querySelector('#navlinks a[href="#bs-nat-fracture"]');
        if (a) a.scrollIntoView({ block: 'center' }); });
      await pg.screenshot({ path: out + '/desk_sidebar_prev.png' });
    }
    await go('#substance');
    await pg.evaluate(() => { const v = document.querySelector('#substance .sp-vl'); if (v) v.scrollIntoView({ block: 'center' }); });
    await pg.waitForTimeout(800);
    await pg.screenshot({ path: out + '/' + name + '_visible_line.png' });
    const opened = await pg.evaluate(() => { const a = document.querySelector('#substance button.sp-pop.sp-a');
      if (!a) return false; a.scrollIntoView({ block: 'center' }); a.click(); return a.textContent.trim(); });
    await pg.waitForTimeout(800);
    await pg.screenshot({ path: out + '/' + name + '_hover_open.png' });
    await go('#sud-meds');
    const ax = await pg.evaluate(() => { const w = document.querySelector('#sud-meds .wax');
      if (!w) return false; w.closest('figure').scrollIntoView({ block: 'center' }); return true; });
    await pg.waitForTimeout(800);
    await pg.screenshot({ path: out + '/' + name + '_shared_axis.png' });
    console.log(name, 'anchor clicked:', opened, '| shared axis found:', ax);
    await ctx.close();
  }
  await b.close(); srv.close();
})();
