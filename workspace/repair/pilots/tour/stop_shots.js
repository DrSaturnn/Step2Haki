// tour stop 1: screenshots and the measured ring and panel rects at six sizes; dark and tinted at one phone and one desktop size
'use strict';
const path = require('path');
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const { serve } = require(path.join(__dirname, '../../../tools/serve_page'));
const PAGE = process.argv[2], OUT = process.argv[3];
const SIZES = [[375, 667, 1], [393, 852, 1], [430, 932, 1], [1101, 800, 0], [1280, 720, 0], [1440, 900, 0]];
(async () => {
  const srv = await serve(PAGE), out = {};
  const br = await chromium.launch({ executablePath: '/usr/bin/google-chrome' });
  const shot = async (w, h, phone, theme) => {
    const cx = await br.newContext(phone ? { viewport: { width: w, height: h }, hasTouch: true, isMobile: true, deviceScaleFactor: 2 } : { viewport: { width: w, height: h }, deviceScaleFactor: 1 });
    if (theme !== 'light') await cx.addInitScript(t => { try { localStorage.setItem('ax-settings', JSON.stringify({ v: 1, s: { theme: t } })); } catch (e) {} }, theme);
    const pg = await cx.newPage(); const errs = []; pg.on('pageerror', e => errs.push(e.message));
    await pg.goto(srv.url); await pg.waitForSelector('#axtour.in', { timeout: 15000 }); await pg.waitForTimeout(900);
    await pg.evaluate(() => document.querySelector('#axtour .tr-go').click());
    await pg.waitForTimeout(1200);
    const k = (phone ? 'p' : 'd') + w + '_' + theme;
    out[k] = await pg.evaluate(() => {
      const q = s => { const r = document.querySelector(s).getBoundingClientRect(); return [r.x, r.y, r.width, r.height].map(Math.round).join(','); };
      const p = document.querySelector('#axtour .tr-panel'), bar = document.getElementById('mbar');
      return { ring: q('#axtour .tr-ring'), panel: q('#axtour .tr-panel'), scroll: p.scrollHeight > p.clientHeight, mbar: bar ? q('#mbar') : '', mode: document.getElementById('axtour').getAttribute('data-m'), side: document.getElementById('axtour').getAttribute('data-side'), lost: document.getElementById('axtour').classList.contains('lost'), inert: [...document.body.children].filter(e => e.inert).length, focus: document.activeElement.className, flag: JSON.parse(localStorage.getItem('ax-settings') || '{}').s && JSON.parse(localStorage.getItem('ax-settings')).s.tour };
    });
    out[k].errs = errs;
    await pg.screenshot({ path: path.join(OUT, 'stop1_' + k + '.png') });
    await cx.close();
  };
  for (const [w, h, p] of SIZES) await shot(w, h, p, 'light');
  for (const t of ['dark', 'tinted']) { await shot(393, 852, 1, t); await shot(1280, 720, 0, t); }
  console.log(JSON.stringify(out, null, 1)); await br.close(); srv.close();
})();
