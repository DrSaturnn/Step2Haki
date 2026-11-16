// the whole tour: every stop's tag resolves at four widths, the ring holds its target, the phone panel stays in budget,
// the end state of a first visit and of a replay, the Help row, the direct-link pill. Optional screenshots per stop.
// Usage: node tour_check.js <page> [shots dir]
'use strict';
const path = require('path');
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const { serve } = require(path.join(__dirname, '../../../tools/serve_page'));
const PAGE = process.argv[2], OUT = process.argv[3];
const ph = (w, h) => ({ viewport: { width: w, height: h }, hasTouch: true, isMobile: true, deviceScaleFactor: 2 }), dt = (w, h) => ({ viewport: { width: w, height: h } });
const TAGS = ['find', 'browse', 'brief', 'bar'];
(async () => {
  const srv = await serve(PAGE), res = []; let bad = 0;
  const ok = (name, v, note) => { res.push((v ? 'PASS ' : 'FAIL ') + name + (note ? ' (' + note + ')' : '')); if (!v) bad++; };
  const br = await chromium.launch({ executablePath: '/usr/bin/google-chrome' });
  const state = (pg, tag) => pg.evaluate(tag => {
    const R = e => { const r = e.getBoundingClientRect(); return { l: r.left, t: r.top, r: r.right, b: r.bottom, w: r.width, h: r.height }; };
    const root = document.getElementById('axtour'); if (!root) return { on: false, hash: location.hash, flag: window.AX.settings.get('tour'), pill: !!document.getElementById('axtourpill') };
    const ring = R(root.querySelector('.tr-ring')), p = root.querySelector('.tr-panel'), pr = R(p);
    const tg = [...document.querySelectorAll('[data-tour~=' + tag + ']')].filter(e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.right > 0 && r.left < innerWidth && r.bottom > 0 && r.top < innerHeight; }).map(R);
    const lim = innerWidth <= 1100 ? pr.t - 8 : innerHeight - 4;
    const holds = tg.length > 0 && tg.every(t => Math.max(t.l, 4) >= ring.l - 1 && Math.max(t.t, 4) >= ring.t - 1 && Math.min(t.r, innerWidth - 4) <= ring.r + 1 && (Math.min(t.b, innerHeight - 4) <= ring.b + 1 || Math.abs(ring.b - lim) <= 1));
    const over = !(pr.r <= ring.l || pr.l >= ring.r || pr.b <= ring.t || pr.t >= ring.b);
    return { on: root.classList.contains('in'), mode: root.getAttribute('data-m'), lost: root.classList.contains('lost'), far: root.classList.contains('far'), flag: window.AX.settings.get('tour'), hash: location.hash, y: scrollY, inert: [...document.body.children].filter(e => e.inert).length, tags: tg.length, holds, over, ring, panel: pr, vw: innerWidth, vh: innerHeight, scroll: p.scrollHeight > p.clientHeight + 1, title: p.querySelector('.tr-sh').textContent, next: p.querySelector('.tr-next').textContent, back: !p.querySelector('.tr-back').hidden, dot: [...p.querySelectorAll('.tr-dots i')].findIndex(d => d.classList.contains('on')), pill: !!document.getElementById('axtourpill') };
  }, tag);
  const load = async (opt, url, init) => { const cx = await br.newContext(opt); if (init) await cx.addInitScript(init); const pg = await cx.newPage(); const errs = []; pg.on('pageerror', e => errs.push(e.message)); await pg.goto(srv.url + (url || '')); await pg.waitForTimeout(2600); return { cx, pg, errs }; };
  const go = async pg => { await pg.evaluate(() => document.querySelector('#axtour .tr-go').click()); await pg.waitForTimeout(1100); };
  const next = async pg => { await pg.evaluate(() => document.querySelector('#axtour .tr-next').click()); await pg.waitForTimeout(1300); };
  // first visit, all four stops, four widths
  for (const [nm, opt, phone] of [['375x667', ph(375, 667), 1], ['393x852', ph(393, 852), 1], ['1101x800', dt(1101, 800), 0], ['1440x900', dt(1440, 900), 0]]) {
    const { cx, pg, errs } = await load(opt); await go(pg);
    for (let i = 0; i < 4; i++) {
      const s = await state(pg, TAGS[i]), n = nm + ' stop ' + (i + 1);
      ok(n + ' is open with its dot and buttons', s.on && s.mode === 'stop' && s.dot === i && s.back === (i > 0) && s.next === (i === 3 ? 'Done' : 'Next'), s.title);
      ok(n + ' the tag resolves and the ring holds it', !s.lost && s.holds, 'tags ' + s.tags);
      ok(n + ' the panel is on screen and clear of the ring', !s.over && s.panel.l >= 0 && s.panel.t >= 0 && s.panel.r <= s.vw && s.panel.b <= s.vh);
      if (phone) ok(n + ' the panel is at most 200 px tall with no scrolling', s.panel.h <= 200 && !s.scroll, Math.round(s.panel.h) + ' px');
      if (phone && i < 3) ok(n + ' the panel sits 8 px above the tab capsule', Math.abs(await pg.evaluate(() => document.getElementById('mbar').getBoundingClientRect().top) - s.panel.b - 8) <= 1);
      if (i === 2) ok(n + ' a brief is open', /^#./.test(s.hash), s.hash);
      if (OUT) await pg.screenshot({ path: path.join(OUT, 'tour_' + nm + '_' + (i + 1) + '.png') });
      if (i === 3) {
        await pg.waitForTimeout(2300); const f = await state(pg, 'replay');
        ok(n + ' the ring moves to the settings control', f.far && f.holds && f.ring.w < 140, JSON.stringify(f.ring));
        if (OUT) await pg.screenshot({ path: path.join(OUT, 'tour_' + nm + '_4b.png') });
      }
      await next(pg);
    }
    const e = await state(pg, 'bar');
    ok(nm + ' Done closes the tour and a first visit ends inside the brief', !e.on && e.flag === '1' && e.inert === 0 && /^#./.test(e.hash), e.hash);
    await pg.reload(); await pg.waitForTimeout(2600);
    ok(nm + ' a second load shows no card and no pill', await pg.evaluate(() => !document.querySelector('#axtour.in') && !document.getElementById('axtourpill')));
    ok(nm + ' no page error', !errs.length, errs.join('; '));
    await cx.close();
  }
  // Back, and replay from the Help row
  for (const [nm, opt, phone] of [['phone', ph(393, 852), 1], ['desktop', dt(1280, 720), 0]]) {
    let r = await load(opt); await go(r.pg); await next(r.pg); await next(r.pg);
    await r.pg.evaluate(() => document.querySelector('#axtour .tr-back').click()); await r.pg.waitForTimeout(1300);
    let s = await state(r.pg, 'browse'); ok(nm + ' Back from stop 3 shows stop 2 on its target', s.dot === 1 && s.holds && !s.lost, s.hash);
    await r.pg.keyboard.press('Escape'); await r.pg.waitForTimeout(700);
    // replay from the starting screen
    if (phone) { await r.pg.evaluate(() => window.AX.emit('phone:home')); await r.pg.waitForTimeout(500); await r.pg.click('#mbar [data-act=settings]'); }
    else { await r.pg.evaluate(() => { history.replaceState(null, '', location.pathname); scrollTo(0, 0); }); await r.pg.click('#axcfg'); }
    await r.pg.waitForTimeout(700);
    const row = await r.pg.evaluate(() => { const b = document.querySelector('#axdisp .axtourbtn'); if (!b) return null; const q = b.getBoundingClientRect(), g = b.closest('.axd-grp'); return { h: q.height, vis: q.width > 0 && q.bottom <= innerHeight, grp: g && g.getAttribute('aria-label'), last: g && !g.nextElementSibling || (g && [...g.parentNode.querySelectorAll('.axd-grp:not([hidden])')].pop() === g), text: b.textContent }; });
    ok(nm + ' the Help group is last in the display sheet and holds the replay row', row && row.vis && row.grp === 'Help' && row.last && row.text === 'Replay tutorial' && row.h >= 42, JSON.stringify(row));
    if (OUT) await r.pg.screenshot({ path: path.join(OUT, 'help_' + nm + '.png') });
    await r.pg.click('#axdisp .axtourbtn'); await r.pg.waitForTimeout(1300);
    s = await state(r.pg, 'find'); ok(nm + ' replay opens the card with the flag set and the sheet closed', s.on && s.mode === 'card' && s.flag === '1' && await r.pg.evaluate(() => !document.querySelector('#axdisp.on') && !document.body.classList.contains('navset')));
    const h0 = s.hash; await go(r.pg); for (let i = 0; i < 4; i++) await next(r.pg);
    s = await state(r.pg, 'bar'); ok(nm + ' a replay returns to the starting screen', !s.on && s.hash === h0 && (!phone ? s.y === 0 : true), JSON.stringify({ hash: s.hash, y: s.y }));
    await r.cx.close();
    // replay from inside a brief
    r = await load(opt, '#backpain', () => { try { localStorage.setItem('ax-settings', JSON.stringify({ v: 1, s: { tour: '1' } })); } catch (e) {} });
    await r.pg.evaluate(() => window.AX.emit('tour:open')); await r.pg.waitForTimeout(900); await go(r.pg);
    s = await state(r.pg, 'find'); ok(nm + ' a replay inside a brief shows stop 1 on its target', s.holds && !s.lost);
    await next(r.pg); await next(r.pg); s = await state(r.pg, 'brief'); ok(nm + ' stop 3 uses the brief in hand', s.hash === '#backpain' && s.holds, s.hash);
    await next(r.pg); await next(r.pg); s = await state(r.pg, 'bar'); ok(nm + ' the replay ends in the brief in hand', !s.on && s.hash === '#backpain');
    await r.cx.close();
    // direct link, first visit
    r = await load(opt, '#backpain'); s = await state(r.pg, 'find');
    ok(nm + ' a direct link shows the pill and no card', !s.on && s.pill && s.flag === null);
    if (OUT) await r.pg.screenshot({ path: path.join(OUT, 'pill_' + nm + '.png') });
    await r.pg.click('#axtourpill .tp-x'); await r.pg.waitForTimeout(300); s = await state(r.pg, 'find');
    ok(nm + ' closing the pill sets the flag', !s.pill && s.flag === '1');
    await r.cx.close();
    r = await load(opt, '#backpain'); await r.pg.click('#axtourpill .tp-go'); await r.pg.waitForTimeout(900); s = await state(r.pg, 'find');
    ok(nm + ' the pill opens the card', s.on && s.mode === 'card' && !s.pill);
    await go(r.pg); for (let i = 0; i < 4; i++) await next(r.pg); s = await state(r.pg, 'bar');
    ok(nm + ' the tour from the pill ends in the linked brief', !s.on && s.hash === '#backpain' && s.flag === '1', s.hash);
    await r.cx.close();
  }
  console.log(res.join('\n')); console.log('TOUR CHECK ' + (bad ? 'FAIL ' + bad : 'PASS ' + res.length));
  await br.close(); srv.close(); process.exit(bad ? 1 : 0);
})();
