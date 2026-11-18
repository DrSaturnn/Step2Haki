// s172b re-measure on current main: issues 1, 2, findings 5 to 7, question views.
//   PAGE=<index.html> node remeasure.js [surface: deck|std]   -> remeasure_<surface>.json
'use strict';
const WS = '/home/claude/Step2Haki/workspace';
const { chromium } = require('playwright');
const { serve } = require(WS + '/tools/serve_page');
const fs = require('fs');
const PAGE = process.env.PAGE || WS + '/index.html';
const SURF = process.argv[2] || 'deck';
const W = 1512, H = 945;
const out = { page: PAGE, surface: SURF, size: W + 'x' + H };
async function open(b, srv, hash, opts = {}) {
  const p = await b.newPage({ viewport: { width: opts.W || W, height: opts.H || H } });
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.errs = errs;
  await p.addInitScript(([surf]) => { try {
    localStorage.setItem('ax-settings', JSON.stringify({ v: 1, s: { tour: '1', surface: surf } })); } catch (e) {} }, [SURF]);
  await p.goto(srv.url + '#' + hash, { waitUntil: 'load' }); await p.waitForTimeout(1800);
  return p;
}
const toTwo = async p => { await p.evaluate(() => document.querySelector('#modes .layout button[data-v="two"]').click()); await p.waitForTimeout(1200); };
const openNav = async p => { await p.evaluate(() => document.querySelector('#ax2rail .ex').click()); await p.waitForTimeout(900); };
// geometry: boxes inside a column that start at or past the column's right edge (held columns excluded)
const GEO = () => { const B = document.querySelector('.brief.ax2-cur'); if (!B) return null; const res = { start: [] };
  B.querySelectorAll('.ax2-col:not(.ax2-hold)').forEach(c => { const R = c.getBoundingClientRect().right;
    [...c.children].forEach(u => { [...u.getClientRects()].forEach(q => { if (q.width && q.left >= R - 1) res.start.push(['unit', Math.round(q.left), Math.round(q.width)]); });
      u.querySelectorAll('*').forEach(x => { [...x.getClientRects()].forEach(q => {
        if (q.width && q.left >= R - 1) res.start.push([x.tagName.toLowerCase() + (typeof x.className === 'string' && x.className ? '.' + x.className.split(' ')[0] : ''), Math.round(q.left), Math.round(q.width)]); }); }); }); });
  res.startN = res.start.length; res.start = res.start.slice(0, 4); return res; };
