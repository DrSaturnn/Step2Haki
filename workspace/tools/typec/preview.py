#!/usr/bin/env python3
"""preview.py: render one Type C brief inside a copy of the live page, with the Type C page setup applied.

  python3 tools/typec/preview.py <brief.html> <out.html> [--replace=<old brief id>]

The brief replaces the old brief with the same id (or --replace) and is shown alone; tools/typec/typec.css and the
transform patch are applied to the copy only. index.html is never modified."""
import os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from pagelib import read_page, brief_by_id

src, out = sys.argv[1], sys.argv[2]
new = open(src, encoding='utf-8').read()
bid = re.search(r'<div class="brief[^"]*" id="([^"]+)"', new).group(1)
old = next((x[10:] for x in sys.argv[3:] if x.startswith('--replace=')), bid)
here = os.path.dirname(os.path.abspath(__file__))
page = read_page(os.path.join(here, '..', '..', 'index.html'))
try:
    b = brief_by_id(page, old)
except KeyError:  # a new brief (psych pilots): no brief to replace, so it is appended and shown alone
    b = None
page = page[:b.start] + new + page[b.end:] if b else page.replace('</main>', new + '</main>', 1)
css = open(os.path.join(here, 'typec.css'), encoding='utf-8').read()
css += '\nbody.pilot main > *:not(.masthead){display:none!important}\nbody.pilot main > #pilot-holder{display:block!important}\n'
T1 = "var dl=document.createElement('dl'); dl.className='rows';"
PATCH = " if(ul.classList.contains('mnem')) dl.classList.add('mnem');"
if PATCH not in page:  # the page already carries the Type C setup once s36 ships; never inject it twice
    k = page.index('function mnemonics(){'); j = page.index(T1, k)
    page = page[:j] + T1 + PATCH + page[j + len(T1):]
page = page.replace('</head>', '<style id="typec-css">' + css + '</style></head>', 1) if 'id="typec-css"' not in page else page.replace('</head>', '<style>' + css[css.index('body.pilot'):] + '</style></head>', 1)
js = ("<script>window.addEventListener('load',function(){var b=document.getElementById('%s');var h=document.createElement('div');"
      "h.id='pilot-holder';h.className='wrap';var n=document.createElement('p');n.className='system-note';"
      "n.textContent='Preview: this brief rendered by the live page code with the Type C page setup. Not on the live site.';"
      "h.appendChild(n);document.querySelector('main').appendChild(h);h.appendChild(b);document.body.classList.add('pilot');scrollTo(0,0);});</script>") % bid
i = page.rindex('</body>'); page = page[:i] + js + page[i:]
open(out, 'w', encoding='utf-8').write(page)
print('preview:', bid, len(page))
