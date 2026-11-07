// every brief in Two-pane: its text with the added labels and repeated headers taken out equals its text in Scrolling
const { chromium } = require('playwright');
const { serve } = require('/home/claude/Step2Haki/workspace/tools/serve_page.js');
const [,, page, W='1512', H='945', limit='999'] = process.argv;
(async () => {
  const srv = await serve(page);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: +W, height: +H } });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.addInitScript(() => { window.T = function(B){ const c = B.cloneNode(true); c.querySelectorAll('.ax2-cont, thead[aria-hidden="true"], .bb-bar, .bb-rail, .bb-end').forEach(x => x.remove()); return c.textContent.replace(/\s+/g, ''); }; });
  await p.goto(srv.url + '#chf', { waitUntil: 'load' }); await p.waitForTimeout(2000);
  const ids = await p.evaluate(() => [...document.querySelectorAll('main .wrap > .brief[id]')].map(x => x.id));
  const before = await p.evaluate(ids => { const o = {}; ids.forEach(id => { AX.brief.ensure(id); o[id] = T(document.getElementById(id)); }); return o; }, ids);
  await p.evaluate(() => document.querySelector('#modes .layout button[data-v="two"]').click()); await p.waitForTimeout(1200);
  const bad = [], stats = [];
  for (const id of ids.slice(0, +limit)) {
    await p.evaluate(id => { location.hash = id; }, id); await p.waitForTimeout(450);
    const r = await p.evaluate(id => {
      const B = document.getElementById(id); if (!B.classList.contains('ax2-cur')) return { id, err: 'not current' };
      const c = B.cloneNode(true); return { id, t: T(B), pages: B.querySelectorAll('.ax2-page').length, screens: +(document.documentElement.scrollHeight / innerHeight).toFixed(2) };
    }, id);
    if (r.err || r.t !== before[id]) bad.push(r.err ? r : { id, lenA: before[id].length, lenB: r.t.length }); else stats.push([id, r.pages, r.screens]);
  }
  await p.evaluate(() => document.querySelector('#modes .layout button[data-v="scroll"]').click()); await p.waitForTimeout(800);
  const after = await p.evaluate(ids => { const o = {}; ids.forEach(id => { o[id] = T(document.getElementById(id)); }); return o; }, ids);
  const restoreBad = ids.slice(0, +limit).filter(id => after[id] !== before[id]);
  const sc = stats.map(s => s[2]).sort((a, b) => a - b);
  console.log(JSON.stringify({ checked: Math.min(ids.length, +limit), ok: stats.length, bad: bad.slice(0, 10), nbad: bad.length, restoreBad: restoreBad.slice(0, 10), nRestoreBad: restoreBad.length,
    screensMedian: sc[Math.floor(sc.length / 2)], screensMax: sc[sc.length - 1], longest: stats.sort((a, b) => b[2] - a[2]).slice(0, 5), errs: errs.slice(0, 5) }));
  await b.close(); process.exit(0);
})();
