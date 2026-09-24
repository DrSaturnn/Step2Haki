#!/usr/bin/env python3
"""make_packet.py: assemble a lean worker packet for one backfill.

  python3 repair/efficiency/make_packet.py <T> <brief_id> <source.md> "<Q heading>" "<task>" index.html [out.md] [--edits PATH]

A packet quotes the source question (vendor text), so it is written under repair/sources/ (local-only,
never tracked): default repair/sources/<T>_packets/<brief_id>.md; an out.md outside repair/sources/ is refused.
The edits path named in the packet's instruction line is --edits PATH, else the first repair/...json path in
the task text, else repair/<T>/10_bf_<brief_id>.json, so the header and the Task line name the same file.

Packet = instruction line, task line, RULES_worker.md, only that question's section of the
source file, the brief's current HTML, every brief id + title, the edit format (tools/EDITS.md).
The Q heading matches a markdown heading line (case-insensitive, exact text or prefix); the
section runs to the next heading of the same or higher level.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, 'tools'))
from pagelib import brief_by_id, briefs, read_page  # noqa: E402


def section(md, heading):
    lines = md.split('\n')
    want = heading.strip().lstrip('#').strip().lower()
    hits = []
    for i, l in enumerate(lines):
        m = re.match(r'^(#{1,6})\s+(.*?)\s*#*\s*$', l)
        if m and (m.group(2).lower() == want or m.group(2).lower().startswith(want)):
            hits.append((i, len(m.group(1))))
    exact = [h for h in hits if re.match(r'^#{1,6}\s+(.*?)\s*#*\s*$', lines[h[0]]).group(1).lower() == want]
    hits = exact or hits
    if len(hits) != 1:
        raise SystemExit('make_packet: heading %r matched %d headings in the source; give the exact heading text' % (heading, len(hits)))
    i, lvl = hits[0]
    j = i + 1
    while j < len(lines):
        m = re.match(r'^(#{1,6})\s', lines[j])
        if m and len(m.group(1)) <= lvl:
            break
        j += 1
    return '\n'.join(lines[i:j]).strip()


def demote(md, top=3):
    """Shift markdown headings so the shallowest becomes level `top` (fenced code untouched)."""
    lines, fence = md.split('\n'), False
    levels = []
    for l in lines:
        if l.lstrip().startswith('```'):
            fence = not fence
        elif not fence:
            m = re.match(r'^(#{1,6})\s', l)
            if m:
                levels.append(len(m.group(1)))
    if not levels:
        return md
    shift = max(0, top - min(levels))
    out, fence = [], False
    for l in lines:
        if l.lstrip().startswith('```'):
            fence = not fence
        elif not fence:
            m = re.match(r'^(#{1,6})(\s.*)$', l)
            if m:
                l = '#' * min(6, len(m.group(1)) + shift) + m.group(2)
        out.append(l)
    return '\n'.join(out)


def backfill_format(fmt):
    """EDITS.md without its title and without the new_brief op (backfills never add briefs)."""
    fmt = re.sub(r'^# .*\n', '', fmt, count=1, flags=re.M).strip()
    fmt = re.sub(r'\n## (new_brief|replace_global)\b.*?(?=\n## |\Z)', '', fmt, flags=re.S).strip()
    fmt = re.sub(r' Save batch files as .*?in name order\.', '', fmt)
    return demote(fmt, 3)


def main(argv):
    edits_opt = None
    if '--edits' in argv:
        i = argv.index('--edits')
        if i + 1 >= len(argv):
            print(__doc__)
            return 2
        edits_opt = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    if len(argv) not in (6, 7):
        print(__doc__)
        return 2
    T, bid, src, qh, task, page = argv[:6]
    out = argv[6] if len(argv) == 7 else os.path.join(REPO, 'repair', 'sources', '%s_packets' % T, '%s.md' % bid)
    local_dir = os.path.join(REPO, 'repair', 'sources') + os.sep
    if not os.path.abspath(out).startswith(local_dir):
        raise SystemExit('make_packet: %s is outside repair/sources/ (local-only); packets quote vendor text and '
                         'must never land in a tracked path' % out)
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    html = read_page(page)
    b = brief_by_id(html, bid)
    q = section(open(src, encoding='utf-8').read(), qh)
    rules = open(os.path.join(HERE, 'RULES_worker.md'), encoding='utf-8').read().strip()
    fmt = open(os.path.join(REPO, 'tools', 'EDITS.md'), encoding='utf-8').read().strip()
    kinds = {'brief': 'topic', 'bs': 'board-style', 'aq': 'Aquifer'}
    titles = '\n'.join('%s | %s | %s' % (x.id, x.title, kinds[x.kind]) for x in briefs(html))
    m = re.search(r'\brepair/[\w./-]+\.json\b', task)
    edits_name = edits_opt or (m.group(0) if m else 'repair/%s/10_bf_%s.json' % (T, bid))
    src_rel = os.path.relpath(os.path.abspath(src), REPO)
    if src_rel.startswith('..'):
        src_rel = os.path.abspath(src)
    verify_cmd = 'python3 tools/verify_edits.py %s --nids %s' % (edits_name, src_rel)
    parts = [
        '# Worker packet %s: brief `%s`' % (T, bid),
        '**Instructions.** Everything you need is in this packet. Do not open the skill files or the full page '
        '(index.html). If something essential is missing, say so rather than guess. Write your edits to `%s` in the '
        'format at the end, run `%s` from the workspace folder (Step2Haki/workspace) and loop until it prints PASS. '
        'Return a 3 to 6 line report.' % (edits_name, verify_cmd),
        '## Task\n%s' % task,
        '## Rules\n%s' % demote(re.sub(r'^# .*\n', '', rules, count=1, flags=re.M).strip(), 3),
        '## Source question (%s)\n%s' % (os.path.basename(src), demote(q, 3)),
        '## Brief `%s` (%s): current HTML\nAnchors must be copied verbatim from this HTML and be unique inside it.\n\n```html\n%s\n```'
        % (bid, b.title, html[b.start:b.end]),
        '## All briefs (id | title | kind), for Pairs-with titles and links\n```\n%s\n```' % titles,
        '## Edit format (backfill ops only)\n%s' % backfill_format(fmt),
    ]
    with open(out, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(parts) + '\n')
    print('make_packet: %s -> %s (%d chars, ~%d tokens; brief %d chars, source %d chars)'
          % (T, out, sum(map(len, parts)), sum(map(len, parts)) // 4, b.end - b.start, len(q)))
    print('verify: %s' % verify_cmd)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
