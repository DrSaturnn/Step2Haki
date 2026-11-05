#!/usr/bin/env node
/* ui_styles.js: computed-style fingerprints of every element (and its ::before and ::after), brief by brief and for the
   page chrome, in one view and theme; a fast, exact companion to the screenshot comparison while CSS is reorganized.

   node tools/ui_styles.js dump PAGE OUT.json [--view desk|phone] [--config NAME] [--briefs a,b] [--detail]
   node tools/ui_styles.js diff A.json B.json [--max 40]

   dump: per brief, one hash per element of every computed property plus its box relative to the brief; with --detail the
   full property maps (for the briefs named). diff: briefs whose hashes differ, and with detailed dumps the properties. */
'use strict';
const fs = require('fs');
const path = require('path');

const VIEWS = { desk: { width: 1512, height: 945 }, phone: { width: 390, height: 844, isMobile: true, hasTouch: true } };
const CONFIGS = {
  'flat-light-read': {}, 'sculpted-light-read': { 'ax-flat': '0' }, 'flat-dark-read': { 'ax-theme': 'dark' },
  'sculpted-dark-read': { 'ax-flat': '0', 'ax-theme': 'dark' }, 'flat-tinted-read': { 'ax-theme': 'tinted' },
  'flat-light-recall': { 'ax-study': '1' }, 'acc-rose-dark': { 'ax-accent': 'rose', 'ax-theme': 'dark' },
  'acc-ocean-light': { 'ax-accent': 'ocean' },
};
const FREEZE = '*,*::before,*::after{content-visibility:visible!important;contain-intrinsic-size:none!important;transition:none!important;animation:none!important;caret-color:transparent!important}';
// fixed choice order and clock, so two runs of one page match
const DETERMINISM = '(function(){var s=20261105;Math.random=function(){s=(Math.imul(s,1103515245)+12345)>>>0;return (s>>>8)/16777216;};})();';
const SIGFN = `window.__axskip = new Set(['transition','transition-duration','transition-timing-function','transition-property','transition-delay',
 'transition-behavior','animation','animation-name','animation-duration','animation-timing-function','animation-delay','animation-iteration-count',
 'animation-direction','animation-fill-mode','animation-play-state','caret-color','animation-composition','animation-range-start','animation-range-end','animation-timeline']);
window.__axh = function(s){ var x = 2166136261 >>> 0; for (var i = 0; i < s.length; i++) { x ^= s.charCodeAt(i); x = Math.imul(x, 16777619) >>> 0; } return x.toString(36); };
window.__axone = function(el, base){ base = base || {left:0, top:0}; var cs = getComputedStyle(el), m = {};
  for (var i = 0; i < cs.length; i++) { var k = cs[i]; if (!__axskip.has(k)) m[k] = cs.getPropertyValue(k); }
  ['::before','::after','::marker','::placeholder'].forEach(function(ps){ var c = getComputedStyle(el, ps);
    if (ps === '::marker' && cs.display !== 'list-item') return;
    if ((ps === '::before' || ps === '::after') && (c.content === 'none' || c.content === 'normal')) return;
    for (var i = 0; i < c.length; i++) { var k = c[i]; if (!__axskip.has(k)) m[ps + k] = c.getPropertyValue(k); } });
  var r = el.getBoundingClientRect(); m['@box'] = (!r.width && !r.height) ? 'empty' : [r.left - base.left, r.top - base.top, r.width, r.height].map(function(v){ return Math.round(v * 2) / 2; }).join(',');
  return m; };
window.__axsig = function(root, id, detail, only, chrome){
  var base = chrome ? {left:0, top:0} : root.getBoundingClientRect();
  var els = chrome ? Array.prototype.filter.call(document.body.querySelectorAll('*'), function(e){ return !e.closest('.brief[id]') && e.tagName !== 'SCRIPT' && e.tagName !== 'STYLE'; })
                   : [root].concat(Array.prototype.slice.call(root.querySelectorAll('*')));
  var hs = [], det = {};
  els.forEach(function(el, i){ var m = __axone(el, base); hs.push(__axh(JSON.stringify(m, Object.keys(m).sort())));
    if (detail && (!only || only.indexOf(i) >= 0)) det[i] = { tag: el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') + (typeof el.className === 'string' && el.className.trim() ? '.' + el.className.trim().split(/\\s+/).join('.') : ''), m: m }; });
  return { n: els.length, hashes: hs, all: __axh(hs.join('')), det: detail ? det : undefined }; };`;
