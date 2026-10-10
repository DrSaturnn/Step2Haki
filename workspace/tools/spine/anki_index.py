"""anki_index: index AnKing exports (Anki "Notes in Plain Text", HTML and tags included) for the spine pipeline.

  python3 tools/spine/anki_index.py <export.txt> [<export.txt> ...] --out repair/sources/anki/anki_index.jsonl
      [--db <collection.sqlite> ...]   (decompressed collection.anki21b from an .apkg export of the same decks:
                                         adds note ids, field names, and Text/Extra chosen by field name)

Card text is never a page source (standing rule). The index exists to (1) list the concepts a deck marks as
high yield for each brief, (2) carry each card's identifiers so a claim map can name the exact card it was
checked from, and (3) link cards to UWorld questions by QID tag. Output lives under repair/sources/anki/
(local-only: never committed). Besides the index it writes anki_cards.txt, the plain card text (Text, Extra
and other text fields), which tools/vendor_scan.py reads as vendor source, so the 10-word copy check covers
card wording. Only that one file counts as vendor text (the exports, index and databases are skipped), so the
"shared by 3 or more source files" stock rule cannot cancel card lines.

Per note (one JSON line):
  deck        export file stem (Psych, Peds, FM), or the export's deck column when present
  guid        Anki unique identifier (export column 1)
  ankihub_id  AnkiHub note UUID (the last field), when present
  nid         Anki note id (the page's data-nid values), from --db; the plain-text export lacks it
  text, extra plain text with clozes shown (answers in [brackets])
  text_html, extra_html   raw HTML (emphasis and colors live here)
  cloze       the cloze answers in Text: the fact the card tests (its anchor)
  hy          the Extra field split into statements [{id, key, text}]: id = <nid or guid>.<key>, key = first 10 hex
              of sha1 of the normalized text (stable across re-exports and reordering); a line ending in ":" is a
              header and is prefixed to the lines under it instead of standing alone. The Extra field is the deck's
              pink text, the high-yield notes (Jonathan 2026-10-09: "the extra"; the AnKingOverhaul notetype CSS
              colors #extra navy, magenta in night mode)
  marks       emphasis spans inside Extra: [{kind: b|u|i|color, color, text}]
  other       other text fields (non-empty after stripping media), {field name (column number without --db): text}
  tags        all tags
  uworld      {"step2": [...], "step1": [...], "comlex": [...]} QIDs from #UWorld tags
  shelves     Step 2 shelf tags (e.g. Psych, Peds, FM) from !Shelf and #Resources_by_rotation
"""
import csv
import hashlib
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


def norm(t):
    return ' '.join(re.findall(r'[a-z0-9]+', t.lower()))


def statements(h, owner):
    out, head = [], ''
    for line in plain(h).split('\n'):
        t = re.sub(r'^\s*(?:[-\u2022*]|\d+[.)])\s*', '', line).strip()
        if len(t) < 4:
            continue
        if t.endswith(':') and len(t) <= 80:
            head = t
            continue
        if head:
            t = head + ' ' + t
        key = hashlib.sha1(norm(t).encode()).hexdigest()[:10]
        out.append({'id': '%s.%s' % (owner, key), 'key': key, 'text': t})
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
    cols = {k: int(hdr.get(k + ' column', 0)) - 1 for k in ('guid', 'tags', 'notetype', 'deck')}
    if cols['guid'] < 0 or cols['tags'] < 0:
        sys.exit('%s: export needs the unique identifier and tags columns' % path)
    return cols, list(csv.reader(lines, delimiter='\t'))


