#!/usr/bin/env node
/* ui_check.js: targeted style checks between two builds of the page (the review redesign of s164b "Deferred" item 1).
   A check is a selector and the properties to compare; only the elements it matches are measured, before and after,
   in each view and setting. Minutes per run instead of the every-element, every-brief hash of ui_styles.

   node tools/ui_check.js css BASE.html CAND.html CHECKS.json
       checks from every style rule whose selector or declarations differ between the two pages (media and layer
       context included): its selectors on both sides and the longhands of every property it sets
   node tools/ui_check.js residues TOKEN_EXTRA.json CHECKS.json
       checks from the "fail" keys of repair/s164b/data/token_extra.json (selector|property)
   node tools/ui_check.js run BASE.html CAND.html CHECKS.json [--views desk,phone] [--configs a,b|all]
       [--max-els 120] [--max-state 6] [--out RES.json] [--allow ALLOW.json] [--all-props]
       compares the checked properties (and with --all-props every computed property) of each matched element, and of
       its ::before or ::after when the selector names one; a selector with :hover, :focus, :focus-visible,
       :focus-within or :active is measured with that state forced (CDP) on up to --max-state elements. Custom
       properties and motion properties are left out (their effect shows in the real properties; motion is checked by
       ui_lint). An element is keyed by its path from the nearest ancestor with an id, so an element added elsewhere does
       not shift the keys. Exit 1 when a difference is not in ALLOW.json ([{sel, prop, setting?}]).
*/
'use strict';
const fs = require('fs'), path = require('path');
const VIEWS = { desk: { width: 1512, height: 945 }, tablet: { width: 1024, height: 768 }, phone: { width: 390, height: 844, isMobile: true, hasTouch: true } };
const CONFIGS = {
  'flat-light-read': {}, 'sculpted-light-read': { 'ax-flat': '0' }, 'flat-dark-read': { 'ax-theme': 'dark' },
  'sculpted-dark-read': { 'ax-flat': '0', 'ax-theme': 'dark' }, 'flat-tinted-read': { 'ax-theme': 'tinted' },
  'flat-light-recall': { 'ax-study': '1' }, 'flat-dark-recall': { 'ax-theme': 'dark', 'ax-study': '1' },
};
const DEFAULT_CONFIGS = Object.keys(CONFIGS);
const FREEZE = '*,*::before,*::after{content-visibility:visible!important;contain-intrinsic-size:none!important;transition:none!important;animation:none!important;caret-color:transparent!important}';
const DETERMINISM = '(function(){var s=20261105;Math.random=function(){s=(Math.imul(s,1103515245)+12345)>>>0;return (s>>>8)/16777216;};})();';
const STATE_RE = /:(hover|focus-visible|focus-within|focus|active)\b/g;
const HAS_STATE = /:(hover|focus-visible|focus-within|focus|active)\b/;
const PSEUDO_RE = /::?(before|after|placeholder|marker|selection|first-line|first-letter|-webkit-[\w-]+)\b/g;
function arg(a, k, d) { const i = a.indexOf(k); return i >= 0 ? a[i + 1] : d; }

// split a selector list on top-level commas
function splitSel(s) { const out = []; let d = 0, cur = ''; for (const ch of s) { if (ch === '(' || ch === '[') d++; else if (ch === ')' || ch === ']') d--; if (ch === ',' && d === 0) { out.push(cur.trim()); cur = ''; } else cur += ch; } if (cur.trim()) out.push(cur.trim()); return out; }

