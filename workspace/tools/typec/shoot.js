#!/usr/bin/env node
/* shoot.js: screenshot one brief from a preview page in reading and study mode, at phone and desktop widths.
   node tools/typec/shoot.js <preview.html> <brief id> <out dir> [label]
   Writes <label>-<width>-<mode>.png. Needs playwright (the web container has it) and a Chromium under PLAYWRIGHT_BROWSERS_PATH. */
'use strict';
const path = require('path');
const { chromium } = require('playwright');
const [file, bid, out, label = bid] = process.argv.slice(2);
(async () => {
  const exe = process.env.PW_CHROME || undefined;
  const browser = await chromium.launch(exe ? { executablePath: exe } : {});
  for (const w of [390, 1280]) {
    const page = await browser.newPage({ viewport: { width: w, height: 900 }, deviceScaleFactor: Number(process.env.PW_SCALE || 2) });
    await page.goto('file://' + path.resolve(file));
    await page.waitForTimeout(600);
    const el = await page.$('#' + bid);
    if (!el) { console.error('no #' + bid); process.exit(1); }
    for (const mode of ['reading', 'study']) {
      if (mode === 'study') await page.evaluate(() => document.body.classList.add('study'));
      await page.waitForTimeout(150);
      const f = path.join(out, `${label}-${w}-${mode}.png`);
      await el.screenshot({ path: f });
      console.log('wrote', f);
    }
    await page.close();
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