function arg(a, k, d) { const i = a.indexOf(k); return i >= 0 ? a[i + 1] : d; }

async function dump(a) {
  const { chromium } = require('playwright');
  const page = a[1], out = a[2], view = arg(a, '--view', 'desk'), cfg = arg(a, '--config', 'flat-light-read');
  const browser = await chromium.launch();
  const V = VIEWS[view];
  const ctx = await browser.newContext({ viewport: { width: V.width, height: V.height }, isMobile: !!V.isMobile, hasTouch: !!V.hasTouch, deviceScaleFactor: 1 });
  await ctx.addInitScript(s => { try { localStorage.clear(); for (const k in s) localStorage.setItem(k, s[k]); } catch (e) {} }, CONFIGS[cfg]);
  await ctx.addInitScript(DETERMINISM);
  await ctx.clock.setFixedTime(new Date('2026-11-05T12:00:00Z'));
  const p = await ctx.newPage(); p.setDefaultTimeout(600000);
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') errs.push(m.type() + ': ' + m.text()); });
  await p.goto('file://' + path.resolve(page), { waitUntil: 'load', timeout: 600000 });
  await p.evaluate(() => document.fonts && document.fonts.ready);
  await p.waitForTimeout(2500);
  await p.addStyleTag({ content: FREEZE });
  await p.evaluate(() => window.scrollTo(0, 0));
  await p.waitForTimeout(500);
  let want = arg(a, '--briefs') ? arg(a, '--briefs').split(',') : null;
  if (arg(a, '--sample')) { const ids = await p.evaluate(() => [...document.querySelectorAll('.brief[id]')].map(e => e.id)); const k = Math.ceil(ids.length / +arg(a, '--sample')); want = ids.filter((_, i) => i % k === 0); }
  const withChrome = !want || a.includes('--chrome');
  const detail = a.includes('--detail');
  const ids = want || await p.evaluate(() => [...document.querySelectorAll('.brief[id]')].map(e => e.id));
  const only = arg(a, '--idx') ? arg(a, '--idx').split(',').map(Number) : null;   // detail for these element indexes
  await p.evaluate(SIGFN);
  const res = { briefs: {}, chrome: {} };
  for (const id of ids) res.briefs[id] = await p.evaluate(({ id, detail, only }) => window.__axsig(document.getElementById(id), id, detail, only, false), { id, detail, only });
  if (withChrome) {
    res.chrome = await p.evaluate(({ detail, only }) => window.__axsig(document.body, '(chrome)', detail, only, true), { detail, only });
    res.root = await p.evaluate(() => ({ html: window.__axone(document.documentElement), body: window.__axone(document.body) }));
  }
  res.errors = errs; res.view = view; res.config = cfg;
  fs.writeFileSync(out, JSON.stringify(res));
  await browser.close();
  console.log('dump', view, cfg, Object.keys(res.briefs).length, 'briefs', res.chrome.n || 0, 'chrome elements', errs.length, 'console');
}

