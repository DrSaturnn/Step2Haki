#!/usr/bin/env python3
"""Old and new plain text of a rewrite lane's changed units, written to local/<batch>/survey_<brief>.md; prints counts.
python3 repair/s175/show.py <batch> <brief> [uid,uid]   (run from workspace/; with uids, prints those units instead)"""
import json, re, subprocess, sys
from bs4 import BeautifulSoup
batch, b = sys.argv[1], sys.argv[2]
f = subprocess.run(['python3', 'tools/spine/folder_of.py', b], capture_output=True, text=True).stdout.split('\t')[1].strip()
def plain(h):
    s = BeautifulSoup(h or '', 'html.parser')
    for x in s.select('span.sp-l, span.sp-ct, span.sp-k, p, td, th, li, caption, div'):
        x.append(' | ')
    return ' '.join(s.get_text(' ').split())
base = {x['uid']: x for x in json.load(open('%s/rewrite_%s/units.json' % (f, batch)))['units']}
rw = json.load(open('%s/rewrite_%s/rewrite_%s.json' % (f, batch, batch)))
out = []
for x in rw['units']:
    u = x['uid']; old = base.get(u, {})
    extra = {k: v for k, v in x.items() if k not in ('uid', 'new', 'html', 'raw')}
    out.append('%s %s\n  OLD %s\n  NEW %s' % (u, json.dumps(extra, ensure_ascii=False), plain(old.get('html', '')), plain(x.get('new') or x.get('raw') or x.get('html') or '')))
other = {k: v for k, v in rw.items() if k != 'units'}
out.append('OTHER ' + json.dumps(other, ensure_ascii=False)[:6000])
if len(sys.argv) > 3:
    want = set(sys.argv[3].split(','))
    print('\n'.join(o for o in out if o.split(' ')[0] in want))
else:
    open('local/%s/survey_%s.md' % (batch, b), 'w').write('\n'.join(out) + '\n')
    print(b, 'units changed', len(rw['units']), 'chars', sum(len(o) for o in out), 'keys', sorted({k for x in rw['units'] for k in x}))
