#!/usr/bin/env node
/* ui_parity.js: screenshots of every brief and of the page's open states, in each view and theme, for a before and
   after comparison (tools/ui_parity_diff.py compares two runs).

   node tools/ui_parity.js shoot PAGE OUT [--views desk,phone] [--configs a,b] [--briefs id,id] [--sample N] [--states]
   node tools/ui_parity.js coverage PAGE OUT

   shoot: OUT/<view>-<config>/<brief>.png for every brief (each brief alone on the page, transitions frozen), plus
   OUT/<view>-<config>/_top.png and _nav.png (the page chrome), and with --states OUT/<view>-states/*.png.
   coverage: Chrome CSS and JS coverage over a walk through every theme, mode, state and brief; OUT/coverage.json. */
'use strict';
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const VIEWS = { desk: { width: 1512, height: 945 }, phone: { width: 390, height: 844, isMobile: true, hasTouch: true } };
const ACCENTS = ['indigo', 'purple', 'navy', 'ocean', 'plum', 'rose', 'graphite'];
const CONFIGS = {
  'flat-light-read': {},
  'sculpted-light-read': { 'ax-flat': '0' },
  'flat-dark-read': { 'ax-theme': 'dark' },
  'sculpted-dark-read': { 'ax-flat': '0', 'ax-theme': 'dark' },
  'flat-tinted-read': { 'ax-theme': 'tinted' },
  'flat-light-recall': { 'ax-study': '1' },
};
for (const a of ACCENTS) {
  CONFIGS['acc-' + a + '-light'] = { 'ax-accent': a };
  CONFIGS['acc-' + a + '-dark'] = { 'ax-accent': a, 'ax-theme': 'dark' };
}
const FULL = Object.keys(CONFIGS).filter(k => !k.startsWith('acc-'));
const ACC_SAMPLE = ['hippos', 'mdd', 'kawasaki', 'asthma', 'neonatal-jaundice', 'pc-ssri', 'meningitis', 'bs-shock',
  'cluster-b', 'thyroid', 'dementia', 'ectopic'];
const FREEZE = '*,*::before,*::after{content-visibility:visible!important;contain-intrinsic-size:none!important;transition:none!important;animation:none!important;caret-color:transparent!important;scroll-behavior:auto!important}';

// fixed choice order and clock, so two runs of one page match
const DETERMINISM = '(function(){var s=20261105;Math.random=function(){s=(Math.imul(s,1103515245)+12345)>>>0;return (s>>>8)/16777216;};})();';
function arg(a, k, d) { const i = a.indexOf(k); return i >= 0 ? a[i + 1] : d; }

async function open(browser, page, view, cfg) {
  const ctx = await browser.newContext({ viewport: { width: VIEWS[view].width, height: VIEWS[view].height },
    isMobile: !!VIEWS[view].isMobile, hasTouch: !!VIEWS[view].hasTouch, deviceScaleFactor: 1, reducedMotion: 'no-preference' });
  await ctx.addInitScript(s => { try { localStorage.clear(); for (const k in s) localStorage.setItem(k, s[k]); } catch (e) {} }, cfg);
  await ctx.addInitScript(DETERMINISM);
  await ctx.clock.setFixedTime(new Date('2026-11-05T12:00:00Z'));
  const p = await ctx.newPage();
  p.setDefaultTimeout(240000);
  await p.goto('file://' + path.resolve(page) + '?axall', { waitUntil: 'load', timeout: 240000 });
  await p.evaluate(() => document.fonts && document.fonts.ready);
  await p.waitForTimeout(1500);
  return { ctx, p };
}

async function freeze(p) { await p.addStyleTag({ content: FREEZE }); await p.waitForTimeout(300); }

async function shotBriefs(p, dir, ids) {
  // fixed and sticky elements follow the scroll; they are shot in place on their own (_top, _mid, _nav)
  await p.evaluate(() => { for (const e of document.body.querySelectorAll('*')) { const ps = getComputedStyle(e).position; if (ps === 'fixed' || ps === 'sticky') e.style.setProperty('visibility', 'hidden', 'important'); } });
  for (const id of ids) {
    await p.evaluate(id => { document.querySelectorAll('.brief[id]').forEach(e => { e.style.display = e.id === id ? '' : 'none'; }); window.scrollTo(0, 0); }, id);
    await p.waitForTimeout(450);
    const el = await p.$('#' + CSS_escape(id));
    if (!el) continue;
    try { await el.screenshot({ path: path.join(dir, id + '.png'), timeout: 240000 }); }
    catch (e) { fs.appendFileSync(path.join(dir, '_errors.txt'), id + ' ' + e.message.split('\n')[0] + '\n'); }
  }
  await p.evaluate(() => document.querySelectorAll('.brief[id]').forEach(e => { e.style.display = ''; }));
}
function CSS_escape(s) { return s.replace(/([^a-zA-Z0-9_-])/g, '\\$1'); }

