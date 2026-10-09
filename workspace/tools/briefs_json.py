"""briefs_json: publish a small index of the page's briefs for outside readers.

  python3 tools/briefs_json.py <page.html> <build> <date> <out.json>

Written by ship.sh next to version.json, so it always matches the deployed page.
The Step2Haki Companion browser extension reads it to match UWorld questions to
briefs without parsing the 4 MB page. The file carries facts only (titles,
subtitles, mimic rows, bolded terms, note ids); how they are weighted for
matching lives in the extension.

Schema 1, per brief:
  id, kind (brief|bs|aq), title, shelf [..], bp [..], sub, phrases [..] (subtitle split
  on the middle dot), question (the subtitle's question), nids [..] (every data-nid in the
  brief, items included, page order), nbme (bool), rows [..] (first cells of table rows
  and mimic-drawer buttons), bold [..] (bolded terms 3 to 60 characters)
Everything after the practice bank opens is left out: distractors would read as topics.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pagelib as P  # noqa: E402

BANK = re.compile(r'<(?:div|ol)\b[^>]*\bclass="bank', re.I)


def uniq(seq):
    seen, out = set(), []
    for x in seq:
        k = x.lower()
        if x and k not in seen:
            seen.add(k)
            out.append(x)
    return out


def record(b):
    inner = b.inner
    cut = BANK.search(inner)
    body = inner[:cut.start()] if cut else inner

    sub_m = re.search(r'<p class="sub">(.*?)(?:<span class="subq">|</p>)', inner, re.S)
    sub = P.text(sub_m.group(1)) if sub_m else ''
    q_m = re.search(r'<span class="subq">(.*?)</span>', inner, re.S)

    # The brief's own data-nid (on its opening tag), then every item's.
    nids = b.attrs.get('data-nid', '').split()
    for g in re.findall(r'data-nid="([^"]*)"', inner):
        nids.extend(g.split())

    rows = [P.text(c) for c in re.findall(r'<tr>\s*<td\b[^>]*>(.*?)</td>', body, re.S)]
    rows += [P.text(c) for c in re.findall(r'<button\b[^>]*class="sp-drw"[^>]*>(.*?)</button>', body, re.S)]
    bold = [P.text(c) for c in re.findall(r'<b(?:\s[^>]*)?>(.{3,60}?)</b>', body, re.S)]

    return {
        'id': b.id,
        'kind': b.kind,
        'title': b.title,
        'shelf': b.attrs.get('data-shelf', '').split(),
        'bp': b.attrs.get('data-bp', '').split(),
        'sub': sub,
        'phrases': [p.strip() for p in sub.split('·') if p.strip()],
        'question': P.text(q_m.group(1)) if q_m else '',
        'nids': uniq(nids),
        'nbme': 'data-nbme=' in inner,
        'rows': uniq([r for r in rows if 2 < len(r) <= 80]),
        'bold': uniq([t for t in bold if 3 <= len(t) <= 60]),
    }


def main():
    if len(sys.argv) != 5:
        sys.exit(__doc__.strip().splitlines()[2].strip())
    page, build, date, out = sys.argv[1:]
    html = P.read_page(page)
    briefs = [record(b) for b in P.briefs(html)]

    ids = [r['id'] for r in briefs]
    if not briefs:
        sys.exit('briefs_json: no briefs found')
    if any(not i for i in ids):
        sys.exit('briefs_json: a brief has no id')
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        sys.exit('briefs_json: duplicate ids %s' % ', '.join(dup))

    data = {'schema': 1, 'build': build, 'date': date, 'count': len(briefs), 'briefs': briefs}
    tmp = out + '.tmp'
    with open(tmp, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
        f.write('\n')
    os.replace(tmp, out)
    linked = sum(1 for r in briefs if r['nids'])
    print('briefs.json: %d briefs, %d with note ids, %d KB' % (len(briefs), linked, os.path.getsize(out) // 1024))


if __name__ == '__main__':
    main()
