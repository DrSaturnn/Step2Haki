#!/usr/bin/env node
// search_parity: compare in-page search between two built pages (s164c, briefs load on demand).
//
//   node tools/search_parity.js BEFORE AFTER --queries FILE [--out OUT.json] [--http]
//
// Loads each page in Chromium (desk view), builds the search index, then for every query (one per line in FILE):
//   hits      brief ids in result order, with the best block's label, rank, words matched and total hits
//   list      the rendered result rows: brief id, block label, whether the snippet is masked (sxm)
//   records   for every brief seen in any hit: the record's text as a sorted word list
// A page argument may carry a query string (cand.html?axall builds every brief at load).
// --http serves each page's folder over local HTTP (tools/serve_page.js), so a page fetches search.json beside it;
// from file:// the fetch fails and the page builds its index in the page (the fallback path). Queries run once the
// index is ready (__axSearch.stats().built).
// Option order in bank items is shuffled at every build, so records compare as word multisets.
// Prints the differences by kind and writes the details to OUT.json. Exit 1 when any query differs.
'use strict';
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');
const { serve } = require('./serve_page');

function args() {
  const a = process.argv.slice(2), o = { out: null, queries: null };
  o.before = a[0]; o.after = a[1];
  for (let i = 2; i < a.length; i++) {
    if (a[i] === '--queries') o.queries = a[++i];
    else if (a[i] === '--out') o.out = a[++i];
    else if (a[i] === '--http') o.http = true;
  }
  if (!o.before || !o.after || !o.queries) { console.error('usage: search_parity.js BEFORE AFTER --queries FILE [--out OUT.json]'); process.exit(2); }
  return o;
}

async function run(browser, page, queries, http) {
  const ctx = await browser.newContext({ viewport: { width: 1512, height: 945 } });
  const p = await ctx.newPage();
  const errors = [];
  p.on('pageerror', e => errors.push(String(e)));
  const [file, qs] = page.split('?');
  const srv = http ? await serve(file) : null;
  await p.goto((srv ? srv.url : 'file://' + path.resolve(file)) + (qs ? '?' + qs : ''), { waitUntil: 'load', timeout: 180000 });
  await p.waitForTimeout(1500);
  await p.evaluate(() => window.__axSearch.build());
  await p.waitForFunction(() => window.__axSearch.stats().built, null, { timeout: 180000 });
  const res = await p.evaluate((qs) => {
    const S = window.__axSearch;
    const builtAt0 = document.querySelectorAll('.brief > template.axl').length;
    const input = document.getElementById('search');
    const out = { queries: {}, records: {} };
    const words = s => s.split(/\s+/).filter(Boolean).sort();
    qs.forEach(q => {
      const r = S.search(q);
      const hits = r.hits.map(x => {
        const k = x.r.blocks[x.best.bi];
        if (!out.records[x.r.id]) out.records[x.r.id] = { all: words(x.r.all).join(' '), blocks: x.r.blocks.map(b => b.label).join('|') };
        return [x.r.id, k.label, k.rank, x.best.m, x.total].join(':');
      });
      input.value = q; S.render();
      const list = Array.from(document.querySelectorAll('#sxres a.sxhit')).map(a =>
        [a.getAttribute('href').slice(1), (a.querySelector('.b') || {}).textContent || '', a.querySelector('.s.sxm') ? 'masked' : 'open'].join(':'));
      out.queries[q] = { hits, other: r.other, list };
    });
    input.value = ''; S.render();
    out.unbuilt = document.querySelectorAll('.brief > template.axl').length;
    out.unbuiltBefore = builtAt0;
    out.stats = S.stats();
    return out;
  }, queries);
  res.errors = errors;
  await ctx.close();
  if (srv) srv.close();
  return res;
}

(async () => {
  const o = args();
  const queries = fs.readFileSync(o.queries, 'utf8').split('\n').map(s => s.trim()).filter(Boolean);
  const browser = await chromium.launch();
  const A = await run(browser, o.before, queries, o.http);
  const B = await run(browser, o.after, queries, o.http);
  await browser.close();
  const diff = { hits: [], other: [], list: [], records: [], blocks: [] };
  queries.forEach(q => {
    const a = A.queries[q], b = B.queries[q];
    if (a.hits.join() !== b.hits.join()) diff.hits.push({ q, before: a.hits, after: b.hits });
    if (a.other !== b.other) diff.other.push({ q, before: a.other, after: b.other });
    if (a.list.join() !== b.list.join()) diff.list.push({ q, before: a.list, after: b.list });
  });
  Object.keys(A.records).forEach(id => {
    const a = A.records[id], b = B.records[id];
    if (!b) return;
    if (a.all !== b.all) diff.records.push({ id });
    if (a.blocks !== b.blocks) diff.blocks.push({ id, before: a.blocks, after: b.blocks });
  });
  const summary = {
    queries: queries.length, briefs_compared: Object.keys(A.records).filter(id => B.records[id]).length,
    differ: { hits: diff.hits.length, other: diff.other.length, list: diff.list.length, records: diff.records.length, blocks: diff.blocks.length },
    after_unbuilt: { before_search: B.unbuiltBefore, after_search: B.unbuilt },
    errors: { before: A.errors.length, after: B.errors.length },
    stats: { before: A.stats, after: B.stats }
  };
  console.log(JSON.stringify(summary, null, 1));
  if (o.out) fs.writeFileSync(o.out, JSON.stringify({ summary, diff, errors: { before: A.errors, after: B.errors }, records: { before: A.records, after: B.records } }, null, 1));
  const bad = Object.values(summary.differ).some(n => n > 0) || B.errors.length > 0;
  process.exit(bad ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2); });
