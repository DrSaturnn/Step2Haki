#!/usr/bin/env node
/* probe.js: s167 steps 5c and 5d checked in a browser on one built page.
   5c: buttons with no accessible name (grouped by class), ids used more than once, console messages at load,
   the review templates rvpin and rvmsg (count in the DOM).
   5d: the old one-key settings migrate into 'ax-settings', the page shows them, a change persists across a reload,
   and the old key is still written for the tools that seed it.

  node repair/s167/probe.js PAGE [--out FILE]
*/
const fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
const page = process.argv[2], outI = process.argv.indexOf('--out'), out = outI > 0 ? process.argv[outI + 1] : null;

async function open(browser, seed, view) {
  const ctx = await browser.newContext(view === 'phone' ? { viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true } : { viewport: { width: 1440, height: 900 } });
  if (seed) await ctx.addInitScript(s => { if (!sessionStorage.getItem('seeded')) { localStorage.clear(); for (const k in s) localStorage.setItem(k, s[k]); sessionStorage.setItem('seeded', '1'); } }, seed);
  const p = await ctx.newPage(); p.setDefaultTimeout(300000);
  const msgs = [];
  p.on('pageerror', e => msgs.push('pageerror: ' + e.message));
  p.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') msgs.push(m.type() + ': ' + m.text().slice(0, 200)); });
  await p.goto('file://' + path.resolve(page), { waitUntil: 'load', timeout: 300000 });
  await p.waitForTimeout(2500);
  return { ctx, p, msgs };
}

const NAMES = () => {
  const name = e => {
    const lb = e.getAttribute('aria-labelledby');
    if (lb) { const t = lb.split(/\s+/).map(i => (document.getElementById(i) || {}).textContent || '').join(' ').trim(); if (t) return t; }
    const a = (e.getAttribute('aria-label') || '').trim(); if (a) return a;
    const t = (e.innerText || e.textContent || '').trim(); if (t) return t;
    if (e.title) return e.title;
    const img = e.querySelector('img[alt]:not([alt=""]),svg title'); if (img) return img.alt || img.textContent;
    if (e.id) { const l = document.querySelector('label[for="' + e.id + '"]'); if (l && l.textContent.trim()) return l.textContent.trim(); }
    return '';
  };
  const unnamed = {};
  document.querySelectorAll('button,[role="button"],a[href],input:not([type="hidden"]),select,textarea,[role="tab"],[role="switch"]').forEach(e => {
    if (name(e)) return;
    const k = e.tagName.toLowerCase() + '.' + (e.className && e.className.baseVal === undefined ? String(e.className).trim().split(/\s+/).join('.') : '');
    unnamed[k] = (unnamed[k] || 0) + 1;
  });
  const ids = {}; document.querySelectorAll('[id]').forEach(e => { ids[e.id] = (ids[e.id] || 0) + 1; });
  const dup = Object.fromEntries(Object.entries(ids).filter(([, n]) => n > 1));
  return { unnamed, dup, rvpin: document.querySelectorAll('#rvpin').length, rvmsg: document.querySelectorAll('#rvmsg').length };
};

(async () => {
  const browser = await chromium.launch(); const R = {};
  for (const view of ['desk', 'phone']) {
    const o = await open(browser, null, view);
    R['5c ' + view] = Object.assign(await o.p.evaluate(NAMES), { console: o.msgs });
    await o.ctx.close();
  }
  // 5d: a reader with the old keys
  const seed = { 'ax-study': '1', 'ax-flat': '0', 'ax-theme': 'dark', 'ax-bankview': 'stack' };
  const o = await open(browser, seed, 'desk');
  const read = () => ({ rec: localStorage.getItem('ax-settings'), study: document.body.classList.contains('study'), flat: document.body.classList.contains('flat'),
    theme: document.documentElement.getAttribute('data-theme'), legacyTheme: localStorage.getItem('ax-theme'), api: !!(window.AX && AX.settings) });
  R['5d migrated'] = await o.p.evaluate(read);
  await o.p.evaluate(() => AX.settings.set('theme', 'light'));
  await o.p.reload({ waitUntil: 'load' }); await o.p.waitForTimeout(2500);
  R['5d after set theme light + reload'] = await o.p.evaluate(read);
  R['5d console'] = o.msgs;
  await o.ctx.close(); await browser.close();
  const s = JSON.stringify(R, null, 1);
  if (out) fs.writeFileSync(out, s);
  for (const [k, v] of Object.entries(R)) {
    if (k.startsWith('5c')) console.log(k, 'unnamed', Object.values(v.unnamed).reduce((a, b) => a + b, 0), JSON.stringify(v.unnamed).slice(0, 300), '| dup ids', JSON.stringify(v.dup).slice(0, 200), '| rvpin', v.rvpin, 'rvmsg', v.rvmsg, '| console', v.console.length, JSON.stringify(v.console).slice(0, 300));
    else console.log(k, JSON.stringify(v).slice(0, 400));
  }
})().catch(e => { console.error(e); process.exit(2); });
