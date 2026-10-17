#!/usr/bin/env python3
"""bank_items (lead tool, s147): a live brief's practice items, one line each, without reading the brief.
  python3 tools/spine/bank_items.py <brief id> [width]        id, type, distractors, lead-in, stem start
  python3 tools/spine/bank_items.py <brief id> 100 k          id and key only"""
import os,sys,re,html
WS=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..'))
sys.path.insert(0,WS+'/tools')
import pagelib as P
pg=P.read_page(WS+'/index.html')
b=P.brief_by_id(pg,sys.argv[1]); t=pg[b.start:b.end]
pl=lambda x: re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]+>',' ',x))).strip()
i=t.find('<ol class="bank')
print('NBME blocks:',t.count('How NBME framed it'),'| tail starts at', 'authored-hdr' in t)
for m in re.finditer(r'<li([^>]*data-item-id[^>]*)>(.*?)</li>', t[i:], re.S):
    a=m.group(1); g=lambda k: (re.search(k+r'="([^"]*)"',a) or [None,''])[1]
    body=pl(m.group(2)); km=re.search(r'&rarr;\s*<b>(.*?)</b>',m.group(2)); key=pl(km.group(1)) if km else '?'
    if len(sys.argv)>3: print('-',g('data-item-id')[:14],'KEY:',key[:80]); continue
    print('-',g('data-item-id')[:14],g('data-type'),'|',g('data-d1')[:28],'/',g('data-d2')[:28],'|',g('data-lead-in')[:60],'|',body[:int(sys.argv[2]) if len(sys.argv)>2 else 160])
