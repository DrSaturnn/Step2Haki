// two_pane_check: every brief in the Two-pane layout keeps its text (site/js/25-two-pane.js moves the brief's own nodes
// into pages and columns). For each brief: its text in Scrolling equals its text in Two-pane once the added
// "<Step>, continued" labels and repeated table headers are taken out; after returning to Scrolling it is unchanged
// and its end cap is its last part (s169). Two pages run at once.
// Cases at each size: the first switch marks the rail; a shelf that hides the open brief opens the shelf's first brief
// (sidebar closed and open); answer, Reveal, Reveal all, Next and a filter chip in Stack leave no part past its
// column's right edge; Two-pane shows the Stack view alone and keeps a saved List view for Scrolling; over every ninth
// brief, rail and sidebar open: no part past a column's edge, no ladder step cut, and the pages, labels and held columns.
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
  // ---- cases: shelf switch, first switch, question actions and views, geometry, cut ladder steps ----
  // a page with the tour marked seen and optional reader settings, opened at #id in Scrolling
  const open = async (W_, H_, id, extra) => {
    const p = await b.newPage({ viewport: { width: W_, height: H_ } });
    const errs = []; p.on('pageerror', e => errs.push(e.message)); p.errs = errs;
    await p.addInitScript(s => { try { localStorage.setItem('ax-settings', JSON.stringify({ v: 1, s })); } catch (e) {} }, Object.assign({ tour: '1' }, extra || {}));
    await p.goto(srv.url + '#' + id, { waitUntil: 'load' }); await p.waitForTimeout(1800);
    return p;
  };
  const toTwo = async p => { await p.evaluate(() => document.querySelector('#modes .layout button[data-v="two"]').click()); await p.waitForTimeout(1200); };
  const toScroll = async p => { await p.evaluate(() => document.querySelector('#modes .layout button[data-v="scroll"]').click()); await p.waitForTimeout(900); };
  const expand = async p => { await p.evaluate(() => document.querySelector('#ax2rail .ex').click()); await p.waitForTimeout(900); };
  // parts of the open brief that start at or past their column's right edge (a held column scrolls, so it is left out)
  const past = p => p.evaluate(() => { const B = document.querySelector('.brief.ax2-cur'); if (!B) return ['no brief open'];
    const hits = [];
    B.querySelectorAll('.ax2-col:not(.ax2-hold)').forEach(c => { const R = c.getBoundingClientRect().right;
      [...c.children].forEach(u => [u, ...u.querySelectorAll('*')].forEach(x => [...x.getClientRects()].forEach(q => {
        if (q.width && q.left >= R - 1 && hits.length < 3) hits.push(x.tagName.toLowerCase() + (typeof x.className === 'string' && x.className ? '.' + x.className.split(' ')[0] : '') + ' at x ' + Math.round(q.left)); }))); });
    return hits; });
  const railHome = p => p.evaluate(() => document.querySelectorAll('#ax2rail .sec.home').length);
  const cases = async (Wd, Ht) => {
    const bad = [], errs = [];
    // the first switch to Two-pane marks the open brief's section on the rail
    { const p = await open(Wd, Ht, 'chf'); await toTwo(p);
      if (!(await railHome(p))) bad.push('first switch: no rail section marked');
      errs.push(...p.errs); await p.close(); }
    // a shelf that hides the open brief: the first brief of the new shelf opens, in the address, its section marked
    for (const [id, sh] of [['chf', 'psych'], ['mdd', 'peds']]) for (const nav of [false, true]) {
      const p = await open(Wd, Ht, id); await toTwo(p); if (nav) await expand(p);
      await p.evaluate(sh => document.querySelector('.shelfpick button[data-shelf="' + sh + '"]').click(), sh); await p.waitForTimeout(1500);
      const r = await p.evaluate(sh => { const c = document.querySelector('.brief.ax2-cur'), first = [...document.querySelectorAll('main .wrap > .brief')].find(x => x.style.display !== 'none');
        return { cur: c && c.id, shown: !!(c && c.offsetHeight), on: !!(c && (c.getAttribute('data-shelf') || '').split(/\s+/).includes(sh)), first: first && first.id, hash: location.hash.slice(1) }; }, sh);
      const tag = `shelf ${id} to ${sh}${nav ? ', sidebar open' : ''}`;
      if (!r.cur || !r.shown) bad.push(tag + ': no brief on screen');
      else if (!r.on || r.cur !== r.first) bad.push(`${tag}: ${r.cur} open, first brief of the shelf ${r.first}`);
      else if (r.hash !== r.cur) bad.push(`${tag}: address #${r.hash}, open ${r.cur}`);
      else if (!(await railHome(p))) bad.push(tag + ': no rail section marked');
      errs.push(...p.errs); await p.close();
    }
    // question actions in Stack keep every part inside its column
    for (const id of ['chf', 'mdd', 'dementia', 'hpv']) {
      const p = await open(Wd, Ht, id); await toTwo(p);
      const cur = 'const q = document.querySelector(".brief.ax2-cur .mcq.sk-cur") || document.querySelector(".brief.ax2-cur .mcq");';
      const acts = [['answer', cur + 'const o = q && q.querySelector(".opts button"); if (o) o.click(); return !!o;'],
        ['reveal', cur + 'const r = q && q.querySelector(".rv"); if (r) r.click(); return !!r;'],
        ['reveal again', cur + 'const r = q && q.querySelector(".rv"); if (r) r.click(); return !!r;'],
        ['Reveal all', 'const r = document.querySelector(".brief.ax2-cur .bkall"); if (r) r.click(); return !!r;'],
        ['Next', 'const r = document.querySelector(".brief.ax2-cur .bknav [data-sk=\'1\']"); if (r && !r.disabled) r.click(); return !!(r && !r.disabled);'],
        ['filter chip', 'const r = document.querySelector(".brief.ax2-cur .bkfilter button:not([aria-pressed=\'true\'])"); if (r) r.click(); return !!r;']];
      const h0 = await past(p); if (h0.length) bad.push(`${id} before any action: ${h0[0]}`);
      else for (const [name, js] of acts) {
        if (!(await p.evaluate(new Function(js)))) continue;
        await p.waitForTimeout(700);
        const h = await past(p); if (h.length) { bad.push(`${id} after ${name}: ${h[0]}`); break; }
      }
      errs.push(...p.errs); await p.close();
    }
    // question views: Stack alone in Two-pane, all three in Scrolling, a saved List view kept for Scrolling
    { const p = await open(Wd, Ht, 'chf', { bankview: 'list' });
      const views = () => p.evaluate(() => { const B = document.getElementById('chf'), w = B.querySelector('.bankwrap');
        return { shown: [...B.querySelectorAll('.bkmode')].filter(x => x.getClientRects().length).map(x => x.dataset.v).join(','), stack: !!(w && w.classList.contains('stack')), saved: AX.settings.get('bankview') }; });
      const s1 = await views(); await toTwo(p); const t = await views(); await toScroll(p); const s2 = await views();
      if (s1.shown !== 'stack,quiz,review') bad.push('views in Scrolling before: ' + s1.shown);
      if (t.shown !== 'stack' || !t.stack) bad.push(`views in Two-pane: ${t.shown || 'none'}${t.stack ? '' : ', not Stack'}`);
      if (t.saved !== 'list' || s2.saved !== 'list' || s2.stack) bad.push(`saved List view: ${t.saved} in Two-pane, ${s2.saved} after${s2.stack ? ', Stack shown in Scrolling' : ''}`);
      errs.push(...p.errs); await p.close(); }
    // the 24-brief sample, rail and sidebar open: parts past a column's edge, cut ladder steps, pages and labels
    for (const nav of [false, true]) {
      const p = await open(Wd, Ht, 'chf'); await toTwo(p); if (nav) await expand(p);
      const ids = await p.evaluate(() => [...document.querySelectorAll('main .wrap > .brief[id]')].map(x => x.id).filter((_, i) => i % 9 === 0));
      const tot = { pages: 0, labels: 0, held: 0 };
      for (const id of ids) {
        await p.evaluate(id => { location.hash = id; }, id); await p.waitForTimeout(950);
        const r = await p.evaluate(() => { const B = document.querySelector('.brief.ax2-cur'); if (!B) return null;
          return { id: B.id, pages: B.querySelectorAll('.ax2-page').length, labels: B.querySelectorAll('.ax2-cont').length, held: B.querySelectorAll('.ax2-hold').length,
            cut: [...B.querySelectorAll('.sp-rung')].filter(x => !x.querySelector(':scope > .sp-node')).length }; });
        if (!r || r.id !== id) { bad.push(`sample ${id}: not shown`); continue; }
        tot.pages += r.pages; tot.labels += r.labels; tot.held += r.held;
        const h = await past(p); if (h.length) bad.push(`sample ${id}${nav ? ' (sidebar open)' : ''}: ${h[0]}`);
        if (r.cut) bad.push(`sample ${id}${nav ? ' (sidebar open)' : ''}: ${r.cut} ladder steps cut`);
      }
      console.log(`  sample ${Wd}x${Ht} ${nav ? 'sidebar open' : 'rail'}: ${ids.length} briefs, ${tot.pages} pages, ${tot.labels} labels, ${tot.held} held`);
      errs.push(...p.errs); await p.close();
    }
    return { bad, errs };
  };
  for (const sz of (sizes.length ? sizes : ['1512x945'])) {
    const [Wd, Ht] = sz.split('x').map(Number);
    const parts = await Promise.all(Array.from({ length: W }, (_, k) => one(Wd, Ht, k)));
    const bad = [].concat(...parts.map(x => x.bad)), errs = [].concat(...parts.map(x => x.errs)), n = parts.reduce((s, x) => s + x.n, 0);
    fail += bad.length + errs.length;
    console.log(`${sz}: ${n} briefs, ${bad.length} differ, ${errs.length} page errors` + (bad.length + errs.length ? ': ' + bad.concat(errs).slice(0, 8).join('; ') : ''));
    const c = await cases(Wd, Ht);
    fail += c.bad.length + c.errs.length;
    console.log(`${sz} cases: ${c.bad.length} fail, ${c.errs.length} page errors` + (c.bad.length + c.errs.length ? ':\n    ' + c.bad.concat(c.errs).slice(0, 14).join('\n    ') : ''));
  }
  // a ladder step cut between columns: chf at 1440 x 900 cuts its treatment ladder on the rail when nothing holds a step whole
  { const p = await open(1440, 900, 'chf'); await toTwo(p);
    const cut = await p.evaluate(() => [...document.getElementById('chf').querySelectorAll('.sp-rung')].filter(x => !x.querySelector(':scope > .sp-node')).length);
    if (cut) fail++;
    console.log(`ladder chf 1440x900: ${cut} ladder steps cut`); await p.close(); }
  await b.close();
  console.log(fail ? 'TWO-PANE FAIL' : 'TWO-PANE PASS');
  process.exit(fail ? 1 : 0);
})();
