"""anki_index: index AnKing exports (Anki "Notes in Plain Text", HTML and tags included) for the spine pipeline.

  python3 tools/spine/anki_index.py <export.txt> [<export.txt> ...] --out repair/sources/anki/anki_index.jsonl

Card text is never a page source (standing rule). The index exists to (1) list the concepts a deck marks as
high yield for each brief, (2) carry each card's identifiers so a claim map can name the exact card it was
checked from, and (3) link cards to UWorld questions by QID tag. Output lives under repair/sources/
(local-only: never committed; vendor_scan treats it as the source side, so the 10-word copy check covers it).

Per note (one JSON line):
  deck        export file stem (Psych, Peds, FM)
  guid        Anki unique identifier (export column 1)
  ankihub_id  AnkiHub note UUID (the last field), when present
  nid         Anki note id: not in a plain-text export; filled later from an .apkg export when available
  text, extra plain text with clozes shown (answers in [brackets])
  text_html, extra_html   raw HTML (emphasis and colors live here)
  hy          the Extra field split into statements (one per line or bullet). The Extra field is the deck's
              pink text, the high-yield notes (Jonathan 2026-10-09: "the extra")
  marks       emphasis spans inside Extra: [{kind: b|u|i|color, color, text}]
  other       other text fields (non-empty after stripping media), {column: text}
  tags        all tags
  uworld      {"step2": [...], "step1": [...], "comlex": [...]} QIDs from #UWorld tags
  shelves     Step 2 shelf tags (e.g. Psych, Peds, FM) from !Shelf and #Resources_by_rotation
"""
import csv
import html as H
import json
import os
import re
import sys

csv.field_size_limit(10 ** 9)

CLOZE = re.compile(r'\{\{c\d+::(.*?)(?:::[^}]*)?\}\}', re.S)
TAG = re.compile(r'<[^>]+>')
UUID = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')
MARK = re.compile(r'<(b|strong|u|i|em)\b[^>]*>(.*?)</\1>|<(?:span|font)\b([^>]*)>(.*?)</(?:span|font)>', re.S | re.I)
COLOR = re.compile(r'(?:color\s*:\s*([^;"\']+)|\bcolor\s*=\s*"?([^"\s>]+))', re.I)
KIND = {'b': 'b', 'strong': 'b', 'u': 'u', 'i': 'i', 'em': 'i'}


def plain(s):
    s = CLOZE.sub(lambda m: '[' + m.group(1) + ']', s)
    s = re.sub(r'<br\s*/?>|</div>|</li>|</tr>', '\n', s, flags=re.I)
    s = H.unescape(TAG.sub('', s))
    s = re.sub(r'[ \t\xa0]+', ' ', s)
    return re.sub(r'\n\s*\n+', '\n', s).strip()


def statements(h):
    out = []
    for line in plain(h).split('\n'):
        t = re.sub(r'^\s*(?:[-\u2022*]|\d+[.)])\s*', '', line).strip()
        if len(t) >= 4:
            out.append(t)
    return out


def marks(h):
    out = []
    for m in MARK.finditer(h):
        if m.group(1):
            t = plain(m.group(2))
            if t:
                out.append({'kind': KIND[m.group(1).lower()], 'text': t})
        else:
            c = COLOR.search(m.group(3) or '')
            t = plain(m.group(4))
            if c and t:
                out.append({'kind': 'color', 'color': (c.group(1) or c.group(2)).strip().lower(), 'text': t})
    return out


def read(path):
    hdr = {}
    lines = []
    with open(path, encoding='utf-8') as f:
        for line in f:
            if line.startswith('#') and not lines and ':' in line:
                k, v = line[1:].rstrip('\n').split(':', 1)
                hdr[k.strip()] = v.strip()
            else:
                lines.append(line)
    if hdr.get('separator') != 'tab' or hdr.get('html') != 'true':
        sys.exit('%s: export must be tab-separated with HTML included (header: %s)' % (path, hdr))
    gcol = int(hdr.get('guid column', 0)) - 1
    tcol = int(hdr.get('tags column', 0)) - 1
    if gcol < 0 or tcol < 0:
        sys.exit('%s: export needs the unique identifier and tags columns' % path)
    return gcol, tcol, list(csv.reader(lines, delimiter='\t'))


def record(deck, row, gcol, tcol):
    fields = [c for i, c in enumerate(row) if i not in (gcol, tcol)]
    text_html = fields[0] if fields else ''
    extra_html = fields[1] if len(fields) > 1 else ''
    ahid = next((c.strip() for c in reversed(fields) if UUID.match(c.strip())), '')
    other = {}
    for i, c in enumerate(fields[2:], start=3):
        if c.strip() == ahid:
            continue
        t = plain(c)
        if len(t) > 3:
            other[str(i)] = t
    tags = row[tcol].split()
    uw = {'step2': [], 'step1': [], 'comlex': []}
    shelves = set()
    for t in tags:
        p = t.split('::')
        if len(p) == 4 and p[1] == '#UWorld' and p[3].isdigit():
            key = 'comlex' if p[2] == 'COMLEX' else ('step2' if p[0].startswith('#AK_Step2') else 'step1')
            uw[key].append(int(p[3]))
        if len(p) >= 3 and p[0].startswith('#AK_Step2') and p[1] in ('!Shelf', '#Resources_by_rotation'):
            shelves.add(p[2])
    return {
        'deck': deck, 'guid': row[gcol], 'ankihub_id': ahid, 'nid': None,
        'text': plain(text_html), 'extra': plain(extra_html),
        'text_html': text_html, 'extra_html': extra_html,
        'hy': statements(extra_html),
        'marks': marks(extra_html), 'other': other, 'tags': tags,
        'uworld': {k: sorted(set(v)) for k, v in uw.items()}, 'shelves': sorted(shelves),
    }


def main():
    args = sys.argv[1:]
    if '--out' not in args or len(args) < 3:
        sys.exit(__doc__.strip().splitlines()[2].strip())
    out = args[args.index('--out') + 1]
    files = [a for a in args if a != '--out' and a != out]
    seen, recs, dup = {}, [], 0
    for path in files:
        deck = os.path.splitext(os.path.basename(path))[0]
        gcol, tcol, rows = read(path)
        n = 0
        for row in rows:
            if len(row) <= max(gcol, tcol):
                continue
            r = record(deck, row, gcol, tcol)
            if r['guid'] in seen:          # same note exported under two decks: keep one, list both decks
                seen[r['guid']]['also'] = sorted(set(seen[r['guid']].get('also', [])) | {deck})
                dup += 1
                continue
            seen[r['guid']] = r
            recs.append(r)
            n += 1
        print('%s: %d notes' % (deck, n))
    os.makedirs(os.path.dirname(out) or '.', exist_ok=True)
    tmp = out + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        for r in recs:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
    os.replace(tmp, out)
    qids = {q for r in recs for v in r['uworld'].values() for q in v}
    print('high-yield statements (Extra): %d across %d notes' % (sum(len(r['hy']) for r in recs), sum(1 for r in recs if r['hy'])))
    print('index: %d notes (%d duplicates across decks), %d with AnkiHub id, %d with a UWorld tag, %d distinct QIDs -> %s'
          % (len(recs), dup, sum(1 for r in recs if r['ankihub_id']),
             sum(1 for r in recs if any(r['uworld'].values())), len(qids), out))


if __name__ == '__main__':
    main()
