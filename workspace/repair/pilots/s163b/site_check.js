// s163b I4 and I7 check in Chromium: system heading counts after load, and every Pairs with block (rendered as a
// list, rows with no link). node site_check.js <page.html>
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('file://' + process.argv[2], { waitUntil: 'load', timeout: 120000 }); await p.waitForTimeout(2500);
  const r = await p.evaluate(() => {
    const heads = [...document.querySelectorAll('h3.system')].map(h => h.id + ': ' + ((h.querySelector('.n') || {}).textContent || '').replace(/\s+/g, ' ').trim());
    const pb = [...document.querySelectorAll('.brief .pearls')].filter(x => /^pairs with/i.test((x.querySelector('.lbl') || {}).textContent || ''));
    const list = pb.filter(x => x.classList.contains('qx-pairs')), nolink = list.filter(x => x.querySelector('.qx-nolink'));
    const sample = ['tics', 'nephrotic-child', 'airway', 'bs-reye', 'drug-hemolysis'].map(id => { const x = document.querySelector('#' + id + ' .pearls.qx-pairs');
      return id + ': ' + (x ? [...x.querySelectorAll('.qx-pair')].map(q => q.querySelector('.qx-pn').textContent + ' | ' + ((q.querySelector('.qx-pd') || {}).textContent || '').slice(0, 70)).join(' || ') : 'not a list'); });
    return { heads, blocks: pb.length, lists: list.length, nolink: nolink.map(x => x.closest('.brief').id), sample };
  });
  const shelf = await p.evaluate(() => { const sel = [...document.querySelectorAll('select')].find(x => [...x.options].some(o => o.value === 'peds')); if (!sel) return ['no shelf select']; const was = sel.value; sel.value = 'peds'; sel.dispatchEvent(new Event('change', {bubbles: true}));
    const o = [...document.querySelectorAll('h3.system')].map(h => h.id + ': ' + ((h.querySelector('.n') || {}).textContent || '').replace(/\s+/g, ' ').trim() + (h.closest('.sectwrap') && h.closest('.sectwrap').style.display === 'none' ? ' (hidden)' : ''));
    sel.value = was; sel.dispatchEvent(new Event('change', {bubbles: true})); return o; });
  console.log(JSON.stringify({ ...r, shelf_peds: shelf, errs }, null, 1)); await b.close();
})();
