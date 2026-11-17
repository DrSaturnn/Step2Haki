// s176h review screenshots: the desktop Home (first and return visit) at 1101, 1280, 1440 and 1920 wide, the phone Home,
// dark and Tinted at 1440, a brief, and the trap block of each sampled waived brief at 1440 and 393 (BEFORE and AFTER).
// node repair/s176h/shots.js NEW.html LIVE.html OUTDIR SAMPLE.json   (from workspace/; NODE_PATH=/opt/npm-tools/node_modules)
const fs = require('fs'), path = require('path'); const {chromium} = require('playwright'); const {serve} = require(path.resolve('tools/serve_page'));
(async () => {
  const [page, live, out, sampleFile] = process.argv.slice(2); fs.mkdirSync(out, {recursive: true});
  const sample = JSON.parse(fs.readFileSync(sampleFile, 'utf8'));
  const sNew = await serve(page), sLive = await serve(live); const br = await chromium.launch(); const log = [];
  const ctx = async (w, h, s, recent) => {
    const cx = await br.newContext({viewport: {width: w, height: h}, deviceScaleFactor: 1});
    await cx.addInitScript(([s, recent]) => { localStorage.setItem('ax-settings', JSON.stringify({v: 1, s})); if (recent) localStorage.setItem('ax-recent', recent); }, [s, recent || '']);
    return cx;
  };
  const RECENT = JSON.stringify([{id: 'backpain', t: 'Low Back Pain in an Adult', n: '2', l: 'Diagnostic criteria', h: 'backpain'}, {id: 'limp', t: 'Limp in a Child', n: '', l: '', h: 'limp'}, {id: 'hippos', t: 'HIPPOS', n: '', l: '', h: 'hippos'}]);
  const shot = async (srv, name, w, h, s, opts) => {
    opts = opts || {}; const cx = await ctx(w, h, s, opts.recent); const pg = await cx.newPage(); const errs = []; pg.on('pageerror', e => errs.push(e.message));
    await pg.goto(srv.url + (opts.hash || '')); await pg.waitForTimeout(opts.wait || 2800);
    if (opts.sel) {
      const el = await pg.$(opts.sel);
      if (!el) { log.push(name + ': no ' + opts.sel); await cx.close(); return; }
      await el.scrollIntoViewIfNeeded(); await pg.waitForTimeout(500); await el.screenshot({path: path.join(out, name + '.png')});
    } else await pg.screenshot({path: path.join(out, name + '.png')});
    const ov = await pg.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1);
    log.push(name + ': errors ' + errs.length + (ov ? ', horizontal overflow' : '') + (errs.length ? ' ' + errs.join('; ') : ''));
    await cx.close();
  };
  const T = {tour: '1'};
  for (const w of [1101, 1280, 1440, 1920]) {
    await shot(sNew, 'home_' + w + '_first', w, 900, T);
    await shot(sNew, 'home_' + w + '_return', w, 900, T, {recent: RECENT});
  }
  await shot(sLive, 'live_home_1440', 1440, 900, T);
  await shot(sNew, 'home_1440_dark', 1440, 900, {tour: '1', theme: 'dark'}, {recent: RECENT});
  await shot(sNew, 'home_1440_tinted', 1440, 900, {tour: '1', theme: 'tinted'}, {recent: RECENT});
  await shot(sNew, 'home_1440_sculpted', 1440, 900, {tour: '1', surface: 'std'}, {recent: RECENT});
  await shot(sNew, 'home_393_phone', 393, 852, T, {recent: RECENT});
  await shot(sNew, 'brief_1440_backpain', 1440, 900, T, {hash: '#backpain', wait: 3500});
  for (const id of sample) {
    for (const [w, h] of [[1440, 900], [393, 852]]) {
      await shot(sLive, 'trap_' + id + '_' + w + '_before', w, h, T, {hash: '#' + id, wait: 3500, sel: '#' + id + ' .traps'});
      await shot(sNew, 'trap_' + id + '_' + w + '_after', w, h, T, {hash: '#' + id, wait: 3500, sel: '#' + id + ' .traps'});
    }
  }
  fs.writeFileSync(path.join(out, 'shots.txt'), log.join('\n') + '\n'); console.log(log.join('\n'));
  await br.close(); sNew.close(); sLive.close();
})();