async function openPage(browser, file, view, cfg, all) {
  const V = VIEWS[view];
  const ctx = await browser.newContext({ viewport: { width: V.width, height: V.height }, isMobile: !!V.isMobile, hasTouch: !!V.hasTouch, deviceScaleFactor: 1 });
  await ctx.addInitScript(s => { try { localStorage.clear(); for (const k in s) localStorage.setItem(k, s[k]); } catch (e) {} }, CONFIGS[cfg] || {});
  await ctx.addInitScript(DETERMINISM);
  await ctx.clock.setFixedTime(new Date('2026-11-05T12:00:00Z'));
  const p = await ctx.newPage(); p.setDefaultTimeout(600000);
  const errs = [];
  p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') errs.push(m.type() + ': ' + m.text()); });
  await p.goto('file://' + path.resolve(file) + (all ? '?axall' : ''), { waitUntil: 'load', timeout: 600000 });
  await p.evaluate(() => document.fonts && document.fonts.ready);
  await p.waitForTimeout(all ? 2500 : 800);
  await p.addStyleTag({ content: FREEZE });
  await p.evaluate(() => window.scrollTo(0, 0));
  await p.waitForTimeout(300);
  return { p, ctx, errs };
}

// every style rule with its context, from the page's own sheets (the minified bundle is parsed by the browser)
const RULES = () => {
  const out = [];
  const walk = (list, ctx) => { for (const r of list) {
    if (r.selectorText !== undefined && r.style) {
      const decl = []; for (let i = 0; i < r.style.length; i++) { const k = r.style[i]; decl.push(k + ':' + r.style.getPropertyValue(k) + (r.style.getPropertyPriority(k) ? '!' : '')); }
      out.push({ ctx: ctx.join(' / '), sel: r.selectorText, decl: decl.sort().join(';'), props: Array.from({ length: r.style.length }, (_, i) => r.style[i]) });
      if (r.cssRules && r.cssRules.length) walk(r.cssRules, ctx.concat(['& ' + r.selectorText]));
    } else if (r.cssRules) {
      const tag = r.media ? '@media ' + r.media.mediaText : r.name !== undefined ? '@layer ' + r.name : r.conditionText !== undefined ? '@supports ' + r.conditionText : '@' + r.constructor.name;
      walk(r.cssRules, ctx.concat([tag]));
    } else if (r.constructor.name === 'CSSLayerStatementRule') { /* order only */ }
  } };
  for (const sh of document.styleSheets) { let rs; try { rs = sh.cssRules; } catch (e) { continue; } if (sh.ownerNode && sh.ownerNode.closest && sh.ownerNode.closest('svg')) continue; walk(rs, []); }
  return out;
};

async function cssChecks(a) {
  const { chromium } = require('playwright');
  const browser = await chromium.launch();
  const side = {};
  for (const [k, f] of [['base', a[1]], ['cand', a[2]]]) { const o = await openPage(browser, f, 'desk', 'flat-light-read', false); side[k] = await o.p.evaluate(RULES); await o.ctx.close(); }
  await browser.close();
  const key = r => r.ctx + '\u0001' + r.sel + '\u0001' + r.decl;
  const count = list => { const m = new Map(); for (const r of list) m.set(key(r), (m.get(key(r)) || 0) + 1); return m; };
  const cb = count(side.base), cc = count(side.cand);
  const changed = [];
  for (const [list, mine, other, tag] of [[side.base, cb, cc, 'base'], [side.cand, cc, cb, 'cand']]) {
    const seen = new Map();
    for (const r of list) { const k = key(r); seen.set(k, (seen.get(k) || 0) + 1); if (seen.get(k) > (other.get(k) || 0)) changed.push(Object.assign({ side: tag }, r)); }
  }
  // one check per selector, properties merged; custom properties are left out (their effect shows in real properties)
  const by = new Map();
  for (const r of changed) for (const s of splitSel(r.sel)) {
    if (/^(?:html|:root)?(?:\[data-[\w-]+(?:[~|^$*]?=[^\]]*)?\])*$/.test(s) && r.props.every(p => p.startsWith('--'))) continue;  // token values on the root
    const c = by.get(s) || { sel: s, props: new Set(), from: new Set() };
    r.props.forEach(p => { if (!p.startsWith('--')) c.props.add(p); });
    if (r.props.some(p => p.startsWith('--'))) c.props.add('*');   // a token changed on a scope: compare everything
    c.from.add(r.side); by.set(s, c);
  }
  const checks = [...by.values()].filter(c => c.props.size).map(c => ({ sel: c.sel, props: [...c.props], from: [...c.from].join('+') }));
  fs.writeFileSync(a[3], JSON.stringify({ base: a[1], cand: a[2], rules: { base: side.base.length, cand: side.cand.length, changed: changed.length }, checks }, null, 1));
  console.log('ui_check css: rules base', side.base.length, 'cand', side.cand.length, 'changed', changed.length, '-> checks', checks.length);
}

