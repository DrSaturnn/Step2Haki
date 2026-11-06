#!/usr/bin/env node
/* theme_gate.js: D-20261105-10 rule (4). Themes change color only.

   node tools/theme_gate.js PAGE [--views desk,phone] [--out OUT.json] [--max 12]

   Per view, the page is loaded in light (flat), every element of the briefs and the chrome (#nav, #axbar, #modes) is
   measured, then the theme is switched in place to dark, tinted and the Sculpted look:
   - moved: an element whose box (left, top, width, height, rounded to 1px) differs from light. Rule: 0.
   - light-in-dark (dark and tinted only): a visible element whose text color or opaque background is the same as in light
     and is a light-theme color (background luminance above 0.6, or text luminance below 0.2). Rule: 0.
   Exit 1 when either count is above 0 in any view. */
'use strict';
const fs = require('fs'), path = require('path');
const VIEWS = { desk: { width: 1512, height: 945 }, tablet: { width: 1024, height: 768 }, phone: { width: 390, height: 844, isMobile: true, hasTouch: true } };
function arg(a, k, d) { const i = a.indexOf(k); return i >= 0 ? a[i + 1] : d; }

const PROBE = () => {
  const els = [...document.querySelectorAll('.brief[id] *, .brief[id], #nav *, #axbar *, #modes *')];
  const lum = c => { const m = c.match(/rgba?\(([\d.]+),\s*([\d.]+),\s*([\d.]+)(?:,\s*([\d.]+))?/); if (!m) return null;
    const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
    return { L: 0.2126 * f(+m[1]) + 0.7152 * f(+m[2]) + 0.0722 * f(+m[3]), a: m[4] === undefined ? 1 : +m[4] }; };
  const key = e => (e.closest('.brief[id]') ? 'brief ' : 'chrome ') + e.tagName.toLowerCase() + (typeof e.className === 'string' && e.className.trim() ? '.' + e.className.trim().split(/\s+/)[0] : '');
  const snap = () => els.map(e => { const r = e.getBoundingClientRect(), cs = getComputedStyle(e);
    return { box: [r.left, r.top + scrollY, r.width, r.height].map(Math.round).join(','), vis: r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.opacity !== '0',
      color: cs.color, bg: cs.backgroundColor, text: !!(e.childNodes && [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) }; });
  const H = document.documentElement, B = document.body, base = snap(), out = {};
  const top = m => Object.entries(m).sort((a, b) => b[1] - a[1]).slice(0, 12);
  const check = (name, colorCheck) => { const s = snap(), moved = {}, light = {}; let nm = 0, nl = 0;
    s.forEach((v, i) => { if (v.box !== base[i].box) { nm++; const k = key(els[i]); moved[k] = (moved[k] || 0) + 1; }
      if (!colorCheck || !v.vis) return;
      const b = lum(v.bg), c = lum(v.color);
      const lightBg = v.bg === base[i].bg && b && b.a > 0.5 && b.L > 0.6;
      const darkText = v.text && v.color === base[i].color && c && c.a > 0.5 && c.L < 0.2;
      if (lightBg || darkText) { nl++; const k = key(els[i]) + (lightBg ? ' bg ' + v.bg : ' color ' + v.color); light[k] = (light[k] || 0) + 1; } });
    out[name] = { moved: nm, light_in_dark: colorCheck ? nl : null, of: els.length, moved_top: top(moved), light_top: top(light) }; };
  const flat = B.classList.contains('flat');
  B.classList.toggle('flat'); check('look', false); B.classList.toggle('flat');
  H.setAttribute('data-theme', 'dark'); check('dark', true);
  H.setAttribute('data-glass', 'tinted'); check('tinted', true);
  H.removeAttribute('data-glass'); H.removeAttribute('data-theme');
  out.flatDefault = flat; return out;
};

(async () => {
  const a = process.argv.slice(2); if (!a.length || a[0].startsWith('--')) { console.log(fs.readFileSync(__filename, 'utf8').split('*/')[0]); return; }
  const { chromium } = require('playwright');
  const page = a[0], views = arg(a, '--views', 'desk,phone').split(','), res = {}; let fail = 0;
  const browser = await chromium.launch();
  for (const v of views) {
    const V = VIEWS[v]; const ctx = await browser.newContext({ viewport: { width: V.width, height: V.height }, isMobile: !!V.isMobile, hasTouch: !!V.hasTouch });
    await ctx.addInitScript(() => { try { localStorage.clear(); } catch (e) {} });
    const p = await ctx.newPage(); p.setDefaultTimeout(900000);
    await p.goto('file://' + path.resolve(page), { waitUntil: 'load', timeout: 600000 }); await p.waitForTimeout(2500);
    await p.addStyleTag({ content: '*,*::before,*::after{transition:none!important;animation:none!important;content-visibility:visible!important}' });
    res[v] = await p.evaluate(PROBE); await ctx.close();
    for (const t of ['look', 'dark', 'tinted']) { const r = res[v][t]; const bad = r.moved + (r.light_in_dark || 0); if (bad) fail++;
      console.log(v, t, 'moved', r.moved, r.light_in_dark === null ? '' : 'light-in-dark ' + r.light_in_dark, 'of', r.of);
      for (const [k, n] of r.moved_top.slice(0, +arg(a, '--max', 6))) console.log('   moved', n + 'x', k);
      for (const [k, n] of r.light_top.slice(0, +arg(a, '--max', 6))) console.log('   light', n + 'x', k); }
  }
  await browser.close();
  if (arg(a, '--out')) fs.writeFileSync(arg(a, '--out'), JSON.stringify(res, null, 1));
  console.log(fail ? 'THEME GATE FAIL' : 'THEME GATE PASS'); process.exit(fail ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2); });
