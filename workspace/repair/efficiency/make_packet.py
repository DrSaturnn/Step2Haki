#!/usr/bin/env python3
"""make_packet.py: assemble a lean worker packet for one backfill.

  python3 repair/efficiency/make_packet.py <T> <brief_id> <source.md> "<Q heading>" "<task>" index.html <out.md>

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


def main(argv):
    if len(argv) != 7:
        print(__doc__)
        return 2
    T, bid, src, qh, task, page, out = argv
    html = read_page(page)
    b = brief_by_id(html, bid)
    q = section(open(src, encoding='utf-8').read(), qh)
    rules = open(os.path.join(HERE, 'RULES_worker.md'), encoding='utf-8').read().strip()
    fmt = open(os.path.join(REPO, 'tools', 'EDITS.md'), encoding='utf-8').read().strip()
    kinds = {'brief': 'topic', 'bs': 'board-style', 'aq': 'Aquifer'}
    titles = '\n'.join('%s | %s | %s' % (x.id, x.title, kinds[x.kind]) for x in briefs(html))
    edits_name = 'repair/efficiency/%s_%s.json' % (T, bid)
    parts = [
        '# Worker packet %s: brief `%s`' % (T, bid),
        '**Instructions.** Everything you need is in this packet. Do not open the skill files or the full page '
        '(index.html). If something essential is missing, say so rather than guess. Write your edits to `%s` in the '
        'format at the end, run `python3 tools/verify_edits.py %s` from the repo root and loop until it prints PASS. '
        'Return a 3 to 6 line report.' % (edits_name, edits_name),
        '## Task\n%s' % task,
        '## Rules\n%s' % re.sub(r'^# .*\n', '', rules, count=1).strip(),
        '## Source question (%s)\n%s' % (os.path.basename(src), q),
        '## Brief `%s` (%s): current HTML\nAnchors must be copied verbatim from this HTML and be unique inside it.\n\n```html\n%s\n```'
        % (bid, b.title, html[b.start:b.end]),
        '## All briefs (id | title | kind), for Pairs-with titles and links\n```\n%s\n```' % titles,
        '## Edit format\n%s' % re.sub(r'^# .*\n', '', fmt, count=1).strip(),
    ]
    with open(out, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(parts) + '\n')
    print('make_packet: %s -> %s (%d chars, ~%d tokens; brief %d chars, source %d chars)'
          % (T, out, sum(map(len, parts)), sum(map(len, parts)) // 4, b.end - b.start, len(q)))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
