// the resize and zoom pass: five cases, each with a screenshot and the measured ring, panel and target.
// 1 rotate a phone mid-stop (stops 1 to 3); 2 cross 1100 px mid-stop and back (stops 2 and 4); 3 browser zoom 200%
// (a 640x360 CSS viewport at device scale 2) at each stop; 4 pinch zoom 2x at stop 1; 5 a removed tag at stop 2.
// Usage: node tour_resize.js <page> [shots dir]
'use strict';
const path = require('path');
const { chromium } = require('playwright');
const { serve } = require(path.join(__dirname, 'serve_page'));
const PAGE = process.argv[2], OUT = process.argv[3];
const TAGS = ['find', 'browse', 'brief', 'bar'];
const ph = (w, h) => ({ viewport: { width: w, height: h }, hasTouch: true, isMobile: true, deviceScaleFactor: 2 });
(async () => {
  const srv = await serve(PAGE), res = [], rows = []; let bad = 0;
  const ok = (name, v, note) => { res.push((v ? 'PASS ' : 'FAIL ') + name + (note ? ' (' + note + ')' : '')); if (!v) bad++; };
  const br = await chromium.launch();
  const state = (pg, tag) => pg.evaluate(tag => {
    const R = e => { const r = e.getBoundingClientRect(); return { l: Math.round(r.left), t: Math.round(r.top), r: Math.round(r.right), b: Math.round(r.bottom), w: Math.round(r.width), h: Math.round(r.height) }; };
    const root = document.getElementById('axtour'), ring = R(root.querySelector('.tr-ring')), p = root.querySelector('.tr-panel'), pr = R(p);
    const tg = [...document.querySelectorAll('[data-tour~=' + tag + ']')].filter(e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.right > 0 && r.left < innerWidth && r.bottom > 0 && r.top < innerHeight; }).map(R);
    const mb0 = document.getElementById('mbar'), up = root.classList.contains('top'); const lim = innerWidth > 1100 ? innerHeight - 4 : up ? mb0.getBoundingClientRect().top - 8 : pr.t - 8;
    const holds = tg.length > 0 && tg.every(t => Math.max(t.l, 4) >= ring.l - 1 && Math.max(t.t, 4) >= ring.t - 1 && Math.min(t.r, innerWidth - 4) <= ring.r + 1 && (Math.min(t.b, innerHeight - 4) <= ring.b + 1 || Math.abs(ring.b - lim) <= 1));
    const over = !(pr.r <= ring.l || pr.l >= ring.r || pr.b <= ring.t || pr.t >= ring.b);
    const vv = window.visualViewport; const mb = document.getElementById('mbar'), mt = mb && innerWidth <= 1100 ? mb.getBoundingClientRect().top : innerHeight; const see = tag === 'bar' || tag === 'replay' ? 999 : Math.round(Math.min(ring.b, mt) - Math.max(ring.t, 0));
    return { see, on: root.classList.contains('in'), mode: root.getAttribute('data-m'), up, lost: root.classList.contains('lost'), wait: root.classList.contains('wait'), side: root.getAttribute('data-side'), tags: tg.length, holds, over, ring, panel: pr, vw: innerWidth, vh: innerHeight, scroll: p.scrollHeight > p.clientHeight + 1, title: p.querySelector('.tr-sh').textContent, dot: [...p.querySelectorAll('.tr-dots i')].findIndex(d => d.classList.contains('on')), hash: location.hash, ringOp: getComputedStyle(root.querySelector('.tr-ring')).visibility === 'hidden' ? 0 : 1, far: root.classList.contains('far'), vv: vv ? { s: vv.scale, l: Math.round(vv.offsetLeft), t: Math.round(vv.offsetTop), w: Math.round(vv.width), h: Math.round(vv.height) } : null };
  }, tag);
  const load = async opt => { const cx = await br.newContext(opt); const pg = await cx.newPage(); const errs = []; pg.on('pageerror', e => errs.push(e.message)); await pg.goto(srv.url); await pg.waitForSelector('#axtour.in', { timeout: 15000 }); await pg.waitForTimeout(900); await pg.evaluate(() => document.querySelector('#axtour .tr-go').click()); await pg.waitForTimeout(1200); return { cx, pg, errs }; };
  const next = async pg => { await pg.evaluate(() => document.querySelector('#axtour .tr-next').click()); await pg.waitForTimeout(1400); };
  const to = async (pg, i) => { for (let k = 0; k < i; k++) await next(pg); };
  const shot = async (pg, name) => { if (OUT) await pg.screenshot({ path: path.join(OUT, name + '.png') }); };
  const onScreen = s => s.panel.l >= 0 && s.panel.t >= 0 && s.panel.r <= s.vw && s.panel.b <= s.vh;
  const note = (name, s) => rows.push({ name, vw: s.vw, vh: s.vh, title: s.title, ring: [s.ring.l, s.ring.t, s.ring.w, s.ring.h].join(','), panel: [s.panel.l, s.panel.t, s.panel.w, s.panel.h].join(','), lost: s.lost, top: s.up, see: s.see, holds: s.holds, over: s.over, scroll: s.scroll });
  const judge = (name, s, i) => {
    note(name, s);
    ok(name + ' the stop is open on dot ' + (i + 1), s.on && s.mode === 'stop' && s.dot === i && !s.wait, s.title);
    ok(name + ' the ring holds the target', !s.lost && s.holds, 'tags ' + s.tags + ' ring ' + JSON.stringify(s.ring));
    ok(name + ' the panel is on screen and clear of the ring', onScreen(s) && !s.over, JSON.stringify(s.panel));
    ok(name + ' at least 64 px of the target shows above the tab capsule', s.see >= 64, s.see + ' px');
  };

  // 1 rotate a phone mid-stop
  for (const i of [0, 1, 2]) {
    const { cx, pg, errs } = await load(ph(393, 852)); await to(pg, i);
    await pg.setViewportSize({ width: 852, height: 393 }); await pg.waitForTimeout(1500);
    let s = await state(pg, TAGS[i]); judge('rotate stop ' + (i + 1) + ' landscape 852x393', s, i); await shot(pg, 'rotate_' + (i + 1) + '_land');
    ok('rotate stop ' + (i + 1) + ' landscape the panel text needs no scrolling', !s.scroll, s.panel.h + ' px');
    await pg.setViewportSize({ width: 393, height: 852 }); await pg.waitForTimeout(1500);
    s = await state(pg, TAGS[i]); judge('rotate stop ' + (i + 1) + ' back to 393x852', s, i); await shot(pg, 'rotate_' + (i + 1) + '_port');
    ok('rotate stop ' + (i + 1) + ' no page error', !errs.length, errs.join('; ')); await cx.close();
  }
  // 2 cross 1100 px mid-stop and back
  for (const i of [1, 3]) {
    const { cx, pg, errs } = await load({ viewport: { width: 1280, height: 800 } }); await to(pg, i);
    // stop 4: the ring is on the bar for 1.8 s after the layout change, then on the settings control
    await pg.setViewportSize({ width: 900, height: 800 }); await pg.waitForTimeout(1200);
    let s = await state(pg, TAGS[i]); judge('cross stop ' + (i + 1) + ' at 900 wide', s, i); await shot(pg, 'cross_' + (i + 1) + '_900');
    if (i === 3) { await pg.waitForTimeout(1500); s = await state(pg, 'replay'); ok('cross stop 4 at 900 wide the ring moves to the Settings tab', s.far && s.holds && s.ring.w < s.vw / 3, JSON.stringify(s.ring)); await shot(pg, 'cross_4_900b'); }
    await pg.setViewportSize({ width: 1280, height: 800 }); await pg.waitForTimeout(1200);
    s = await state(pg, TAGS[i]); judge('cross stop ' + (i + 1) + ' back at 1280 wide', s, i); await shot(pg, 'cross_' + (i + 1) + '_1280');
    if (i === 3) { await pg.waitForTimeout(1500); s = await state(pg, 'replay'); ok('cross stop 4 back at 1280 wide the ring moves to the settings button', s.far && s.holds && s.ring.w < 140, JSON.stringify(s.ring)); await shot(pg, 'cross_4_1280b'); }
    ok('cross stop ' + (i + 1) + ' the popover is beside or below the ring again', s.side === 'r' || s.side === 'b', s.side);
    ok('cross stop ' + (i + 1) + ' no page error', !errs.length, errs.join('; ')); await cx.close();
  }
  // 3 browser zoom 200%: a 1280x720 window at 200% is a 640x360 CSS viewport at device scale 2
  {
    const { cx, pg, errs } = await load({ viewport: { width: 640, height: 360 }, deviceScaleFactor: 2 });
    for (let i = 0; i < 4; i++) {
      const s = await state(pg, TAGS[i]); judge('zoom 200% stop ' + (i + 1), s, i); await shot(pg, 'zoom200_' + (i + 1));
      ok('zoom 200% stop ' + (i + 1) + ' the panel text needs no scrolling', !s.scroll, s.panel.h + ' px');
      if (i < 3) await next(pg);
    }
    ok('zoom 200% no page error', !errs.length, errs.join('; ')); await cx.close();
  }
  // 4 pinch zoom 2x at stop 1
  {
    const { cx, pg, errs } = await load(ph(393, 852));
    const cdp = await cx.newCDPSession(pg);
    await cdp.send('Emulation.setPageScaleFactor', { pageScaleFactor: 2 }); await pg.waitForTimeout(900);
    let s = await state(pg, 'find'); note('pinch 2x stop 1', s);
    ok('pinch 2x stop 1 the visual viewport is zoomed', s.vv && s.vv.s > 1.9, JSON.stringify(s.vv));
    ok('pinch 2x stop 1 the ring still holds the target in the layout', !s.lost && s.holds, JSON.stringify(s.ring));
    await shot(pg, 'pinch_1_zoomed');
    await cdp.send('Emulation.setPageScaleFactor', { pageScaleFactor: 1 }); await pg.waitForTimeout(900);
    s = await state(pg, 'find'); judge('pinch stop 1 back at 1x', s, 0); await shot(pg, 'pinch_1_back');
    ok('pinch no page error', !errs.length, errs.join('; ')); await cx.close();
  }
  // 5 a removed tag at stop 2, phone and desktop
  for (const [nm, opt] of [['phone', ph(393, 852)], ['desktop', { viewport: { width: 1280, height: 800 } }]]) {
    const { cx, pg, errs } = await load(opt);
    await pg.evaluate(() => document.querySelectorAll('[data-tour~=browse]').forEach(e => e.removeAttribute('data-tour')));
    await pg.evaluate(() => document.querySelector('#axtour .tr-next').click()); await pg.waitForTimeout(2600);
    const s = await state(pg, 'browse'); note('removed tag stop 2 ' + nm, s);
    const cx0 = (s.panel.l + s.panel.r) / 2, cy0 = (s.panel.t + s.panel.b) / 2;
    ok('removed tag stop 2 ' + nm + ' shows the text as a centered card with no ring', s.on && s.lost && s.dot === 1 && !s.wait && s.ringOp === 0 && Math.abs(cx0 - s.vw / 2) <= 2 && Math.abs(cy0 - s.vh / 2) <= s.vh * 0.2, JSON.stringify({ panel: s.panel, ringOp: s.ringOp }));
    await shot(pg, 'lost_2_' + nm);
    await next(pg); const t = await state(pg, 'brief');
    ok('removed tag ' + nm + ' Next reaches stop 3 on its target', t.dot === 2 && !t.lost && t.holds, t.hash);
    ok('removed tag ' + nm + ' no page error', !errs.length, errs.join('; ')); await cx.close();
  }
  if (OUT) console.log(JSON.stringify(rows, null, 0).replace(/\},\{/g, '},\n{'));
  console.log(res.join('\n')); console.log('TOUR RESIZE ' + (bad ? 'FAIL ' + bad : 'PASS ' + res.length));
  await br.close(); srv.close(); process.exit(bad ? 1 : 0);
})();
