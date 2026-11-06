#!/usr/bin/env node
// jump_land: where long jumps by link land on a page whose briefs load on demand (s164c chunk 3 (b)).
//
//   node tools/jump_land.js PAGE [--phone] [--http]
//
// Each case starts from a fresh load. After the jump settles (4 s), the target element must be built and its top must
// sit in the upper half of the viewport (-4 px to half the viewport height). Cases:
//   hash      PAGE#id on load: the last brief, a brief in the middle, a step heading inside a far brief
//   sidebar   a click on a brief in the sidebar list (phone: the index opened first): the last and a middle brief
//   xref      a "Pairs with" cross-reference link (a.xref) in a brief near the top to a brief at least 40 briefs away
//   drawer    a brief-drawer button (.sp-drw) in a built brief whose target is unbuilt, then a click on the drawer's
//             "Open the full brief" link (07 jump); first (chunk 3 (c)): the target brief was unbuilt, and the preview
//             (phone: first tap) and the drawer show its built content
//   next      the "Next" link at a brief's end (09 go)
// Prints one line per case and exits 1 when any target is out of view or unbuilt.
'use strict';
const path = require('path');
const { chromium } = require('playwright');
const { serve } = require('./serve_page');

const argv = process.argv.slice(2), phone = argv.includes('--phone'), http = argv.includes('--http');
const page = argv.find(a => !a.startsWith('--'));
if (!page) { console.error('usage: jump_land.js PAGE [--phone] [--http]'); process.exit(2); }