def record(deck, row, cols, db=None):
    gcol, tcol = cols['guid'], cols['tags']
    meta = {v for v in cols.values() if v >= 0}
    fields = [c for i, c in enumerate(row) if i not in meta]
    ntname = row[cols['notetype']] if cols['notetype'] >= 0 else ''
    if cols['deck'] >= 0:
        deck = row[cols['deck']]
    nid, fn = None, {}
    if db is not None:
        hit = db[0].get(row[gcol])
        if hit:
            nid, mid = hit
            fn = db[1].get(mid, {})
        elif ntname in db[2]:
            fn = db[1].get(db[2][ntname], {})
    byname = {v: k for k, v in fn.items()}
    if 'Text' in byname and 'Extra' in byname:
        text_html, extra_html = fields[byname['Text']], fields[byname['Extra']]
        skip, by = {byname['Text'], byname['Extra']}, 'name'
    else:                       # notetype not in the collections (or no Text/Extra): first two fields
        text_html = fields[0] if fields else ''
        extra_html = fields[1] if len(fields) > 1 else ''
        skip, by = {0, 1}, 'position'
    ahid = next((c.strip() for c in reversed(fields) if UUID.match(c.strip())), '')
    other = {}
    for i, c in enumerate(fields):
        if i in skip or c.strip() == ahid:
            continue
        t = plain(c)
        if len(t) > 3:
            other[fn.get(i, str(i + 2))] = t
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
        'deck': deck, 'notetype': ntname, 'fields_by': by, 'guid': row[gcol], 'ankihub_id': ahid, 'nid': nid,
        'text': plain(text_html), 'extra': plain(extra_html),
        'text_html': text_html, 'extra_html': extra_html,
        'cloze': [plain(m) for m in CLOZE.findall(text_html)],
        'hy': statements(extra_html, nid or row[gcol]),
        'marks': marks(extra_html), 'other': other, 'tags': tags,
        'uworld': {k: sorted(set(v)) for k, v in uw.items()}, 'shelves': sorted(shelves),
    }


def load_dbs(paths):
    import sqlite3
    notes, names, ntids = {}, {}, {}
    for p in paths:
        c = sqlite3.connect(p)
        for ntid, name in c.execute('select id, name from notetypes'):
            ntids[name] = ntid
        for ntid, ord_, name in c.execute('select ntid, ord, name from fields'):
            names.setdefault(ntid, {})[ord_] = name
        for nid, guid, mid in c.execute('select id, guid, mid from notes'):
            notes[guid] = (nid, mid)
    return notes, names, ntids


def main():
    args = sys.argv[1:]
    if '--out' not in args or len(args) < 3:
        sys.exit(__doc__.strip().splitlines()[2].strip())
    files, dbs, out, mode = [], [], None, None
    for a in args:
        if a in ('--out', '--db'):
            mode = a
        elif mode == '--out':
            out, mode = a, None
        elif mode == '--db':
            dbs.append(a)          # every value after --db until the next flag
        else:
            files.append(a)
    if not out or not files:
        sys.exit(__doc__.strip().splitlines()[2].strip())
    db = load_dbs(dbs) if dbs else None
    seen, recs, dup = {}, [], 0
    for path in files:
        deck = os.path.splitext(os.path.basename(path))[0]
        cols, rows = read(path)
        n = 0
        for row in rows:
            if len(row) <= max(cols.values()):
                continue
            r = record(deck, row, cols, db)
            if r['guid'] in seen:          # same note exported under two decks: keep one, list both decks
                seen[r['guid']]['also'] = sorted(set(seen[r['guid']].get('also', [])) | {deck})
                dup += 1
                continue
            seen[r['guid']] = r
            recs.append(r)
            n += 1
        print('%s: %d notes' % (deck, n))
    if db is not None:
        print('note ids from %d collection(s): %d of %d notes (the rest need an .apkg or collection covering them); fields by name for %d'
              % (len(dbs), sum(1 for r in recs if r['nid']), len(recs), sum(1 for r in recs if r['fields_by'] == 'name')))
    os.makedirs(os.path.dirname(out) or '.', exist_ok=True)
    cards = os.path.join(os.path.dirname(out) or '.', 'anki_cards.txt')
    with open(cards + '.tmp', 'w', encoding='utf-8') as f:
        for r in recs:
            f.write('\n'.join([r['text'], r['extra']] + list(r['other'].values())) + '\n\n')
    os.replace(cards + '.tmp', cards)
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
