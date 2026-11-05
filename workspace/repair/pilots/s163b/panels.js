// s163b I5: open the change log, the review panel and a desktop drawer at wide windows (the page zooms 110% at
// 1500 px and up) and report each panel's box against the window. node panels.js <page.html> [WxH ...]
const { chromium } = require('playwright');
const [,, page, ...sizes] = process.argv;
(async () => {
  const b = await chromium.launch();
  for (const sz of (sizes.length ? sizes : ['1600x900', '1920x1080', '1400x900'])) {
    const [W, H] = sz.split('x').map(Number);
    const p = await b.newPage({ viewport: { width: W, height: H } });
    await p.goto('file://' + page, { waitUntil: 'load', timeout: 120000 });
    await p.waitForTimeout(1500);
    const res = {};
    const box = async sel => { const e = await p.$(sel); const r = e && await e.boundingBox(); return r ? Math.round(r.y) + '..' + Math.round(r.y + r.height) : 'none'; };
    // change log
    await p.evaluate(() => { const x = document.querySelector('.axlogbtn'); if (x) x.click(); });
    await p.waitForTimeout(600); res.log = await box('.axlog');
    await p.keyboard.press('Escape'); await p.evaluate(() => { const s = document.querySelector('.axlog-scrim'); if (s) s.remove(); });
    // review panel
    await p.evaluate(() => { const x = document.querySelector('[aria-controls="axrv"]'); if (x) x.click(); });
    await p.waitForTimeout(600); res.review = await box('#axrv:not([hidden])');
    await p.keyboard.press('Escape'); await p.waitForTimeout(300);
    // desktop drawer: a drawer button low in the window
    await p.evaluate(() => { location.hash = 'kawasaki'; });
    await p.waitForTimeout(1500);
    await p.evaluate(() => { const bs = [...document.querySelectorAll('#kawasaki .sp-drw')]; const x = bs[bs.length - 1]; x.scrollIntoView({block: 'end'}); window.scrollBy(0, 40); x.click(); });
    await p.waitForTimeout(1200); res.drawer = await box('aside.sp-drawer');
    console.log(sz, JSON.stringify(res));
    await p.close();
  }
  await b.close();
})();
