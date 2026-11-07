// offline_test: offline use end to end on a built candidate.  node repair/s165/offline_test.js PAGE [--phone] [--shots DIR]
// PAGE is a page built by tools/site_build.py (sw.js, manifest, icons and search.json beside it). The test serves it
// over local HTTP, lets the worker save the site, takes the server and the network away, then checks the reload,
// the offline note, search, a sidebar jump, Recall and a Review mark. Then it serves a newer build (stamp s165t,
// written to DIR2 beside PAGE) and checks the update bar, Refresh, the old cache's removal and the new build offline.
'use strict';
const fs = require('fs'), path = require('path'), { execFileSync } = require('child_process');
const { chromium } = require('playwright'); const { serve } = require('../../tools/serve_page');
const WS = path.join(__dirname, '..', '..');
const page = path.resolve(process.argv[2]), phone = process.argv.includes('--phone');
const shots = process.argv.includes('--shots') ? process.argv[process.argv.indexOf('--shots') + 1] : null;
const res = {}, bad = [];
function ok(name, cond, info) { res[name] = cond ? 'ok' : 'FAIL' + (info ? ' (' + info + ')' : ''); if (!cond) bad.push(name); }

function newer() {
  const d = path.join(path.dirname(page), 'v2'); fs.mkdirSync(d, { recursive: true });
  const html = fs.readFileSync(page, 'utf8').replace(/<meta name="ax-build" content="[^"|]*\|/, '<meta name="ax-build" content="s165t|');
  const out = path.join(d, 'index.html'); fs.writeFileSync(out, html);
  fs.copyFileSync(path.join(path.dirname(page), 'search.json'), path.join(d, 'search.json'));
  execFileSync('python3', [path.join(WS, 'tools', 'site_build.py'), out, '--pwa-only'], { cwd: WS });
  fs.writeFileSync(path.join(d, 'version.json'), JSON.stringify({ build: 's165t', date: '2026-11-07' }));
  return out;
}

