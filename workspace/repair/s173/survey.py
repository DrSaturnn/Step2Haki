#!/usr/bin/env python3
"""Print old and new plain text of named units, and scan every changed line for patterns the lint does not count."""
import json, re, sys, subprocess
from bs4 import BeautifulSoup

def folder(b):
    return subprocess.run(['python3', 'tools/spine/folder_of.py', b], capture_output=True, text=True).stdout.split('\t')[1].strip()

def plain(h):
    s = BeautifulSoup(h, 'html.parser')
    for x in s.select('span.sp-l, span.sp-ct, span.sp-k, p, td, th, li'):
        x.append(' | ')
    return ' '.join(s.get_text(' ').split())

PAT = [r'^(Worst|Also|Some|Maximum|Most|Best|Others?):', r'\b(the former|the latter|less of both)\b', r'(^|\| )(This|These|It|They) ',
       r', (which|so|making|meaning)\b', r'\b\w+ too\b', r'(^|\| )(And|But) ', r'\bnot\b[^|]*\bbut\b', r'\?', r'\b(rather than|instead of|otherwise|even|only after)\b',
       r', not \b', r'\b(label|AnKing|UWorld|NBME|Merck|MSD|board)\b']
mode = sys.argv[1]
if mode == 'units':
    for arg in sys.argv[2:]:
        b, us = arg.split(':'); f = folder(b)
        base = {x['uid']: x for x in json.load(open(f + '/rewrite_s173/units.json'))['units']}
        new = {x['uid']: x for x in json.load(open(f + '/rewrite_s173/rewrite_s173.json'))['units']}
        for uid in us.split(','):
            print('%s %s\n  OLD %s\n  NEW %s' % (b, uid, plain(base[uid]['html']), plain(new[uid]['new']) if uid in new else '(unchanged)'))
else:
    n = 0
    for b in sys.argv[2:]:
        f = folder(b)
        for x in json.load(open(f + '/rewrite_s173/rewrite_s173.json'))['units']:
            for line in plain(x['new']).split(' | '):
                line = line.strip()
                hit = [p for p in PAT if re.search(p, line)]
                if hit and line:
                    n += 1; print('%s %s [%s] %s' % (b, x['uid'], len(hit), line[:230]))
    print('scan hits', n)
