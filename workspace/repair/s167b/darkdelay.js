const { chromium } = require('playwright');
const pages = process.argv.slice(2);
(async () => {
  const b = await chromium.launch();
  for (const p of pages) {
    const pg = await b.newPage({ viewport: { width: 1440, height: 900 } });
    await pg.goto('file://' + p + '?shelf=step2'); await pg.waitForTimeout(3000);
    const r = await pg.evaluate(async () => {
      const btn = document.querySelector('#modes button.dark:not(.tint)'); if (!btn) return 'no button';
      const bg = () => getComputedStyle(document.body).backgroundColor + ' / html ' + getComputedStyle(document.documentElement).backgroundColor;
      const t0 = performance.now(); btn.click(); const out = [];
      let last = '';
      while (performance.now() - t0 < 4000) {
        await new Promise(r => requestAnimationFrame(r));
        const v = bg() + ' root=' + document.documentElement.getAttribute('data-theme');
        if (v !== last) { out.push(Math.round(performance.now() - t0) + 'ms ' + v); last = v; }
      }
      return out.join('\n');
    });
    console.log('==', p, '\n' + r);
    await pg.close();
  }
  await b.close();
})();
