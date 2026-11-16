// tour stop 1 behavior: ring on the tagged elements, panel inside its budget, exits, focus, re-measure, missing target
'use strict';
const path = require('path');
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const { serve } = require(path.join(__dirname, '../../../tools/serve_page'));
const PAGE = process.argv[2];
const ph = (w, h) => ({ viewport: { width: w, height: h }, hasTouch: true, isMobile: true, deviceScaleFactor: 2 }), dt = (w, h) => ({ viewport: { width: w, height: h } });
(async () => {
  const srv = await serve(PAGE), res = []; let bad = 0;
  const ok = (name, v, note) => { res.push((v ? 'PASS ' : 'FAIL ') + name + (note ? ' (' + note + ')' : '')); if (!v) bad++; };
  const br = await chromium.launch({ executablePath: '/usr/bin/google-chrome' });
  const state = pg => pg.evaluate(() => {
    const R = e => { const r = e.getBoundingClientRect(); return { l: r.left, t: r.top, r: r.right, b: r.bottom, w: r.width, h: r.height }; };
    const root = document.getElementById('axtour'), ring = R(root.querySelector('.tr-ring')), p = root.querySelector('.tr-panel'), pr = R(p);
    const tg = [...document.querySelectorAll('[data-tour~=find]')].filter(e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.right > 0 && r.left < innerWidth && r.bottom > 0 && r.top < innerHeight; }).map(R);
    const bar = document.getElementById('mbar'), mb = bar ? R(bar) : null;
    const holds = tg.length > 0 && tg.every(t => Math.max(t.l, 4) >= ring.l - 1 && Math.max(t.t, 4) >= ring.t - 1 && Math.min(t.r, innerWidth - 4) <= ring.r + 1 && Math.min(t.b, innerHeight - 4) <= ring.b + 1);
    const over = !(pr.r <= ring.l || pr.l >= ring.r || pr.b <= ring.t || pr.t >= ring.b);
    return { on: root.classList.contains('in'), mode: root.getAttribute('data-m'), lost: root.classList.contains('lost'), flag: window.AX.settings.get('tour'), inert: [...document.body.children].filter(e => e.inert).length, nav: document.body.classList.contains('navopen'), tags: tg.length, holds, over, ring, panel: pr, mbar: mb, vw: innerWidth, vh: innerHeight, scroll: p.scrollHeight > p.clientHeight, ringShown: getComputedStyle(root.querySelector('.tr-ring')).visibility !== 'hidden', focusIn: !!document.activeElement.closest('#axtour .tr-panel') };
  });
  const start = async (opt, init) => { const cx = await br.newContext(opt); if (init) await cx.addInitScript(init); const pg = await cx.newPage(); const errs = []; pg.on('pageerror', e => errs.push(e.message)); await pg.goto(srv.url); await pg.waitForSelector('#axtour.in', { timeout: 15000 }); await pg.waitForTimeout(700); await pg.evaluate(() => document.querySelector('#axtour .tr-go').click()); await pg.waitForTimeout(900); return { cx, pg, errs }; };
  for (const [nm, opt, phone] of [['375x667', ph(375, 667), 1], ['393x852', ph(393, 852), 1], ['430x932', ph(430, 932), 1], ['1101x800', dt(1101, 800), 0], ['1280x720', dt(1280, 720), 0], ['1440x900', dt(1440, 900), 0]]) {
    const { cx, pg, errs } = await start(opt); const s = await state(pg);
    ok(nm + ' stop 1 is open, the page is inert, focus is in the panel', s.on && s.mode === 'stop' && s.inert > 5 && s.focusIn && s.flag === '1');
    ok(nm + ' the ring holds every tagged element', s.holds && !s.lost, 'tags ' + s.tags);
    ok(nm + ' the panel is on screen and clear of the ring', !s.over && s.panel.l >= 0 && s.panel.t >= 0 && s.panel.r <= s.vw && s.panel.b <= s.vh);
    if (phone) {
      ok(nm + ' the panel is at most 200 px tall with no scrolling', s.panel.h <= 200 && !s.scroll, Math.round(s.panel.h) + ' px');
      ok(nm + ' the panel sits 8 px above the tab capsule', Math.abs(s.mbar.t - s.panel.b - 8) <= 1, 'gap ' + Math.round(s.mbar.t - s.panel.b));
    } else ok(nm + ' the popover starts right of the sidebar', s.panel.l >= 328, 'x ' + Math.round(s.panel.l));
    ok(nm + ' no page error', !errs.length, errs.join('; '));
    await cx.close();
  }
  for (const [nm, opt, phone] of [['phone', ph(393, 852), 1], ['desktop', dt(1280, 720), 0]]) {
    for (const how of ['x', 'esc']) {
      const { cx, pg } = await start(opt);
      if (how === 'x') await pg.click('#axtour .tr-panel .tr-x'); else if (how === 'esc') await pg.keyboard.press('Escape'); else await pg.click('#axtour .tr-next');
      await pg.waitForTimeout(800); const s = await state(pg);
      ok(nm + ' stop exit by ' + how, !s.on && s.flag === '1' && s.inert === 0);
      if (how === 'x') { await pg.reload(); await pg.waitForTimeout(2600); ok(nm + ' second load after a stop exit shows no card', !(await pg.evaluate(() => !!document.querySelector('#axtour.in')))); }
      await cx.close();
    }
    let r = await start(opt);
    await r.pg.mouse.click(phone ? 196 : 900, phone ? 420 : 500); await r.pg.waitForTimeout(500); let s = await state(r.pg);
    ok(nm + ' a tap on the dimmed page does nothing', s.on && s.mode === 'stop' && !s.nav);
    await r.pg.mouse.click(phone ? 196 : 170, phone ? 90 : 120); await r.pg.waitForTimeout(500); s = await state(r.pg);
    ok(nm + ' a tap on the highlighted element does nothing', s.on && s.mode === 'stop' && !s.nav && s.focusIn);
    for (let i = 0; i < 5; i++) await r.pg.keyboard.press('Tab');
    ok(nm + ' focus stays in the panel', (await state(r.pg)).focusIn || await r.pg.evaluate(() => !!document.activeElement.closest('#axtour .tr-panel')));
    await r.pg.evaluate(() => document.querySelectorAll('[data-tour~=find]').forEach(e => e.removeAttribute('data-tour')));
    await r.pg.evaluate(() => window.dispatchEvent(new Event('resize'))); await r.pg.waitForTimeout(700); s = await state(r.pg);
    ok(nm + ' a missing target shows the text as a centered card with no ring', s.lost && !s.ringShown && Math.abs((s.panel.l + s.panel.r) / 2 - s.vw / 2) <= 2 && Math.abs((s.panel.t + s.panel.b) / 2 - s.vh / 2) <= 40, JSON.stringify(s.panel));
    await r.cx.close();
  }
  // re-measure: desktop resize, crossing 1100 px, phone rotation
  let r = await start(dt(1280, 720));
  await r.pg.setViewportSize({ width: 1440, height: 900 }); await r.pg.waitForTimeout(900); let s = await state(r.pg);
  ok('desktop resize keeps the ring on the tagged elements', s.holds && !s.over);
  await r.pg.setViewportSize({ width: 900, height: 800 }); await r.pg.waitForTimeout(1200); s = await state(r.pg);
  ok('crossing 1100 px mid-stop keeps the stop usable', s.on && s.mode === 'stop' && (s.lost || (s.holds && !s.over)) && s.panel.r <= s.vw && s.panel.b <= s.vh && s.panel.l >= 0, JSON.stringify({ lost: s.lost, tags: s.tags, panel: s.panel }));
  await r.cx.close();
  r = await start(ph(393, 852));
  await r.pg.setViewportSize({ width: 852, height: 393 }); await r.pg.waitForTimeout(1200); s = await state(r.pg);
  ok('phone rotation mid-stop keeps the panel on screen', s.on && s.panel.t >= 0 && s.panel.b <= s.vh && (s.lost || s.holds), JSON.stringify({ lost: s.lost, over: s.over, panel: s.panel, ring: s.ring }));
  await r.cx.close();
  // swipe down on the phone panel
  r = await start(ph(393, 852));
  const cdp = await r.cx.newCDPSession(r.pg);
  const swipe = async (dy) => { const x = 196, y0 = 640; await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x, y: y0 }] }); for (let i = 1; i <= 8; i++) { await cdp.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x, y: y0 + dy * i / 8 }] }); await r.pg.waitForTimeout(40); } await r.pg.waitForTimeout(200); await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] }); await r.pg.waitForTimeout(800); };
  await swipe(24); s = await state(r.pg); ok('phone short drag down on the panel springs back', s.on && s.mode === 'stop');
  await swipe(110); s = await state(r.pg); ok('phone long drag down on the panel closes the tour', !s.on && s.inert === 0 && !s.nav);
  await r.cx.close();
  // reduced motion
  const cx = await br.newContext({ ...dt(1280, 720), reducedMotion: 'reduce' }); const pg = await cx.newPage(); await pg.goto(srv.url); await pg.waitForSelector('#axtour.in'); await pg.waitForTimeout(300);
  await pg.evaluate(() => document.querySelector('#axtour .tr-go').click()); await pg.waitForTimeout(120); s = await state(pg);
  ok('reduced motion: the ring and popover are in place with no timed move', s.holds && !s.over && await pg.evaluate(() => getComputedStyle(document.querySelector('#axtour .tr-panel')).opacity === '1'));
  await cx.close();
  console.log(res.join('\n')); console.log('STOP CHECK ' + (bad ? 'FAIL ' + bad : 'PASS ' + res.length));
  await br.close(); srv.close(); process.exit(bad ? 1 : 0);
})();