function residueChecks(a) {
  const d = JSON.parse(fs.readFileSync(a[1]));
  const by = new Map();
  for (const kp of Object.keys(d.fail || {})) { const i = kp.lastIndexOf('|'); const s = kp.slice(0, i), p = kp.slice(i + 1); if (p.startsWith('--')) continue;
    for (const one of splitSel(s)) { const c = by.get(one) || { sel: one, props: new Set() }; c.props.add(p); by.set(one, c); } }
  const checks = [...by.values()].map(c => ({ sel: c.sel, props: [...c.props], from: 'token_extra.fail' }));
  fs.writeFileSync(a[2], JSON.stringify({ checks }, null, 1));
  console.log('ui_check residues:', checks.length, 'checks from', Object.keys(d.fail || {}).length, 'fail keys');
}

// in-page measurement: per check, the matched elements (sampled), their path keys and the compared values
const MEASURE = ({ checks, maxEls, allProps }) => {
  const SKIP = /^(--|transition|animation|caret-color)/;
  const longhands = new Map(), probe = document.createElement('div');
  const expand = p => { if (longhands.has(p)) return longhands.get(p); let v = [p];
    if (p !== '*') { probe.removeAttribute('style'); try { probe.style.setProperty(p, 'inherit'); } catch (e) {} if (probe.style.length) v = Array.from({ length: probe.style.length }, (_, i) => probe.style[i]); }
    longhands.set(p, v); return v; };
  const pathOf = e => { const parts = []; let n = e; while (n && n.nodeType === 1) { if (n.id && n !== e) { parts.unshift('#' + n.id); break; } if (n.id && n === e) { parts.unshift('#' + n.id); break; } const par = n.parentElement; if (!par) { parts.unshift(n.tagName.toLowerCase()); break; } parts.unshift(n.tagName.toLowerCase() + ':' + Array.prototype.indexOf.call(par.children, n)); n = par; } return parts.join('>'); };
  const h = s => { let x = 2166136261 >>> 0; for (let i = 0; i < s.length; i++) { x ^= s.charCodeAt(i); x = Math.imul(x, 16777619) >>> 0; } return x.toString(36); };
  const read = (e, pe, props) => { const cs = getComputedStyle(e, pe || null), m = {};
    if (props.includes('*') || allProps) { for (let i = 0; i < cs.length; i++) { const k = cs[i]; if (!SKIP.test(k)) m[k] = cs.getPropertyValue(k); } }
    else props.forEach(p => expand(p).forEach(l => { if (!SKIP.test(l)) m[l] = cs.getPropertyValue(l); }));
    if (!pe) { const r = e.getBoundingClientRect(); m['@box'] = [r.left, r.top + scrollY, r.width, r.height].map(v => Math.round(v)).join(','); }
    return m; };
  const res = [];
  checks.forEach((c, ci) => {
    const pe = ((c.sel.match(/::?(before|after|placeholder|marker)\b/) || [])[1]);
    const stripped = c.sel.replace(/::?(before|after|placeholder|marker|selection|first-line|first-letter|-webkit-[\w-]+)\b(\([^)]*\))?/g, '').replace(/:(hover|focus-visible|focus-within|focus|active)\b/g, '').replace(/\s+/g, ' ').replace(/([>+~])\s*$/, '$1 *').trim() || '*';
    let els; try { els = Array.from(document.querySelectorAll(stripped)); } catch (e) { res.push({ ci, bad: String(e.message).slice(0, 80) }); return; }
    const n = els.length; if (n > maxEls) { const k = n / maxEls; els = Array.from({ length: maxEls }, (_, i) => els[Math.floor(i * k)]); }
    const out = {};
    els.forEach(e => { const m = read(e, pe ? '::' + pe : null, c.props); out[pathOf(e)] = m; });
    res.push({ ci, n, out });
  });
  return res;
};

