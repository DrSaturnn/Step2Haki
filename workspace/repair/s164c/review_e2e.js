// s164c chunk 3 (d): a Review session end to end. node local/s164c/review_e2e.js PAGE [--http]
const { chromium } = require('playwright'); const path = require('path'); const { serve } = require('../../tools/serve_page');
(async () => {
  const page = process.argv[2], http = process.argv.includes('--http');
  const srv = http ? await serve(page) : null, url = srv ? srv.url : 'file://' + path.resolve(page);
  const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 1512, height: 945 } });
  await ctx.addInitScript(() => { if (!localStorage.getItem('ax-rev-profiles')) { localStorage.setItem('ax-rev-profiles', JSON.stringify([{ id: 'ptest', name: 'Test', made: 0 }])); } });
  const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(String(e)));
  await p.goto(url, { waitUntil: 'load' }); await p.waitForTimeout(1500);
  const s = await p.evaluate(() => { const R = __axRev; R.startReview('ptest'); const ids = Array.from(document.querySelectorAll('.rvmark')).map(m => m.closest('.brief').id);
    return { ids, unbuilt: document.querySelectorAll('.brief > template.axl').length }; });
  const out = [];
  for (const [i, id] of s.ids.entries()) {
    // answer the first bank item in the brief, then mark the brief
    const r = await p.evaluate(id => { const q = document.querySelector('#' + CSS.escape(id) + ' .mcq'); if (!q) return 'no item';
      q.scrollIntoView({ block: 'center', behavior: 'instant' }); const o = q.querySelector('.opts button'); o.click(); return q.classList.contains('done') ? 'answered' : 'not answered'; }, id);
    await p.waitForTimeout(400);
    await p.click('#' + id + ' .rvmark button[data-v="' + (i % 2 ? 'no' : 'ok') + '"]'); await p.waitForTimeout(1200);
    out.push([id, r]);
  }
  await p.click('#rvbar .fin'); await p.waitForTimeout(600);
  const d1 = await p.evaluate(() => __axRev.dataOf('ptest'));
  await p.reload({ waitUntil: 'load' }); await p.waitForTimeout(1200);
  const d2 = await p.evaluate(() => __axRev.dataOf('ptest'));
  console.log(JSON.stringify({ session: s, answered: out, box: d1.box, runs: d1.runs, persisted: JSON.stringify(d1.box) === JSON.stringify(d2.box) && d2.runs === d1.runs, errs }));
  await b.close(); if (srv) srv.close();
})();
