#!/usr/bin/env node
/* a11y_scan.js: accessibility scan (axe-core) of a sample of briefs and the page chrome, per view and theme.

   node tools/a11y_scan.js PAGE [--views desk,phone] [--configs a,b] [--sample 20] [--out OUT.json]
                                [--baseline tools/spine/a11y_baseline.json] [--write]

   Per view two pages load with every brief rendered (?axall) and take every other setting, switched in place (--fresh:
   one load per view and setting, as before s169); the sample is every k-th brief (k = briefs /
   sample) plus #nav, #axbar and #modes. axe runs the WCAG 2.0 and 2.1 A and AA rules on that set; only serious and
   critical violations are kept, counted per rule as nodes.
   --baseline: exit 1 when a view/setting/rule count is above the baseline (a rule missing from the baseline counts 0).
   --write: write the counts as the new baseline. */
'use strict';
const fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
const VIEWS = { desk: { width: 1512, height: 945 }, tablet: { width: 1024, height: 768 }, phone: { width: 390, height: 844, isMobile: true, hasTouch: true } };
const CONFIGS = {
  'flat-light-read': { 'ax-flat': '1' }, 'sculpted-light-read': { 'ax-flat': '0' }, 'flat-dark-read': { 'ax-flat': '1', 'ax-theme': 'dark' },
  'flat-tinted-read': { 'ax-flat': '1', 'ax-theme': 'tinted' }, 'flat-light-recall': { 'ax-flat': '1', 'ax-study': '1' },
};
function arg(a, k, d) { const i = a.indexOf(k); return i >= 0 ? a[i + 1] : d; }
const AXE = fs.readFileSync(require.resolve('axe-core/axe.min.js'), 'utf8');

// one load per view (s169, D-20261107-14): the page loads in flat light Read, then each setting is switched in place the
// way ui_check and theme_gate switch it, and axe runs again; --fresh loads the page once per setting instead
const APPLY = s => { const H = document.documentElement, B = document.body;
  B.classList.toggle('flat', s.flat); B.classList.toggle('study', s.study);
  if (s.dark) H.setAttribute('data-theme', 'dark'); else H.removeAttribute('data-theme');
  if (s.tinted) H.setAttribute('data-glass', 'tinted'); else H.removeAttribute('data-glass');
  // the page restyles regions a few per frame after a mode switch: wait until the region counts hold for 10 frames
  return new Promise(r => { let last = '', same = 0, n = 0; const tick = () => { const k = document.querySelectorAll('.axm-flat').length + ':' + document.querySelectorAll('.axm-study').length;
    same = k === last ? same + 1 : 0; last = k; if (same >= 10 || ++n > 3000) r(); else requestAnimationFrame(tick); }; requestAnimationFrame(tick); }); };
