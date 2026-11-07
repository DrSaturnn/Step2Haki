#!/usr/bin/env node
/* why.js: for ui_check difference groups, the rule that sets the property on each page (CDP matched rules).

   node repair/s167/why.js A.html B.html VIEW CONFIG "path|prop[|pseudo]" ...

   path is a ui_check element key (#id>tag:i>... or html>body:1>...); pseudo is after or before. Prints, per item and
   page, the last matched rule (cascade order) that declares prop or its shorthand, with its selector, value, !important
   and source position. */
'use strict';
const path = require('path');
const { chromium } = require('playwright');
const VIEWS = { desk: { width: 1512, height: 945 }, tablet: { width: 1024, height: 768 }, phone: { width: 390, height: 844, isMobile: true, hasTouch: true } };
const CONFIGS = {
  'flat-light-read': {}, 'sculpted-light-read': { 'ax-flat': '0' }, 'flat-dark-read': { 'ax-theme': 'dark' },
  'sculpted-dark-read': { 'ax-flat': '0', 'ax-theme': 'dark' }, 'flat-tinted-read': { 'ax-theme': 'tinted' },
  'flat-light-recall': { 'ax-study': '1' }, 'flat-dark-recall': { 'ax-theme': 'dark', 'ax-study': '1' },
};
const [A, B, view, cfg, ...items] = process.argv.slice(2);
const short = p => [p, p.replace(/-(color|image|size|position|repeat|style|width|weight|family)$/, ''), p.split('-')[0]];

async function one(browser, file) {
  const V = VIEWS[view];
  const ctx = await browser.newContext({ viewport: { width: V.width, height: V.height }, isMobile: !!V.isMobile, hasTouch: !!V.hasTouch });
  await ctx.addInitScript(s => { try { localStorage.clear(); for (const k in s) localStorage.setItem(k, s[k]); } catch (e) {} }, CONFIGS[cfg]);
  const p = await ctx.newPage(); p.setDefaultTimeout(600000);
  await p.goto('file://' + path.resolve(file) + '?axall', { waitUntil: 'load', timeout: 600000 });
  await p.waitForTimeout(2500);
  const found = await p.evaluate(keys => keys.map((k, i) => {
    const parts = k.split('>'); let e = parts[0].startsWith('#') ? document.getElementById(parts[0].slice(1)) : document.documentElement;
    for (const s of parts.slice(1)) { if (!e) break; const [tag, n] = s.split(':'); const c = e.children[+n]; e = c && c.tagName.toLowerCase() === tag ? c : null; }
    if (e) e.setAttribute('data-why', ((e.getAttribute('data-why') || '') + ' ' + i).trim()); return !!e;
  }), items.map(x => x.split('|')[0]));
  const cdp = await ctx.newCDPSession(p);
  await cdp.send('DOM.enable'); await cdp.send('CSS.enable');
  const { root } = await cdp.send('DOM.getDocument', { depth: 0 });
  const out = [];
  for (let i = 0; i < items.length; i++) {
    const [, prop, pseudo] = items[i].split('|');
    if (!found[i]) { out.push('not found'); continue; }
    const h = await p.evaluateHandle(j => document.querySelector('[data-why~="' + j + '"]'), i);
    const { result } = await cdp.send('Runtime.evaluate', { expression: 'document.querySelector(\'[data-why~="' + i + '"]\')' });
    await h.dispose(); if (!result.objectId) { out.push('lost after load (' + result.subtype + ')'); continue; }
    const { nodeId } = await cdp.send('DOM.requestNode', { objectId: result.objectId });
    const m = await cdp.send('CSS.getMatchedStylesForNode', { nodeId });
    let rules = m.matchedCSSRules || [];
    if (pseudo) rules = ((m.pseudoElements || []).find(x => x.pseudoType === pseudo) || {}).matches || [];
    const names = short(prop), hits = [];
    for (const r of rules) for (const d of r.rule.style.cssProperties) if (names.includes(d.name) && d.text && !d.disabled)
      hits.push({ sel: r.rule.selectorList.text.slice(0, 140), media: (r.rule.media || []).map(x => x.text).join(' ').slice(0, 40), decl: d.text.slice(0, 90), imp: !!d.important });
    const win = hits.filter(h => h.imp).pop() || hits[hits.length - 1];
    out.push(win ? win.sel + (win.media ? ' @' + win.media : '') + ' { ' + win.decl + ' }' + '   [' + hits.length + ' declaring]' : 'no rule');
  }
  await ctx.close();
  return out;
}

(async () => {
  const browser = await chromium.launch();
  const ra = await one(browser, A), rb = await one(browser, B);
  await browser.close();
  items.forEach((it, i) => { console.log('* ' + it + '\n  A: ' + ra[i] + '\n  B: ' + rb[i]); });
})().catch(e => { console.error(e); process.exit(1); });
