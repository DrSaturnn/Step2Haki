#!/usr/bin/env python3
"""Lane packets for the anchor re-judging: python3 repair/s172e/packets.py PAGE OUTDIR [--sample N SEED]

Writes OUTDIR/rows.json (every term-anchored hover: brief, pop, trigger, masked flag, line, row head, kicker, title,
body) and two packets split by brief, OUTDIR/judge_1/LANE_PACKET.md and OUTDIR/judge_2/LANE_PACKET.md. With --sample,
also OUTDIR/second/LANE_PACKET.md holding N rows drawn with SEED. Text inside a study-mode mask is shown in double
square brackets.
"""
import json
import os
import random
import re
import sys

WS = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.insert(0, os.path.join(WS, 'tools'))
sys.path.insert(0, os.path.join(WS, 'repair', 's170', 'anchors'))
import anchors as A  # noqa: E402
import pagelib as P  # noqa: E402
import site_build  # noqa: E402

MASK = re.compile(r'<span class="(?:nm )?mask(?: w5om)?"[^>]*>')
CARD = re.compile(r'<span class="sp-pop-b"')


def strip_cards(h):
    """h without any hover card body (balanced spans)."""
    out, i = [], 0
    while True:
        m = CARD.search(h, i)
        if not m:
            out.append(h[i:])
            return ''.join(out)
        out.append(h[i:m.start()])
        depth, k = 0, m.start()
        for t in re.finditer(r'<span\b|</span>', h[m.start():]):
            depth += 1 if t.group(0) == '<span' else -1
            if depth == 0:
                k = m.start() + t.end()
                break
        else:
            k = len(h)
        i = k


def mark_masks(h):
    """mask spans become [[...]] (balanced)."""
    while True:
        m = MASK.search(h)
        if not m:
            return h
        depth, k = 1, None
        for t in re.finditer(r'<span\b|</span>', h[m.end():]):
            depth += 1 if t.group(0) == '<span' else -1
            if depth == 0:
                k = m.end() + t.start()
                break
        if k is None:
            return h[:m.start()] + '[[' + h[m.end():]
        h = h[:m.start()] + '[[' + h[m.end():k] + ']]' + h[k + 7:]


def show(h):
    return A.txt(mark_masks(strip_cards(h)))


def in_mask(whole, pos):
    depth_open = None
    for m in MASK.finditer(whole, max(0, pos - 4000), pos):
        depth, closed = 1, False
        for t in re.finditer(r'<span\b|</span>', whole[m.end():pos]):
            depth += 1 if t.group(0) == '<span' else -1
            if depth == 0:
                closed = True
                break
        if not closed:
            depth_open = m.start()
    return depth_open is not None


def rows(page):
    out = []
    for b in P.briefs(page):
        whole = page[b.start:b.end]
        for m in A.BTN.finditer(whole):
            cls, pid = m.group(1), m.group(2)
            if 'sp-a' not in cls.split():
                continue
            bs = A.body_span(whole, pid)
            enc = A.enclosing(whole, m.start())
            if not bs or not enc:
                continue
            body = whole[bs[1]:bs[2]]
            kick = A.txt(''.join(re.findall(r'<span class="sp-k[^"]*">(.*?)</span>', body, re.S)))
            title = A.txt(''.join(re.findall(r'<span class="sp-ct">(.*?)</span>', body, re.S)))
            rest = re.sub(r'<span class="sp-k[^"]*">.*?</span>|<span class="sp-ct">.*?</span>', '', body, flags=re.S)
            lines = [A.txt(x) for x in re.findall(r'<span class="sp-l[^"]*">(.*?)</span>', rest, re.S)] or [A.txt(rest)]
            head = ''
            rs, re_ = whole.rfind('<tr', 0, m.start()), whole.find('</tr>', m.start())
            if rs >= 0 and re_ >= 0 and whole.find('</tr>', rs, m.start()) < 0:
                c = re.compile(r'<(td|th)\b[^>]*>').search(whole, rs, re_)
                if c:
                    ce = whole.find('</%s>' % c.group(1), c.end(), re_)
                    if ce >= 0 and not (c.end() <= m.start() < ce):
                        head = show(whole[c.end():ce])
            out.append({'brief': b.id, 'pop': pid, 'trigger': A.txt(m.group(3)), 'masked': in_mask(whole, m.start()),
                        'line': show(whole[enc[0]:enc[1]])[:1500], 'head': head, 'kicker': kick, 'title': title,
                        'body': ' / '.join(l for l in lines if l)})
    return out


def packet(rs, path, title):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write('# %s: %d hovers\n' % (title, len(rs)))
        cur = None
        for r in rs:
            if r['brief'] != cur:
                cur = r['brief']
                f.write('\n## Brief: %s\n' % cur)
            f.write('\n### %s\n' % r['pop'])
            f.write('Trigger: %s%s\n' % (r['trigger'], '  (trigger sits inside a mask)' if r['masked'] else ''))
            f.write('Line: %s\n' % r['line'])
            if r['head']:
                f.write('Row head: %s\n' % r['head'])
            f.write('Card kicker: %s\nCard title: %s\nCard body: %s\n' % (r['kicker'] or '(none)', r['title'] or '(none)', r['body']))


def main():
    a = sys.argv[1:]
    page = site_build.unwrap(P.read_page(a[0]))
    out = a[1]
    rs = rows(page)
    os.makedirs(out, exist_ok=True)
    json.dump(rs, open(os.path.join(out, 'rows.json'), 'w'), indent=1, ensure_ascii=False)
    briefs = []
    for r in rs:
        if r['brief'] not in briefs:
            briefs.append(r['brief'])
    half, n, cut = len(rs) / 2, 0, len(briefs)
    for i, b in enumerate(briefs):
        n += sum(1 for r in rs if r['brief'] == b)
        if n >= half:
            cut = i + 1
            break
    l1 = [r for r in rs if r['brief'] in briefs[:cut]]
    l2 = [r for r in rs if r['brief'] in briefs[cut:]]
    packet(l1, os.path.join(out, 'judge_1', 'LANE_PACKET.md'), 'Hover anchors, lane 1')
    packet(l2, os.path.join(out, 'judge_2', 'LANE_PACKET.md'), 'Hover anchors, lane 2')
    msg = 'packets: %d hovers in %d briefs; lane 1 %d, lane 2 %d' % (len(rs), len(briefs), len(l1), len(l2))
    if '--sample' in a:
        k = a.index('--sample')
        smp = random.Random(int(a[k + 2])).sample(rs, int(a[k + 1]))
        ids = {r['pop'] for r in smp}
        smp = [r for r in rs if r['pop'] in ids]
        packet(smp, os.path.join(out, 'second', 'LANE_PACKET.md'), 'Hover anchors, second read')
        json.dump(sorted(ids), open(os.path.join(out, 'second', 'sample_ids.json'), 'w'))
        msg += '; sample %d' % len(smp)
    print(msg)


if __name__ == '__main__':
    main()