(async () => {
  const srv = http ? await serve(page) : null;
  const base = srv ? srv.url : 'file://' + path.resolve(page);
  const browser = await chromium.launch();
  const view = phone ? { viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true } : { viewport: { width: 1512, height: 945 } };
  let bad = 0;
  async function open(hash) {
    const ctx = await browser.newContext(view), p = await ctx.newPage(), errors = [];
    p.on('pageerror', e => errors.push(String(e)));
    await p.goto(base + (hash ? '#' + hash : ''), { waitUntil: 'load', timeout: 180000 });
    await p.waitForTimeout(1500);
    return { ctx, p, errors };
  }
  async function measure(p, id) {
    return p.evaluate(id => {
      const t = document.getElementById(id), b = t && (t.classList.contains('brief') ? t : t.closest('.brief'));
      if (!t) return { found: false };
      const r = t.getBoundingClientRect();
      return { found: true, built: !!b && !b.querySelector(':scope > template.axl'), top: Math.round(r.top), vh: innerHeight,
        hash: decodeURIComponent(location.hash.slice(1)), unbuilt: document.querySelectorAll('.brief > template.axl').length };
    }, id);
  }
  function report(kind, id, m, errors, note) {
    const ok = m.found && m.built && m.top >= -4 && m.top <= m.vh / 2 && !errors.length;
    bad += !ok;
    console.log((ok ? 'ok  ' : 'BAD ') + kind.padEnd(8) + id.padEnd(28) + JSON.stringify(m) + (note ? ' ' + note : '') + (errors.length ? ' errors: ' + errors.slice(0, 2).join(' | ') : ''));
  }
  // ids from a probe load
  const probe = await open('');
  if (phone) { await probe.p.click('#navtab'); await probe.p.waitForTimeout(700); }
  const ids = await probe.p.evaluate(() => {
    const all = Array.from(document.querySelectorAll('.brief')).filter(b => b.id && b.offsetParent !== null);
    const side = Array.from(document.querySelectorAll('#nav a[data-id]')).filter(a => { const r = a.getBoundingClientRect(); return r.height > 4 && r.width > 4 && (!a.checkVisibility || a.checkVisibility({ checkOpacity: true, checkVisibilityCSS: true })); }).map(a => a.dataset.id);   // links a reader can see (open groups)
    // a step heading id inside a far brief's template
    let step = null;
    for (let i = all.length - 1; i > all.length / 2 && !step; i--) {
      const t = all[i].querySelector(':scope > template.axl'), h = t && t.content.querySelector('h5[id], .dp[id], [id].step');
      if (h) step = h.id;
    }
    return { last: all[all.length - 1].id, mid: all[Math.floor(all.length / 2)].id, step, side: side.length ? [side[side.length - 1], side[Math.floor(side.length / 2)]] : [] };
  });
  await probe.ctx.close();

  for (const id of [ids.last, ids.mid, ids.step].filter(Boolean)) {
    const { ctx, p, errors } = await open(id);
    await p.waitForTimeout(2500);
    report('hash', id, await measure(p, id), errors);
    await ctx.close();
  }
  for (const id of ids.side) {
    const { ctx, p, errors } = await open('');
    if (phone) { await p.click('#navtab'); await p.waitForTimeout(700); }
    const a = p.locator('#nav a[data-id="' + id + '"]').first();
    await a.scrollIntoViewIfNeeded(); await a.click(); await p.waitForTimeout(4000);
    report('sidebar', id, await measure(p, id), errors);
    await ctx.close();
  }
  {
    const { ctx, p, errors } = await open('');
    const x = await p.evaluate(() => {
      const all = Array.from(document.querySelectorAll('.brief')), at = {};
      all.forEach((b, i) => { at[b.id] = i; });
      for (let i = 0; i < all.length; i++) {
        if (window.AX && AX.brief) AX.brief.ensure(all[i]);
        const a = Array.from(all[i].querySelectorAll('a.xref')).find(a => { const j = at[a.getAttribute('href').slice(1)]; return j !== undefined && j - i >= 40 && a.offsetParent !== null; });
        if (a) { a.setAttribute('data-jl', '1'); a.scrollIntoView({ block: 'center', behavior: 'instant' }); return { from: all[i].id, to: a.getAttribute('href').slice(1) }; }
      }
      return null;
    });
    if (x) {
      await p.waitForTimeout(1500);
      await p.click('a[data-jl="1"]'); await p.waitForTimeout(4000);
      report('xref', x.to, await measure(p, x.to), errors, 'from ' + x.from);
    } else console.log('--  xref     no cross-reference 40 briefs away');
    await ctx.close();
  }
  {
    const { ctx, p, errors } = await open('');
    const x = await p.evaluate(() => {
      const all = Array.from(document.querySelectorAll('.brief')), at = {}, lazy = !!document.querySelector('.brief > template.axl');
      all.forEach((b, i) => { at[b.id] = i; });
      for (let i = 0; i < all.length; i++) {
        if (window.AX && AX.brief) AX.brief.ensure(all[i]);
        const d = Array.from(all[i].querySelectorAll('.sp-drw')).find(d => { const j = at[d.getAttribute('data-brief')]; const tb = j !== undefined && all[j]; return tb && j - i >= 20 && d.offsetParent !== null && (!lazy || tb.querySelector(':scope > template.axl')); });
        if (d) { const tb = document.getElementById(d.getAttribute('data-brief'));
          d.setAttribute('data-jl', '1'); d.scrollIntoView({ block: 'center', behavior: 'instant' });
          return { from: all[i].id, to: d.getAttribute('data-brief'), lazy, unbuilt: !!(tb && tb.querySelector(':scope > template.axl')) }; }
      }
      return null;
    });
    if (x) {
      await p.waitForTimeout(1500);
      // touch: the first tap opens a preview (20-site-148f openPv), the second the drawer; desktop: one click opens it
      let pv = null;
      if (phone) {
        await p.click('[data-jl="1"]'); await p.waitForTimeout(900);
        pv = await p.evaluate(() => { const v = document.querySelector('.qx-pv'); return v ? v.textContent.replace(/\s+/g, ' ').trim().length : 0; });
      }
      await p.click('[data-jl="1"]'); await p.waitForTimeout(1200);
      const dtext = await p.evaluate(() => { const v = document.querySelector('.sp-drawer'); return v ? v.textContent.replace(/\s+/g, ' ').trim().length : 0; });
      const okc = (x.unbuilt || !x.lazy) && dtext > 200 && (pv === null || pv > 40);
      bad += !okc;
      console.log((okc ? 'ok  ' : 'BAD ') + 'preview'.padEnd(8) + x.to.padEnd(28) + JSON.stringify({ unbuiltBefore: x.unbuilt, previewChars: pv, drawerChars: dtext }));
      // the drawer's own title link, else any brief link in it, jumps to a brief
      const to = await p.evaluate(() => {
        const dr = document.querySelector('.sp-drawer');
        if (!dr) return null;
        const a = dr.querySelector('a.sp-dopen') || dr.querySelector('a[href^="#"]');
        if (!a) return null;
        a.setAttribute('data-jl2', '1');
        return (a.getAttribute('href') || '#' + (a.getAttribute('data-brief') || '')).slice(1);
      });
      if (to) {
        await p.click('[data-jl2="1"]'); await p.waitForTimeout(4000);
        const holder = await p.evaluate(id => { const t = document.getElementById(id); const b = t && (t.classList.contains('brief') ? t : t.closest('.brief')); return b ? b.id : id; }, to);
        report('drawer', to, await measure(p, to), errors, 'from ' + x.from + ' (drawer for ' + x.to + ', brief ' + holder + ')');
      } else { bad++; console.log('BAD drawer   no drawer opened (or no link in it) for ' + x.to + ' from ' + x.from); }
    } else console.log('--  drawer   no drawer button 20 briefs away');
    await ctx.close();
  }
  {
    const { ctx, p, errors } = await open(ids.mid);
    await p.waitForTimeout(2500);
    const to = await p.evaluate(id => {
      const b = document.getElementById(id), nx = b && b.querySelector('.bb-end .bb-next');
      if (!nx) return null;
      nx.setAttribute('data-jl', '1'); nx.scrollIntoView({ block: 'center', behavior: 'instant' });
      const vis = Array.from(document.querySelectorAll('.brief')).filter(x => x.offsetParent !== null), i = vis.indexOf(b);
      return i > -1 && vis[i + 1] ? vis[i + 1].id : null;   // the Next link has href "#": it goes to the next visible brief
    }, ids.mid);
    if (to) {
      await p.waitForTimeout(1200);
      await p.click('[data-jl="1"]'); await p.waitForTimeout(4000);
      report('next', to, await measure(p, to), errors, 'from ' + ids.mid);
    } else console.log('--  next     no Next link at the end of ' + ids.mid);
    await ctx.close();
  }
  await browser.close(); if (srv) srv.close();
  console.log(bad ? bad + ' case(s) out of view' : 'all cases in view');
  process.exit(bad ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2); });