(async () => {
  const srv = await serve(page); const socks = new Set(); srv.on('connection', s => { socks.add(s); s.on('close', () => socks.delete(s)); });
  const down = () => new Promise(r => { srv.close(() => r()); socks.forEach(s => s.destroy()); });
  const port = new URL(srv.url).port;
  const b = await chromium.launch();
  const vp = phone ? { viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true } : { viewport: { width: 1512, height: 945 } };
  const ctx = await b.newContext(Object.assign({ deviceScaleFactor: shots ? 2 : 1 }, vp));
  await ctx.addInitScript(() => { if (!localStorage.getItem('ax-rev-profiles')) localStorage.setItem('ax-rev-profiles', JSON.stringify([{ id: 'ptest', name: 'Test', made: 0 }])); });
  const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(String(e)));
  const build = () => p.evaluate(() => (document.querySelector('meta[name="ax-build"]').content || '').split('|')[0]);

  // 1. first visit: the worker saves the site
  await p.goto(srv.url, { waitUntil: 'load' });
  await p.waitForFunction(() => navigator.serviceWorker.controller, null, { timeout: 60000 });
  const saved = await p.evaluate(async () => { const out = {}; for (const k of await caches.keys()) out[k] = (await (await caches.open(k)).keys()).map(r => new URL(r.url).pathname + new URL(r.url).search); return out; });
  const keys = Object.keys(saved);
  ok('first visit: one cache, named for the build', keys.length === 1 && keys[0] === 'step2haki-' + await build(), JSON.stringify(keys));
  ok('first visit: page, search.json, manifest, 4 icons saved', keys.length === 1 && saved[keys[0]].length === 7 && ['/', '/search.json', '/manifest.webmanifest'].every(x => saved[keys[0]].includes(x)), JSON.stringify(saved));
  ok('online: no offline note', await p.evaluate(() => !document.querySelector('.axoffline.on')));
  const manifest = await p.evaluate(async () => { const r = await fetch(document.querySelector('link[rel=manifest]').href); return r.json(); });
  ok('manifest: standalone, 192 and 512 icons', manifest.display === 'standalone' && manifest.icons.some(i => i.sizes === '192x192') && manifest.icons.some(i => i.sizes === '512x512'));

  // 2. no server, no network: reload
  await down(); await ctx.setOffline(true);
  const t0 = Date.now(); await p.reload({ waitUntil: 'load' }); const reloadMs = Date.now() - t0;
  ok('offline reload: page served', await p.evaluate(() => document.querySelectorAll('.brief').length) === 209);
  await p.waitForSelector('.axoffline.on', { timeout: 5000 }).catch(() => {});
  const noteTxt = await p.evaluate(() => { const n = document.querySelector('.axoffline.on'); return n ? n.textContent : ''; });
  ok('offline note shown', /^Offline: saved copy from [A-Z][a-z]{2} \d+, \d{4}$/.test(noteTxt), noteTxt);
  if (shots) { await p.waitForTimeout(600); await p.screenshot({ path: path.join(shots, (phone ? 'phone' : 'desk') + '_offline.png') }); }

  // search (index file served by the worker)
  await p.waitForFunction(() => window.__axSearch && ['file', 'page'].includes(__axSearch.stats().mode), null, { timeout: 30000 });
  const sx = await p.evaluate(() => { const st = __axSearch.stats(); const r = __axSearch.search('lithium tremor'); return { mode: st.mode, note: st.note, hits: r.hits.length }; });
  ok('offline search: index file read, hits found', sx.mode === 'file' && sx.hits > 0, JSON.stringify(sx));
  // sidebar jump to an unbuilt brief
  if (!phone) {
    const tid = 'pc-other';
    await p.evaluate(id => document.querySelector('#axn a.axn-b[href="#' + id + '"]').click(), tid); await p.waitForTimeout(1800);
    const j = await p.evaluate(id => { const e = document.getElementById(id); const r = e.getBoundingClientRect(); return { id, built: !e.querySelector(':scope > template.axl'), top: Math.round(r.top) }; }, tid);
    ok('offline sidebar jump: brief built and in view', j.built && j.top > -50 && j.top < 400, JSON.stringify(j));
  } else {
    await p.evaluate(() => { location.hash = 'pc-other'; }); await p.waitForTimeout(1500);
    const j = await p.evaluate(() => { const e = document.getElementById('pc-other'); return { built: !e.querySelector(':scope > template.axl') }; });
    ok('offline link jump: brief built', j.built, JSON.stringify(j));
  }
  // Recall
  const rc = await p.evaluate(() => { const btn = document.querySelector('button[data-m="study"]') || document.querySelector('button[data-act="study"]'); if (!btn) return 'no button'; btn.click(); return document.body.classList.contains('study') ? 'on' : 'off'; });
  ok('offline Recall: turns on', rc === 'on', rc);
  await p.evaluate(() => { const btn = document.querySelector('button[data-m="read"]') || document.querySelector('button[data-act="study"]'); if (btn) btn.click(); });
  // Review: one brief marked, schedule saved on the device
  const rv = await p.evaluate(() => { __axRev.startReview('ptest'); const m = document.querySelector('.rvmark'); return m ? m.closest('.brief').id : ''; });
  let rvOk = false, rvInfo = rv;
  if (rv) {
    await p.evaluate(id => { const q = document.querySelector('#' + CSS.escape(id) + ' .mcq'); if (q) { q.scrollIntoView({ block: 'center', behavior: 'instant' }); q.querySelector('.opts button').click(); } }, rv);
    await p.waitForTimeout(400);
    await p.click('#' + rv + ' .rvmark button[data-v="ok"]'); await p.waitForTimeout(1200);
    await p.click('#rvbar .fin'); await p.waitForTimeout(600);
    const d = await p.evaluate(() => __axRev.dataOf('ptest')); rvOk = !!(d && d.box && Object.keys(d.box).length); rvInfo = rv + ' ' + JSON.stringify(d && d.box);
  }
  ok('offline Review: mark saved on the device', rvOk, rvInfo);
  ok('offline: no page errors', errs.length === 0, errs.slice(0, 3).join(' | '));

  // 3. a newer build ships: the worker saves it, the bar offers Refresh, Refresh loads it
  const v2 = newer();
  // serve v2 on the original port (same origin, same worker scope)
  const same = await new Promise((resolve, reject) => {
    const h = require('http').createServer((req, res) => {
      const u = decodeURIComponent(req.url.split('?')[0]); const dir = path.dirname(v2);
      const f = u === '/' || u === '/index.html' ? v2 : path.join(dir, u);
      if (!f.startsWith(dir) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); res.end(); return; }
      const T = { '.html': 'text/html; charset=utf-8', '.json': 'application/json', '.js': 'text/javascript; charset=utf-8', '.webmanifest': 'application/manifest+json', '.png': 'image/png' };
      res.writeHead(200, { 'content-type': T[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(res);
    });
    h.on('error', reject); h.listen(+port, '127.0.0.1', () => resolve(h));
  });
  await ctx.setOffline(false);
  await p.evaluate(() => window.dispatchEvent(new Event('online')));
  const bar = await p.waitForSelector('.axupdate', { timeout: 90000 }).then(() => true).catch(() => false);
  ok('newer build: update bar after the worker saved it', bar);
  ok('online again: offline note hidden', await p.evaluate(() => !document.querySelector('.axoffline.on')));
  if (shots && bar) await p.screenshot({ path: path.join(shots, (phone ? 'phone' : 'desk') + '_update.png') });
  if (bar) {
    await Promise.all([p.waitForNavigation({ waitUntil: 'load', timeout: 60000 }), p.click('.axupdate button')]);
    ok('Refresh: newer build loaded', await build() === 's165t', await build());
    const k2 = await p.evaluate(() => caches.keys());
    ok('Refresh: old cache removed', k2.length === 1 && k2[0] === 'step2haki-s165t', JSON.stringify(k2));
    await new Promise(r => same.close(r)); await ctx.setOffline(true);
    await p.reload({ waitUntil: 'load' });
    ok('newer build offline: served', await build() === 's165t');
  }
  console.log(JSON.stringify({ view: phone ? 'phone' : 'desk', reloadMs, results: res, failed: bad.length }, null, 1));
  await b.close(); try { same.close(); } catch (e) {}
  process.exit(bad.length ? 1 : 0);
})();
