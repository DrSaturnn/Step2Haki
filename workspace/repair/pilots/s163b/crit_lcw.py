"""s163b I2 survey: the lcw window figures inside each brief's step 2 (Diagnostic criteria), with their row names.
python3 repair/pilots/s163b/crit_lcw.py <page> > local/s163b/survey_lcw.md"""
import re, sys
sys.path.insert(0, 'tools')
import pagelib as P
h = P.read_page(sys.argv[1])
for b in P.briefs(h):
    m = re.search(r'<h5[^>]*id="[^"]*-s2"[^>]*>(.*?)</h5>', b.inner, re.S)
    if not m or 'riteria' not in m.group(1):
        continue
    nxt = re.search(r'<h5 class="tsec', b.inner[m.end():])
    sec = b.inner[m.end(): m.end() + nxt.start() if nxt else len(b.inner)]
    for f in re.finditer(r'<figure class="(lc[wp])[^"]*"', sec):
        rows = re.findall(r'<li class="wr[^"]*"[^>]*>.*?<span class="nm">(.*?)</span>', sec[f.start():], re.S)
        cap = re.search(r'<figcaption[^>]*>(.*?)</figcaption>', sec[f.start():], re.S)
        print('- %s %s | %s | rows: %s' % (b.id, f.group(1), P.text(cap.group(1))[:70] if cap else '', '; '.join(P.text(r) for r in rows[:12])))
