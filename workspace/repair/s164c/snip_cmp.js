// s164c chunk 4c: compare the rendered search rows (href, block label, snippet text) of two pages over local HTTP.
//   node repair/s164c/snip_cmp.js BEFORE.html AFTER.html QUERIES.txt [--max N] [--show K]
'use strict';
const fs = require('fs');
const { chromium } = require('playwright');
const { serve } = require('../../tools/serve_page');
const [A, B, Q] = process.argv.slice(2);
const arg = (k, d) => { const i = process.argv.indexOf(k); return i > 0 ? +process.argv[i + 1] : d; };
const queries = fs.readFileSync(Q, 'utf8').split('\n').map(s => s.trim()).filter(Boolean).slice(0, arg('--max', 1e9));

async function rows(browser, page) {
  const srv = await serve(page);
  const ctx = await browser.newContext({ viewport: { width: 1512, height: 945 } }); const p = await ctx.newPage();
  await p.goto(srv.url, { waitUntil: 'load' });
  await p.waitForFunction(() => window.__axSearch && (!window.__axSearch.stats || window.__axSearch.stats().ready !== false), null, { timeout: 60000 }).catch(() => {});
  await p.waitForTimeout(5000);
  await p.evaluate(() => window.__axSearch.build && window.__axSearch.build());
  const out = await p.evaluate(qs => {
    const S = window.__axSearch, input = document.getElementById('search'), r = {};
    qs.forEach(q => { input.value = q; S.render();
      r[q] = Array.from(document.querySelectorAll('#sxres a.sxhit')).map(a => [a.getAttribute('href').slice(1), (a.querySelector('.b') || {}).textContent || '', ((a.querySelector('.s') || {}).textContent || '').replace(/\s+/g, ' ').trim()]); });
    input.value = ''; S.render(); return r;
  }, queries);
  await ctx.close(); srv.close(); return out;
}

(async () => {
  const browser = await chromium.launch();
  const x = await rows(browser, A), y = await rows(browser, B);
  await browser.close();
  let nq = 0, nrow = 0, shown = 0; const show = arg('--show', 6);
  for (const q of queries) {
    const a = x[q] || [], b = y[q] || [], byKey = new Map(b.map(r => [r[0] + '|' + r[1], r[2]]));
    let d = 0;
    for (const r of a) { const s = byKey.get(r[0] + '|' + r[1]); if (s !== undefined && s !== r[2]) { d++; if (shown < show) { shown++; console.log('Q ' + q + ' | ' + r[0] + ' ' + r[1] + '\n  before: ' + r[2].slice(0, 160) + '\n  after:  ' + s.slice(0, 160)); } } }
    if (d) { nq++; nrow += d; }
  }
  console.log('queries', queries.length, 'with snippet differences', nq, 'rows', nrow);
})();