const STATE = cfg => ({ flat: !/sculpted/.test(cfg), dark: /dark|tinted/.test(cfg), tinted: /tinted/.test(cfg), study: /recall/.test(cfg) });
async function load(browser, file, view, cfg) {
  const V = VIEWS[view];
  const ctx = await browser.newContext({ viewport: { width: V.width, height: V.height }, isMobile: !!V.isMobile, hasTouch: !!V.hasTouch, deviceScaleFactor: 1 });
  await ctx.addInitScript(s => { try { localStorage.clear(); for (const k in s) localStorage.setItem(k, s[k]); } catch (e) {} }, CONFIGS[cfg]);
  const p = await ctx.newPage(); p.setDefaultTimeout(900000);
  await p.goto('file://' + path.resolve(file) + '?axall', { waitUntil: 'load', timeout: 900000 });
  await p.waitForTimeout(2500);
  await p.addStyleTag({ content: '*,*::before,*::after{transition:none!important;animation:none!important}' });
  await p.addScriptTag({ content: AXE });
  return { p, ctx };
}
async function axeRun(p, sample) {
  return p.evaluate(async n => {
    const ids = [...document.querySelectorAll('.brief[id]')].map(e => e.id), k = Math.ceil(ids.length / n);
    const include = ids.filter((_, i) => i % k === 0).map(id => ['#' + CSS.escape(id)]).concat([['#nav'], ['#axbar'], ['#modes']])
      .filter(s => document.querySelector(s[0]));
    const r = await window.axe.run({ include }, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'] }, resultTypes: ['violations'] });
    const out = {};
    for (const v of r.violations) {
      const nodes = v.nodes.filter(x => x.impact === 'serious' || x.impact === 'critical');
      if (nodes.length) out[v.id] = { count: nodes.length, impact: v.impact, help: v.help, eg: nodes.slice(0, 3).map(x => x.target.join(' ')) };
    }
    return { briefs: include.length - 3, out };
  }, sample);
}
async function scan(browser, file, view, cfg, sample) {
  const o = await load(browser, file, view, cfg);
  const res = await axeRun(o.p, sample);
  await o.ctx.close();
  return res;
}

(async () => {
  const a = process.argv.slice(2), file = a[0];
  if (!file) { console.error('usage: a11y_scan.js PAGE [--views desk,phone] [--configs a,b] [--sample 20] [--out F] [--baseline F] [--write]'); process.exit(2); }
  const views = arg(a, '--views', 'desk,phone').split(','), configs = arg(a, '--configs', Object.keys(CONFIGS).join(',')).split(',');
  const sample = +arg(a, '--sample', '20'), out = arg(a, '--out'), bl = arg(a, '--baseline'), t0 = Date.now();
  const browser = await chromium.launch(), counts = {}, detail = {};
  const fresh = a.includes('--fresh');
  // two pages per view, each loaded once and taking every other setting (axe's contrast pass is most of the time and
  // runs on one core per page)
  const worker = async (view, list) => {
    const base = fresh ? null : await load(browser, file, view, 'flat-light-read');
    const got = [];
    for (const cfg of list) {
      const t = Date.now();
      let r;
      if (fresh) r = await scan(browser, file, view, cfg, sample);
      else { await base.p.evaluate(APPLY, STATE(cfg)); r = await axeRun(base.p, sample); }
      got.push([cfg, r, Date.now() - t]);
    }
    if (base) await base.ctx.close();
    return got;
  };
  for (const view of views) {
    const parts = await Promise.all([0, 1].map(k => worker(view, configs.filter((_, i) => i % 2 === k))));
    const byCfg = new Map([].concat(...parts).map(x => [x[0], x]));
    for (const cfg of configs) {
      const [, r, ms] = byCfg.get(cfg), key = view + ':' + cfg;
      counts[key] = {}; detail[key] = r.out;
      for (const id in r.out) counts[key][id] = r.out[id].count;
      console.log('a11y ' + key + ': ' + r.briefs + ' briefs, ' + Object.keys(r.out).length + ' rules, ' +
        Object.values(counts[key]).reduce((s, x) => s + x, 0) + ' nodes (' + Math.round(ms / 1000) + ' s)');
    }
  }
  await browser.close();
  if (out) fs.writeFileSync(out, JSON.stringify({ counts, detail }, null, 1));
  if (a.includes('--write') && bl) { fs.writeFileSync(bl, JSON.stringify(counts, null, 1) + '\n'); console.log('a11y baseline written: ' + bl); return; }
  if (!bl) return;
  const base = JSON.parse(fs.readFileSync(bl, 'utf8')), worse = [];
  for (const key in counts) for (const id in counts[key]) {
    const was = (base[key] || {})[id] || 0;
    if (counts[key][id] > was) worse.push(key + ' ' + id + ' ' + was + ' > ' + counts[key][id] + ' (' + detail[key][id].eg.join(' | ') + ')');
  }
  if (worse.length) { console.log('A11Y WORSE: ' + worse.length + '\n  ' + worse.join('\n  ')); process.exit(1); }
  console.log('A11Y PASS (no serious or critical count above the baseline; ' + Math.round((Date.now() - t0) / 1000) + ' s)');
})().catch(e => { console.error(e); process.exit(2); });