async function chrome(p, dir, view) {
  await p.evaluate(() => window.scrollTo(0, 0));
  await p.waitForTimeout(400);
  await p.screenshot({ path: path.join(dir, '_top.png') });
  await p.evaluate(() => { const b = document.getElementById('mdd'); if (b) b.scrollIntoView(); window.scrollBy(0, 300); });
  await p.waitForTimeout(800);
  await p.screenshot({ path: path.join(dir, '_mid.png') });
  await p.evaluate(() => window.scrollTo(0, 0));
  if (view === 'desk') {
    await p.evaluate(() => document.querySelectorAll('#nav .sect[aria-expanded="false"]').forEach(s => s.click()));
  } else {
    const t = await p.$('#navtab'); if (t) await t.click().catch(() => {});
  }
  await p.waitForTimeout(2500);
  await p.evaluate(() => { const n = document.getElementById('nav'); if (n) for (const e of [n, ...n.querySelectorAll('*')]) if (e.scrollTop) e.scrollTop = Math.round(e.scrollTop / 40) * 40; });
  await p.waitForTimeout(300);
  await p.screenshot({ path: path.join(dir, '_nav.png') });
}

async function states(browser, page, out, view) {
  const dir = path.join(out, view + '-states'); fs.mkdirSync(dir, { recursive: true });
  const { ctx, p } = await open(browser, page, view, {});
  await freeze(p);
  const snap = async n => { await p.waitForTimeout(700); await p.screenshot({ path: path.join(dir, n + '.png') }); };
  const into = async (sel) => { await p.evaluate(s => { const e = document.querySelector(s); if (e) { e.scrollIntoView({ block: 'center' }); } }, sel); await p.waitForTimeout(500); };
  // drawer
  await into('#mdd button.sp-drw');
  const d = await p.$('#mdd button.sp-drw'); if (d) { await d.click(); await snap('drawer-mdd'); }
  await p.keyboard.press('Escape'); await p.waitForTimeout(500);
  await p.evaluate(() => document.querySelectorAll('[class*="drw"] .x,[class*="drawer"] .x').forEach(x => x.click()));
  // hover card
  await into('#mdd button.sp-pop');
  const h = await p.$('#mdd button.sp-pop');
  if (h) { if (view === 'desk') await h.hover(); else await h.tap().catch(() => h.click()); await snap('hover-mdd'); }
  await p.mouse.move(2, 2); await p.keyboard.press('Escape');
  // practice bank views
  for (const v of ['Stack', 'List', 'Review']) {
    const ok = await p.evaluate(v => {
      const b = document.querySelector('#asthma'); if (!b) return false;
      const btn = [...b.querySelectorAll('button')].find(x => x.textContent.trim() === v);
      if (!btn) return false; btn.scrollIntoView({ block: 'start' }); btn.click(); return true;
    }, v);
    if (ok) await snap('bank-' + v.toLowerCase() + '-asthma');
  }
  await p.keyboard.press('Escape');
  await ctx.close();
}

async function shoot(a) {
  const page = a[1], out = a[2];
  const views = arg(a, '--views', 'desk,phone').split(',');
  const cfgs = arg(a, '--configs', FULL.join(',') + ',acc').split(',').flatMap(c => c === 'acc' ? Object.keys(CONFIGS).filter(k => k.startsWith('acc-')) : [c]);
  const browser = await chromium.launch();
  const t0 = Date.now();
  for (const view of views) {
    if (a.includes('--states')) { await states(browser, page, out, view); console.log(view, 'states', Math.round((Date.now() - t0) / 1000) + 's'); }
    for (const c of cfgs) {
      if (a.includes('--states-only')) break;
      const dir = path.join(out, view + '-' + c); fs.mkdirSync(dir, { recursive: true });
      const { ctx, p } = await open(browser, page, view, CONFIGS[c]);
      await freeze(p);
      let ids = await p.evaluate(() => [...document.querySelectorAll('.brief[id]')].map(e => e.id));
      if (arg(a, '--briefs')) ids = arg(a, '--briefs').split(',');
      else if (c.startsWith('acc-')) ids = ACC_SAMPLE;
      if (arg(a, '--sample')) { const n = +arg(a, '--sample'); ids = ids.filter((_, i) => i % Math.ceil(ids.length / n) === 0); }
      await p.waitForTimeout(2500);
      await chrome(p, dir, view);
      await p.reload({ waitUntil: 'load' }); await p.waitForTimeout(1500); await freeze(p);
      await shotBriefs(p, dir, ids);
      await ctx.close();
      console.log(view, c, ids.length, Math.round((Date.now() - t0) / 1000) + 's');
    }
  }
  await browser.close();
}

