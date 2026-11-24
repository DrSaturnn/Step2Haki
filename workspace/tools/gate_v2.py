#!/usr/bin/env python3
"""gate_v2: checks on format v2 brief records. Each check reads slots; none reads page markup for meaning.

  python3 tools/gate_v2.py check RECORDS_DIR [--ids A,B] [--move DIR] [--sources DIR] [--waive FILE] [--held-ok FILE]
                                 [--schema FILE] [--lint DIR] [--no-draw] [--held-out FILE]
  python3 tools/gate_v2.py seed MOVE.json ASSEMBLED.json OUT.claims.json     a claim map with every page line listed
  python3 tools/gate_v2.py lines FILE.json [--move]                          the lines of a record, or of a move record
  python3 tools/gate_v2.py selftest PILOTS_DIR [--schema FILE] [--lint DIR]  every check on a planted defect
  python3 tools/gate_v2.py --list

RECORDS_DIR holds ID.json (the record render_v2.py draws) and ID.claims.json (the claim map of the edit pass). --move
is the folder of move records (extract.py), the page's own text per brief. --sources is the folder that holds one
folder per brief id with its source files. --waive lists records that carry no claim map, each with a reason.
--held-ok lists held lines the owner has decided. Exit 0 pass, 1 fail.

A page line is one visible line of a block of the move record, named "BLOCK.LINE" (block 0 is the title and the
lead). A record line is one string or one run list of the record. The claim map gives every page line one row:
  carried   the same words, in the mapped slot          "new": [record line, ...]
  moved     the same words, in another slot or brief    "new": [...], optional "to_brief": ID
  edited    reworded; every number, hedge, negation, side and name of the page line is in "new" plus "also"
  cut       "reason": repeat (with "carried_in": [record line, ...] that hold every token), chrome (a label the
            renderer draws or the format drops) or off-page (a source vignette)
  held      a line with no carrier that the editor would cut or cannot place: fails until listed in --held-ok
Every record line outside Practice is named by a row ("new") or by an "added" entry whose "src" names where it comes
from: {"at": "BLOCK.LINE"} or {"file": PATH, "n": LINE NUMBER, "text": THAT LINE}. A label of the pilots needs no source.
An added entry with "held": REASON in place of "src" is a record line with no source found: it fails as held.
"""
import copy
import csv
import importlib.util
import json
import os
import re
import sys
import tempfile
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

CATALOG = {
    'v2-record': ('every brief drawn in format v2 has a record whose id is the brief id, and the record matches the schema',
                  'write or repair the record; run record_lint.py on it'),
    'v2-slots': ('the required slots of the entry type are present and filled',
                 'fill the slot from the page blocks mapped to it; a slot the page cannot fill is held for the owner'),
    'v2-score': ('a score is shown with its items, their points and its cutoffs; a named instrument is never a cutoff alone',
                 'add the items and points beside the cutoffs (criteria.score), from the board source or the score lookup'),
    'v2-legacy': ('a converted record holds no legacy block and no assembler note',
                  'place each remaining block in its slot (move) or account for it in the claim map (edit), then empty legacy'),
    'v2-empty': ('a converted record has no empty cell or line that the edit pass has not marked as intended',
                 'write the content from the page, or list the place in empty_ok with a reason'),
    'v2-rules': ('the record follows the format rules a schema cannot state (record_lint.py)',
                 'fix the named line'),
    'v2-prose': ('no record line has a prose lint hit above the brief\'s baseline (a converted brief has none)',
                 'rewrite the line in review-book register; the pattern name says which structure is banned'),
    'v2-draw': ('the renderer draws the record, and the drawn strings equal the record strings',
                'fix the record shape the renderer refuses; never edit the drawn markup'),
    'v2-identity': ('brief id and attributes, NBME coverage links, practice items, their ids, order, attributes and markup equal the page',
                    'restore the practice block and the brief attributes from the move record; never edit an id'),
    'v2-claims': ('every page line has exactly one claim row whose "line" is the page line, with a known status',
                  'add the missing row with gate_v2.py seed; a row is never deleted'),
    'v2-lock': ('a carried or moved line keeps its words; an edited line and a repeat cut keep every number, hedge, negation, side and name',
                'restore the dropped token in the record line, name the record line that carries it in "also", or hold the line'),
    'v2-cut': ('a cut names an allowed reason: repeat with carriers, chrome for a label, off-page for a vignette block',
               'give the carrier lines, or mark the line held'),
    'v2-held': ('no line is held without the owner\'s decision',
                'send the held list to the owner; a decided line goes in the held-ok file'),
    'v2-source': ('every record line is named by a claim row or by an added entry with a source line that exists and holds its numbers and names',
                  'name the page line or the source file line the wording comes from; wording with no source is removed'),
}

# ---------- text ----------
def norm(s):
    return ' '.join(str(s).replace(' ', ' ').split())

def words(s):
    return Counter(re.findall(r'[^\W_]+', norm(s).lower()))

BLOCK = {'div', 'p', 'li', 'ul', 'ol', 'table', 'thead', 'tbody', 'tfoot', 'tr', 'td', 'th', 'dl', 'dt', 'dd', 'details',
         'summary', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'section', 'figure', 'figcaption', 'caption', 'blockquote', 'svg',
         'text', 'g', 'title', 'body', 'html', 'pre', 'hr', 'template'}
