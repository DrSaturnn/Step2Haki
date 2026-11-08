// two_pane_check: every brief in the Two-pane layout keeps its text (site/js/25-two-pane.js moves the brief's own nodes
// into pages and columns). For each brief: its text in Scrolling equals its text in Two-pane once the added
// "<Step>, continued" labels and repeated table headers are taken out; after returning to Scrolling it is unchanged
// and its end cap is its last part (s169). Two pages run at once.
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
  // two pages at once, each taking every other brief (the per-brief wait is a timer, so the pages overlap well)
  const W = 2;
  const one = async (W_, H_, k) => {
    const p = await b.newPage({ viewport: { width: W_, height: H_ } });
    const errs = []; p.on('pageerror', e => errs.push(e.message));
    await p.addInitScript(() => { window.__t = B => { const c = B.cloneNode(true); c.querySelectorAll('.ax2-cont, thead[aria-hidden="true"], .bb-bar, .bb-rail, .bb-end').forEach(x => x.remove()); return c.textContent.replace(/\s+/g, ''); }; });
    await p.goto(srv.url + '#chf', { waitUntil: 'load' }); await p.waitForTimeout(2000);
    const all = await p.evaluate(() => [...document.querySelectorAll('main .wrap > .brief[id]')].map(x => x.id));
    const ids = all.filter((_, i) => i % W === k);
    const before = await p.evaluate(ids => { const o = {}; ids.forEach(id => { AX.brief.ensure(id); o[id] = __t(document.getElementById(id)); }); return o; }, ids);
    await p.evaluate(() => document.querySelector('#modes .layout button[data-v="two"]').click()); await p.waitForTimeout(1200);
    const bad = [];
    for (const id of ids) {
      await p.evaluate(id => { location.hash = id; }, id); await p.waitForTimeout(450);
      const r = await p.evaluate(id => { const B = document.getElementById(id); return B.classList.contains('ax2-cur') ? __t(B) : null; }, id);
      if (r === null) bad.push(id + ' (not shown)'); else if (r !== before[id]) bad.push(id + ' (text)');
    }
    await p.evaluate(() => document.querySelector('#modes .layout button[data-v="scroll"]').click()); await p.waitForTimeout(800);
    // back in Scrolling every brief has its text again, and its end cap (Back to top, Next) is its last part
    const after = await p.evaluate(ids => { const o = {}; ids.forEach(id => { const B = document.getElementById(id), e = B.querySelector(':scope > .bb-end');
      o[id] = [__t(B), !e || B.lastElementChild === e]; }); return o; }, ids);
    ids.forEach(id => { if (after[id][0] !== before[id]) bad.push(id + ' (not restored)'); if (!after[id][1]) bad.push(id + ' (end cap not last)'); });
    await p.close();
    return { n: ids.length, bad, errs };
  };
  for (const sz of (sizes.length ? sizes : ['1512x945'])) {
    const [Wd, Ht] = sz.split('x').map(Number);
    const parts = await Promise.all(Array.from({ length: W }, (_, k) => one(Wd, Ht, k)));
    const bad = [].concat(...parts.map(x => x.bad)), errs = [].concat(...parts.map(x => x.errs)), n = parts.reduce((s, x) => s + x.n, 0);
    fail += bad.length + errs.length;
    console.log(`${sz}: ${n} briefs, ${bad.length} differ, ${errs.length} page errors` + (bad.length + errs.length ? ': ' + bad.concat(errs).slice(0, 8).join('; ') : ''));
  }
  await b.close();
  console.log(fail ? 'TWO-PANE FAIL' : 'TWO-PANE PASS');
  process.exit(fail ? 1 : 0);
})();
