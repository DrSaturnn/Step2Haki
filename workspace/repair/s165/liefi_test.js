// liefi_test: the device reports a connection but the server cannot be reached (weak signal). After the worker has
// saved the site, the server goes away with the network still "online"; the reload comes from the saved copy and the
// version check's failure shows the offline note. Also screenshots the note in the dark theme.
//   node repair/s165/liefi_test.js PAGE [--shots DIR]
'use strict';
const path = require('path'); const { chromium } = require('playwright'); const { serve } = require('../../tools/serve_page');
const page = process.argv[2], shots = process.argv.includes('--shots') ? process.argv[process.argv.indexOf('--shots') + 1] : null;
(async () => {
  const srv = await serve(page); const socks = new Set(); srv.on('connection', s => { socks.add(s); s.on('close', () => socks.delete(s)); });
  const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 1512, height: 945 }, deviceScaleFactor: shots ? 2 : 1 });
  const p = await ctx.newPage();
  await p.goto(srv.url, { waitUntil: 'load' });
  await p.waitForFunction(() => navigator.serviceWorker.controller, null, { timeout: 60000 });
  await new Promise(r => { srv.close(() => r()); socks.forEach(s => s.destroy()); });
  await p.reload({ waitUntil: 'load' });
  const before = await p.evaluate(() => !!document.querySelector('.axoffline.on'));
  const shown = await p.waitForSelector('.axoffline.on', { timeout: 15000 }).then(() => true).catch(() => false);
  const txt = await p.evaluate(() => { const n = document.querySelector('.axoffline'); return n ? n.textContent : ''; });
  if (shots) {
    await p.evaluate(() => document.documentElement.setAttribute('data-theme', 'dark')); await p.waitForTimeout(500);
    await p.screenshot({ path: path.join(shots, 'desk_offline_dark.png'), clip: { x: 1512 - 450, y: 945 - 130, width: 450, height: 130 } });
  }
  console.log(JSON.stringify({ onLine: await p.evaluate(() => navigator.onLine), noteBeforeCheck: before, noteAfterCheck: shown, text: txt }));
  await b.close();
})();
