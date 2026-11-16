// r9: node r9_shots.js PAGE OUTDIR. The picked settings on every shelf the page offers, a shelf with no topics, a long shelf name, the Settings tab toggle.
const { chromium, devices } = require('playwright');
const { serve } = require('../../../tools/serve_page.js');
(async () => {
  const [page, out] = process.argv.slice(2);
  const srv = await serve(page); const b = await chromium.launch(); const errs = [];
  const ctx = await b.newContext({ ...devices['iPhone 14'], serviceWorkers: 'block' });
  const p = await ctx.newPage(); p.on('pageerror', e => errs.push(e.message));
  const shot = async n => { await p.waitForTimeout(700); await p.screenshot({ path: `${out}/r9_${n}.png` }); };
  const open = () => p.evaluate(() => document.body.classList.contains('navopen'));
  await p.goto(srv.url, { waitUntil: 'load' }); await p.waitForTimeout(2600);
  console.log('attrs', await p.evaluate(() => [...document.documentElement.attributes].filter(a => a.name.startsWith('data-ph')).map(a => a.name.slice(8) + '=' + a.value).join(' ')));
  // Settings twice returns to the same place, on Home and in a brief
  await p.evaluate(() => scrollTo(0, 600)); await p.waitForTimeout(300);
  await p.tap('#mbar [data-act="settings"]'); await p.waitForTimeout(600); const s1 = await p.evaluate(() => document.body.classList.contains('navset'));
  await p.tap('#mbar [data-act="settings"]'); await p.waitForTimeout(600);
  console.log('settings_toggle_home', JSON.stringify({ opened: s1, closed: !(await open()), y: await p.evaluate(() => scrollY), tab: await p.evaluate(() => document.querySelector('#mbar [aria-current="page"]').dataset.act) }));
  await p.tap('#mbar [data-act="index"]'); await p.waitForTimeout(500); await p.tap('#mbar [data-act="settings"]'); await p.waitForTimeout(500); await p.tap('#mbar [data-act="settings"]'); await p.waitForTimeout(600);
  console.log('settings_from_browse_closes', !(await open()), 'y', await p.evaluate(() => scrollY));
  const shelves = await p.evaluate(() => [...document.querySelectorAll('.masthead .shelfpick [data-shelf]')].map(b => ({ id: b.dataset.shelf, soon: b.classList.contains('soon') })));
  for (const s of shelves.filter(x => !x.soon)) {
    await p.evaluate(() => scrollTo(0, 0));
    await p.selectOption('#phhome .hh-shelf select', s.id); await p.waitForTimeout(900);
    const r = { shelf: s.id };
    r.sub = await p.evaluate(() => document.querySelector('#phhome .hh-sub').innerText.replace(/\n/g, ' | '));
    r.rows = await p.evaluate(() => [...document.querySelectorAll('#phhome .hh-h + .hh-list .hh-r')].map(e => e.firstChild.textContent.slice(0, 14) + ' ' + (e.querySelector('.hh-b') || {}).textContent).join(', '));
    r.sum = await p.evaluate(() => [...document.querySelectorAll('#phhome .hh-h + .hh-list .hh-r .hh-b')].reduce((a, e) => a + (+e.textContent), 0));
    const hasSeg = await p.$('#phhome .hh-seg');
    // every system row opens the drawer with its own group expanded and holding at least one visible topic
    const rows = await p.$$('#phhome .hh-h + .hh-list .hh-r'); let bad = [];
    for (let i = 0; i < rows.length; i++) {
      const name = await rows[i].evaluate(e => e.firstChild.textContent); await rows[i].scrollIntoViewIfNeeded(); await rows[i].tap(); await p.waitForTimeout(450);
      const st = await p.evaluate(nm => { const ex = [...document.querySelectorAll('#axn .axn-sys[aria-expanded="true"]')].filter(x => x.offsetParent); const sc = document.getElementById('navscroll').getBoundingClientRect(); const top = ex.filter(x => { const r = x.getBoundingClientRect(); return r.top >= sc.top - 4 && r.top < sc.top + 140; }).map(x => x.innerText.replace(/\s+/g, ' ').trim()); const vis = [...document.querySelectorAll('#axn a.axn-b')].filter(a => a.offsetParent).length; return { open: document.body.classList.contains('navopen'), vis, top }; }, name);
      if (!st.open || !st.vis || !st.top.length) bad.push(name + ' -> ' + JSON.stringify(st.top));
      if (i === 0) await shot(s.id + '_drawer');
      if (st.open) { await p.tap('#mbar [data-act="index"]'); await p.waitForTimeout(350); }
    }
    r.rows_tested = rows.length; r.rows_failed = bad;
    if (hasSeg) { await p.evaluate(() => scrollTo(0, 0)); await p.tap('#phhome .hh-seg [data-v="cc"]'); await p.waitForTimeout(300); r.complaint_rows = await p.evaluate(() => document.querySelectorAll('#phhome .hh-seg ~ .hh-r').length); await p.tap('#phhome .hh-seg [data-v="sys"]'); } else r.complaint_rows = 'no switch';
    // open the first topic of the shelf from the drawer, then Home shows it under Continue
    await p.tap('#mbar [data-act="index"]'); await p.waitForTimeout(500);
    const g0 = await p.evaluate(() => { const g = [...document.querySelectorAll('#axn .axn-sys')].filter(x => x.offsetParent)[0]; if (g && g.getAttribute('aria-expanded') !== 'true') g.click(); return !!g; }); await p.waitForTimeout(400);
    const tid = await p.evaluate(() => { const a = [...document.querySelectorAll('#axn a.axn-b')].filter(x => x.offsetParent)[0]; if (a) { a.scrollIntoView({ block: 'center' }); a.click(); } return a ? a.dataset.id : null; });
    await p.waitForTimeout(1500); await p.mouse.move(195, 400); await p.mouse.wheel(0, 1500); await p.waitForTimeout(800);
    r.brief = { id: tid, solo: await p.evaluate(() => document.documentElement.classList.contains('ph-open')), header: await p.evaluate(() => document.getElementById('phead').classList.contains('on')) };
    if (s.id === shelves[0].id) await shot(s.id + '_brief');
    await p.tap('#mbar [data-act="home"]'); await p.waitForTimeout(700); await p.evaluate(() => scrollTo(0, 0));
    r.cont = await p.evaluate(() => (document.querySelector('#phhome .hh-c b') || {}).textContent || null);
    await shot(s.id + '_home');
    console.log(JSON.stringify(r));
  }
  // Continue lists only briefs of the shelf in view
  await p.selectOption('#phhome .hh-shelf select', shelves[0].id); await p.waitForTimeout(800);
  console.log('continue_rows_all_shelf', await p.evaluate(() => document.querySelectorAll('#phhome .hh-c, #phhome .hh-c ~ .hh-r').length));
  // a future shelf: a long name on a listed shelf, then a shelf whose sections are all filtered out
  await p.evaluate(() => { const b = document.querySelector('.masthead .shelfpick [data-shelf].on'); b.firstChild.textContent = 'Emergency Medicine and Critical Care'; document.dispatchEvent(new Event('ax-shelf')); });
  await p.waitForTimeout(400); await p.evaluate(() => scrollTo(0, 0)); await shot('future_longname');
  console.log('long_name', JSON.stringify(await p.evaluate(() => ({ overflow: document.documentElement.scrollWidth > innerWidth, shelf_w: Math.round(document.querySelector('#phhome .hh-shelf').getBoundingClientRect().width), right: Math.round(document.querySelector('#phhome .hh-shelf').getBoundingClientRect().right) }))));
  await p.evaluate(() => { document.querySelectorAll('main .wrap > .sectwrap, main .wrap > .psub').forEach(e => { e.style.display = 'none'; }); document.dispatchEvent(new Event('ax-shelf')); });
  await p.waitForTimeout(400); await shot('future_empty');
  console.log('empty_shelf', JSON.stringify(await p.evaluate(() => ({ rows: document.querySelectorAll('#phhome .hh-h + .hh-list .hh-r').length, none: (document.querySelector('#phhome .hh-none') || {}).textContent || null, seg: !!document.querySelector('#phhome .hh-seg') }))));
  await p.evaluate(() => { const ps = [...document.querySelectorAll('main .wrap > .sectwrap')].find(w => w.querySelector('#presentations')); ps.style.display = ''; document.querySelectorAll('main .wrap > .psub').forEach(e => { e.style.display = ''; }); document.dispatchEvent(new Event('ax-shelf')); });
  await p.waitForTimeout(400);
  console.log('complaint_only_shelf', JSON.stringify(await p.evaluate(() => ({ rows: document.querySelectorAll('#phhome .hh-h + .hh-list .hh-r').length, seg: !!document.querySelector('#phhome .hh-seg'), none: !!document.querySelector('#phhome .hh-none') }))));
  console.log('errors', JSON.stringify(errs)); await b.close(); process.exit(0);
})();
