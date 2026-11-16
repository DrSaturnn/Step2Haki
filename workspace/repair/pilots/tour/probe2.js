'use strict';
const path = require('path');
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const { serve } = require(path.join(__dirname, '../../../tools/serve_page'));
const PAGE = path.join(__dirname, '../../../index.html');
(async () => {
  const srv = await serve(PAGE), out = {};
  const br = await chromium.launch({ executablePath: '/usr/bin/google-chrome' });
  for (const [w, h] of [[1101, 800], [1280, 720], [1440, 900]]) {
    const cx = await br.newContext({ viewport: { width: w, height: h } }), pg = await cx.newPage();
    await pg.goto(srv.url + '#scaphoid'); await pg.waitForTimeout(4000);
    out['d' + w] = await pg.evaluate(() => { const q = s => { const e = document.querySelector(s); if(!e) return null; const r = e.getBoundingClientRect(); return [r.x, r.y, r.width, r.height].map(Math.round).join(','); };
      return { rail: q('#nav .axn-rail'), n: document.querySelectorAll('#nav .axn-rail .axn-s').length, tile: q('#nav .axn-rail') && (function(){ const p = document.querySelector('#nav .axn-rail').previousElementSibling; const r = p.getBoundingClientRect(); return p.className + ' ' + [r.x, r.y, r.width, r.height].map(Math.round).join(','); })(), sy: Math.round(scrollY) }; });
    await cx.close();
  }
  for (const [w, h] of [[375, 667], [393, 852]]) {
    const cx = await br.newContext({ viewport: { width: w, height: h }, hasTouch: true, isMobile: true, deviceScaleFactor: 2 }), pg = await cx.newPage();
    await pg.goto(srv.url); await pg.waitForTimeout(2500);
    out['p' + w] = await pg.evaluate(() => { const r = {};
      const u = document.createElement('div'); u.className = 'axupdate'; u.innerHTML = '<span>A newer version is ready.</span><button>Refresh</button>'; document.body.appendChild(u);
      const o = document.createElement('div'); o.className = 'axoffline'; o.textContent = 'Offline: showing the saved copy'; document.body.appendChild(o);
      ['.axupdate', '.axoffline', '#mbar'].forEach(s => { const e = document.querySelector(s), b = e.getBoundingClientRect(); r[s] = [b.x, b.y, b.width, b.height].map(Math.round).join(',') + ' z' + getComputedStyle(e).zIndex; }); return r; });
    await cx.close();
  }
  console.log(JSON.stringify(out, null, 1)); await br.close(); srv.close();
})();
