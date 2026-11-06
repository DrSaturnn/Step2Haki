#!/usr/bin/env node
/* subset_check.js: which in-between light rules get a token (s164b chunk 6b0 step 2). For each candidate from
   `python3 repair/s164b/tokenize.py --candidates` (theme key K, property P, light selectors B that the theme rule outranked
   on B's rule), whether every element B matches on the before page also matches K. Then the theme
   value showed on all of B's elements before, and B's token carries it after the conversion.
   node repair/s164b/subset_check.js local/s164b/before.html [--views desk,phone] [--configs flat-dark-read,...]
   Writes repair/s164b/data/token_extra.json {extra: {"K|P": [B, ...]}, fail, empty, invalid}. Pseudo-elements and user-action
   pseudo-classes (:hover, :focus, :focus-visible, :focus-within, :active) are removed from both selectors before matching;
   a pair is kept only when K's state pseudo-classes and pseudo-element are all on B too (else listed under state);
   a B matching no element in every run is listed under empty and gets no token. */
'use strict';
const fs = require('fs'), path = require('path');
const VIEWS = { desk: { width: 1512, height: 945 }, tablet: { width: 1024, height: 768 }, phone: { width: 390, height: 844, isMobile: true, hasTouch: true } };
const CONFIGS = { 'flat-dark-read': { 'ax-theme': 'dark' }, 'sculpted-dark-read': { 'ax-flat': '0', 'ax-theme': 'dark' },
  'flat-tinted-read': { 'ax-theme': 'tinted' }, 'flat-dark-recall': { 'ax-theme': 'dark', 'ax-study': '1' } };
function arg(a, k, d) { const i = a.indexOf(k); return i >= 0 ? a[i + 1] : d; }
const strip = s => s.replace(/::?(before|after|placeholder|marker|selection|first-line|first-letter|-webkit-[\w-]+)\b/g, '')
  .replace(/:(hover|focus-visible|focus-within|focus|active)\b/g, '').replace(/\s+/g, ' ').trim();
// K's state pseudo-classes must all be on B too (B :hover inside K is a subset; the reverse is not); the pseudo-elements
// are the same on both (a theme rule on the element does not reach its ::before)
const states = s => (s.match(/::?(hover|focus-visible|focus-within|focus|active|before|after|placeholder|marker|selection|first-line|first-letter)\b/g) || []).map(x => x.replace(/^::?/, '')).sort();
const pe = s => (s.match(/::?(before|after|placeholder|marker|selection|first-line|first-letter)\b/g) || []).map(x => x.replace(/^::?/, '')).sort().join();
const stateSubset = (k, b) => { if (pe(k) !== pe(b)) return false; const bs = states(b); return states(k).every(x => { const i = bs.indexOf(x); if (i < 0) return false; bs.splice(i, 1); return true; }); };
// sels: stripped selectors; pairs: [bIndex, kIndex]. Per pair: -1 a selector is invalid, -2 some B element is not a K
// element, else the number of B elements
const EVAL = ({ sels, pairs }) => {
  const id = new Map(); let next = 0;
  const memo = new Map();
  const els = i => { if (memo.has(i)) return memo.get(i); let v; try { v = Array.from(document.querySelectorAll(sels[i]), e => { if (!id.has(e)) id.set(e, next++); return id.get(e); }); } catch (e) { v = null; } memo.set(i, v); return v; };
  const sets = new Map();
  const set = i => { if (!sets.has(i)) { const v = els(i); sets.set(i, v && new Set(v)); } return sets.get(i); };
  return pairs.map(([bi, ki]) => { const B = els(bi), K = set(ki); if (!B || !K) return -1; for (const e of B) if (!K.has(e)) return -2; return B.length; });
};
(async () => {
  const a = process.argv.slice(2), page = a[0];
  const cand = JSON.parse(fs.readFileSync(path.join(__dirname, '../../local/s164b/extra_candidates.json')));
  const sels = [], ix = new Map(), pairs = [], meta = [];
  const at = s => { const t = strip(s); if (!ix.has(t)) { ix.set(t, sels.length); sels.push(t); } return ix.get(t); };
  for (const [b, ks] of Object.entries(cand)) for (const [k, props] of Object.entries(ks)) {
    if (!stateSubset(k, b)) { meta.push([b, k, props, 'state']); continue; }
    pairs.push([at(b), at(k)]); meta.push([b, k, props, pairs.length - 1]);
  }
  const { chromium } = require('playwright'); const browser = await chromium.launch();
  const runs = {};
  for (const view of arg(a, '--views', 'desk,phone').split(',')) for (const cfg of arg(a, '--configs', 'flat-dark-read,sculpted-dark-read,flat-tinted-read').split(',')) {
    const V = VIEWS[view];
    const ctx = await browser.newContext({ viewport: { width: V.width, height: V.height }, isMobile: !!V.isMobile, hasTouch: !!V.hasTouch });
    await ctx.addInitScript(s => { try { localStorage.clear(); for (const k in s) localStorage.setItem(k, s[k]); } catch (e) {} }, CONFIGS[cfg]);
    const p = await ctx.newPage(); p.setDefaultTimeout(1800000);
    await p.goto('file://' + path.resolve(page), { waitUntil: 'load', timeout: 600000 }); await p.waitForTimeout(2500);
    const r = await p.evaluate(EVAL, { sels, pairs });
    runs[view + '/' + cfg] = r; await ctx.close();
    process.stdout.write(view + '/' + cfg + ' done\n');
  }
  await browser.close();
  const out = { extra: {}, fail: {}, empty: {}, invalid: {}, runs: Object.keys(runs) };
  out.state = {};
  const R = Object.values(runs);
  for (const [b, k, props, j] of meta) {
    const put = o => { for (const pr of props) (o[k + '|' + pr] = o[k + '|' + pr] || []).push(b); };
    if (j === 'state') { put(out.state); continue; }
    const rs = R.map(r => r[j]);
    if (rs.includes(-1)) put(out.invalid);
    else if (rs.includes(-2)) put(out.fail);
    else if (rs.every(x => x === 0)) put(out.empty);
    else put(out.extra);
  }
  const keep = o => Object.fromEntries(Object.entries(o).map(([kp, v]) => [kp, v.length]));
  out.fail = keep(out.fail); out.empty = keep(out.empty); out.state = keep(out.state);   // counts only: the lists are long
  fs.writeFileSync(path.join(__dirname, 'data', 'token_extra.json'), JSON.stringify(out, null, 1));
  const n = o => Object.values(o).reduce((s, v) => s + (typeof v === 'number' ? v : v.length), 0);
  console.log('pairs', meta.length, 'extra', n(out.extra), 'state', n(out.state), 'fail', n(out.fail), 'empty', n(out.empty), 'invalid', n(out.invalid));
})().catch(e => { console.error(e); process.exit(1); });
