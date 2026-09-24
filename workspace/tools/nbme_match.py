#!/usr/bin/env python3
"""nbme_match.py: rank candidate owning briefs for a question.

  python3 tools/nbme_match.py "<key>" "<stem>" [--page index.html] [-n 5]

TF-IDF (log tf, smoothed idf) over each brief's text; the brief title is counted
3x and the key 2x in the query. Prints the top N briefs (id, title, score) and, for
each, the closest existing bank item (id and keyed answer) so the match can be
confirmed by reading it. A match means the same decision, not the same topic.
"""
import math
import os
import re
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pagelib import briefs, items, read_page, text  # noqa: E402

STOP = set('''a an the and or of to in on for with without at by from as is are was were be been being this that these
those it its he she his her they their them patient patients which what who whom most likely following next best
appropriate step management year old yo y o m f man woman boy girl child infant has have had no not after before
than then there into over under about also only other more less very may can should would will his her all any
each per day days week weeks month months hour hours time since during because due shows show showed presents
presented history exam examination physical reveals revealed'''.split())


def toks(s):
    return [w for w in re.findall(r'[a-z0-9]+', s.lower()) if w not in STOP and len(w) > 1 and not w.isdigit()]


def vec(tf, idf):
    v = {w: (1 + math.log(c)) * idf.get(w, 0.0) for w, c in tf.items()}
    n = math.sqrt(sum(x * x for x in v.values())) or 1.0
    return {w: x / n for w, x in v.items()}


def main(argv):
    page = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'index.html')
    n = 5
    rest = []
    i = 0
    while i < len(argv):
        if argv[i] == '--page':
            page = argv[i + 1]
            i += 2
        elif argv[i] == '-n':
            n = int(argv[i + 1])
            i += 2
        else:
            rest.append(argv[i])
            i += 1
    if len(rest) < 2:
        print(__doc__)
        return 2
    key, stem = rest[0], rest[1]
    html = read_page(page)
    bl = briefs(html)
    docs = []
    for b in bl:
        tf = Counter(toks(text(b.inner)))
        for w in toks(b.title):
            tf[w] += 3
        docs.append(tf)
    df = Counter(w for d in docs for w in d)
    N = len(docs)
    idf = {w: math.log((N + 1) / (c + 0.5)) for w, c in df.items()}
    q = Counter(toks(stem))
    for w in toks(key):
        q[w] += 2
    qv = vec(q, idf)
    scored = []
    for b, d in zip(bl, docs):
        dv = vec(d, idf)
        scored.append((sum(x * dv.get(w, 0.0) for w, x in qv.items()), b))
    scored.sort(key=lambda t: -t[0])
    by_brief = {}
    for it in items(html):
        by_brief.setdefault(it.brief_id, []).append(it)
    print('%-5s %-28s %-6s %s' % ('rank', 'brief id', 'score', 'title  |  closest item'))
    for r, (s, b) in enumerate(scored[:n], 1):
        best, bs = None, -1.0
        for it in by_brief.get(b.id, []):
            iv = vec(Counter(toks(it.stem + ' ' + it.key)), idf)
            sc = sum(x * iv.get(w, 0.0) for w, x in qv.items())
            if sc > bs:
                best, bs = it, sc
        tail = '  |  %s -> %s' % (best.id, best.key[:60]) if best else ''
        print('%-5d %-28s %-6.3f %s%s' % (r, b.id, s, b.title[:60], tail))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
