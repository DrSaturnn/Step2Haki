#!/usr/bin/env node
// search_index: the prebuilt search index for a built page (s164c, D-20261106-4).
//
//   node tools/search_index.js PAGE OUT          write the index for PAGE to OUT (minified JSON)
//   node tools/search_index.js --check PAGE [FILE]
//        FILE (default: search.json beside PAGE) must list every brief on PAGE and equal a fresh dump; exit 1 if not
//
// Loads PAGE?axall in Chromium (every brief built, as a reader would see it) and calls window.__axSearch.dump(): the
// search record of every brief, read from the built page by the same code the page uses. Math.random is seeded so the
// bank option order (shuffled at every build) is the same on every dump, and two dumps of one page are byte-equal.
//
// Format (v 1):
//   briefs  [{id, title, sub, blocks: [[label, rank, bank, raw, mr, stemEnd?], ...]}, ...] in page order
//           raw: the block text, whitespace collapsed; mr: masked ranges [[start, end], ...] in raw; bank: item index
//           or -1; stemEnd (bank items only): length of the unmasked part
//   groups  alias groups (the hand map, then "ACRONYM (expansion)" pairs found in brief text), normalized phrases
//   oneway  one-way alias phrases
// The page rebuilds the folded text (sxNorm) on load, so the file carries raw text only.
'use strict';
const fs = require('fs');
const os = require('os');
const path = require('path');
const { chromium } = require('playwright');

const SEED = `(() => { let s = 20261106; Math.random = () => { s = (s * 16807) % 2147483647; return (s - 1) / 2147483646; }; })();`;

async function dump(page) {
  const browser = await chromium.launch();
  try {
    const ctx = await browser.newContext({ viewport: { width: 1512, height: 945 } });
    await ctx.addInitScript(SEED);
    const p = await ctx.newPage();
    const errors = [];
    p.on('pageerror', e => errors.push(String(e)));
    await p.goto('file://' + path.resolve(page) + '?axall', { waitUntil: 'load', timeout: 300000 });
    await p.waitForFunction(() => window.__axSearch && window.AX && AX.brief && !AX.brief.pending().length, null, { timeout: 300000 });
    const d = await p.evaluate(() => {
      const d = window.__axSearch.dump();
      d.ids = Array.from(document.querySelectorAll('.brief')).map(b => b.id).filter(Boolean);
      return d;
    });
    if (errors.length) throw new Error('page errors: ' + errors.slice(0, 3).join(' | '));
    return d;
  } finally {
    await browser.close();
  }
}

function text(d) {
  const o = { v: d.v, briefs: d.briefs, groups: d.groups, oneway: d.oneway };
  return JSON.stringify(o);
}

(async () => {
  const a = process.argv.slice(2);
  if (a[0] === '--check') {
    const page = a[1];
    if (!page) { console.error('usage: search_index.js --check PAGE [FILE]'); process.exit(2); }
    const file = a[2] || path.join(path.dirname(path.resolve(page)), 'search.json');
    if (!fs.existsSync(file)) { console.log('search_index check: FAIL (no ' + file + ')'); process.exit(1); }
    const have = fs.readFileSync(file, 'utf8');
    const d = await dump(page);
    const fresh = text(d);
    let listed = [];
    try { listed = JSON.parse(have).briefs.map(b => b.id); } catch (e) { console.log('search_index check: FAIL (unreadable ' + file + ')'); process.exit(1); }
    const missing = d.ids.filter(id => listed.indexOf(id) < 0), extra = listed.filter(id => d.ids.indexOf(id) < 0);
    if (have === fresh) { console.log('search_index check: PASS (' + d.ids.length + ' briefs, ' + have.length + ' bytes)'); process.exit(0); }
    let first = '';
    if (!missing.length && !extra.length) {
      const A = JSON.parse(have).briefs, B = d.briefs;
      for (let i = 0; i < B.length; i++) if (JSON.stringify(A[i]) !== JSON.stringify(B[i])) { first = B[i].id; break; }
      if (!first) first = 'alias groups';
    }
    console.log('search_index check: FAIL (' + path.basename(file) + ' differs from a fresh dump of the page' +
      (missing.length ? '; missing ' + missing.slice(0, 5).join(', ') + (missing.length > 5 ? ' +' + (missing.length - 5) : '') : '') +
      (extra.length ? '; not on the page ' + extra.slice(0, 5).join(', ') : '') + (first ? '; first difference: ' + first : '') +
      '; rebuild with tools/site_build.py)');
    process.exit(1);
  }
  const [page, out] = a;
  if (!page || !out) { console.error('usage: search_index.js PAGE OUT | --check PAGE [FILE]'); process.exit(2); }
  const t0 = Date.now();
  const d = await dump(page);
  const s = text(d);
  const tmp = path.join(os.tmpdir(), 'search-index-' + process.pid + '.json');
  fs.writeFileSync(tmp, s);
  fs.copyFileSync(tmp, out); fs.unlinkSync(tmp);
  console.log('search_index: ' + d.briefs.length + ' briefs, ' + d.groups.length + ' alias groups, ' + s.length + ' bytes -> ' + out + ' (' + (Date.now() - t0) + ' ms)');
})().catch(e => { console.error('search_index: ' + (e && e.message || e)); process.exit(2); });
