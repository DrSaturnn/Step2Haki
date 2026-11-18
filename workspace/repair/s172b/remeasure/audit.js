// Cold audit probes for the Two-pane fixes: rail fit by window height, focus and the card in view after a question
// action, a click on bank text, the sidebar's current row after a shelf switch, the hpv schedule grid, the settings tile.
//   node repair/s172b/remeasure/audit.js PAGE [probe ...]     probes: rail focus text shelf grid cfg (default all)
'use strict';
const path = require('path');
const WS = path.resolve(__dirname, '..', '..', '..');
const { chromium } = require('playwright');
const { serve } = require(WS + '/tools/serve_page');
const PAGE = process.argv[2], want = process.argv.slice(3);
const run = n => !want.length || want.includes(n);
(async () => {
  const b = await chromium.launch(), srv = await serve(PAGE);
  const open = async (W, H, id, extra) => {
    const p = await b.newPage({ viewport: { width: W, height: H } });
    p.on('pageerror', e => console.log('  PAGE ERROR', e.message));
    await p.addInitScript(s => localStorage.setItem('ax-settings', JSON.stringify({ v: 1, s })), Object.assign({ tour: '1' }, extra || {}));
    await p.goto(srv.url + '#' + id, { waitUntil: 'load' }); await p.waitForTimeout(1800);
    await p.evaluate(() => document.querySelector('#modes .layout button[data-v="two"]').click()); await p.waitForTimeout(1500);
    return p;
  };
  if (run('rail')) for (const [W, H] of [[1512, 945], [1512, 860], [1440, 900], [1440, 780], [1280, 800], [1280, 680]]) {
    const p = await open(W, H, 'chf');
    const r = await p.evaluate(() => { const R = document.getElementById('ax2rail'), c = R.querySelector('.cfg'), q = c.getBoundingClientRect(), s = R.querySelector('.sec').getBoundingClientRect(), rr = R.getBoundingClientRect();
      return { client: R.clientHeight, scroll: R.scrollHeight, cfgBottom: Math.round(q.bottom), railBottom: Math.round(rr.bottom), tile: Math.round(s.width) + 'x' + Math.round(s.height), n: R.querySelectorAll('.sec').length }; });
    console.log(`rail ${W}x${H}: ${JSON.stringify(r)} ${r.scroll > r.client ? 'SCROLLS' : 'fits'}`);
    await p.close();
  }
  if (run('focus')) for (const id of ['chf', 'mdd']) {
    const p = await open(1512, 945, id);
    const state = () => p.evaluate(() => { const a = document.activeElement, q = document.querySelector('.brief.ax2-cur .mcq.sk-cur'), r = q && q.getBoundingClientRect();
      return { focus: a === document.body ? 'body' : a.tagName.toLowerCase() + '.' + (a.className || ''), inBank: !!(a.closest && a.closest('.bankwrap')), cardTop: r && Math.round(r.top), cardLeft: r && Math.round(r.left), vh: innerHeight, vw: innerWidth, y: Math.round(scrollY) }; });
    await p.evaluate(() => document.querySelector('.brief.ax2-cur .mcq.sk-cur').closest('.ax2-page').scrollIntoView()); await p.waitForTimeout(300);
    console.log(`focus ${id} before:`, JSON.stringify(await state()));
    await p.locator('.brief.ax2-cur .mcq.sk-cur .opts button').first().click(); await p.waitForTimeout(700);
    console.log(`focus ${id} after answer:`, JSON.stringify(await state()));
    await p.keyboard.press('ArrowRight'); await p.waitForTimeout(700);
    const s1 = await p.evaluate(() => document.querySelector('.brief.ax2-cur .bankwrap')._sk);
    await p.keyboard.press('ArrowRight'); await p.waitForTimeout(700);
    const s2 = await p.evaluate(() => document.querySelector('.brief.ax2-cur .bankwrap')._sk);
    console.log(`focus ${id} after two ArrowRight: card index ${s1} then ${s2};`, JSON.stringify(await state()));
    await p.close();
  }
  if (run('text')) {
    const p = await open(1512, 945, 'chf');
    await p.evaluate(() => { document.querySelector('.brief.ax2-cur .mcq.sk-cur').closest('.ax2-page').scrollIntoView(); scrollBy(0, 60); }); await p.waitForTimeout(300);
    await p.evaluate(() => { window.__pg = document.querySelector('.ax2-page'); window.__y = scrollY; });
    const stem = p.locator('.brief.ax2-cur .mcq.sk-cur').first();
    const bb = await stem.boundingBox();
    await p.mouse.dblclick(bb.x + 60, bb.y + 30); await p.waitForTimeout(600);
    const r = await p.evaluate(() => ({ relaid: !window.__pg.isConnected, sel: String(getSelection()).length, dy: Math.round(scrollY - window.__y) }));
    console.log('text double click on a card:', JSON.stringify(r));
    await p.close();
  }
  if (run('shelf')) {
    const p = await open(1512, 945, 'chf');
    await p.evaluate(() => document.querySelector('#ax2rail .ex').click()); await p.waitForTimeout(900);
    await p.evaluate(() => document.querySelector('.shelfpick button[data-shelf="psych"]').click()); await p.waitForTimeout(1500);
    const r = await p.evaluate(() => { const c = document.querySelector('.brief.ax2-cur'), cur = [...document.querySelectorAll('#axn a[aria-current="page"]')].map(a => a.getAttribute('href'));
      return { open: c && c.id, navCurrent: cur, steps: document.querySelectorAll('#axn .axn-rail a.axn-s').length, hash: location.hash }; });
    console.log('shelf, sidebar open:', JSON.stringify(r));
    await p.close();
  }
  if (run('grid')) for (const [W, H, nav] of [[1512, 945, false], [1512, 945, true], [1440, 900, false], [1280, 800, false]]) {
    const p = await open(W, H, 'hpv');
    if (nav) { await p.evaluate(() => document.querySelector('#ax2rail .ex').click()); await p.waitForTimeout(1400); }
    const r = await p.evaluate(() => { const B = document.querySelector('.brief.ax2-cur'), out = [];
      B.querySelectorAll('dl').forEach(d => { const cs = getComputedStyle(d); if (cs.display !== 'grid') return;
        const dd = [...d.querySelectorAll(':scope > dd')], w = dd.map(x => Math.round(x.getBoundingClientRect().width));
        out.push({ cls: d.className, cols: cs.gridTemplateColumns, w: Math.round(d.getBoundingClientRect().width), ddMin: Math.min(...w), rows: dd.length,
          head: (d.previousElementSibling && d.previousElementSibling.textContent || '').slice(0, 40), unit: d.closest('.ax2-u').dataset.name, col: Math.round(d.closest('.ax2-col').getBoundingClientRect().width) }); });
      return out; });
    console.log(`grid hpv ${W}x${H}${nav ? ' sidebar open' : ''}:`); r.forEach(x => console.log('   ', JSON.stringify(x)));
    await p.close();
  }
  if (run('cfg')) {
    const p = await open(1512, 945, 'chf');
    await p.locator('#ax2rail .cfg').click(); await p.waitForTimeout(700);
    const st = () => p.evaluate(() => { const a = document.activeElement, d = document.getElementById('axdisp');
      return { over: document.documentElement.classList.contains('ax2-over'), sheet: !!(d && d.getClientRects().length), focus: a === document.body ? 'body' : a.tagName.toLowerCase() + '#' + a.id + '.' + a.className, navset: document.body.className }; });
    console.log('cfg after click:', JSON.stringify(await st()));
    await p.keyboard.press('Escape'); await p.waitForTimeout(500);
    console.log('cfg after Escape:', JSON.stringify(await st()));
    await p.locator('#ax2rail .cfg').click({ timeout: 2000 }).catch(e => console.log('  cfg second click failed:', e.message.split('\n')[0])); await p.waitForTimeout(700);
    console.log('cfg after second click:', JSON.stringify(await st()));
    await p.close();
  }
  await b.close(); srv.close();
})();
