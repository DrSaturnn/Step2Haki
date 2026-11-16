// step 1 probe: desktop step list, shelf card, z-index layers, drawer swipe under a stub overlay, bottom notices
'use strict';
const path = require('path');
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const { serve } = require(path.join(__dirname, '../../../tools/serve_page'));
const PAGE = path.join(__dirname, '../../../index.html');
const rect = async (pg, sel) => pg.evaluate(s => { const e = document.querySelector(s); if(!e) return null; const r = e.getBoundingClientRect(); return [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)].join(','); }, sel);
(async () => {
  const srv = await serve(PAGE), out = {};
  const br = await chromium.launch({ executablePath: '/usr/bin/google-chrome' });
  for (const [w, h] of [[1101, 800], [1280, 720], [1440, 900]]) {
    const cx = await br.newContext({ viewport: { width: w, height: h } }), pg = await cx.newPage();
    await pg.goto(srv.url + '#scaphoid'); await pg.waitForTimeout(2500);
    const o = out['d' + w] = {};
    for (const s of ['.axn-srch', '.axn-shelfrow', '#navscroll', '#axcfg', '#axbar']) o[s] = await rect(pg, s);
    o.rail = await pg.evaluate(() => { const a = document.querySelector('#nav [aria-current="step"]'); if(!a) return null; let p = a.parentNode; while(p && p.querySelectorAll('a').length < 5) p = p.parentNode; const r = p.getBoundingClientRect(); return { cls: p.className, tag: p.tagName, id: p.id, rect: [r.x, r.y, r.width, r.height].map(Math.round).join(','), n: p.querySelectorAll('a').length, tile: p.parentNode.className }; });
    if (w === 1440) o.z = await pg.evaluate(() => [...document.querySelectorAll('body *')].map(e => [+getComputedStyle(e).zIndex, e.id || e.className]).filter(a => a[0] > 160).map(a => a[0] + ' ' + String(a[1]).slice(0, 40)));
    await cx.close();
  }
  for (const [w, h] of [[375, 667], [393, 852]]) {
    const cx = await br.newContext({ viewport: { width: w, height: h }, hasTouch: true, isMobile: true, deviceScaleFactor: 2 }), pg = await cx.newPage();
    await pg.goto(srv.url); await pg.waitForTimeout(2500);
    const o = out['p' + w] = {};
    const swipe = async () => {
      const cdp = await cx.newCDPSession(pg);
      const pt = x => [{ x, y: 400 > h - 120 ? 300 : 400 }];
      await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: pt(80) });
      for (let x = 100; x <= 300; x += 20) { await cdp.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: pt(x) }); await pg.waitForTimeout(16); }
      await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] }); await pg.waitForTimeout(700);
      return pg.evaluate(() => ({ body: document.body.className, html: document.documentElement.className, nav: Math.round(document.querySelector('#nav').getBoundingClientRect().x) }));
    };
    await pg.evaluate(() => { const d = document.createElement('div'); d.id = 'stub'; d.style.cssText = 'position:fixed;inset:0;z-index:10010;background:rgba(0,0,0,.3)'; document.body.appendChild(d); });
    o.before = await pg.evaluate(() => ({ body: document.body.className, html: document.documentElement.className, nav: Math.round(document.querySelector('#nav').getBoundingClientRect().x) }));
    o.swipeOnStub = await swipe();
    // notices with a 200 px panel docked 8 px above the capsule
    await pg.evaluate(() => { document.dispatchEvent(new Event('x')); });
    o.mbar = await rect(pg, '#mbar');
    o.notes = await pg.evaluate(() => { const r = {}; ['.axupdate', '.axoffline'].forEach(s => { const e = document.querySelector(s); r[s] = e ? [getComputedStyle(e).display, JSON.stringify(e.getBoundingClientRect().toJSON())] : null; }); return r; });
    await cx.close();
  }
  console.log(JSON.stringify(out, null, 1)); await br.close(); srv.close();
})();
