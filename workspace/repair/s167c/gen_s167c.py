#!/usr/bin/env python3
"""s167c generator (D-20261107-9): components and sidebar, from the live page, by offset splicing.

  python3 repair/s167c/gen_s167c.py IN_PAGE OUT_PAGE

1. N7 hover triggers A+F (repair/pilots/s167c/hovers.py) and N16 shared timeline axis (timelines.py), brief by brief.
2. N13 the Board-style and Aquifer bands in the body go (div.bsband); NBME badges stay.
3. N11 to N13 moves (MOVES below), the two new Presentations sub headers, static counts.
4. N12, N20 the sidebar is rebuilt from the body: sections from h3.system, sub headers from div.psub and, in the two
   psych sections, from each brief's data-navgrp (added here from the live sidebar); link labels from data-navlabel
   where a brief's sidebar label differs from its title (added here), else the title.
5. N14 sidebar subtitle "By RapidRounds".
Writes repair/s167c/stats/gen_stats.json (outside build.py's *.json glob). Brief text order is unchanged (prose_lint.text_key equal) apart from the moves.
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.dirname(os.path.dirname(HERE))
sys.path[:0] = [os.path.join(WS, 'tools'), os.path.join(WS, 'repair', 'pilots', 's167c')]
import pagelib, hovers, timelines  # noqa: E402

# (brief, where): where is ('psub', id) = end of that Presentations group, ('after', brief), ('section', h3 id) = end
MOVES = [
    ('bs-learning', ('psub', 'pres-psych')), ('peds-sleep', ('after', 'bs-learning')),
    ('bs-shock', ('psub', 'pres-cv')),
    ('aq-bruising', ('psub', 'pres-heme')),
    ('bs-genital-ulcer', ('psub', 'pres-id')),
    ('aq-infant-hypotonia', ('psub', 'pres-neuro')), ('aq-child-headache', ('after', 'aq-infant-hypotonia')),
    ('bs-eyelid-lump', ('after', 'aq-child-headache')), ('bs-reye', ('after', 'bs-eyelid-lump')),
    ('parkinson', ('section', 'neuro')), ('scd-dyspnea', ('section', 'heme')),
    ('hypercalcemia', ('section', 'endo')), ('bs-nat-fracture', ('after', 'elder')),
]
NEW_PSUB = [('pres-heme', 'Hematology', 'pres-id'), ('pres-neuro', 'Neuro &amp; HEENT', 'pres-psych')]  # (id, label, insert before)
SUBTITLE = 'By RapidRounds'


def brief_blocks(h):
    """{id: (start, end)} of each brief div including its trailing newline."""
    out = {}
    for b in pagelib.briefs(h):
        e = b.end + (1 if h[b.end:b.end + 1] == '\n' else 0)
        out[b.id] = (b.start, e)
    return out


def body_seq(h):
    """Ordered body markers: ('h3', id, start), ('psub', id, start), ('brief', id, start, end)."""
    seq = []
    nav_end = h.find('</aside>')
    for m in re.finditer(r'<h3 class="system" id="([^"]+)"|<div class="psub" id="([^"]+)"', h[nav_end:]):
        seq.append(('h3' if m.group(1) else 'psub', m.group(1) or m.group(2), nav_end + m.start()))
    for bid, (s, e) in brief_blocks(h).items():
        seq.append(('brief', bid, s, e))
    seq.sort(key=lambda x: x[2])
    return seq


def group_end(h, kind, key):
    """Offset after the last brief of a psub group or an h3 section (before the next psub/h3)."""
    seq = body_seq(h)
    i = next(k for k, x in enumerate(seq) if x[0] == kind and x[1] == key)
    last = seq[i][2] + h[seq[i][2]:].find('</div>\n') + 7 if kind == 'psub' else None
    for x in seq[i + 1:]:
        if x[0] == 'h3' or (kind == 'psub' and x[0] == 'psub'):
            break
        if x[0] == 'brief':
            last = x[3]
    if last is None:
        raise SystemExit('empty %s %s' % (kind, key))
    return last


def main(src, dst):
    h = pagelib.read_page(src)
    stats = {'hovers': {}, 'timelines': {}}
    # 0. the live sidebar: labels and psych groups (before anything moves)
    a0 = h.find('<div id="navlinks">'); a1 = h.find('</aside>', a0)
    nav = h[a0:a1]
    sects, label, grp, sect_of = [], {}, {}, {}
    cur_sect = cur_sub = None
    for m in re.finditer(r'<div class="(sect[^"]*)"[^>]*>(.*?)</div>|<div class="navsub[^"]*"[^>]*>(.*?)</div>|<a [^>]*href="#([^"]+)"[^>]*>(.*?)</a>', nav):
        if m.group(1):
            cur_sect = (m.group(1), re.sub(r'\s*<span class="count">.*', '', m.group(2)).strip()); sects.append(cur_sect); cur_sub = None
        elif m.group(3) is not None:
            cur_sub = m.group(3).strip()
        else:
            label[m.group(4)] = m.group(5).strip(); sect_of[m.group(4)] = cur_sect
            if cur_sect[0].startswith('sect') and cur_sect[1].startswith('Psych') and cur_sub:
                grp[m.group(4)] = cur_sub
    # 1. brief transforms and data attributes
    edits = []
    for b in pagelib.briefs(h):
        inner, st = b.inner, {}
        inner, s1, _ = hovers.transform(inner)
        inner, s2 = timelines.transform(inner)
        for k, v in s1.items(): stats['hovers'][k] = stats['hovers'].get(k, 0) + v
        for k, v in s2.items(): stats['timelines'][k] = stats['timelines'].get(k, 0) + v
        if inner != b.inner:
            edits.append((b.inner_start, b.inner_end, inner))
        tag = h[b.start:b.open_end]
        new = tag
        if b.id in grp and 'data-navgrp=' not in tag:
            new = new[:-1] + ' data-navgrp="%s">' % grp[b.id]
        lab = label.get(b.id)
        if lab is not None and pagelib.text(lab) != b.title and 'data-navlabel=' not in tag:
            new = new[:-1] + ' data-navlabel="%s">' % pagelib.esc_attr(pagelib.text(lab))
        if new != tag:
            edits.append((b.start, b.open_end, new))
    h = pagelib.splice(h, edits)
    # 2. bands
    bands = list(re.finditer(r'[ \t]*<div class="bsband[^"]*"[^>]*>.*?</div>\n?', h))
    h = pagelib.splice(h, [(m.start(), m.end(), '') for m in bands])
    stats['bands_removed'] = len(bands)
    # 3. new sub headers, then moves
    for pid, lab, before in NEW_PSUB:
        at = h.find('<div class="psub" id="%s"' % before)
        h = h[:at] + '<div class="psub" id="%s"><span class="t">%s</span><span class="n">0</span></div>\n' % (pid, lab) + h[at:]
    for bid, (kind, key) in MOVES:
        s, e = brief_blocks(h)[bid]
        block = h[s:e] if h[e - 1] == '\n' else h[s:e] + '\n'
        h = h[:s] + h[e:]
        if kind == 'after':
            at = brief_blocks(h)[key][1]
        else:
            at = group_end(h, 'psub' if kind == 'psub' else 'h3', key)
        h = h[:at] + block + h[at:]
    stats['moved'] = len(MOVES)
    # static counts: psub .n and the Presentations h3
    seq = body_seq(h)
    counts, cur = {}, None
    for x in seq:
        if x[0] == 'psub': cur = x[1]; counts[cur] = 0
        elif x[0] == 'h3': cur = None
        elif cur: counts[cur] += 1
    for pid, n in counts.items():
        h = re.sub(r'(<div class="psub" id="%s"><span class="t">[^<]*</span><span class="n">)\d+' % pid, r'\g<1>%d' % n, h)
    h = re.sub(r'(<h3 class="system" id="presentations">Presentations <span class="n">)\d+', r'\g<1>%d' % sum(counts.values()), h)
    # data-sys: the section each brief sits in (N20); the gate holds body, sidebar and tag together
    sys_edits, cur = [], None
    for x in body_seq(h):
        if x[0] == 'h3': cur = x[1]
        elif x[0] == 'brief':
            b = pagelib.brief_by_id(h, x[1]); tag = h[b.start:b.open_end]
            new = re.sub(r'\s+data-sys="[^"]*"', '', tag)[:-1] + ' data-sys="%s">' % cur
            if new != tag: sys_edits.append((b.start, b.open_end, new))
    h = pagelib.splice(h, sys_edits)
    stats['data_sys'] = len(sys_edits)
    # 4. the sidebar from the body
    h = rebuild_nav(h, sects)
    # 5. subtitle; masthead board-style count
    h = h.replace('<p>Step 2 &middot; Family Med &middot; Peds</p>', '<p>%s</p>' % SUBTITLE, 1)
    h = re.sub(r'\n\s*<span><b>\d+</b> board-style</span>', '', h, count=1)
    pagelib.write_page(dst, h)
    json.dump(stats, open(os.path.join(HERE, 'stats', 'gen_stats.json'), 'w'), indent=1)
    print(json.dumps(stats))


def rebuild_nav(h, sects):
    """#navlinks from the body: h3.system -> sect (labels in the live sidebar's order), psub -> navsub, briefs -> links."""
    seq = body_seq(h)
    blocks = {b.id: b for b in pagelib.briefs(h)}
    h3ids, cur_h3 = [], None
    for x in seq:
        if x[0] == 'h3': cur_h3 = x[1]
        elif x[0] == 'brief' and cur_h3 and cur_h3 not in h3ids: h3ids.append(cur_h3)
    if len(h3ids) != len(sects):
        raise SystemExit('sidebar sections %d vs body sections %d' % (len(sects), len(h3ids)))
    smap = dict(zip(h3ids, sects))
    out, cur, items = [], None, []

    def flush():
        if cur is None: return
        cls, lab = smap[cur]
        n = sum(1 for i in items if i[0] == 'a')
        out.append('\n    <div class="%s">%s <span class="count">%d</span></div>' % (cls, lab, n))
        last = None
        for i in items:
            if i[0] == 'sub':
                last = i[1]; out.append('\n    <div class="navsub">%s</div>' % i[1])
            else:
                g = i[2]
                if g and g != last:
                    last = g; out.append('\n    <div class="navsub">%s</div>' % g)
                out.append('\n    <a href="#%s">%s</a>' % (i[1], i[3]))
        out.append('\n')
    for x in seq:
        if x[0] == 'h3':
            flush(); cur = x[1] if x[1] in smap else None; items = []
        elif cur is None:
            continue
        elif x[0] == 'psub':
            t = re.search(r'<div class="psub" id="%s"><span class="t">([^<]*)</span>' % x[1], h).group(1)
            items.append(('sub', t))
        else:
            b = blocks[x[1]]
            g = b.attrs.get('data-navgrp')
            lab = b.attrs.get('data-navlabel') or pagelib.esc_attr(b.title).replace('&quot;', '"')
            items.append(('a', b.id, g, lab))
    flush()
    a0 = h.find('<div id="navlinks">') + len('<div id="navlinks">')
    a1 = h.find('\n  </div>', a0)
    return h[:a0] + '\n' + ''.join(out) + h[a1:]


if __name__ == '__main__':
    main(*sys.argv[1:3])
