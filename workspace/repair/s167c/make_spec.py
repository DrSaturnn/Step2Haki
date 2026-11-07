#!/usr/bin/env python3
"""s167c: turn gen_s167c.py's page into repair/s167c/40_s167c.json, so ship.sh's build.py reproduces it byte for byte.

  python3 repair/s167c/make_spec.py LIVE_PAGE GEN_PAGE

Ops, in order: set_attr on each brief tag (data-navgrp, data-navlabel, data-sys); one replace per changed region
between ol.bank blocks of each brief (widened until unique in the brief); the two new Presentations
sub headers (replace_global); the 13 moves (move_brief, MOVES order); replace_global for every remaining chrome change
(bands, counts, sidebar, subtitle, masthead). The result is checked with apply_edits against GEN_PAGE: every brief and
every chrome segment byte-equal, blank-line runs between briefs aside (the moves space them differently); exit 1 otherwise.
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.dirname(os.path.dirname(HERE))
sys.path[:0] = [os.path.join(WS, 'tools'), HERE]
import pagelib, apply_edits  # noqa: E402
import gen_s167c  # noqa: E402

TOK = re.compile(r'<[^>]*>|[^<]+')
ATTRS = ('data-navgrp', 'data-navlabel', 'data-sys')


def run(html, edits):
    out, _ = apply_edits.apply(html, {'edits': edits})
    return out


BANK = re.compile(r'<ol\b[^>]*class="bank\b.*?</ol>', re.S)


def brief_hunks(bid, old_in, new_in):
    """replace ops for one brief: the brief is split at its ol.bank blocks (no change falls in one, so they are equal in
    both); each region that differs gets one replace from its first to its last changed byte, widened to tag
    boundaries and until unique in the brief. Last region first."""
    ob, nb = [m.group(0) for m in BANK.finditer(old_in)], [m.group(0) for m in BANK.finditer(new_in)]
    if ob != nb:
        raise SystemExit('%s: a bank changed' % bid)
    oparts, nparts = BANK.split(old_in), BANK.split(new_in)
    out, cur, off = [], old_in, [0]
    for k, part in enumerate(oparts[:-1]):
        off.append(off[-1] + len(part) + len(ob[k]))
    for k in reversed(range(len(oparts))):
        a, b = oparts[k], nparts[k]
        if a == b:
            continue
        p = 0
        while p < min(len(a), len(b)) and a[p] == b[p]:
            p += 1
        s = 0
        while s < min(len(a), len(b)) - p and a[len(a) - 1 - s] == b[len(b) - 1 - s]:
            s += 1
        lo = a.rfind('>', 0, p) + 1 if p else 0
        nx = a.find('<', len(a) - s)
        hi = nx if nx != -1 else len(a)
        while True:
            find = a[lo:hi]
            if find and cur.count(find) == 1:
                break
            if lo == 0 and hi == len(a):
                raise SystemExit('%s: region %d is not unique in the brief' % (bid, k))
            lo, hi = max(0, lo - 40), min(len(a), hi + 40)
        rep = a[lo:p] + b[p:len(b) - s] + a[len(a) - s:hi]
        out.append({'op': 'replace', 'brief': bid, 'find': find, 'with': rep})
        at = off[k] + lo
        cur = cur[:at] + rep + cur[at + len(find):]
    return out


def segments(h):
    """[(start, end)] of the chrome between briefs (before the first, between each pair, after the last)."""
    bl = pagelib.briefs(h)
    cuts = [0] + [x for b in bl for x in (b.start, b.end)] + [len(h)]
    return [(cuts[i], cuts[i + 1]) for i in range(0, len(cuts), 2)], [b.id for b in bl]


def chrome_ops(cur, gen):
    """replace_global ops turning cur into gen outside briefs. Briefs must already match one for one, in order; each
    chrome segment is diffed on its own after trimming the common prefix and suffix. Last segment first, so earlier
    offsets hold; each find is widened (inside its segment) until unique in the page as it then stands."""
    cs, cids = segments(cur)
    gs, gids = segments(gen)
    if cids != gids:
        raise SystemExit('brief order differs after the moves')
    out, page = [], cur
    for (c0, c1), (g0, g1) in reversed(list(zip(cs, gs))):
        a, b = cur[c0:c1], gen[g0:g1]
        if a == b or (not a.strip() and not b.strip()):   # blank lines between briefs (moves space them differently)
            continue
        p = 0
        while p < min(len(a), len(b)) and a[p] == b[p]:
            p += 1
        s = 0
        while s < min(len(a), len(b)) - p and a[len(a) - 1 - s] == b[len(b) - 1 - s]:
            s += 1
        lo, hi = p, len(a) - s          # differing span in a; widen to tag boundaries, then until unique
        lo = a.rfind('>', 0, lo) + 1 if lo else 0
        nx = a.find('<', hi)
        hi = nx if nx != -1 else len(a)
        while True:
            find = a[lo:hi]
            if find and page.count(find) == 1:
                break
            lo, hi = max(0, lo - 40), min(len(a), hi + 40)
        rep = a[lo:p] + b[p:len(b) - s] + a[len(a) - s:hi] if lo <= p and hi >= len(a) - s else None
        if rep is None:
            raise SystemExit('widening error')
        out.append({'op': 'replace_global', 'find': find, 'with': rep})
        at = page.find(find)
        page = page[:at] + rep + page[at + len(find):]
    return out


def main(live, genp):
    old, gen = pagelib.read_page(live), pagelib.read_page(genp)
    ob = {b.id: b for b in pagelib.briefs(old)}
    gb = {b.id: b for b in pagelib.briefs(gen)}
    E = []
    for bid, b in ob.items():
        g = gb[bid]
        for a in ATTRS:
            if b.attrs.get(a) != g.attrs.get(a):
                E.append({'op': 'set_attr', 'target': bid, 'attr': a, 'value': g.attrs[a]})
        if b.inner != g.inner:
            E += brief_hunks(bid, b.inner, g.inner)
    for pid, lab, before in gen_s167c.NEW_PSUB:
        a = '<div class="psub" id="%s"' % before
        E.append({'op': 'replace_global', 'find': a,
                  'with': '<div class="psub" id="%s"><span class="t">%s</span><span class="n">0</span></div>\n%s' % (pid, lab, a)})
    cur = run(old, E)
    for bid, (kind, key) in gen_s167c.MOVES:
        if kind == 'after':
            e = {'op': 'move_brief', 'brief': bid, 'after': key}
        else:
            # end of a group: after its last brief, or after the empty header
            seq = gen_s167c.body_seq(cur)
            i = next(k for k, x in enumerate(seq) if x[0] == ('psub' if kind == 'psub' else 'h3') and x[1] == key)
            last = None
            for x in seq[i + 1:]:
                if x[0] == 'h3' or (kind == 'psub' and x[0] == 'psub'):
                    break
                if x[0] == 'brief' and x[1] != bid:
                    last = x[1]
            if last:
                e = {'op': 'move_brief', 'brief': bid, 'after': last}
            else:
                m = re.search(r'<div class="psub" id="%s">.*?</div>' % key, cur)
                e = {'op': 'move_brief', 'brief': bid, 'after_anchor': m.group(0)}
        E.append(e)
        cur = run(cur, [e])
    E += chrome_ops(cur, gen)
    out = run(old, E)
    os_, oids = segments(out)
    gs_, gids = segments(gen)
    ob2 = {b.id: out[b.start:b.end] for b in pagelib.briefs(out)}
    gb2 = {b.id: gen[b.start:b.end] for b in pagelib.briefs(gen)}
    ws = sum(1 for (a0, a1), (b0, b1) in zip(os_, gs_) if out[a0:a1] != gen[b0:b1])
    bad = [i for i, ((a0, a1), (b0, b1)) in enumerate(zip(os_, gs_))
           if out[a0:a1] != gen[b0:b1] and (out[a0:a1].strip() or gen[b0:b1].strip())]
    ok = oids == gids and ob2 == gb2 and not bad
    print('briefs byte-equal: %s; chrome segments differing only in blank lines: %d; other differences: %d'
          % (ob2 == gb2, ws - len(bad), len(bad)))
    dst = os.path.join(HERE, '40_s167c.json')
    json.dump({'edits': E}, open(dst, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    kinds = {}
    for e in E:
        kinds[e['op']] = kinds.get(e['op'], 0) + 1
    print('%d edits %s; build equals gen page (blank lines between briefs aside): %s' % (len(E), kinds, ok))
    if not ok:
        for i in bad[:3]:
            print('segment %d after %s:\n built %r\n gen   %r' % (i, oids[i - 1] if i else None, out[slice(*os_[i])][:300], gen[slice(*gs_[i])][:300]))
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main(*sys.argv[1:3]))