function diff(a) {
  const A = JSON.parse(fs.readFileSync(a[1])), B = JSON.parse(fs.readFileSync(a[2])), max = +arg(a, '--max', 40);
  const bad = [];
  for (const id of Object.keys(A.briefs)) {
    const x = A.briefs[id], y = B.briefs[id];
    if (!y) { bad.push([id, 'missing']); continue; }
    if (x.all !== y.all) {
      let first = -1, nd = 0;
      for (let i = 0; i < Math.max(x.hashes.length, y.hashes.length); i++) if (x.hashes[i] !== y.hashes[i]) { nd++; if (first < 0) first = i; }
      bad.push([id, 'elements ' + x.n + '/' + y.n + ', differ ' + nd + ', first ' + first]);
      if (x.det && y.det && first >= 0) props(x.det, y.det, max);
      if (!x.det) { const idx = []; for (let i = 0; i < x.hashes.length && idx.length < 30; i++) if (x.hashes[i] !== y.hashes[i]) idx.push(i); console.log('   idx', idx.join(',')); }
    }
  }
  if (A.chrome && A.chrome.hashes && B.chrome) {
    if (A.chrome.all !== B.chrome.all) {
      let nd = 0; for (let i = 0; i < A.chrome.hashes.length; i++) if (A.chrome.hashes[i] !== B.chrome.hashes[i]) nd++;
      bad.push(['(chrome)', 'elements ' + A.chrome.n + '/' + B.chrome.n + ', differ ' + nd]);
      if (A.chrome.det) props(A.chrome.det, B.chrome.det, max); else { const idx = []; for (let i = 0; i < A.chrome.hashes.length && idx.length < 30; i++) if (A.chrome.hashes[i] !== B.chrome.hashes[i]) idx.push(i); console.log('   chrome idx', idx.join(',')); }
    }
    for (const k of ['html', 'body']) {
      const d = Object.keys(A.root[k]).filter(p => A.root[k][p] !== B.root[k][p]);
      if (d.length) bad.push(['(' + k + ')', d.slice(0, 12).map(p => p + ': ' + A.root[k][p] + ' > ' + B.root[k][p]).join('; ')]);
    }
  }
  for (const b of bad) console.log('DIFF', b[0], b[1]);
  console.log(bad.length ? 'STYLES DIFFER: ' + bad.length : 'STYLES SAME', '(' + Object.keys(A.briefs).length + ' briefs)');
  if (JSON.stringify(A.errors) !== JSON.stringify(B.errors)) console.log('console before', JSON.stringify(A.errors).slice(0, 400), '\nconsole after', JSON.stringify(B.errors).slice(0, 400));
}
const GEO = /^(@box|block-size|inline-size|height|width|perspective-origin|transform-origin|min-block-size|min-inline-size|max-block-size|max-inline-size|top|left|right|bottom|inset-[a-z-]+|r|cx|cy|x|y|d)$/;
const a_all = process.argv.includes('--geo');
function props(X, Y, max) {
  let shown = 0;
  for (const i of Object.keys(X)) {
    if (shown >= max) break;
    const x = X[i], y = Y[i]; if (!y) continue;
    let d = Object.keys(Object.assign({}, x.m, y.m)).filter(k => x.m[k] !== y.m[k]);
    const nongeo = d.filter(k => !GEO.test(k));
    if (nongeo.length) d = nongeo; else if (!a_all) continue;
    if (d.length) { shown++; console.log('   [' + i + '] ' + x.tag.slice(0, 90) + ' :: ' + d.slice(0, 8).map(k => k + ': ' + String(x.m[k]).slice(0, 60) + ' > ' + String(y.m[k]).slice(0, 60)).join(' | ')); }
  }
}