LABEL_TAG = {'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'th', 'caption', 'summary', 'dt', 'figcaption'}
LABEL_CLS = re.compile(r'\b(lbl|label|cap|hd|head|kicker|sub|ttl|title|sec|k|tag|chip|step)\b')

def html_lines(html):
    """[(text, inline html, is_label)] for one block of page markup"""
    from bs4 import BeautifulSoup, NavigableString, Comment
    root = BeautifulSoup('<div>%s</div>' % html, 'lxml').div
    for x in root.find_all(['script', 'style']):
        x.decompose()
    out = []

    def label(el):
        return el.name in LABEL_TAG or bool(LABEL_CLS.search(' '.join(el.get('class') or [])))

    def walk(el, lab):
        buf = []

        def flush():
            t = norm(''.join(x[0] for x in buf))
            if t:
                out.append((t, norm(''.join(x[1] for x in buf)), lab or all(x[2] for x in buf if norm(x[0]))))
            del buf[:]
        for c in el.children:
            if isinstance(c, Comment):
                continue
            if isinstance(c, NavigableString):
                buf.append((str(c), str(c).replace('<', '&lt;'), False))
            elif c.name == 'br':
                flush()
            elif c.name in BLOCK or c.find(list(BLOCK)):
                flush()
                walk(c, lab or label(c))
            else:
                buf.append((c.get_text(' ') if c.find(True) else c.get_text(), str(c), label(c)))
        flush()
    walk(root, False)
    return out

def page_lines(move):
    """{at: (text, html, is_label, fill)} in page order"""
    out = {}
    env = [move.get('title'), move.get('lead')]
    for i, s in enumerate(x for x in env if x and norm(x)):
        out['0.%d' % (i + 1)] = (norm(s), norm(s), i == 0, 'move')
    for b in move.get('legacy', []):
        if b.get('slot') == 'practice':          # a question bank: compared whole by the identity check
            continue
        for i, (t, h, lab) in enumerate(html_lines(b['html'])):
            out['%s.%d' % (b.get('block'), i + 1)] = (t, h, lab, b.get('fill', ''))
    return out

STRUCT = {'avoid_form', 'geometry', 'head_first', 'c', 'under', 'assembled', 'empty', 'empty_ok', 'chrome', 'mark', 'ref', 'xdom',
          'kind', 'align', 'x', 'lv', 'row', 'once', 'warn', 'format', 'id', 'entry', 'source', 'attrs', 'tone', 'form', 'task',
          'to', 'src', 'version', 'status', 'urgent', 'correct', 'key', 'b', 'i', 'nbme', 'op', 'type', 'nl', 'm', 'label_col', 'inside'}
ENVELOPE = ('practice', 'legacy', 'claims', 'layout', 'flags', 'sections', 'parts', 'kicker', 'aka')

def is_run(x):
    return isinstance(x, dict) and ('t' in x or 'rich' in x or set(x) <= {'op', 'nl'})

def rec_lines(rec):
    """[(path, text, html)] for every string or run list outside practice and legacy"""
    out = []

    def run_html(r):
        t = ''.join(run_html(y) for y in r['rich']) if 'rich' in r else str(r.get('t', '')).replace('<', '&lt;')
        return '<b>%s</b>' % t if r.get('b') else t

    def walk(o, key, path):
        if isinstance(o, str):
            if key not in STRUCT and norm(o):
                out.append((path, norm(o), norm(o).replace('<', '&lt;')))
        elif isinstance(o, list):
            if o and all(is_run(x) for x in o):
                buf = []

                def flush():
                    t = norm(''.join(re.sub(r'<[^>]+>', '', h) for h in buf))
                    if t:
                        out.append((path, norm(t.replace('&lt;', '<')), norm(''.join(buf))))
                    del buf[:]
                for x in o:
                    if x.get('nl'):
                        flush()
                    buf.append(run_html(x))
                flush()
                for j, x in enumerate(o):
                    for k in ('tip', 'why'):
                        if k in x:
                            walk(x[k], k, '%s/%d/%s' % (path, j, k))
            else:
                for j, x in enumerate(o):
                    walk(x, key, '%s/%d' % (path, j))
        elif isinstance(o, dict):
            if is_run(o) and key not in (None,):
                walk([o], key, path)
                return
            for k, v in o.items():
                if k not in STRUCT:
                    walk(v, k, '%s/%s' % (path, k))
    walk({k: v for k, v in rec.items() if k not in ENVELOPE}, None, '')
    return out

def empties(o, path=''):
    if o == '':
        yield path
    elif isinstance(o, list):
        for j, x in enumerate(o):
            yield from empties(x, '%s/%d' % (path, j))
    elif isinstance(o, dict):
        for k, v in o.items():
            if k not in ('practice', 'legacy', 'attrs', 'kicker', 'empty', 'empty_ok'):
                yield from empties(v, '%s/%s' % (path, k))

# ---------- the lock ----------
_ML = None
def lock():
    global _ML
    if _ML is None:
        d = os.path.join(HERE, 'spine')
        _ML = load_mod('meaning_lock', d if os.path.exists(os.path.join(d, 'meaning_lock.py')) else HERE)
    return _ML

def missing(old_html, new_text):
    """tokens of old that new does not hold"""
    return lock().check_pair(old_html, new_text.replace('<', '&lt;'))

# ---------- checks on the record alone ----------
INSTRUMENTS = ['Wells', 'CHA2DS2-VASc', 'CHADS', 'CURB-65', 'Centor', 'PHQ-9', 'PHQ-2', 'GAD-7', 'CIWA', 'COWS', 'Ranson',
               'Glasgow Coma', 'APGAR', 'Apgar', 'Kocher', 'PERC', 'HEART score', 'TIMI', 'MMSE', 'MoCA', 'AUDIT-C', 'CAGE',
               'Bishop', 'Child-Pugh', 'MELD', 'ABCD2', 'qSOFA', 'SOFA', 'Alvarado', 'HAS-BLED', 'Edinburgh', 'Mini-Cog',
               'Geneva', 'PECARN', 'Duke criteria', 'Jones criteria', 'Rome IV', 'NIHSS', 'FRAX', 'ASCVD risk', 'Gleason',
               'Ballard', 'Vanderbilt', 'M-CHAT', 'SAD PERSONS', 'Caprini', 'Light', 'Rotterdam', 'Amsel', 'Tanner']
CUTOFF = re.compile(r'(?:[≥≤<>]\s*\d|\b\d+(?:\.\d+)?\s*(?:to|–|-)\s*\d+(?:\.\d+)?\s*(?:points?\b|or (?:more|higher|greater|less|lower))|\bscore of \d|\b\d+ or (?:more|higher|greater) (?:points?|criteria)\b|\b\d+ points?\b)', re.I)

def shown_instruments(o, out):
    """names of every structure that lists items: a score, a table with two rows or more, a mnemonic, labeled rows"""
    if isinstance(o, dict):
        if 'items' in o and 'cutoffs' in o:
            out.append(str(o.get('name', '')))
        if isinstance(o.get('rows'), list) and len(o['rows']) >= 2:
            for k in ('caption', 'title', 'label', 'name', 'head'):
                if k in o:
                    out.append(json.dumps(o[k], ensure_ascii=False))
        if 'letters' in o:
            out.append(str(o.get('title', '')))
        for v in o.values():
            shown_instruments(v, out)
    elif isinstance(o, list):
        for x in o:
            shown_instruments(x, out)

def check_score(rec):
    out = []

    def scores(o, path):
        if isinstance(o, dict):
            if 'score' in o and isinstance(o['score'], dict):
                yield path + '/score', o['score']
            for k, v in o.items():
                yield from scores(v, '%s/%s' % (path, k))
        elif isinstance(o, list):
            for j, x in enumerate(o):
                yield from scores(x, '%s/%d' % (path, j))
    for path, sc in scores(rec.get('slots', {}), ''):
        items, cuts = sc.get('items') or [], sc.get('cutoffs') or []
        if len(items) < 2:
            out.append('%s: the score %r shows %d item(s)' % (path, sc.get('name'), len(items)))
        if any(not norm(json.dumps(i.get('item', ''))) .strip('"') or not norm(str(i.get('points', ''))) for i in items):
            out.append('%s: an item of %r has no text or no points' % (path, sc.get('name')))
        if not cuts or any(not norm(json.dumps(c.get('range', ''))).strip('"') for c in cuts):
            out.append('%s: the score %r has no cutoff, or a cutoff with no range' % (path, sc.get('name')))
    shown = []
    shown_instruments(rec.get('slots', {}), shown)
    shown = ' '.join(shown).lower()
    for path, t, _ in rec_lines(rec):
        if not CUTOFF.search(t) or path.startswith('/slots/differential'):
            continue
        for name in INSTRUMENTS:
            if re.search(r'(?<![\w-])%s(?![\w-])' % re.escape(name), t) and name.lower() not in shown:
                out.append('%s: %r gives a cutoff of %s, and no slot shows its items' % (path, t[:70], name))
    return out

def load_mod(name, folder):
    p = os.path.join(folder, name + '.py')
    spec = importlib.util.spec_from_file_location(name, p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

class Env:
    def __init__(self, schema=None, lint=None, draw=True):
        if not (schema and lint):
            try:
                import docs_path
                bd = docs_path.batch_dir('s177')
            except Exception:
                bd = HERE
            lint = lint or (bd if os.path.exists(os.path.join(bd, 'record_lint.py')) else HERE)
            schema = schema or os.path.join(lint, 'record.schema.json')
        self.schema = json.load(open(schema, encoding='utf-8'))
        self.L = load_mod('record_lint', lint)
        self.R = None
        if draw:
            import render_v2
            self.R = render_v2
        d = os.path.join(HERE, 'spine')
        d = d if os.path.exists(os.path.join(d, 'prose_lint.py')) else HERE
        if d not in sys.path:
            sys.path.append(d)
        self.P = load_mod('prose_lint', d)
        self.prose_base = {}
        lab = os.path.join(HERE, 'v2_labels.txt')
        self.labels = set(norm(x) for x in open(lab, encoding='utf-8')) if os.path.exists(lab) else set()

def check_record(rec, env):
    """[(code, message)] from the record alone"""
    import jsonschema
    out = []
    S = env.schema
    ent = rec.get('entry')
    need = (S['$defs'].get(ent) or {}).get('required', [])
    slots = rec.get('slots') or {}
    for k in need:
        if not slots.get(k):
            out.append(('v2-slots', 'required slot %s is missing or empty (%s)' % (k, ent)))
        else:
            ref = ((S['$defs'][ent].get('properties') or {}).get(k) or {}).get('$ref', '#/$defs/' + k)
            sub = S['$defs'].get(ref.split('/')[-1], {})
            for kk in sub.get('required', []) if isinstance(slots[k], dict) else []:
                if not slots[k].get(kk):
                    out.append(('v2-slots', 'required slot %s.%s is missing or empty' % (k, kk)))
    if ent not in ('disease', 'hub', 'drug'):
        out.append(('v2-record', 'entry type %r has no format v2 layout' % ent))
    full = copy.deepcopy(S)
    full['properties']['source'] = {'enum': ['page', 'mockup', 'convert']}
    full['properties']['empty_ok'] = {'type': 'array', 'items': {'type': 'object', 'required': ['at', 'reason'],
                                      'properties': {'at': {'type': 'string'}, 'reason': {'type': 'string', 'minLength': 8}}}}
    full['$defs']['text'] = {'oneOf': S['$defs']['text']['oneOf'] + [{'const': ''}]}
    strict = copy.deepcopy(full)
    strict['$defs']['text'] = S['$defs']['text']
    refused = ['/' + '/'.join(str(p) for p in e.absolute_path) for e in jsonschema.Draft202012Validator(strict).iter_errors(rec)]
    for e in jsonschema.Draft202012Validator(full).iter_errors(rec):
        at = '/'.join(str(p) for p in e.absolute_path)
        if 'required property' in e.message and at.startswith('slots') and at.count('/') <= 1:
            continue
        out.append(('v2-record', 'schema: %s at %s' % (e.message[:120], at)))
    if not any(c == 'v2-record' for c, _ in out):
        r2 = dict(rec, source='mockup' if rec.get('source') == 'convert' else rec.get('source'))
        try:
            for m in env.L.rules(r2):
                out.append(('v2-legacy' if m.startswith('legacy slot') else 'v2-rules', m))
        except Exception as e:
            out.append(('v2-rules', 'record_lint could not read the record: %r' % e))
    if rec.get('legacy') and not any(c == 'v2-legacy' for c, _ in out):
        out.append(('v2-legacy', '%d block(s) left in legacy' % len(rec['legacy'])))
    if rec.get('assembled'):
        out.append(('v2-legacy', 'assembler notes are still in the record'))
    ok = set(x['at'] for x in rec.get('empty_ok', []) if isinstance(x, dict))
    for p in empties(rec):
        if p not in ok and any(p == q or p.startswith(q + '/') for q in refused):
            out.append(('v2-empty', 'empty cell or line at %s' % p))
    for m in check_score(rec):
        out.append(('v2-score', m))
    hits = []
    for p, t, _ in rec_lines(rec):
        for pat, mt in env.P.text_checks(t, 'cell'):
            if pat not in env.P.REPORT_ONLY:
                hits.append('%s at %s: %r' % (pat, p, t[:80]))
    if len(hits) > int(env.prose_base.get(rec.get('id'), 0)):
        out += [('v2-prose', h) for h in hits]
    if env.R and not any(c == 'v2-record' for c, _ in out):
        try:
            inner, _, _ = env.R.render(rec)
            lost, added = env.R.check({k: v for k, v in rec.items() if k not in ENVELOPE}, inner)
            for s in list(lost)[:5]:
                out.append(('v2-draw', 'not drawn: %r' % s[:80]))
            for s in list(added)[:5]:
                out.append(('v2-draw', 'drawn, not in the record: %r' % s[:80]))
        except Exception as e:
            out.append(('v2-draw', 'the renderer stops on this record: %s: %s' % (type(e).__name__, str(e)[:120])))
    return out

# ---------- checks against the page: identity, claim map, lock, sources ----------
STATUS = ('carried', 'moved', 'edited', 'cut', 'held')
RETIRED = {'Diagnostic workup', 'Diagnostic test', 'Pause point', 'Chain', 'Insights', 'Bottom line', 'Offered as', 'Pearls',
           'Common wrong answers', 'General rule', 'NBME framing', 'Key points', 'Related topics'}

def is_chrome(text, lab, labels=()):
    """a line the layout draws or drops: an arrow or other mark with no word, a retired or pilot label, a short label element"""
    if not re.search(r'[^\W_]', text):
        return True
    if re.search(r'\d', text) or len(text.split()) > 6:
        return False
    return bool(lab) or text in RETIRED or text in labels

def check_identity(rec, move):
    out = []
    if rec.get('id') != move.get('id'):
        out.append('record id %r, brief id %r' % (rec.get('id'), move.get('id')))
    if rec.get('attrs') != move.get('attrs'):
        out.append('brief attributes differ from the page')
    for k in ('kicker', 'aka'):
        if rec.get(k) != move.get(k):
            out.append('%s differs from the page' % k)
    want = set(re.findall(r'data-nbme="([^"]+)"', ' '.join(b.get('html', '') for b in move.get('legacy', []))))
    have = set()                                       # links the renderer draws: src on an object with nbme: true
    def walk(o):
        if isinstance(o, dict):
            if o.get('nbme') is True and isinstance(o.get('src'), str):
                have.update(o['src'].split())
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk({k: v for k, v in rec.items() if k not in ('legacy', 'attrs')})     # data-nid in attrs is not a coverage link
    want = set(x for v in want for x in v.split())
    for n in sorted(want - have):
        out.append('NBME coverage link %s of the page is not in the record (an object with src and nbme: true)' % n)
    a, b = rec.get('practice', {}).get('items', []), move.get('practice', {}).get('items', [])
    if [x.get('id') for x in a] != [x.get('id') for x in b]:
        out.append('practice item ids or their order differ from the page (%d against %d)' % (len(a), len(b)))
    elif a != b:
        n = sum(x != y for x, y in zip(a, b))
        out.append('%d practice item(s) differ from the page in attributes or markup' % n)
    return out

def check_claims(rec, move, claims, env, others=None, sources=None, held_ok=()):
    """[(code, message)] for the claim map of one converted brief"""
    out = []
    P = page_lines(move)
    bank = set(str(b.get('block')) for b in move.get('legacy', []) if b.get('slot') == 'practice')
    RL = rec_lines(rec)
    rtext = {}
    for _, t, h in RL:
        rtext.setdefault(t, h)
    rows = claims.get('rows', [])
    seen = Counter(str(r.get('at')) for r in rows)
    for at in P:
        if seen[at] != 1:
            out.append(('v2-claims', 'page line %s has %d rows: %r' % (at, seen[at], P[at][0][:60])))
    named = set()

    def carriers(r, key, at):
        got = []
        other = (others or {}).get(r.get('to_brief')) if r.get('to_brief') else None
        if r.get('to_brief') and other is None:
            out.append(('v2-lock', '%s: to_brief %r has no record in this folder' % (at, r.get('to_brief'))))
        pool = set(t for _, t, _ in rec_lines(other)) if other else rtext
        for s in r.get(key) or []:
            s = norm(s)
            if s in pool:
                got.append(s)
                if not other:
                    named.add(s)
            else:
                out.append(('v2-lock', '%s: %s names a line that is not in the record: %r' % (at, key, s[:70])))
        return got

    for r in rows:
        at = str(r.get('at'))
        if at.split('.')[0] in bank:
            continue
        if at not in P:
            out.append(('v2-claims', 'row %s names no page line' % at))
            continue
        text, html, lab, fill = P[at]
        if norm(r.get('line', '')) != text:
            out.append(('v2-claims', '%s: "line" is not the page line %r' % (at, text[:60])))
            continue
        st = r.get('status')
        if st not in STATUS:
            out.append(('v2-claims', '%s: status %r' % (at, st)))
            continue
        if st in ('carried', 'moved'):
            new = carriers(r, 'new', at)
            if not new:
                out.append(('v2-lock', '%s: %s with no record line' % (at, st)))
            elif words(' '.join(new)) != words(text):
                d = (words(text) - words(' '.join(new))) + (words(' '.join(new)) - words(text))
                out.append(('v2-lock', '%s: %s but the words differ (%s): mark it edited' % (at, st, ', '.join(list(d)[:6]))))
        elif st == 'edited':
            new, also = carriers(r, 'new', at), carriers(r, 'also', at)
            if not new:
                out.append(('v2-lock', '%s: edited with no record line' % at))
                continue
            miss = missing(html, ' ; '.join(new + also))
            if miss:
                out.append(('v2-lock', '%s: the edit drops %s from %r' % (at, ', '.join('%s %s' % m for m in miss[:6]), text[:50])))
            src_text = [html] + src_texts(r.get('src'), P, sources, rec, out, at)
            for s in new:
                back = missing(rtext[s], ' ; '.join(re.sub(r'<[^>]+>', '', x) for x in src_text))
                back = [m for m in back if m[0] in ('number', 'negation', 'side', 'direction') or (m[0] == 'name' and m[1].lower() not in text.lower())]
                if back:
                    out.append(('v2-source', '%s: the new line %r adds %s that its page line and sources do not hold' % (at, s[:50], ', '.join('%s %s' % m for m in back[:6]))))
        elif st == 'cut':
            why = r.get('reason')
            if why == 'repeat':
                car = carriers(r, 'carried_in', at)
                if not car:
                    out.append(('v2-cut', '%s: a repeat cut names no carrier line' % at))
                else:
                    miss = missing(html, ' ; '.join(car))
                    if miss:
                        out.append(('v2-lock', '%s: the carriers of the cut lack %s' % (at, ', '.join('%s %s' % m for m in miss[:6]))))
            elif why == 'chrome':
                if not is_chrome(text, lab, env.labels):
                    out.append(('v2-cut', '%s: %r is not a label, so it cannot be cut as chrome' % (at, text[:60])))
            elif why == 'off-page':
                if fill != 'off-page':
                    out.append(('v2-cut', '%s: the block is not an off-page block' % at))
            else:
                out.append(('v2-cut', '%s: cut reason %r is not allowed (repeat, chrome, off-page); a line with no carrier is held' % (at, why)))
        elif st == 'held':
            if (rec.get('id'), at) not in held_ok:
                out.append(('v2-held', '%s: held (%s): %r' % (at, r.get('reason', 'no reason'), text[:70])))
    added = claims.get('added', [])
    for a in added:
        t = norm(a.get('text', ''))
        if t not in rtext:
            out.append(('v2-source', 'an added entry names a line that is not in the record: %r' % t[:70]))
            continue
        named.add(t)
        if a.get('held'):
            if (rec.get('id'), 'added:' + t) not in held_ok:
                out.append(('v2-held', 'record line held, no source found (%s): %r' % (a['held'], t[:70])))
            continue
        if not a.get('src'):
            out.append(('v2-source', 'the added line %r names no source' % t[:70]))
            continue
        n0 = len(out)
        st = src_texts(a['src'], P, sources, rec, out, 'added')
        if len(out) > n0:
            continue
        back = missing(rtext[t], ' ; '.join(re.sub(r'<[^>]+>', '', x) for x in st))
        back = [m for m in back if m[0] != 'source']
        if back:
            out.append(('v2-source', 'the added line %r holds %s that its source lines do not' % (t[:50], ', '.join('%s %s' % m for m in back[:6]))))
    env_lines = set(norm(x) for x in [rec.get('title'), rec.get('lead')] if x)
    for _, t, _ in RL:
        if t in named or t in env.labels:
            continue
        if t in env_lines and any(P[a][0] == t for a in P if a.startswith('0.')):
            continue
        out.append(('v2-source', 'record line with no claim row and no source: %r' % t[:80]))
    return out

def src_texts(src, P, sources, rec, out, at):
    got = []
    for s in src or []:
        if 'at' in s:
            if str(s['at']) in P:
                got.append(P[str(s['at'])][1])
            else:
                out.append(('v2-source', '%s: source page line %s does not exist' % (at, s['at'])))
        elif 'file' in s:
            rel = os.path.normpath(str(s['file']))
            base = os.path.join(sources or '', str(rec.get('id')))
            p = os.path.join(base, rel)
            if rel.startswith('..') or os.path.isabs(rel) or not sources or not os.path.isfile(p):
                out.append(('v2-source', '%s: source file %r is not in the brief\'s source folder' % (at, s['file'])))
                continue
            ls = open(p, encoding='utf-8', errors='replace').read().split('\n')
            n = s.get('n')
            if not isinstance(n, int) or not 1 <= n <= len(ls):
                out.append(('v2-source', '%s: %s has no line %r' % (at, s['file'], n)))
            elif norm(s.get('text', '')) != norm(ls[n - 1]) or not norm(ls[n - 1]):
                out.append(('v2-source', '%s: "text" is not line %d of %s' % (at, n, s['file'])))
            else:
                got.append(norm(ls[n - 1]).replace('<', '&lt;'))
        else:
            out.append(('v2-source', '%s: a source names neither "at" nor "file"' % at))
    return got

# ---------- run ----------
def read_csv_set(path, n):
    if not path or not os.path.exists(path):
        return {}
    return {tuple(r[:n]) if n > 1 else r[0]: r for r in csv.reader(open(path, encoding='utf-8')) if r and not r[0].startswith('#') and r[0] != 'id'}

def held_rows(rid, move, claims):
    """[(id, at, reason, line)]: the held lines the owner decides. A row whose `at` is no page line (a question-bank
    row: identity compares the bank whole) is not listed."""
    P = page_lines(move)
    out = [(rid, str(r.get('at')), r.get('reason', ''), P[str(r.get('at'))][0]) for r in claims.get('rows', [])
           if r.get('status') == 'held' and str(r.get('at')) in P]
    return out + [(rid, 'added:' + norm(x.get('text', '')), x['held'], norm(x.get('text', ''))) for x in claims.get('added', []) if x.get('held')]

def check_dir(rdir, env, ids=None, move_dir=None, sources=None, waive=None, held_ok=None, held_out=None, claims_only=()):
    """{id: [(code, message)]} for every record of the folder"""
    recs = {}
    for f in sorted(os.listdir(rdir)):
        if f.endswith('.json') and f.count('.') == 1:
            recs[f[:-5]] = json.load(open(os.path.join(rdir, f), encoding='utf-8'))
    wv = read_csv_set(waive, 1)
    env.prose_base = {k: v[1] for k, v in read_csv_set(os.path.join(rdir, 'PROSE_BASELINE.csv'), 1).items()}
    ho = set(read_csv_set(held_ok, 2))
    res, held = {}, []
    for rid, rec in recs.items():
        if ids and rid not in ids:
            continue
        out = []
        if rec.get('id') != rid:
            out.append(('v2-record', 'file %s.json holds record id %r' % (rid, rec.get('id'))))
        out += check_record(rec, env)
        cp = os.path.join(rdir, rid + '.claims.json')
        if rid in wv:
            pass
        elif not os.path.exists(cp):
            out.append(('v2-claims', 'no claim map (%s.claims.json) and no waiver' % rid))
        elif not move_dir or not os.path.exists(os.path.join(move_dir, rid + '.json')):
            out.append(('v2-claims', 'no move record for %s: the page text cannot be compared' % rid))
        else:
            move = json.load(open(os.path.join(move_dir, rid + '.json'), encoding='utf-8'))
            claims = json.load(open(cp, encoding='utf-8'))
            if rid not in claims_only:
                out += [('v2-identity', m) for m in check_identity(rec, move)]
            c = check_claims(rec, move, claims, env, recs, sources, ho)
            out += c
            held += held_rows(rid, move, claims)
        res[rid] = out
    if held_out:
        w = csv.writer(open(held_out, 'w', encoding='utf-8', newline=''))
        w.writerow(['id', 'at', 'reason', 'line', 'decided'])
        for h in held:
            w.writerow(list(h) + ['yes' if (h[0], h[1]) in ho else ''])
    return res

def seed(move, assembled):
    """a claim map with one row per page line; lines whose words equal a record line are marked carried"""
    rt = {}
    for _, t, _ in rec_lines(assembled):
        rt.setdefault(json.dumps(sorted(words(t).items())), t)
    rows = []
    for at, (t, _, lab, fill) in page_lines(move).items():
        r = {'at': at, 'line': t, 'status': ''}
        k = json.dumps(sorted(words(t).items()))
        if fill == 'off-page':
            r.update(status='cut', reason='off-page')
        elif not re.search(r'[^\W_]', t) or t in RETIRED:
            r.update(status='cut', reason='chrome')
        elif k in rt:
            r.update(status='carried', new=[rt[k]])
        rows.append(r)
    return {'id': move.get('id'), 'rows': rows, 'added': []}

# ---------- selftest ----------
def fixture(rec):
    """a move record and a full claim map built from a pilot record: every record line is a page line, carried"""
    rec = copy.deepcopy(rec)
    rec['source'] = 'convert'
    lines = []
    for _, t, h in rec_lines(rec):
        if t not in [x[0] for x in lines]:
            lines.append((t, h))
    blocks = []
    for i in range(0, len(lines), 6):
        blocks.append({'block': str(len(blocks) + 1), 'section': 'Fixture', 'kind': 'div', 'slot': 'x', 'fill': 'edit', 'masks': '0',
                       'html': '<div>%s</div>' % ''.join('<p>%s</p>' % h for _, h in lines[i:i + 6])})
    blocks.append({'block': str(len(blocks) + 1), 'section': 'Practice', 'kind': 'ol.bank', 'slot': 'practice', 'fill': 'move', 'masks': '0',
                   'html': '<ol class="bank"><li>A 40-year-old woman has 3 weeks of cough.</li></ol>'})
    blocks.append({'block': str(len(blocks) + 1), 'section': 'Fixture', 'kind': 'div', 'slot': 'x', 'fill': 'edit', 'masks': '0',
                   'html': '<div><p>Chain</p><p>\u2192</p></div>'})
    blocks.append({'block': str(len(blocks) + 1), 'section': 'Fixture', 'kind': 'div.vignette', 'slot': '', 'fill': 'off-page', 'masks': '0',
                   'html': '<div class="vignette"><p>A 30-year-old man has 2 days of chest pain.</p></div>'})
    blocks.append({'block': str(len(blocks) + 1), 'section': 'Fixture', 'kind': 'div', 'slot': 'x', 'fill': 'edit', 'masks': '0',
                   'html': '<div><span class="lbl">Bottom line</span><p>Fever over 39 C for 5 days may suggest Kawasaki disease.</p></div>'})
    rec['kicker'] = 'one · two · three'
    move = {'id': rec['id'], 'attrs': copy.deepcopy(rec.get('attrs')), 'kicker': rec.get('kicker'), 'aka': copy.deepcopy(rec.get('aka')), 'practice': copy.deepcopy(rec['practice']), 'legacy': blocks}
    P = page_lines(move)
    rows = []
    for at, (t, _, lab, fill) in P.items():
        if fill == 'off-page':
            rows.append({'at': at, 'line': t, 'status': 'cut', 'reason': 'off-page'})
        elif t in ('Bottom line', 'Chain', '\u2192'):
            rows.append({'at': at, 'line': t, 'status': 'cut', 'reason': 'chrome'})
        elif t.startswith('Fever over 39'):
            rows.append({'at': at, 'line': t, 'status': 'held', 'reason': 'no slot'})
            held = (rec['id'], at)
        else:
            rows.append({'at': at, 'line': t, 'status': 'carried', 'new': [t]})
    return rec, move, {'id': rec['id'], 'rows': rows, 'added': []}, held

def first_line(rec, pred=lambda t: True):
    for p, t, _ in rec_lines(rec):
        if p.startswith('/slots') and pred(t):
            return p, t
    raise LookupError

def set_path(rec, path, fn):
    """apply fn to the string or run list at path"""
    keys = [k for k in path.split('/') if k != '']
    o = rec
    for k in keys[:-1]:
        o = o[int(k)] if isinstance(o, list) else o[k]
    k = keys[-1]
    k = int(k) if isinstance(o, list) else k
    v = o[k]
    if isinstance(v, str):
        o[k] = fn(v)
    else:
        runs = [v] if isinstance(v, dict) else v
        for r in reversed(runs):
            if 't' in r and fn(r['t']) != r['t']:
                r['t'] = fn(r['t'])
                break

def relink(rec, claims, path, old):
    """after an edit at path: point the claim row of the old line at the line that replaced it"""
    before = set(x.get('new', [None])[0] for x in claims['rows'])
    new = [t for p, t, _ in rec_lines(rec) if p == path and t not in before]
    if not new:
        raise LookupError
    row = next(x for x in claims['rows'] if x.get('new') == [old])
    row.update(status='edited', new=new[:1])

def selftest(pdir, env):
    pil = {f[:-5]: json.load(open(os.path.join(pdir, f), encoding='utf-8')) for f in sorted(os.listdir(pdir)) if f.endswith('.json') and f.count('.') == 1}
    bad = 0
    env.prose_base = {k: v[1] for k, v in read_csv_set(os.path.join(pdir, 'PROSE_BASELINE.csv'), 1).items()}
    print('pilot records, record checks:')
    for rid, rec in pil.items():
        f = check_record(rec, env)
        print('  %-18s %s' % (rid, 'PASS' if not f else 'FAIL ' + '; '.join('[%s] %s' % x for x in f[:3])))
        bad += bool(f)
    tmp = tempfile.mkdtemp()
    rows = []

    def run(rec, move, claims, held, src=None):
        out = check_record(rec, env)
        out += [('v2-identity', m) for m in check_identity(rec, move)]
        out += check_claims(rec, move, claims, env, {rec['id']: rec}, src, {held})
        return out

    for rid in [r for r in ('pe', 'limp', 'lithium-effects', 'aki') if r in pil]:
        rec, move, claims, held = fixture(pil[rid])
        env.prose_base[rid] = env.prose_base.get(rid, 0)
        clean = run(rec, move, claims, held)
        print('fixture %s (claim map of %d rows): %s' % (rid, len(claims['rows']), 'PASS' if not clean else 'FAIL ' + '; '.join('[%s] %s' % x for x in clean[:4])))
        bad += bool(clean)
        sd = os.path.join(tmp, 'sources')
        os.makedirs(os.path.join(sd, rid), exist_ok=True)
        open(os.path.join(sd, rid, 'source.md'), 'w').write('Heading\nTroponin over 14 ng/L suggests myocardial injury.\n')
        num = lambda t: bool(re.search(r'\d', t)) and len(t.split()) > 2
        plain = lambda t: len(t.split()) > 3

        def d_slot(r, m, c):
            r['slots'].pop(env.schema['$defs'][r['entry']]['required'][0])
        def d_sub(r, m, c):
            D = env.schema['$defs']
            for k in D[r['entry']]['required']:
                sub = D.get(D[r['entry']]['properties'][k].get('$ref', '').split('/')[-1], {})
                if sub.get('required') and isinstance(r['slots'][k], dict):
                    r['slots'][k][sub['required'][-1]] = []
                    return
            raise LookupError
        def d_legacy(r, m, c):
            r['legacy'] = [copy.deepcopy(m['legacy'][0])]
        def d_asm(r, m, c):
            r['assembled'] = [{'block': 1, 'slot': 'script.rows'}]
        def d_empty(r, m, c):
            p, t = first_line(r, plain)
            set_path(r, p, lambda s: '')
        def d_mark(r, m, c):
            p, t = first_line(r, plain)
            set_path(r, p, lambda s: s + ' (UWorld)')
        def d_draw(r, m, c):
            r['title'] = {'t': 'x'}
        def d_pid(r, m, c):
            r['practice']['items'][0]['id'] = 'q_00000000000000000000'
        def d_porder(r, m, c):
            r['practice']['items'].reverse()
        def d_pedit(r, m, c):
            it = r['practice']['items'][0]
            k = next(k for k, v in it.items() if isinstance(v, str) and k not in ('id',))
            it[k] = it[k] + ' '
        def d_attr(r, m, c):
            r['attrs'] = dict(r.get('attrs') or {}, **{'data-shelf': 'zz'})
        def d_norow(r, m, c):
            del c['rows'][3]
        def d_duprow(r, m, c):
            c['rows'].append(copy.deepcopy(c['rows'][3]))
        def d_echo(r, m, c):
            c['rows'][3]['line'] += ' x'
        def d_status(r, m, c):
            c['rows'][3]['status'] = 'done'
        def d_reword(r, m, c):
            p, t = first_line(r, plain)
            set_path(r, p, lambda s: s + ' today')
        def d_number(r, m, c):
            p, t = first_line(r, num)
            set_path(r, p, lambda s: re.sub(r'\d+(?:\.\d+)?', '', s, count=1))
            relink(r, c, p, t)
        def d_newnum(r, m, c):
            p, t = first_line(r, plain)
            set_path(r, p, lambda s: s + ' in 73%')
            relink(r, c, p, t)
        def d_cut(r, m, c):
            row = next(x for x in c['rows'] if x.get('new') and num(x['line']))
            row.pop('new'); row.update(status='cut', reason='low yield')
        def d_repeat(r, m, c):
            row = next(x for x in c['rows'] if x.get('new') and num(x['line']))
            oth = next(x for x in c['rows'] if x.get('new') and not re.search(r'\d', x['line']) and x is not row)
            row.pop('new'); row.update(status='cut', reason='repeat', carried_in=oth['new'])
        def d_chrome(r, m, c):
            row = next(x for x in c['rows'] if x.get('new') and num(x['line']))
            row.pop('new'); row.update(status='cut', reason='chrome')
        def d_offpage(r, m, c):
            row = next(x for x in c['rows'] if x.get('new') and plain(x['line']))
            row.pop('new'); row.update(status='cut', reason='off-page')
        def d_held(r, m, c):
            row = next(x for x in c['rows'] if x.get('new') and plain(x['line']))
            row.pop('new'); row.update(status='held', reason='length')
        def add_line(r, text):
            sl = r['slots']['differential']
            sl.setdefault('notes', [])
            sl['notes'].append(text)
        def d_added(r, m, c):
            add_line(r, 'Troponin over 14 ng/L suggests myocardial injury.')
        def d_nosrc(r, m, c):
            add_line(r, 'Troponin over 14 ng/L suggests myocardial injury.')
            c['added'].append({'text': 'Troponin over 14 ng/L suggests myocardial injury.', 'src': []})
        def d_srcat(r, m, c):
            add_line(r, 'Troponin over 14 ng/L suggests myocardial injury.')
            c['added'].append({'text': 'Troponin over 14 ng/L suggests myocardial injury.', 'src': [{'at': '99.1'}]})
        def d_srcfile(r, m, c):
            add_line(r, 'Troponin over 14 ng/L suggests myocardial injury.')
            c['added'].append({'text': 'Troponin over 14 ng/L suggests myocardial injury.', 'src': [{'file': 'missing.md', 'n': 2, 'text': 'Troponin over 14 ng/L suggests myocardial injury.'}]})
        def d_srcline(r, m, c):
            add_line(r, 'Troponin over 14 ng/L suggests myocardial injury.')
            c['added'].append({'text': 'Troponin over 14 ng/L suggests myocardial injury.', 'src': [{'file': 'source.md', 'n': 9, 'text': 'Troponin over 14 ng/L suggests myocardial injury.'}]})
        def d_srcecho(r, m, c):
            add_line(r, 'Troponin over 14 ng/L suggests myocardial injury.')
            c['added'].append({'text': 'Troponin over 14 ng/L suggests myocardial injury.', 'src': [{'file': 'source.md', 'n': 1, 'text': 'Troponin over 14 ng/L suggests myocardial injury.'}]})
        def d_srcout(r, m, c):
            add_line(r, 'Troponin over 14 ng/L suggests myocardial injury.')
            c['added'].append({'text': 'Troponin over 14 ng/L suggests myocardial injury.', 'src': [{'file': '../../gate_v2.py', 'n': 1, 'text': '#!/usr/bin/env python3'}]})
        def d_srcnum(r, m, c):
            add_line(r, 'Troponin over 52 ng/L suggests myocardial injury.')
            c['added'].append({'text': 'Troponin over 52 ng/L suggests myocardial injury.', 'src': [{'file': 'source.md', 'n': 2, 'text': 'Troponin over 14 ng/L suggests myocardial injury.'}]})
        def d_srcneg(r, m, c):
            add_line(r, 'Troponin over 14 ng/L does not suggest myocardial injury.')
            c['added'].append({'text': 'Troponin over 14 ng/L does not suggest myocardial injury.', 'src': [{'file': 'source.md', 'n': 2, 'text': 'Troponin over 14 ng/L suggests myocardial injury.'}]})
        def d_heldadd(r, m, c):
            add_line(r, 'Troponin over 14 ng/L suggests myocardial injury.')
            c['added'].append({'text': 'Troponin over 14 ng/L suggests myocardial injury.', 'held': 'no source found'})
        def d_ghost(r, m, c):
            c['added'].append({'text': 'A line that the record does not hold.', 'src': [{'at': '1.1'}]})
        def d_tobrief(r, m, c):
            row = next(x for x in c['rows'] if x.get('new') and plain(x['line']))
            row.update(status='moved', to_brief='nowhere')
        def d_instr(r, m, c):
            p = next(p for p, t, _ in rec_lines(r) if p.startswith('/slots') and not p.startswith('/slots/differential') and plain(t))
            set_path(r, p, lambda s: s + ' CURB-65 of 2 or more points: admit.')
        def d_prose(r, m, c):
            hit = lambda t: plain(t) and any(x[0] not in env.P.REPORT_ONLY for x in env.P.text_checks(t + ', not the other drug', 'cell'))
            p, t = first_line(r, hit)
            set_path(r, p, lambda s: s + ', not the other drug')
            relink(r, c, p, t)
        def d_nbme(r, m, c):
            m['legacy'][-2]['html'] = m['legacy'][-2]['html'].replace('<p>', '<p data-nbme="psych-form-000000">', 1)
        def d_kicker(r, m, c):
            r['kicker'] = 'changed'
        tests = [('kicker changed', 'v2-identity', d_kicker), ('NBME coverage link dropped', 'v2-identity', d_nbme), ('contrast form added to a line', 'v2-prose', d_prose), ('required slot removed', 'v2-slots', d_slot), ('required inner slot emptied', 'v2-slots', d_sub),
                 ('legacy block left', 'v2-legacy', d_legacy), ('assembler notes left', 'v2-legacy', d_asm),
                 ('empty line', 'v2-empty', d_empty), ('source named in a line', 'v2-rules', d_mark),
                 ('record the schema refuses', 'v2-record', d_draw),
                 ('practice id changed', 'v2-identity', d_pid), ('practice order changed', 'v2-identity', d_porder),
                 ('practice item edited', 'v2-identity', d_pedit), ('brief attribute changed', 'v2-identity', d_attr),
                 ('claim row deleted', 'v2-claims', d_norow), ('claim row doubled', 'v2-claims', d_duprow),
                 ('claim row line altered', 'v2-claims', d_echo), ('unknown status', 'v2-claims', d_status),
                 ('record line reworded under a carried row', 'v2-lock', d_reword),
                 ('edit drops a number', 'v2-lock', d_number), ('edit adds a number', 'v2-source', d_newnum),
                 ('cut for a reason outside the list', 'v2-cut', d_cut), ('repeat cut whose carrier lacks the number', 'v2-lock', d_repeat),
                 ('a fact cut as chrome', 'v2-cut', d_chrome), ('a page block cut as off-page', 'v2-cut', d_offpage),
                 ('held line with no decision', 'v2-held', d_held), ('record line held with no decision', 'v2-held', d_heldadd),
                 ('added line with no entry', 'v2-source', d_added), ('added line with no source', 'v2-source', d_nosrc),
                 ('source page line that does not exist', 'v2-source', d_srcat), ('source file that does not exist', 'v2-source', d_srcfile),
                 ('source line number past the file', 'v2-source', d_srcline), ('source text not on that line', 'v2-source', d_srcecho),
                 ('source file outside the brief folder', 'v2-source', d_srcout), ('added number its source lacks', 'v2-source', d_srcnum),
                 ('added negation its source lacks', 'v2-source', d_srcneg), ('added entry for a line not in the record', 'v2-source', d_ghost),
                 ('moved to a brief with no record', 'v2-lock', d_tobrief), ('instrument cutoff with no items', 'v2-score', d_instr)]
        if any(True for _ in _scores(rec)):
            def d_items(r, m, c):
                next(_scores(r))['items'] = []
            def d_cutoffs(r, m, c):
                next(_scores(r))['cutoffs'] = []
            tests += [('score items removed', 'v2-score', d_items), ('score cutoffs removed', 'v2-score', d_cutoffs)]
        for name, code, fn in tests:
            r, m, c = copy.deepcopy(rec), copy.deepcopy(move), copy.deepcopy(claims)
            try:
                fn(r, m, c)
            except (StopIteration, LookupError, KeyError, IndexError) as e:
                rows.append((rid, name, code, 'NOT PLANTED (%s)' % type(e).__name__)); bad += 1
                continue
            got = set(x[0] for x in run(r, m, c, held, sd))
            ok = code in got
            rows.append((rid, name, code, 'caught' if ok else 'MISSED (got %s)' % (', '.join(sorted(got)) or 'nothing')))
            bad += not ok
        if env.R:
            real = env.R.render
            p0, t0 = first_line(rec, plain)

            def broken(r_, bank=''):
                inner, a_, b_ = real(r_, bank)
                w = t0.split()[0]
                return inner.replace(w, '', 1) if w in inner else inner[:len(inner) // 2], a_, b_
            env.R.render = broken
            got = set(x[0] for x in run(copy.deepcopy(rec), move, claims, held, sd))
            env.R.render = real
            rows.append((rid, 'renderer that drops a word of the record', 'v2-draw', 'caught' if 'v2-draw' in got else 'MISSED (got %s)' % ', '.join(sorted(got))))
            bad += 'v2-draw' not in got
        ok_added = copy.deepcopy((rec, move, claims))
        add_line(ok_added[0], 'Troponin over 14 ng/L suggests myocardial injury.')
        ok_added[2]['added'].append({'text': 'Troponin over 14 ng/L suggests myocardial injury.', 'src': [{'file': 'source.md', 'n': 2, 'text': 'Troponin over 14 ng/L suggests myocardial injury.'}]})
        f = run(ok_added[0], ok_added[1], ok_added[2], held, sd)
        rows.append((rid, 'added line with a true source line', 'none', 'passes' if not f else 'FAILS ' + str(f[:2])))
        bad += bool(f)
    for r in rows:
        if r[3] not in ('caught', 'passes'):
            print('  %-16s %-48s %-12s %s' % r)
    n = sum(r[3] == 'caught' for r in rows)
    print('planted defects: %d of %d caught, on %d fixtures; codes covered: %s' % (n, sum(r[2] != 'none' for r in rows), len(set(r[0] for r in rows)), ', '.join(sorted(set(r[2] for r in rows if r[3] == 'caught')))))
    miss = sorted(set(CATALOG) - set(r[2] for r in rows if r[3] == 'caught'))
    if miss:
        print('codes with no caught defect:', ', '.join(miss)); bad += 1
    print('selftest %s' % ('PASS' if not bad else 'FAIL'))
    return 1 if bad else 0

def _scores(o):
    if isinstance(o, dict):
        if isinstance(o.get('score'), dict):
            yield o['score']
        for v in o.values():
            yield from _scores(v)
    elif isinstance(o, list):
        for x in o:
            yield from _scores(x)

def main(a):
    if '--list' in a:
        for k, (d, fx) in CATALOG.items():
            print('%-12s %s\n%-12s fix: %s' % (k, d, '', fx))
        return 0
    opt = lambda k: a[a.index(k) + 1] if k in a else None
    flags = ('--ids', '--move', '--sources', '--waive', '--held-ok', '--schema', '--lint', '--held-out')
    pos = [x for i, x in enumerate(a) if not x.startswith('--') and (i == 0 or a[i - 1] not in flags)]
    cmd = pos[0] if pos else ''
    if cmd == 'lines':
        o = json.load(open(pos[1], encoding='utf-8'))
        if '--move' in a:
            for at, (t, _, lab, fill) in page_lines(o).items():
                print('%s\t%s%s\t%s' % (at, fill, ' label' if lab else '', t))
        else:
            for p, t, _ in rec_lines(o):
                print('%s\t%s' % (p, t))
        return 0
    if cmd == 'seed':
        c = seed(json.load(open(pos[1], encoding='utf-8')), json.load(open(pos[2], encoding='utf-8')))
        json.dump(c, open(pos[3], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        n = Counter(r['status'] or 'open' for r in c['rows'])
        print('%s: %d page lines; %s' % (c['id'], len(c['rows']), ', '.join('%s %d' % x for x in sorted(n.items()))))
        return 0
    env = Env(opt('--schema'), opt('--lint'), draw='--no-draw' not in a)
    if cmd == 'selftest':
        return selftest(pos[1], env)
    if cmd == 'check':
        res = check_dir(pos[1], env, set(opt('--ids').split(',')) if opt('--ids') else None, opt('--move'), opt('--sources'),
                        opt('--waive'), opt('--held-ok'), opt('--held-out'))
        bad = 0
        for rid, f in res.items():
            print('%-20s %s' % (rid, 'PASS' if not f else 'FAIL %d' % len(f)))
            for code, m in f[:30]:
                print('  [%s] %s\n      fix: %s' % (code, m, CATALOG[code][1]))
            if len(f) > 30:
                print('  ... %d more' % (len(f) - 30))
            bad += bool(f)
        print('gate_v2: %s, %d record(s), %d failing, %d checks' % ('FAIL' if bad else 'PASS', len(res), bad, len(CATALOG)))
        return 1 if bad else 0
    print(__doc__)
    return 2

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