// forced states, batched: every sampled element of every state check (and the ancestors a state names) is forced at
// once, the elements are marked with data-axst, read in one pass, then released. The same set is forced on both pages,
// so a cross-effect between two forced elements shows on both.
async function measureStates(page, checks, maxState) {
  const cdp = await page.context().newCDPSession(page);
  await cdp.send('DOM.enable'); await cdp.send('CSS.enable');
  const { root } = await cdp.send('DOM.getDocument', { depth: 0 });
  const force = new Map(), marks = [];   // nodeId -> Set(states); [ci, nodeId, pe]
  const counts = {};
  for (let ci = 0; ci < checks.length; ci++) {
    const c = checks[ci]; const st = [...new Set((c.sel.match(STATE_RE) || []).map(x => x.slice(1)))];
    if (!st.length) continue;
    const pe = ((c.sel.match(/::?(before|after|placeholder|marker)\b/) || [])[1]) || '';
    const stripped = c.sel.replace(PSEUDO_RE, '').replace(STATE_RE, '').replace(/\s+/g, ' ').trim() || '*';
    let ids; try { ids = (await cdp.send('DOM.querySelectorAll', { nodeId: root.nodeId, selector: stripped })).nodeIds; } catch (e) { continue; }
    counts[ci] = ids.length;
    const pick = ids.length > maxState ? Array.from({ length: maxState }, (_, i) => ids[Math.floor(i * ids.length / maxState)]) : ids;
    const compounds = c.sel.split(/\s*[>+~\s]\s*(?![^(\[]*[)\]])/);
    const last = compounds[compounds.length - 1];
    const lastSt = [...new Set((last.match(STATE_RE) || []).map(x => x.slice(1)))];
    const anc = compounds.slice(0, -1).filter(x => HAS_STATE.test(x)).map(x => [x.replace(PSEUDO_RE, '').replace(STATE_RE, '') || '*', [...new Set((x.match(STATE_RE) || []).map(y => y.slice(1)))]]);
    for (const nodeId of pick) {
      const add = (id, sts) => { const z = force.get(id) || new Set(); sts.forEach(x => z.add(x)); force.set(id, z); };
      if (lastSt.length) add(nodeId, lastSt);
      if (anc.length) {
        const { object } = await cdp.send('DOM.resolveNode', { nodeId });
        for (const [sel, sts] of anc) { try { const r = await cdp.send('Runtime.callFunctionOn', { objectId: object.objectId, functionDeclaration: 'function(s){return this.parentElement && this.parentElement.closest(s)}', arguments: [{ value: sel }] });
          if (r.result && r.result.objectId) { const nn = await cdp.send('DOM.requestNode', { objectId: r.result.objectId }); if (nn.nodeId) add(nn.nodeId, sts); } } catch (e) {} }
      }
      marks.push([ci, nodeId, pe]);
    }
  }
  const byNode = new Map();
  marks.forEach(([ci, nodeId, pe], k) => { const l = byNode.get(nodeId) || []; l.push(k); byNode.set(nodeId, l); });
  for (const [nodeId, l] of byNode) await cdp.send('DOM.setAttributeValue', { nodeId, name: 'data-axst', value: l.join(' ') });
  for (const [nodeId, sts] of force) await cdp.send('CSS.forcePseudoState', { nodeId, forcedPseudoClasses: [...sts] });
  const read = await page.evaluate(({ marks, props }) => {
    const SKIP = /^(--|transition|animation|caret-color)/, pr = document.createElement('div'), out = {};
    const ex = (cs, p) => { if (p === '*') { const a = []; for (let i = 0; i < cs.length; i++) a.push(cs[i]); return a; } pr.removeAttribute('style'); try { pr.style.setProperty(p, 'inherit'); } catch (e) {} return pr.style.length ? Array.from({ length: pr.style.length }, (_, i) => pr.style[i]) : [p]; };
    const pathOf = e => { const parts = []; let n = e; while (n && n.nodeType === 1) { if (n.id) { parts.unshift('#' + n.id); break; } const par = n.parentElement; if (!par) { parts.unshift(n.tagName.toLowerCase()); break; } parts.unshift(n.tagName.toLowerCase() + ':' + Array.prototype.indexOf.call(par.children, n)); n = par; } return parts.join('>'); };
    document.querySelectorAll('[data-axst]').forEach(e => { e.getAttribute('data-axst').split(' ').forEach(k => { const [ci, , pe] = marks[+k];
      const cs = getComputedStyle(e, pe ? '::' + pe : null), m = {}; props[ci].forEach(p => ex(cs, p).forEach(l => { if (!SKIP.test(l)) m[l] = cs.getPropertyValue(l); }));
      (out[ci] = out[ci] || {})[pathOf(e)] = m; }); });
    return out; }, { marks, props: checks.map(c => c.props) });
  for (const [nodeId] of force) await cdp.send('CSS.forcePseudoState', { nodeId, forcedPseudoClasses: [] });
  for (const [nodeId] of byNode) await cdp.send('DOM.removeAttribute', { nodeId, name: 'data-axst' });
  await cdp.detach();
  return Object.keys(counts).map(ci => ({ ci: +ci, n: counts[ci], out: read[ci] || {}, state: [...new Set((checks[ci].sel.match(STATE_RE) || []).map(x => x.slice(1)))].join(',') }));
}