async function why(a) {
  const { chromium } = require('playwright');
  const page = a[1], id = a[2], idx = +a[3], prop = a[4], view = arg(a, '--view', 'desk'), cfg = arg(a, '--config', 'flat-light-read');
  const browser = await chromium.launch(); const V = VIEWS[view];
  const ctx = await browser.newContext({ viewport: { width: V.width, height: V.height }, isMobile: !!V.isMobile, hasTouch: !!V.hasTouch });
  await ctx.addInitScript(s => { try { localStorage.clear(); for (const k in s) localStorage.setItem(k, s[k]); } catch (e) {} }, CONFIGS[cfg]);
  await ctx.addInitScript(DETERMINISM);
  const p = await ctx.newPage(); p.setDefaultTimeout(600000);
  await p.goto('file://' + path.resolve(page), { waitUntil: 'load', timeout: 600000 }); await p.waitForTimeout(2500);
  await p.evaluate(({ id, idx }) => { const b = id === '(chrome)' ? null : document.getElementById(id);
    const els = b ? [b, ...b.querySelectorAll('*')] : [...document.body.querySelectorAll('*')].filter(e => !e.closest('.brief[id]') && e.tagName !== 'SCRIPT' && e.tagName !== 'STYLE');
    els[idx].setAttribute('data-axwhy', '1'); }, { id, idx });
  const c = await ctx.newCDPSession(p);
  await c.send('DOM.enable'); await c.send('CSS.enable');
  const doc = await c.send('DOM.getDocument', { depth: 0 });
  const { nodeId } = await c.send('DOM.querySelector', { nodeId: doc.root.nodeId, selector: '[data-axwhy]' });
  const r = await c.send('CSS.getMatchedStylesForNode', { nodeId });
  const props = prop.split(',');
  const show = (label, list) => { for (const m of list || []) { const rule = m.rule; const ds = rule.style.cssProperties.filter(cp => props.includes(cp.name) && cp.text);
      if (!ds.length) continue; const sel = rule.selectorList.text; const lay = (rule.layers || []).map(l => l.text).join('.');
      const med = (rule.media || []).map(x => x.text).join(' & ');
      console.log(label, '[' + (lay || '-') + ']', med ? '@' + med : '', sel.slice(0, 160), '{', ds.map(cp => cp.name + ':' + cp.value + (cp.important ? '!' : '')).join('; '), '}'); } };
  show('match', r.matchedCSSRules);
  for (const inh of r.inherited || []) show('inherit', inh.matchedCSSRules);
  console.log('inline', JSON.stringify((r.inlineStyle && r.inlineStyle.cssProperties || []).filter(cp => props.includes(cp.name)).map(cp => cp.name + ':' + cp.value)));
  await browser.close();
}


