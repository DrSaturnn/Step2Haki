#!/usr/bin/env node
/* render.js: jsdom v24 smoke render of the AxBx page.
   Usage: node tools/render.js [index.html] [--json] [--allow tools/render_allowlist.txt]
   Prints one summary line; prints each failure (with its fix) only when there are failures.
   Exit 0 = pass, 1 = failures, 2 = could not render.
   jsdom MUST be v24 (v30 hangs inside the transform's DOMContentLoaded). */
'use strict';
const fs = require('fs');
const path = require('path');
const repo = path.resolve(__dirname, '..');
let JSDOM, VirtualConsole, ver;
try {
  ({ JSDOM, VirtualConsole } = require(path.join(repo, 'node_modules', 'jsdom')));
  ver = require(path.join(repo, 'node_modules', 'jsdom', 'package.json')).version;
} catch (e) { console.log('render: FAIL cannot load jsdom (run: npm i jsdom@24 in ' + repo + ')'); process.exit(2); }
if (!/^24\./.test(ver)) { console.log('render: FAIL jsdom ' + ver + ' installed; v24 required (npm i jsdom@24)'); process.exit(2); }

const args = process.argv.slice(2);
const asJson = args.includes('--json');
let allowPath = path.join(__dirname, 'render_allowlist.txt');
const ai = args.indexOf('--allow'); if (ai >= 0) allowPath = args[ai + 1];
const file = args.find((a, i) => !a.startsWith('--') && args[i - 1] !== '--allow') || path.join(repo, 'index.html');
const html = fs.readFileSync(file, 'utf8');

