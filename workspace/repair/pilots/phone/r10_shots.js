// r10: node r10_shots.js PAGE OUTDIR. Fixed Home bar, the reading header on opening a brief, the coverage matrix with and without review records.
const { chromium, devices } = require('playwright');
const { serve } = require('../../../tools/serve_page.js');
(async () => {
  const [page, out] = process.argv.slice(2);
  const srv = await serve(page); const b = await chromium.launch(); const errs = [];
  async function run(tag, dark) {
    const ctx = await b.newContext({ ...devices['iPhone 14'], serviceWorkers: 'block' });
    if (dark) await ctx.addInitScript("localStorage.setItem('ax-theme','dark');");
    const p = await ctx.newPage(); p.on('pageerror', e => errs.push(tag + ': ' + e.message));
    const shot = async n => { await p.waitForTimeout(700); await p.screenshot({ path: `${out}/${tag}_${n}.png` }); };
    await p.goto(srv.url, { waitUntil: 'load' }); await p.waitForTimeout(2600); await shot('1home');
    const bar0 = await p.evaluate(() => { const r = document.getElementById('phbar').getBoundingClientRect(); const f = document.querySelector('#phhome').firstElementChild.getBoundingClientRect(); return { top: r.top, h: Math.round(r.height), first_card_top: Math.round(f.top) }; });
    await p.mouse.move(195, 500); await p.mouse.wheel(0, 700); await shot('2scrolled');
    const bar1 = await p.evaluate(() => { const r = document.getElementById('phbar').getBoundingClientRect(); return { top: r.top, h: Math.round(r.height), sm: document.getElementById('phbar').classList.contains('sm'), search_visible: document.querySelector('#phbar .hh-s').getBoundingClientRect().top > 0 }; });
    console.log(tag, 'bar', JSON.stringify({ bar0, bar1 }));
    await p.evaluate(() => document.querySelector('#phhome .hh-mx').scrollIntoView({ block: 'center' })); await shot('3matrix');
    console.log(tag, 'matrix', JSON.stringify(await p.evaluate(() => ({ rows: document.querySelectorAll('#phhome .mx-r').length, total: document.querySelector('#phhome .mx-t').innerText.replace(/\s+/g, ' '), old_hidden: !document.querySelector('#bpview .bpsys') || getComputedStyle(document.querySelector('#bpview .bpsys')).display === 'none', overflow: document.documentElement.scrollWidth > innerWidth }))));
    // the bar's search and shelf selector work while scrolled
    await p.tap('#phbar .hh-s'); await p.waitForTimeout(600); const f = await p.evaluate(() => [(document.activeElement || {}).tagName, document.body.classList.contains('navopen')]); await p.tap('#mbar [data-act="index"]'); await p.waitForTimeout(500);
    await p.selectOption('#phbar select', 'psych'); await p.waitForTimeout(900); await shot('4psych');
    console.log(tag, 'bar_controls', JSON.stringify({ search: f, shelf: await p.evaluate(() => document.querySelector('#phbar .hh-shelf span').textContent), matrix_rows: await p.evaluate(() => document.querySelectorAll('#phhome .mx-r').length), outline: await p.evaluate(() => document.querySelector('#phhome .hh-mx').previousElementSibling.innerText.replace(/\n/g, ' | ')) }));
    await p.selectOption('#phbar select', 'step2'); await p.waitForTimeout(700);
    // a brief opens with its header in place before any scroll
    await p.evaluate(() => { location.hash = '#mdd'; }); await p.waitForTimeout(1300); await shot('5brief_open');
    console.log(tag, 'brief', JSON.stringify(await p.evaluate(() => { const h = document.getElementById('phead'); return { header_on: h.classList.contains('on'), title: h.querySelector('.ph-ti b').textContent, y: scrollY, homebar: getComputedStyle(document.getElementById('phbar')).display, steps: h.querySelectorAll('.ph-steps button').length }; })));
    // review records: a profile and a few reviewed briefs written into the review store the way the module reads them
    await p.tap('#mbar [data-act="home"]'); await p.waitForTimeout(500);
    const seeded = await p.evaluate(NS => { const id = window.axRv.add('Test'); window.axRv.use(id); const ids = [...document.querySelectorAll('main .wrap > .brief[id]')].filter(x => x.style.display !== 'none').filter((x, i) => i % 3 === 0).map(x => x.id); const box = {}; ids.forEach(i => { box[i] = { due: 99999, n: 1 }; }); localStorage.setItem(NS + '-d-' + id, JSON.stringify({ v: 1, box, runs: 1, last: null })); return { n: ids.length, seen: (window.axRv.seen() || []).length }; }, 'ax-rev');
    await p.reload({ waitUntil: 'load' }); await p.waitForTimeout(2600);
    await p.evaluate(() => document.querySelector('#phhome .hh-mx').scrollIntoView({ block: 'start' })); await p.mouse.move(195, 500); await p.mouse.wheel(0, -150); await shot('6matrix_reviewed');
    console.log(tag, 'reviewed', JSON.stringify({ seeded, total: await p.evaluate(() => document.querySelector('#phhome .mx-t').innerText.replace(/\s+/g, ' ')), me: await p.evaluate(() => document.querySelector('#phbar .hh-me').textContent) }));
    await ctx.close();
  }
  await run('r10'); await run('r10dark', true);
  console.log('errors', JSON.stringify(errs)); await b.close(); process.exit(0);
})();