async function coverage(a) {
  const page = a[1], out = a[2]; fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch();
  const res = { css: {}, js: {} };
  for (const view of ['desk', 'phone']) {
    const ctx = await browser.newContext({ viewport: { width: VIEWS[view].width, height: VIEWS[view].height }, isMobile: !!VIEWS[view].isMobile, hasTouch: !!VIEWS[view].hasTouch });
    const p = await ctx.newPage(); p.setDefaultTimeout(240000);
    await p.coverage.startCSSCoverage({ resetOnNavigation: false });
    await p.coverage.startJSCoverage({ resetOnNavigation: false, reportAnonymousScripts: true });
    for (const c of FULL.concat(Object.keys(CONFIGS).filter(k => k.startsWith('acc-')))) {
      await p.evaluate(s => { try { localStorage.clear(); for (const k in s) localStorage.setItem(k, s[k]); } catch (e) {} }, CONFIGS[c]).catch(() => {});
      await p.goto('file://' + path.resolve(page) + '?axall', { waitUntil: 'load', timeout: 240000 });
      await p.evaluate(() => document.fonts && document.fonts.ready);
      await p.waitForTimeout(1000);
      if (c.startsWith('acc-')) continue;
      // walk every brief: scroll it into view (spy, rail, lazy layout), hover and open what it offers
      await p.evaluate(async () => {
        const sleep = ms => new Promise(r => setTimeout(r, ms));
        for (const b of document.querySelectorAll('.brief[id]')) { b.scrollIntoView(); await sleep(30); }
        window.scrollTo(0, 0);
      });
      await chrome(p, out, view).catch(() => {});
    }
    await states(browser, page, path.join(out, 'cov-shots'), view).catch(e => console.log('states', e.message));
    // states() opens its own context; also exercise them here so they count
    for (const sel of ['#mdd button.sp-drw', '#hippos button.sp-pop']) {
      const e = await p.$(sel); if (e) { await e.scrollIntoViewIfNeeded(); await (view === 'desk' ? e.hover() : e.tap().catch(() => {})); await e.click().catch(() => {}); await p.waitForTimeout(600); await p.keyboard.press('Escape'); }
    }
    await p.evaluate(async () => {
      const sleep = ms => new Promise(r => setTimeout(r, ms));
      for (const id of ['asthma', 'mdd', 'kawasaki']) {
        const b = document.getElementById(id); if (!b) continue;
        for (const v of ['Stack', 'List', 'Review']) { const btn = [...b.querySelectorAll('button')].find(x => x.textContent.trim() === v); if (btn) { btn.scrollIntoView(); btn.click(); await sleep(300); } }
        const ch = b.querySelector('ol.bank button, ol.bank li [data-k]'); if (ch) { ch.click(); await sleep(200); }
      }
      document.querySelectorAll('#modes button').forEach(x => { try { x.click(); x.click(); } catch (e) {} });
    }).catch(() => {});
    const css = await p.coverage.stopCSSCoverage();
    const js = await p.coverage.stopJSCoverage();
    for (const e of css) { const k = e.url + '#' + e.text.length; (res.css[k] = res.css[k] || { text: e.text, ranges: [] }).ranges.push(...e.ranges); }
    for (const e of js) {
      const k = e.url + '#' + (e.source || '').length;
      const used = []; for (const f of e.functions) for (const r of f.ranges) if (r.count > 0) used.push([r.startOffset, r.endOffset]);
      const unused = []; for (const f of e.functions) for (const r of f.ranges) if (r.count === 0) unused.push([r.startOffset, r.endOffset]);
      (res.js[k] = res.js[k] || { len: (e.source || '').length, head: (e.source || '').slice(0, 200), used: [], unused: [] });
      res.js[k].used.push(...used); res.js[k].unused.push(...unused);
    }
    await ctx.close();
    console.log('coverage', view, 'done');
  }
  fs.writeFileSync(path.join(out, 'coverage.json'), JSON.stringify(res));
  await browser.close();
}

const a = process.argv.slice(2);
(a[0] === 'shoot' ? shoot(a) : a[0] === 'coverage' ? coverage(a) : Promise.resolve(console.log(fs.readFileSync(__filename, 'utf8').split('*/')[0])))
  .catch(e => { console.error(e); process.exit(1); });
