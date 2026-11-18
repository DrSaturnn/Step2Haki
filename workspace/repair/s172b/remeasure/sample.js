// s172b re-measure: the 24-brief sample (every ninth brief) in Two-pane on current main.
// Per variant and window: pages, "continued" labels, held columns, text check, briefs with a box past the column's
// right edge (finding 8), cut ladder rungs (finding 9), squeezed text blocks (under 110 px wide, 6 or more lines).
//   PAGE=<index.html> node sample.js SIZES VARIANTS [surface]   e.g. 1512x945 rail,open-today,P1+P2 deck
'use strict';
const WS = '/home/claude/Step2Haki/workspace';
const { chromium } = require('playwright');
const { serve } = require(WS + '/tools/serve_page');
const V = require(__dirname + '/variants.js'), fs = require('fs');
const PAGE = process.env.PAGE || WS + '/index.html';
const VARS = { 'rail': { open: false }, 'open-today': { open: true }, 'P1+P2': { open: true, nav: 216, look: true, css: ['P2'] } };
const sizes = (process.argv[2] || '1512x945').split(','), names = (process.argv[3] || 'rail,open-today,P1+P2').split(','), SURF = process.argv[4] || 'deck';
(async () => {
  const srv = await serve(PAGE); const b = await chromium.launch(); const out = {};
  await Promise.all(sizes.map(async sz => {
    const [W, H] = sz.split('x').map(Number);
    for (const name of names) {
      const v = VARS[name];
      const p = await b.newPage({ viewport: { width: W, height: H } });
      const errs = []; p.on('pageerror', e => errs.push(e.message));
      await p.addInitScript(surf => { try { localStorage.setItem('ax-settings', JSON.stringify({ v: 1, s: { tour: '1', surface: surf } })); } catch (e) {}
        window.__t = B => { const c = B.cloneNode(true); c.querySelectorAll('.ax2-cont, thead[aria-hidden="true"], .bb-bar, .bb-rail, .bb-end').forEach(x => x.remove()); return c.textContent.replace(/\s+/g, ''); }; }, SURF);
      await p.goto(srv.url + '#chf', { waitUntil: 'load' }); await p.waitForTimeout(1800);
      const ids = await p.evaluate(() => [...document.querySelectorAll('main .wrap > .brief[id]')].map(x => x.id).filter((_, i) => i % 9 === 0));
      const before = await p.evaluate(ids => { const o = {}; ids.forEach(id => { AX.brief.ensure(id); o[id] = __t(document.getElementById(id)); }); return o; }, ids);
      await p.evaluate(() => document.querySelector('#modes .layout button[data-v="two"]').click()); await p.waitForTimeout(1000);
      if (v.open) { await p.evaluate(() => document.querySelector('#ax2rail .ex').click()); await p.waitForTimeout(700); }
      await V.apply(p, v); await p.evaluate(() => { AX.emit('layout:hold', true); AX.emit('layout:hold', false); }); await p.waitForTimeout(900);
      const tot = { n: ids.length, pages: 0, labels: 0, held: 0, textdiff: [], over: [], rungcut: [], squeezed: [], col: 0, per: {} };
      for (const id of ids) {
        await p.evaluate(id => { location.hash = id; }, id); await p.waitForTimeout(950);
        const r = await p.evaluate(id => { const B = document.getElementById(id); if (!B.classList.contains('ax2-cur')) return null;
          const cols = [...B.querySelectorAll('.ax2-cols:not(.ax2-w1) .ax2-col')];
          let over = null; B.querySelectorAll('.ax2-col:not(.ax2-hold)').forEach(c => { const R = c.getBoundingClientRect().right;
            [...c.children].forEach(u => { [u, ...u.querySelectorAll('*')].forEach(x => { [...x.getClientRects()].forEach(q => {
              if (!over && q.width && q.left >= R - 1) { const h = x.closest('.ax2-u, [data-hid]'); over = [x.tagName.toLowerCase() + (typeof x.className === 'string' && x.className ? '.' + x.className.split(' ')[0] : ''), Math.round(q.left), Math.round(q.width), (u.querySelector('.ax2-uh, h5') || {}).textContent || '']; } }); }); }); });
          const rungcut = [...B.querySelectorAll('.sp-rung')].filter(x => !x.querySelector(':scope > .sp-node')).length;
          let squeezed = 0; B.querySelectorAll('.ax2-col p, .ax2-col li, .ax2-col dd, .ax2-col td, .ax2-col div').forEach(x => {
            if (x.children.length && [...x.childNodes].every(n => n.nodeType !== 3 || !n.textContent.trim())) return;
            const w = x.getBoundingClientRect().width, lh = parseFloat(getComputedStyle(x).lineHeight) || 16, h = x.getBoundingClientRect().height;
            if (w > 0 && w < 110 && h / lh >= 6 && x.textContent.trim().length > 20) squeezed++; });
          return { pages: B.querySelectorAll('.ax2-page').length, labels: B.querySelectorAll('.ax2-cont').length, held: B.querySelectorAll('.ax2-hold').length,
            col: cols[0] ? cols[0].getBoundingClientRect().width : 0, text: __t(B), over, rungcut, squeezed }; }, id);
        if (!r) { tot.textdiff.push(id + ' (not shown)'); continue; }
        tot.pages += r.pages; tot.labels += r.labels; tot.held += r.held; if (r.text !== before[id]) tot.textdiff.push(id);
        if (r.over) tot.over.push([id, ...r.over]); if (r.rungcut) tot.rungcut.push([id, r.rungcut]); if (r.squeezed) tot.squeezed.push([id, r.squeezed]);
        if (!tot.col) tot.col = Math.round(r.col); tot.per[id] = [r.pages, r.labels];
      }
      tot.errs = errs.length; out[sz + ' ' + name] = tot;
      console.log(sz, name, 'col', tot.col, 'pages', tot.pages, 'labels', tot.labels, 'held', tot.held, 'textdiff', tot.textdiff.length,
        'over', tot.over.length, JSON.stringify(tot.over.map(x => x[0])), 'rungcut', JSON.stringify(tot.rungcut), 'squeezed', tot.squeezed.length, 'errs', errs.length);
      await p.close();
    }
  }));
  fs.writeFileSync(__dirname + '/sample_' + SURF + '_' + (process.argv[5] || 'all') + '.json', JSON.stringify(out, null, 1));
  await b.close(); srv.close();
})();
