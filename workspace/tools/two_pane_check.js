// two_pane_check: every brief in the Two-pane layout keeps its text (site/js/25-two-pane.js moves the brief's own nodes
// into pages and columns). For each brief: its text in Scrolling equals its text in Two-pane once the added
// "<Step>, continued" labels and repeated table headers are taken out; after returning to Scrolling it is unchanged.
// The brief chrome (.bb-bar, .bb-rail, .bb-end) is left out: it carries the current step and the next brief.
//   node tools/two_pane_check.js PAGE [WIDTHxHEIGHT ...]     (default 1512x945)   -> TWO-PANE PASS | TWO-PANE FAIL, exit 1
'use strict';
const { chromium } = require('playwright');
const { serve } = require('./serve_page');
const [page, ...sizes] = process.argv.slice(2);
if (!page) { console.log('usage: node tools/two_pane_check.js PAGE [WxH ...]'); process.exit(2); }
(async () => {
  const srv = await serve(page);
  const b = await chromium.launch();
  let fail = 0;
  for (const sz of (sizes.length ? sizes : ['1512x945'])) {
    const [W, H] = sz.split('x').map(Number);
    const p = await b.newPage({ viewport: { width: W, height: H } });
    const errs = []; p.on('pageerror', e => errs.push(e.message));
    await p.addInitScript(() => { window.__t = B => { const c = B.cloneNode(true); c.querySelectorAll('.ax2-cont, thead[aria-hidden="true"], .bb-bar, .bb-rail, .bb-end').forEach(x => x.remove()); return c.textContent.replace(/\s+/g, ''); }; });
    await p.goto(srv.url + '#chf', { waitUntil: 'load' }); await p.waitForTimeout(2000);
    const ids = await p.evaluate(() => [...document.querySelectorAll('main .wrap > .brief[id]')].map(x => x.id));
    const before = await p.evaluate(ids => { const o = {}; ids.forEach(id => { AX.brief.ensure(id); o[id] = __t(document.getElementById(id)); }); return o; }, ids);
    await p.evaluate(() => document.querySelector('#modes .layout button[data-v="two"]').click()); await p.waitForTimeout(1200);
    const bad = [];
    for (const id of ids) {
      await p.evaluate(id => { location.hash = id; }, id); await p.waitForTimeout(450);
      const r = await p.evaluate(id => { const B = document.getElementById(id); return B.classList.contains('ax2-cur') ? __t(B) : null; }, id);
      if (r === null) bad.push(id + ' (not shown)'); else if (r !== before[id]) bad.push(id + ' (text)');
    }
    await p.evaluate(() => document.querySelector('#modes .layout button[data-v="scroll"]').click()); await p.waitForTimeout(800);
    const after = await p.evaluate(ids => { const o = {}; ids.forEach(id => { o[id] = __t(document.getElementById(id)); }); return o; }, ids);
    ids.forEach(id => { if (after[id] !== before[id]) bad.push(id + ' (not restored)'); });
    const n = bad.length + errs.length;
    fail += n;
    console.log(`${sz}: ${ids.length} briefs, ${bad.length} differ, ${errs.length} page errors` + (n ? ': ' + bad.concat(errs).slice(0, 8).join('; ') : ''));
    await p.close();
  }
  await b.close();
  console.log(fail ? 'TWO-PANE FAIL' : 'TWO-PANE PASS');
  process.exit(fail ? 1 : 0);
})();
