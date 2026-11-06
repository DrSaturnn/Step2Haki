#!/usr/bin/env node
// perf_load: load-time and element-count measurement for a built page.
//
//   node tools/perf_load.js PAGE [--runs 3] [--views desk,phone] [--json OUT] [--hash brief-id]
//
// Serves PAGE's folder over a local HTTP server and loads it in Chromium. Per view, per run:
//   fcp     first contentful paint (ms from navigation start)
//   dcl     DOMContentLoaded event end
//   load    load event end
//   ready   end of the last long task before 1.5 s with no long task (main thread settled)
//   tbt     total blocking time from navigation to ready (sum of long task time over 50 ms)
//   el_dcl, el_load, el_ready   document element count at those points
//   heap    JS heap used at ready (MB)
// The phone view emulates a 390x844 touch screen with the CPU slowed 4x. The median of the runs is printed.
'use strict';
const http = require('http');
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

function args() {
  const a = process.argv.slice(2), o = { runs: 3, views: ['desk', 'phone'], json: null, hash: '' };
  o.page = a[0];
  for (let i = 1; i < a.length; i++) {
    if (a[i] === '--runs') o.runs = +a[++i];
    else if (a[i] === '--views') o.views = a[++i].split(',');
    else if (a[i] === '--json') o.json = a[++i];
    else if (a[i] === '--hash') o.hash = a[++i];
  }
  if (!o.page) { console.error('usage: perf_load.js PAGE [--runs N] [--views desk,phone] [--json OUT] [--hash id]'); process.exit(2); }
  return o;
}

function serve(file) {
  const dir = path.dirname(path.resolve(file)), name = path.basename(file);
  const srv = http.createServer((req, res) => {
    const u = decodeURIComponent(req.url.split('?')[0]);
    const p = u === '/' ? path.join(dir, name) : path.join(dir, u);
    if (!p.startsWith(dir) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); res.end(); return; }
    const type = p.endsWith('.html') ? 'text/html; charset=utf-8' : p.endsWith('.json') ? 'application/json' : 'application/octet-stream';
    res.writeHead(200, { 'content-type': type });
    fs.createReadStream(p).pipe(res);
  });
  return new Promise(r => srv.listen(0, '127.0.0.1', () => r(srv)));
}

const VIEWS = {
  desk: { viewport: { width: 1512, height: 945 }, deviceScaleFactor: 1, cpu: 1 },
  phone: { viewport: { width: 390, height: 844 }, deviceScaleFactor: 1, isMobile: true, hasTouch: true, cpu: 4 },
};

const INIT = `(() => {
  const P = window.__perf = { lt: [], el: {} };
  try { new PerformanceObserver(l => { for (const e of l.getEntries()) P.lt.push([e.startTime, e.duration]); })
    .observe({ type: 'longtask', buffered: true }); } catch (e) {}
  const count = () => document.getElementsByTagName('*').length;
  document.addEventListener('DOMContentLoaded', () => { P.el.dcl = count(); }, { capture: true, once: true });
  window.addEventListener('load', () => { setTimeout(() => { P.el.load = count(); }, 0); }, { once: true });
})();`;

async function once(browser, view, url) {
  const v = VIEWS[view];
  const ctx = await browser.newContext({ viewport: v.viewport, deviceScaleFactor: v.deviceScaleFactor, isMobile: !!v.isMobile, hasTouch: !!v.hasTouch });
  await ctx.addInitScript(INIT);
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', e => errors.push(String(e.message || e)));
  const cdp = await ctx.newCDPSession(page);
  await cdp.send('Emulation.setCPUThrottlingRate', { rate: v.cpu });
  await cdp.send('Network.enable');
  await cdp.send('Network.setCacheDisabled', { cacheDisabled: true });
  await page.goto(url, { waitUntil: 'load', timeout: 180000 });
  // settle: 1.5 s with no new long task
  let last = -1, quiet = 0;
  for (let i = 0; i < 120 && quiet < 3; i++) {
    await page.waitForTimeout(500);
    const n = await page.evaluate(() => window.__perf.lt.length);
    if (n === last) quiet++; else { quiet = 0; last = n; }
  }
  const r = await page.evaluate(() => {
    const nav = performance.getEntriesByType('navigation')[0];
    const fcp = (performance.getEntriesByName('first-contentful-paint')[0] || {}).startTime || 0;
    const P = window.__perf;
    const lt = P.lt.slice().sort((a, b) => a[0] - b[0]);
    const ready = Math.max(nav.loadEventEnd, lt.length ? lt[lt.length - 1][0] + lt[lt.length - 1][1] : 0);
    const tbt = lt.reduce((s, x) => s + Math.max(0, x[1] - 50), 0);
    const longest = lt.reduce((m, x) => Math.max(m, x[1]), 0);
    return {
      fcp: Math.round(fcp), dcl: Math.round(nav.domContentLoadedEventEnd), load: Math.round(nav.loadEventEnd),
      ready: Math.round(ready), tbt: Math.round(tbt), longest: Math.round(longest),
      el_dcl: P.el.dcl, el_load: P.el.load, el_ready: document.getElementsByTagName('*').length,
      briefs_built: document.querySelectorAll('.brief').length - document.querySelectorAll('.brief > template.axl').length,
      heap: performance.memory ? Math.round(performance.memory.usedJSHeapSize / 1048576) : null,
    };
  });
  r.errors = errors.length;
  await ctx.close();
  return r;
}

function median(rows, k) {
  const v = rows.map(r => r[k]).filter(x => x != null).sort((a, b) => a - b);
  return v.length ? v[Math.floor((v.length - 1) / 2)] : null;
}

(async () => {
  const o = args();
  const srv = await serve(o.page);
  const url = 'http://127.0.0.1:' + srv.address().port + '/' + (o.hash ? '#' + o.hash : '');
  const browser = await chromium.launch();
  const out = { page: o.page, size: fs.statSync(o.page).size, views: {} };
  for (const view of o.views) {
    const rows = [];
    for (let i = 0; i < o.runs; i++) rows.push(await once(browser, view, url));
    const keys = Object.keys(rows[0]);
    const med = {};
    keys.forEach(k => { med[k] = median(rows, k); });
    out.views[view] = { median: med, runs: rows };
    console.log(view + ' ' + keys.map(k => k + '=' + med[k]).join(' '));
  }
  await browser.close();
  srv.close();
  if (o.json) fs.writeFileSync(o.json, JSON.stringify(out, null, 1));
})().catch(e => { console.error(e); process.exit(1); });
