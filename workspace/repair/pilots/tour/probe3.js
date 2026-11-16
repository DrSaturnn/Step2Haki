'use strict';
const path = require('path');
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const { serve } = require(path.join(__dirname, '../../../tools/serve_page'));
(async () => {
  const srv = await serve(path.join(__dirname, '../../../index.html'));
  const br = await chromium.launch({ executablePath: '/usr/bin/google-chrome' });
  for (const [w, h] of [[1101, 800], [1440, 900]]) {
    const cx = await br.newContext({ viewport: { width: w, height: h } }), pg = await cx.newPage();
    pg.on('pageerror', e => console.log('ERR', e.message));
    await pg.goto(srv.url + '#scaphoid'); await pg.waitForTimeout(3000);
    await pg.mouse.wheel(0, 200); await pg.waitForTimeout(1500);
    console.log(w, JSON.stringify(await pg.evaluate(() => { const q = s => { const e = document.querySelector(s); if(!e) return null; const r = e.getBoundingClientRect(); return [r.x, r.y, r.width, r.height].map(Math.round).join(','); };
      const cls = {}; document.querySelectorAll('#nav [class*=axn-]').forEach(e => { e.className.split(/\s+/).forEach(c => { if(c.indexOf('axn-') === 0) cls[c] = (cls[c] || 0) + 1; }); });
      return { rail: q('#nav .axn-rail'), cur: q('#nav [aria-current]'), curCls: (document.querySelector('#nav [aria-current]') || {}).className, cls, firstHome: (document.querySelector('#nav a[href^="#"]') || {}).outerHTML }; })));
    await pg.screenshot({ path: path.join(__dirname, '../../../local/s176f/d' + w + '_brief.png') });
    await cx.close();
  }
  await br.close(); srv.close();
})();
