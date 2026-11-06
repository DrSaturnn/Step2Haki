#!/usr/bin/env node
// s164c: the search parity query set (chat 2's local/s164c/queries.txt was lost with the private repo; chat 3 rebuilds
// it here so it can be regenerated). node repair/s164c/make_queries.js PAGE OUT
// From PAGE's search.json (beside PAGE): 60 title words, 60 two-word title phrases, 80 words from block text
// (5 letters or more), 40 two-word phrases from block text, 40 alias phrases, fixed probes; seeded, deduplicated.
'use strict';
const fs = require('fs'), path = require('path');
const [page, out] = process.argv.slice(2);
const d = JSON.parse(fs.readFileSync(path.join(path.dirname(path.resolve(page)), 'search.json'), 'utf8'));
let s = 164; const rnd = n => { s = (s * 16807) % 2147483647; return s % n; };
const words = t => t.toLowerCase().replace(/[^a-z0-9\s-]/g, ' ').split(/\s+/).filter(Boolean);
const q = new Set(['next step', 'next week', 'lithium', 'ssri', 'qt prolongation', 'serotonin syndrome', 'nms', 'tsh',
  'first line', 'most likely', 'ct', 'mri', 'b12', 'ace inhibitor', 'pregnancy', 'child', 'kawasaki', 'dka']);
const pick = (arr, n, f) => { for (let i = 0, g = 0; i < n && g < n * 20; g++) { const v = f(arr[rnd(arr.length)]); if (v && !q.has(v)) { q.add(v); i++; } } };
const B = d.briefs;
pick(B, 60, b => { const w = words(b.title).filter(x => x.length > 3); return w.length ? w[rnd(w.length)] : null; });
pick(B, 60, b => { const w = words(b.title); if (w.length < 2) return null; const i = rnd(w.length - 1); return w[i] + ' ' + w[i + 1]; });
const blocks = []; B.forEach(b => b.blocks.forEach(k => blocks.push(k[3])));
pick(blocks, 80, t => { const w = words(t).filter(x => x.length >= 5 && /^[a-z]/.test(x)); return w.length ? w[rnd(w.length)] : null; });
pick(blocks, 40, t => { const w = words(t).filter(x => x.length > 2); if (w.length < 2) return null; const i = rnd(w.length - 1); return w[i] + ' ' + w[i + 1]; });
pick(d.groups, 40, g => g[rnd(g.length)]);
fs.writeFileSync(out, Array.from(q).join('\n') + '\n');
console.log(q.size + ' queries -> ' + out);