const allow = new Set();
if (fs.existsSync(allowPath)) fs.readFileSync(allowPath, 'utf8').split('\n').forEach(l => {
  l = l.replace(/#.*/, '').trim(); if (l) allow.add(l.split(/\s+/).slice(0, 2).join(' '));
});

/* static expectations, from the raw file */
const body = html.slice(0, html.indexOf('<script'));
const staticBriefs = (body.match(/<div\b[^>]*class="brief(?:\s[^"]*)?"/g) || []).length;
const staticBanks = (body.match(/<ol\b[^>]*class="bank(?:\s[^"]*)?"/g) || []).length;

const errors = [];
const vc = new VirtualConsole();
vc.on('jsdomError', e => errors.push(String(e && (e.message || e)).split('\n')[0]));
vc.on('error', (...a) => errors.push('console.error: ' + a.map(String).join(' ').slice(0, 200)));
let axLine = '';
vc.on('log', (...a) => { const s = a.map(String).join(' '); if (s.startsWith('[ax]')) axLine = s; });

const killer = setTimeout(() => { console.log('render: FAIL timed out after 90 s (jsdom hang; is jsdom v24?)'); process.exit(2); }, 90000);

const dom = new JSDOM(html, {
  url: 'http://localhost/index.html', runScripts: 'dangerously', pretendToBeVisual: true, virtualConsole: vc,
  beforeParse(w) {
    w.IntersectionObserver = class { observe() {} unobserve() {} disconnect() {} takeRecords() { return []; } };
    w.scrollTo = () => {}; w.Element.prototype.scrollIntoView = function () {};
    if (!w.matchMedia) w.matchMedia = q => ({ matches: false, media: q, onchange: null, addListener() {}, removeListener() {}, addEventListener() {}, removeEventListener() {}, dispatchEvent() { return false; } });
    delete w.fetch; /* sync must never be load-bearing: render without fetch */
  }
});
const w = dom.window;
w.addEventListener('load', () => setTimeout(check, 400));

function check() {
  const d = w.document, fails = [];
  const F = (code, key, msg, fix) => fails.push({ code, key, msg, fix });
  const briefs = d.querySelectorAll('.brief').length;
  if (briefs !== staticBriefs) F('brief-count', '*', `rendered ${briefs} briefs, file has ${staticBriefs}`, 'a brief block is malformed (unbalanced <div>) or was swallowed; run gate.py');
  const bankwraps = d.querySelectorAll('.bankwrap').length;
  if (bankwraps !== staticBanks) F('bankwrap-count', '*', `${bankwraps} bankwraps for ${staticBanks} ol.bank`, 'an ol.bank sits outside a .brief or its markup is broken');
  const mcqs = Array.from(d.querySelectorAll('.mcq'));
  const ax = w.__axCheck || null;
  if (!ax) F('axcheck', '*', 'window.__axCheck missing: the transform did not finish', 'read the first error below; node --check every script');
  let malformed = 0;
  mcqs.forEach(m => {
    const btn = m.querySelectorAll('.opts > button');
    const labels = Array.from(btn).map(b => { const c = b.cloneNode(true); const k = c.querySelector('.k'); if (k) k.remove(); return c.textContent.replace(/\s+/g, ' ').trim().toLowerCase(); });
    const correct = Array.from(btn).filter(b => b.dataset.correct === '1').length;
    let why = '';
    if (btn.length !== 3) why = btn.length + ' option buttons';
    else if (correct !== 1) why = correct + ' keyed options';
    else if (labels.some(l => !l)) why = 'empty option label';
    else if (new Set(labels).size !== 3) why = 'duplicate option labels';
    if (why) { malformed++; F('mcq-malformed', m.dataset.itemId || '?', `${m.dataset.itemId}: ${why}`, 'each item needs a direct-child arrow, a non-empty keyed segment and distinct data-d1/data-d2'); }
  });
  const grid = sel => { const all = Array.from(d.querySelectorAll(sel)); const bad = all.filter(b => !b.querySelector(':scope > dl.rows'));
    bad.forEach(b => { const br = b.closest('.brief'); F('not-gridded', (br ? br.id : '?') + ':' + sel, `${sel} in ${br ? br.id : '?'} did not columnize`, "author as <b>Term</b> — definition items separated by ' · ' (60%+ of parts must be Term — definition)"); });
    return [all.length - bad.length, all.length]; };
  const crit = grid('.crit'), vig = grid('.vignette');
  const vmask = Array.from(d.querySelectorAll('.vignette .mask'));
  vmask.forEach(m => { const br = m.closest('.brief'); F('vignette-mask', br ? br.id : '?', `vignette in ${br ? br.id : '?'} masks`, 'the vignette never masks; its definitions must be .nomask (do not edit the transform to fix content)'); });
  const ids = new Set(Array.from(d.querySelectorAll('[id]')).map(e => e.id));
  let dead = 0;
  d.querySelectorAll('a[href^="#"]').forEach(a => { const t = decodeURIComponent(a.getAttribute('href').slice(1)); if (t && !ids.has(t)) { dead++; F('dead-anchor', t, `link to #${t} has no target`, 'point the href at an existing id; brief ids are permanent'); } });
  d.querySelectorAll('.scaleref[data-scale]').forEach(s => { const t = s.getAttribute('data-scale'); if (!ids.has(t)) { dead++; F('dead-scaleref', t, `scaleref -> ${t} has no target`, 'give the enumerating element that id'); } });
  const idc = {}; d.querySelectorAll('[id]').forEach(e => { idc[e.id] = (idc[e.id] || 0) + 1; });
  Object.keys(idc).filter(k => idc[k] > 1).forEach(k => F('dup-id-rendered', k, `id ${k} occurs ${idc[k]}x after render`, 'rename the new duplicate (never an existing brief id)'));
  if (ax && ax.before !== ax.after) F('content-invariance', '*', `transform changed word count ${ax.before} -> ${ax.after}`, 'a block lost or duplicated text during transform; inspect the edited brief');
  errors.forEach((e, i) => F('js-error', 'e' + i, e, 'fix the script or markup that throws; run node --check'));

  const real = fails.filter(f => !allow.has(f.code + ' ' + f.key));
  const allowed = fails.length - real.length;
  const summary = `render: ${real.length ? 'FAIL' : 'PASS'} jsdom ${ver} | briefs ${briefs} | bankwraps ${bankwraps} | mcq ${mcqs.length}` +
    `${ax ? ' (axCheck ' + ax.mcq + ', reveal-only ' + ax.reveal + ')' : ''} | malformed ${malformed} | crit gridded ${crit[0]}/${crit[1]} | vignette gridded ${vig[0]}/${vig[1]}` +
    ` | vignette masks ${vmask.length} | dead anchors ${dead} | js errors ${errors.length}` + (allowed ? ` | allowlisted ${allowed}` : '') + (real.length ? ` | ${real.length} failure(s)` : '');
  if (asJson) console.log(JSON.stringify({ briefs, bankwraps, mcq: mcqs.length, ax, malformed, crit, vig, vmask: vmask.length, dead, errors, fails: real, allowed }));
  else { console.log(summary); real.slice(0, 60).forEach(f => console.log(`  [${f.code}] ${f.msg}\n      fix: ${f.fix}`)); if (real.length > 60) console.log(`  ... ${real.length - 60} more`); }
  clearTimeout(killer);
  w.close();
  process.exit(real.length ? 1 : 0);
}
