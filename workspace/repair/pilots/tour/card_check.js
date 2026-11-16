// welcome card behavior: exits set the flag, a second load shows no card, returning readers and direct links get none
'use strict';
const path = require('path');
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const { serve } = require(path.join(__dirname, '../../../tools/serve_page'));
const PAGE = process.argv[2];
const PH = { viewport: { width: 393, height: 852 }, hasTouch: true, isMobile: true, deviceScaleFactor: 2 }, DT = { viewport: { width: 1280, height: 720 } };
(async () => {
  const srv = await serve(PAGE), res = []; let bad = 0;
  const ok = (name, v, note) => { res.push((v ? 'PASS ' : 'FAIL ') + name + (note ? ' (' + note + ')' : '')); if (!v) bad++; };
  const br = await chromium.launch({ executablePath: '/usr/bin/google-chrome' });
  const state = pg => pg.evaluate(() => !window.AX ? { err: location.href } : ({ on: !!document.querySelector('#axtour.in'), flag: window.AX.settings.get('tour'), inert: [...document.body.children].filter(e => e.inert).length, nav: document.body.classList.contains('navopen') }));
  const fresh = async (opt, url, init) => { const cx = await br.newContext(opt); if (init) await cx.addInitScript(init); const pg = await cx.newPage(); await pg.goto(srv.url + (url || '')); await pg.waitForTimeout(2600); return { cx, pg }; };
  for (const [nm, opt] of [['phone', PH], ['desktop', DT]]) {
    for (const how of ['x', 'skip', 'go', 'esc', 'scrim']) {
      const { cx, pg } = await fresh(opt); let s = await state(pg);
      ok(nm + ' first visit opens', s.on && s.flag === null && s.inert > 5);
      if (how === 'x') await pg.click('#axtour .tr-x'); else if (how === 'skip') await pg.click('#axtour .tr-skip'); else if (how === 'go') await pg.click('#axtour .tr-go');
      else if (how === 'esc') await pg.keyboard.press('Escape'); else await pg.mouse.click(8, 8);
      await pg.waitForTimeout(800); s = await state(pg);
      ok(nm + ' exit by ' + how, !s.on && s.flag === '1' && s.inert === 0, JSON.stringify(s));
      if (how === 'x') {
        await pg.reload(); await pg.waitForTimeout(2600); s = await state(pg); ok(nm + ' second load shows no card', !s.on);
        await pg.evaluate(() => window.AX.emit('tour:open')); await pg.waitForTimeout(700); s = await state(pg); ok(nm + ' replay opens with the flag set', s.on && s.flag === '1');
        await pg.keyboard.press('Tab'); await pg.keyboard.press('Tab'); await pg.keyboard.press('Tab'); await pg.keyboard.press('Tab');
        ok(nm + ' focus stays in the card', await pg.evaluate(() => !!document.activeElement.closest('#axtour')));
      }
      await cx.close();
    }
    let r = await fresh(opt, '', () => { try { localStorage.setItem('ax-recent', '[{"id":"scaphoid"}]'); } catch (e) {} });
    ok(nm + ' reader with ax-recent gets no card', !(await state(r.pg)).on); await r.cx.close();
    r = await fresh(opt, '', () => { try { localStorage.setItem('ax-rev:x', '{}'); } catch (e) {} });
    ok(nm + ' reader with an ax-rev key gets no card', !(await state(r.pg)).on); await r.cx.close();
    r = await fresh(opt, '#scaphoid'); let s = await state(r.pg);
    ok(nm + ' direct link to a brief gets no card', !s.on && s.flag === null); await r.cx.close();
  }
  // phone: swipes on the sheet
  const touch = async (cx, pg, pts) => { const c = await cx.newCDPSession(pg); await c.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [pts[0]] }); for (const p of pts.slice(1)) { await c.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [p] }); await pg.waitForTimeout(16); } await c.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] }); await pg.waitForTimeout(800); };
  let { cx, pg } = await fresh(PH);
  await touch(cx, pg, Array.from({ length: 12 }, (_, i) => ({ x: 60 + i * 22, y: 500 })));
  let s = await state(pg); ok('phone swipe right on the sheet leaves the drawer shut', s.on && !s.nav, JSON.stringify(s));
  await touch(cx, pg, Array.from({ length: 6 }, (_, i) => ({ x: 200, y: 420 + i * 12 })));
  s = await state(pg); ok('phone short drag down springs back', s.on, JSON.stringify(s));
  await touch(cx, pg, Array.from({ length: 14 }, (_, i) => ({ x: 200, y: 400 + i * 22 })));
  s = await state(pg); ok('phone long drag down closes and sets the flag', !s.on && s.flag === '1', JSON.stringify(s));
  await cx.close();
  const rm = await br.newContext(Object.assign({ reducedMotion: 'reduce' }, PH)); const p2 = await rm.newPage(); await p2.goto(srv.url); await p2.waitForSelector('#axtour.in'); await p2.waitForTimeout(300);
  ok('reduced motion: the card is in place with no timed move', await p2.evaluate(() => { const c = getComputedStyle(document.querySelector('#axtour .tr-card')); return c.transform === 'none' && parseFloat(c.transitionDuration) < 0.001 && c.opacity === '1'; })); await rm.close();
  console.log(res.join('\n')); console.log(bad ? 'CARD CHECK FAIL ' + bad : 'CARD CHECK PASS ' + res.length); await br.close(); srv.close(); process.exit(bad ? 1 : 0);
})();