async function run(a) {
  const { chromium } = require('playwright');
  const C = JSON.parse(fs.readFileSync(a[3])).checks;
  const views = (arg(a, '--views', 'desk,phone')).split(',');
  const cfgArg = arg(a, '--configs', 'all'); const configs = cfgArg === 'all' ? DEFAULT_CONFIGS : cfgArg.split(',');
  const maxEls = +arg(a, '--max-els', 120), maxState = +arg(a, '--max-state', 6), allProps = a.includes('--all-props');
  const allow = arg(a, '--allow') ? JSON.parse(fs.readFileSync(arg(a, '--allow'))) : [];
  const allowed = (sel, prop, setting) => allow.some(x => (!x.sel || x.sel === sel) && (!x.prop || x.prop === prop || (x.prop.endsWith('*') && prop.startsWith(x.prop.slice(0, -1)))) && (!x.setting || x.setting === setting));
  const plain = C.map((c, i) => Object.assign({ i }, c));
  const stateful = C.filter(c => HAS_STATE.test(c.sel));
  const diffs = [], errs = {}, t0 = Date.now();
  let matched = 0;
  // one load per page and view; the settings are switched in place (as theme_gate does), the same way on both pages
  const APPLY = cfg => { const H = document.documentElement, B = document.body;
    const want = { flat: !/sculpted/.test(cfg), dark: /dark|tinted/.test(cfg), tinted: /tinted/.test(cfg), study: /recall/.test(cfg) };
    B.classList.toggle('flat', want.flat); B.classList.toggle('study', want.study);
    if (want.dark) H.setAttribute('data-theme', 'dark'); else H.removeAttribute('data-theme');
    if (want.tinted) H.setAttribute('data-glass', 'tinted'); else H.removeAttribute('data-glass');
    return new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))); };
  const got = { base: {}, cand: {} };
  for (const [k, f] of [['base', a[1]], ['cand', a[2]]]) for (const view of views) {
    const browser = await chromium.launch();
    const t1 = Date.now();
    const o = await openPage(browser, f, view, 'flat-light-read', true);
    const tl = Date.now() - t1;
    for (const cfg of configs) {
      const setting = view + ':' + cfg; const t2 = Date.now();
      await o.p.evaluate(APPLY, cfg);
      const m = await o.p.evaluate(MEASURE, { checks: plain, maxEls, allProps });
      const t3 = Date.now();
      const s = stateful.length && maxState ? await measureStates(o.p, stateful, maxState) : [];
      got[k][setting] = { m, s };
      console.log('ui_check', k, setting, 'load', Math.round(tl / 1000) + ' s, measure', Math.round((t3 - t2) / 1000) + ' s, states', Math.round((Date.now() - t3) / 1000) + ' s');
    }
    errs[view + ' ' + k] = o.errs.slice(0, 5);
    await browser.close();
  }
  for (const view of views) for (const cfg of configs) {
    const setting = view + ':' + cfg;
    const cmp = (A, B, label) => {
      const bi = new Map(B.map(r => [r.ci, r]));
      for (const ra of A) { const rb = bi.get(ra.ci); if (ra.bad) continue; const sel = (label === 'state' ? stateful : C)[ra.ci].sel;
        if (!rb || rb.bad) { diffs.push({ setting, sel, path: '-', prop: '(selector)', before: 'ok', after: rb ? rb.bad : 'missing' }); continue; }
        if (label === 'plain') matched += Object.keys(ra.out).length;
        for (const p of Object.keys(ra.out)) { const x = ra.out[p], y = rb.out[p];
          if (!y) { if (ra.n === rb.n) diffs.push({ setting, sel, path: p, prop: '(element)', before: 'present', after: 'absent' }); continue; }
          for (const k of Object.keys(x)) if (x[k] !== y[k] && !allowed(sel, k, setting)) diffs.push({ setting, sel, path: p, prop: k, before: x[k], after: y[k], state: label === 'state' ? (ra.state || '') : undefined });
        }
        if (ra.n !== rb.n) diffs.push({ setting, sel, path: '-', prop: '(count)', before: ra.n, after: rb.n });
      } };
    cmp(got.base[setting].m, got.cand[setting].m, 'plain');
    cmp(got.base[setting].s, got.cand[setting].s, 'state');
  }
  // summary: one line per (selector, property, before, after), with the settings and the element count
  const groups = new Map();
  for (const d of diffs) { const k = [d.sel, d.prop, d.before, d.after].join('\u0001'); const g = groups.get(k) || { sel: d.sel, prop: d.prop, before: d.before, after: d.after, settings: new Set(), paths: new Set(), state: d.state }; g.settings.add(d.setting); g.paths.add(d.path); groups.set(k, g); }
  const summary = [...groups.values()].map(g => ({ sel: g.sel, prop: g.prop, before: String(g.before).slice(0, 120), after: String(g.after).slice(0, 120), state: g.state, settings: [...g.settings], elements: g.paths.size, example: [...g.paths][0] }));
  const out = arg(a, '--out');
  if (out) fs.writeFileSync(out, JSON.stringify({ checks: C.length, views, configs, matched, differences: diffs.length, summary, errors: errs }, null, 1));
  for (const g of summary.slice(0, 40)) console.log('DIFF', g.settings.length + ' settings', g.elements + ' el', JSON.stringify(g.sel).slice(0, 90), g.prop, g.state ? '[' + g.state + ']' : '', JSON.stringify(g.before), '->', JSON.stringify(g.after), g.example);
  console.log(summary.length ? 'UI-CHECK DIFFER: ' + summary.length + ' groups, ' + diffs.length + ' values' : 'UI-CHECK SAME', '(' + C.length + ' checks, ' + matched + ' element measurements, ' + views.length * configs.length + ' settings, ' + Math.round((Date.now() - t0) / 1000) + ' s)');
  process.exitCode = summary.length ? 1 : 0;
}

const a = process.argv.slice(2);
if (a[0] === 'css') cssChecks(a).catch(e => { console.error(e); process.exit(2); });
else if (a[0] === 'residues') residueChecks(a);
else if (a[0] === 'run') run(a).catch(e => { console.error(e); process.exit(2); });
else { console.log(fs.readFileSync(__filename, 'utf8').split('*/')[0]); process.exit(2); }