(async () => {
  const srv = await serve(PAGE); const b = await chromium.launch();
  // finding 5: first switch to Two-pane marks a current rail section
  { const p = await open(b, srv, 'chf'); await toTwo(p);
    out.f5 = await p.evaluate(() => ({ tiles: document.querySelectorAll('#ax2rail .sec').length, home: [...document.querySelectorAll('#ax2rail .sec.home')].map(x => x.textContent), cur: (document.querySelector('.brief.ax2-cur') || {}).id }));
    await p.close(); }
  // finding 7: top fade in Scrolling and in Two-pane
  { const p = await open(b, srv, 'chf'); await p.evaluate(() => scrollTo(0, 900)); await p.waitForTimeout(300);
    const f = () => { const e = document.getElementById('axtopfade'); return e ? getComputedStyle(e).display : 'absent'; };
    const s = await p.evaluate(f); await toTwo(p); const t = await p.evaluate(f);
    out.f7 = { scrolling: s, twopane: t, surface: await p.evaluate(() => document.documentElement.getAttribute('data-surface')) }; await p.close(); }
  // issue 1 and finding 6: shelf switch in Two-pane, sidebar closed and open
  out.i1 = [];
  for (const [id, sh] of [['chf', 'psych'], ['mdd', 'peds']]) {
    for (const nav of [false, true]) {
      const p = await open(b, srv, id); await toTwo(p); if (nav) await openNav(p);
      const r0 = await p.evaluate(() => ({ cur: (document.querySelector('.brief.ax2-cur') || {}).id, shelf: axShelf() }));
      await p.evaluate(sh => document.querySelector('.shelfpick button[data-shelf="' + sh + '"]').click(), sh); await p.waitForTimeout(1500);
      const r = await p.evaluate(() => { const c = document.querySelector('.brief.ax2-cur'); const vis = [...document.querySelectorAll('main .wrap > .brief')].filter(x => x.offsetHeight > 0);
        const rows = [...document.querySelectorAll('#nav a.axn-b[href^="#"]')]; const shown = rows.filter(a => a.getClientRects().length);
        const hiddenRows = shown.filter(a => { const t = document.getElementById(a.getAttribute('href').slice(1)); return t && t.style.display === 'none'; });
        return { shelf: axShelf(), cur: c ? c.id : null, curShown: !!(c && c.offsetHeight > 0), briefsOnScreen: vis.length, mainH: Math.round(document.querySelector('main').getBoundingClientRect().height),
          hash: location.hash, railHome: [...document.querySelectorAll('#ax2rail .sec.home')].map(x => x.textContent), sideRowsShown: shown.length, sideRowsHiddenBrief: hiddenRows.length }; });
      out.i1.push({ id, to: sh, sidebarOpen: nav, before: r0, after: r, errs: p.errs.length }); await p.close();
    }
  }
  // issue 2: question actions in Stack; which question views show
  out.i2 = [];
  for (const id of ['chf', 'mdd', 'hpv', 'dementia']) {
    const p = await open(b, srv, id); await toTwo(p);
    const step = async (name, fn) => { const ok = await p.evaluate(fn); await p.waitForTimeout(700); const g = await p.evaluate(GEO); return { name, ok, startN: g && g.startN, sample: g && (g.start[0] || null) }; };
    const rec = { id, steps: [] };
    rec.views = await p.evaluate(() => { const B = document.querySelector('.brief.ax2-cur'); return B ? [...B.querySelectorAll('.bkmode')].filter(x => x.offsetHeight).map(x => x.dataset.v + (x.classList.contains('on') ? '*' : '')) : null; });
    const cur = 'document.querySelector(".brief.ax2-cur .mcq.sk-cur") || document.querySelector(".brief.ax2-cur .mcq")';
    rec.steps.push(await step('start', () => true));
    rec.steps.push(await step('answer', new Function('const q = ' + cur + '; const o = q && q.querySelector(".opts button"); if (!o) return false; o.click(); return true;')));
    rec.steps.push(await step('reveal-toggle-1', new Function('const q = ' + cur + '; const r = q && q.querySelector(".rv"); if (!r) return false; r.click(); return true;')));
    rec.steps.push(await step('reveal-toggle-2', new Function('const q = ' + cur + '; const r = q && q.querySelector(".rv"); if (!r) return false; r.click(); return true;')));
    rec.steps.push(await step('reveal-all', () => { const r = document.querySelector('.brief.ax2-cur .bkall'); if (!r) return false; r.click(); return true; }));
    rec.steps.push(await step('next', () => { const r = document.querySelector('.brief.ax2-cur .bknav [data-sk="1"]'); if (!r || r.disabled) return false; r.click(); return true; }));
    rec.steps.push(await step('filter-chip', () => { const r = document.querySelector('.brief.ax2-cur .bkfilter button:not([aria-pressed="true"])'); if (!r) return false; r.click(); return true; }));
    rec.steps.push(await step('view-list', () => { const r = document.querySelector('.brief.ax2-cur .bkmode[data-v="quiz"]'); if (!r) return false; r.click(); return true; }));
    rec.steps.push(await step('view-review', () => { const r = document.querySelector('.brief.ax2-cur .bkmode[data-v="review"]'); if (!r) return false; r.click(); return true; }));
    rec.steps.push(await step('relayout', () => { AX.emit('layout:hold', true); AX.emit('layout:hold', false); return true; }));
    rec.errs = p.errs.length; out.i2.push(rec); await p.close();
  }
  fs.writeFileSync(__dirname + '/remeasure_' + SURF + '.json', JSON.stringify(out, null, 1));
  console.log(JSON.stringify(out));
  await b.close(); srv.close();
})();
