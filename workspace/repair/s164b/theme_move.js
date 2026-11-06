#!/usr/bin/env node
// theme_move.js PAGE desk|phone: elements (briefs, sidebar, toolbar) whose box changes when only the theme (dark, tinted) or the Flat/Sculpted look changes.
// count elements whose box changes when only the theme changes (light -> dark, light -> tinted)
const path = require('path'); const { chromium } = require('playwright');
(async () => { const [page, view] = process.argv.slice(2);
  const V = view === 'phone' ? { width: 390, height: 844, isMobile: true, hasTouch: true } : { width: 1512, height: 945 };
  const b = await chromium.launch(); const c = await b.newContext({ viewport: { width: V.width, height: V.height }, isMobile: !!V.isMobile, hasTouch: !!V.hasTouch });
  await c.addInitScript(() => { try { localStorage.clear(); } catch (e) {} });
  const p = await c.newPage(); p.setDefaultTimeout(900000);
  await p.goto('file://' + path.resolve(page), { waitUntil: 'load', timeout: 600000 }); await p.waitForTimeout(2500);
  await p.addStyleTag({ content: '*,*::before,*::after{transition:none!important;animation:none!important;content-visibility:visible!important}' });
  const r = await p.evaluate(() => {
    const els = [...document.querySelectorAll('.brief[id] *, #nav *, #axbar *, #modes *')];
    const snap = () => els.map(e => { const r = e.getBoundingClientRect(); return [r.left, r.top + scrollY, r.width, r.height].map(Math.round).join(','); });
    const H = document.documentElement, base = snap(), out = {}; const col = () => getComputedStyle(document.querySelector('.brief[id]')).backgroundColor + '/' + getComputedStyle(document.body).backgroundImage.slice(0,30);
    const B = document.body, diff = s => { const moved = {}; let n = 0; s.forEach((v, i) => { if (v !== base[i]) { n++; const e = els[i]; const k = (e.closest('.brief[id]') ? 'brief ' : 'chrome ') + e.tagName.toLowerCase() + '.' + String(e.className).split(' ')[0]; moved[k] = (moved[k] || 0) + 1; } }); return { n, top: Object.entries(moved).sort((a, b) => b[1] - a[1]).slice(0, 10) }; };
    B.classList.toggle('flat'); out.look = diff(snap()); B.classList.toggle('flat'); out.look.flatDefault = B.classList.contains('flat');
    for (const t of ['dark', 'tinted']) { H.setAttribute('data-theme', t); if (t === 'tinted') { H.setAttribute('data-theme', 'dark'); H.setAttribute('data-glass', 'tinted'); } const s = snap(); out['c_' + t] = col(); H.removeAttribute('data-glass'); H.removeAttribute('data-theme');
      const moved = {}; let n = 0; s.forEach((v, i) => { if (v !== base[i]) { n++; const e = els[i]; const k = (e.closest('.brief[id]') ? 'brief ' : 'chrome ') + e.tagName.toLowerCase() + '.' + String(e.className).split(' ')[0]; moved[k] = (moved[k] || 0) + 1; } });
      out[t] = { col: col(), n, of: els.length, top: Object.entries(moved).sort((a, b) => b[1] - a[1]).slice(0, 12) }; }
    return out; });
  console.log(JSON.stringify(r)); await b.close(); })();
