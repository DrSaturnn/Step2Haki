#!/usr/bin/env python3
"""s170 pilot (runbook 8 step 1): the hover-line display and block headings on the seven s170 briefs.

  python3 repair/pilots/s170/make_pilot.py SRC_PAGE OUT_PAGE

Hovers listed in golden_lines.json get the approved TEXTBOOK_STYLE rows as written (title and lines). Every other
hover body in the seven briefs is split into one sentence per line with its wording unchanged (data-pilot="split"),
so the display can be judged before the rewrite lanes write the final lines. Kickers naming a source are dropped
(C7). The pc-snri and pc-antidep key points take P1 to P3 and P7 to P9 with their block headings. Nothing outside
the seven briefs changes. Then build the candidate with tools/site_build.py OUT_PAGE --out <candidate>.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(WS, 'tools'))
import pagelib  # noqa: E402

BRIEFS = ['pc-ssri', 'pc-snri', 'pc-antidep', 'pc-tca', 'pc-maoi', 'mdd', 'voices']
ARROW = '<span class="op op-a" role="img" aria-label="leads to"></span>'
SRC_KICKER = re.compile(r'^(?:Label|AnKing|Merck|MSD|UWorld|NBME)\b')
OPEN = re.compile(r'<span class="sp-pop-b"[^>]*\bid="([^"]+)"[^>]*>')


def pops(inner):
    """(start, open_end, close_start, end, id) for each hover body, with span nesting balanced."""
    out = []
    for m in OPEN.finditer(inner):
        depth, k = 1, m.end()
        for t in re.finditer(r'<span\b|</span>', inner[m.end():]):
            depth += 1 if t.group(0) == '<span' else -1
            if depth == 0:
                k = m.end() + t.start(); break
        out.append((m.start(), m.end(), k, k + len('</span>'), m.group(1)))
    return out


def arrows(s):
    return s.replace(' → ', ' ' + ARROW + ' ')


def line(s, extra=''):
    cls = 'sp-l'
    if s.startswith('# '):
        cls += ' sp-bh'; s = s[2:]
    elif s.startswith('> '):
        cls += ' sp-la'; s = ARROW + ' ' + s[2:]
    return '<span class="%s"%s>%s</span>' % (cls, extra, arrows(s))


def split_hover(inner, gold):
    """inner: the hover body's inner HTML. Returns the new inner HTML."""
    m = re.match(r'((?:<span class="sp-k[^"]*">[^<]*</span>)?)(<span class="sp-ct">[^<]*</span>)?(.*)$', inner, re.S)
    kick, title, body = m.group(1) or '', m.group(2) or '', m.group(3)
    kt = re.sub(r'<[^>]+>', '', kick)
    if kick and (SRC_KICKER.match(kt) or (gold and gold.get('drop_kicker'))):
        kick = ''
    if gold:
        title = '<span class="sp-ct">%s</span>' % gold['title']
        return kick + title + ''.join(line(x) for x in gold['lines'])
    parts = [p.strip() for p in re.split(r'(?<=[.!?])\s+(?=[A-Z"(])', body.strip()) if p.strip()]
    return kick + title + ''.join(line(p, ' data-pilot="split"') for p in parts)


def keypoint(inner, kp):
    i = inner.index('<ul class="bl">') + len('<ul class="bl">')
    j = inner.index('</ul>', i)
    lis = re.findall(r'<li>.*?</li>', inner[i:j], re.S)
    keep = lis[kp['replace']:]
    new, under = [], False
    for s in kp['lines']:
        if s.startswith('# '):
            new.append('<li class="sp-bh">%s</li>' % s[2:]); under = True
        elif under and not s.startswith('<b>'):
            new.append('<li class="sp-bl">%s</li>' % arrows(s))
        else:
            under = False
            new.append('<li>%s</li>' % arrows(s))
    return inner[:i] + '\n' + '\n'.join(new + keep) + '\n' + inner[j:]


def main(src, dst):
    gold = json.load(open(os.path.join(HERE, 'golden_lines.json')))
    h = pagelib.read_page(src)
    edits, stats = [], {'golden': 0, 'split': 0, 'keypoints': 0}
    for b in pagelib.briefs(h):
        if b.id not in BRIEFS:
            continue
        inner = b.inner

        for a, oe, cs, e, pid in reversed(pops(inner)):
            g = gold['hovers'].get(pid)
            stats['golden' if g else 'split'] += 1
            inner = inner[:oe] + split_hover(inner[oe:cs], g) + inner[cs:]
        if b.id in gold['keypoints']:
            inner = keypoint(inner, gold['keypoints'][b.id]); stats['keypoints'] += 1
        if inner != b.inner:
            edits.append((b.inner_start, b.inner_end, inner))
    pagelib.write_page(dst, pagelib.splice(h, edits))
    print('pilot: briefs changed %d; hovers golden %d, split %d; key points %d' % (len(edits), stats['golden'],
                                                                                 stats['split'], stats['keypoints']))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
