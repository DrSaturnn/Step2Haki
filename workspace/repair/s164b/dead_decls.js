#!/usr/bin/env node
/* dead_decls.js: for every declaration of the theme-keyed rules (local/s164b/css_rules.json), whether it is in effect on
   any element of the page, in each view and config given. Run on the before page.
   node repair/s164b/dead_decls.js PAGE OUT.json --views desk,tablet,phone --configs flat-dark-read,sculpted-dark-read
   A declaration is in effect on an element when setting it inline there changes no computed value. Per declaration:
   matched elements, live elements; rules whose selector matches nothing (states, pseudo-elements) are "unknown". */
'use strict';
const fs = require('fs'), path = require('path');
const VIEWS = { desk: { width: 1512, height: 945 }, tablet: { width: 1024, height: 768 }, phone: { width: 390, height: 844, isMobile: true, hasTouch: true } };
const CONFIGS = { 'flat-dark-read': { 'ax-theme': 'dark' }, 'sculpted-dark-read': { 'ax-flat': '0', 'ax-theme': 'dark' },
  'flat-tinted-read': { 'ax-theme': 'tinted' }, 'flat-dark-recall': { 'ax-theme': 'dark', 'ax-study': '1' },
  'acc-rose-dark': { 'ax-accent': 'rose', 'ax-theme': 'dark' } };
function arg(a, k, d) { const i = a.indexOf(k); return i >= 0 ? a[i + 1] : d; }
const THEME = /\[data-(?:theme|axa|glass)[^\]]*\]/, HACK = 'html:is([data-theme],:not([data-theme]))';
const EVAL = rules => {
      const out = {};
      const mq = c => c.every(x => { const m = x.match(/^@media\s+(.*)$/); return !m || matchMedia(m[1]).matches; });
      for (const ru of rules) {
        if (!mq(ru.ctx)) { out[ru.i] = 'media'; continue; }
        let els; try { els = Array.from(document.querySelectorAll(ru.sel)); } catch (e) { out[ru.i] = 'unknown'; continue; }
        if (0) try { els = document.querySelectorAll(ru.sel); } catch (e) { out[ru.i] = 'unknown'; continue; }
        if (!els.length) { out[ru.i] = 'nomatch'; continue; }
        if (els.length > 300) { const k = els.length / 300; els = Array.from({ length: 300 }, (_, j) => els[Math.floor(j * k)]); }
        const per = {};
        ru.decl.forEach(([prop, val]) => {
          let live = 0, n = 0;
          const probe = document.createElement('div'); probe.style.setProperty(prop, val);
          const longs = probe.style.length ? Array.from(probe.style) : [prop];
          for (const el of els) {
            if (!el.style) continue; n++;
            const oldV = el.style.getPropertyValue(prop), oldP = el.style.getPropertyPriority(prop);
            const cs = getComputedStyle(el), before = longs.map(k => cs.getPropertyValue(k));
            el.style.setProperty(prop, val, 'important');
            const after = longs.map(k => getComputedStyle(el).getPropertyValue(k));
            if (oldV) el.style.setProperty(prop, oldV, oldP); else el.style.removeProperty(prop);
            if (before.every((v, j) => v === after[j])) live++;
          }
          per[prop] = [n, live];
        });
        out[ru.i] = per;
      }
      return out;
    };
(async () => {
  const a = process.argv.slice(2), page = a[0], out = a[1];
  const css = JSON.parse(fs.readFileSync(path.join(__dirname, '../../local/s164b/css_rules.json')));
  const rules = css.rules.filter(r => r.sel && THEME.test(r.sel.replace(HACK, '').replace(/:not\(\[data-theme[^\]]*\]\)/g, '')))
    .map(r => ({ i: r.i, sel: r.sel.replace(/\/\*[\s\S]*?\*\//g, ''), ctx: r.ctx, decl: r.decl.map(d => [d[0], d[1].replace(/\/\*[\s\S]*?\*\//g, '').trim()]) }));
  const { chromium } = require('playwright'); const browser = await chromium.launch();
  const res = {};
  for (const view of arg(a, '--views', 'desk').split(',')) for (const cfg of arg(a, '--configs', 'flat-dark-read').split(',')) {
    const V = VIEWS[view];
    let ctx, p;
    const open = async () => {
      if (ctx) await ctx.close().catch(() => {});
      ctx = await browser.newContext({ viewport: { width: V.width, height: V.height }, isMobile: !!V.isMobile, hasTouch: !!V.hasTouch });
      await ctx.addInitScript(s => { try { localStorage.clear(); for (const k in s) localStorage.setItem(k, s[k]); } catch (e) {} }, CONFIGS[cfg]);
      p = await ctx.newPage(); p.setDefaultTimeout(1800000);
      await p.goto('file://' + path.resolve(page), { waitUntil: 'load', timeout: 600000 }); await p.waitForTimeout(2500);
      await p.addStyleTag({ content: '*,*::before,*::after{transition:none!important;animation:none!important;content-visibility:visible!important}' });
    };
    await open();
    const r = {};
    for (let b = 0, tries = 0; b < rules.length; ) { try { Object.assign(r, await p.evaluate(EVAL, rules.slice(b, b + 20))); b += 20; tries = 0; }
      catch (e) { if (++tries > 3) throw e; process.stdout.write(view + '/' + cfg + ' retry at ' + b + '\n'); await open(); } }
    
    res[view + '/' + cfg] = r; await ctx.close(); fs.writeFileSync(out, JSON.stringify(res));
    process.stdout.write(view + '/' + cfg + ' done\n');
  }
  fs.writeFileSync(out, JSON.stringify(res));
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