// explain A B DIFFJSON_A DIFFJSON_B: for every element whose non-geometric computed style differs, the rule that wins
// each differing property in A and in B (CDP), aggregated; writes OUT.json and prints the most common pairs
async function explain(a) {
  const { chromium } = require('playwright');
  const [, pa, pb, da, db, out] = a; const view = arg(a, '--view', 'desk'), cfg = arg(a, '--config', 'flat-light-read');
  const A = JSON.parse(fs.readFileSync(da)), B = JSON.parse(fs.readFileSync(db));
  const limit = +arg(a, '--per', 60);
  const todo = [];
  for (const id of Object.keys(A.briefs)) { const x = A.briefs[id], y = B.briefs[id]; if (!y || x.all === y.all) continue;
    let k = 0; for (let i = 0; i < x.hashes.length && k < limit; i++) if (x.hashes[i] !== y.hashes[i]) { todo.push([id, i]); k++; } }
  if (A.chrome && A.chrome.hashes) { let k = 0; for (let i = 0; i < A.chrome.hashes.length && k < limit * 3; i++) if (A.chrome.hashes[i] !== B.chrome.hashes[i]) { todo.push(['(chrome)', i]); k++; } }
  const browser = await chromium.launch(); const V = VIEWS[view];
  async function open(page) {
    const ctx = await browser.newContext({ viewport: { width: V.width, height: V.height }, isMobile: !!V.isMobile, hasTouch: !!V.hasTouch });
    await ctx.addInitScript(s => { try { localStorage.clear(); for (const k in s) localStorage.setItem(k, s[k]); } catch (e) {} }, CONFIGS[cfg]);
    await ctx.addInitScript(DETERMINISM);
    const p = await ctx.newPage(); p.setDefaultTimeout(600000);
    await p.goto('file://' + path.resolve(page), { waitUntil: 'load', timeout: 600000 }); await p.waitForTimeout(2500);
    await p.addStyleTag({ content: FREEZE }); await p.evaluate(SIGFN);
    const c = await ctx.newCDPSession(p); await c.send('DOM.enable'); await c.send('CSS.enable');
    return { p, c };
  }
  const PA = await open(pa), PB = await open(pb);
  async function info(P, id, i) {
    const m = await P.p.evaluate(({ id, i }) => { document.querySelectorAll('[data-axwhy]').forEach(e => e.removeAttribute('data-axwhy'));
      const b = id === '(chrome)' ? null : document.getElementById(id);
      const els = b ? [b, ...b.querySelectorAll('*')] : [...document.body.querySelectorAll('*')].filter(e => !e.closest('.brief[id]') && e.tagName !== 'SCRIPT' && e.tagName !== 'STYLE');
      const el = els[i]; if (!el) return null; el.setAttribute('data-axwhy', '1');
      return { m: window.__axone(el, b ? b.getBoundingClientRect() : { left: 0, top: 0 }), tag: el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') + (typeof el.className === 'string' && el.className.trim() ? '.' + el.className.trim().split(/\s+/).slice(0, 3).join('.') : '') }; }, { id, i });
    if (!m) return null;
    const doc = await P.c.send('DOM.getDocument', { depth: 0 });
    const { nodeId } = await P.c.send('DOM.querySelector', { nodeId: doc.root.nodeId, selector: '[data-axwhy]' });
    const r = await P.c.send('CSS.getMatchedStylesForNode', { nodeId });
    return { m: m.m, tag: m.tag, r };
  }
  function winner(r, prop) {
    // matched rules come in ascending cascade order; the last one declaring the property wins (important ones after normal)
    let w = null, wi = null;
    const scan = (list, inh) => { for (const mm of list || []) { const st = mm.rule.style; for (const cp of st.cssProperties) { if (cp.name !== prop || !cp.text || cp.disabled) continue;
      const rec = (inh ? 'inh ' : '') + '[' + ((mm.rule.layers || []).map(l => l.text).join('.') || '-') + '] ' + ((mm.rule.media || []).map(x => '@' + x.text).join(' ')) + ' ' + mm.rule.selectorList.text.slice(0, 150) + ' {' + cp.name + ':' + cp.value + (cp.important ? '!' : '') + '}';
      if (cp.important) wi = rec; else w = rec; } } };
    const ins = (r.inlineStyle && r.inlineStyle.cssProperties || []).find(cp => cp.name === prop && cp.text);
    scan(r.matchedCSSRules, false);
    if (ins && !wi) return 'inline';
    return wi || w;
  }
  const agg = {}; const rows = [];
  for (const [id, i] of todo) {
    const x = await info(PA, id, i), y = await info(PB, id, i); if (!x || !y) continue;
    const d = Object.keys(Object.assign({}, x.m, y.m)).filter(k => x.m[k] !== y.m[k] && !GEO.test(k) && !k.startsWith('::'));
    for (const prop of d.slice(0, 6)) {
      const base = prop.replace(/^(border-(?:block|inline)-(?:start|end)|border-(?:top|right|bottom|left))-color$/, 'border-$1-color');
      const wa = winner(x.r, prop), wb = winner(y.r, prop);
      const key = prop + '\n  A ' + wa + '\n  B ' + wb;
      agg[key] = (agg[key] || 0) + 1; rows.push({ id, i, tag: x.tag, prop, a: x.m[prop], b: y.m[prop], wa, wb });
    }
  }
  fs.writeFileSync(out, JSON.stringify(rows, null, 0));
  const top = Object.entries(agg).sort((p, q) => q[1] - p[1]);
  for (const [k, n] of top.slice(0, +arg(a, '--top', 40))) console.log(n + 'x ' + k);
  console.log('explained', rows.length, 'property differences on', todo.length, 'elements;', top.length, 'distinct');
  await browser.close();
}

const a = process.argv.slice(2);
if (a[0] === 'dump') dump(a).catch(e => { console.error(e); process.exit(1); });
else if (a[0] === 'diff') diff(a);
else if (a[0] === 'explain') explain(a).catch(e => { console.error(e); process.exit(1); });
else if (a[0] === 'why') why(a).catch(e => { console.error(e); process.exit(1); });
else console.log(fs.readFileSync(__filename, 'utf8').split('*/')[0]);
