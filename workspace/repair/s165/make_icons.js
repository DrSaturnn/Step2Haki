// make_icons: draws the app icons from the sidebar brand mark (#nav .brand .mark: "S2", weight 800, white on #15151B,
// font 11px in a 38px tile, radius 11px, letter spacing .5px) at icon sizes, into workspace/site/pwa/icons/.
//   node repair/s165/make_icons.js
'use strict';
const path = require('path');
const { chromium } = require('playwright');
const OUT = path.join(__dirname, '..', '..', 'site', 'pwa', 'icons');
const icons = [
  { file: 'icon-192.png', size: 192, round: true },
  { file: 'icon-512.png', size: 512, round: true },
  { file: 'icon-maskable-512.png', size: 512, round: false },
  { file: 'apple-touch-icon.png', size: 180, round: false },
];
(async () => {
  const b = await chromium.launch();
  for (const ic of icons) {
    const p = await b.newPage({ viewport: { width: ic.size, height: ic.size }, deviceScaleFactor: 1 });
    const s = ic.size, k = s / 38;
    await p.setContent(`<html><body style="margin:0;background:transparent">
      <div style="width:${s}px;height:${s}px;display:flex;align-items:center;justify-content:center;background:#15151B;
        border-radius:${ic.round ? 11 * k : 0}px;color:#fff;font:800 ${11 * k}px/1 Inter,system-ui,sans-serif;
        letter-spacing:${0.5 * k}px;text-indent:${0.5 * k}px">S2</div></body></html>`);
    await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: path.join(OUT, ic.file), omitBackground: true });
    await p.close();
  }
  await b.close();
  console.log('icons: ' + icons.map(i => i.file).join(', '));
})();
