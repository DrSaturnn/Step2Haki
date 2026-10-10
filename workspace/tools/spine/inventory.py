"""inventory: one record per brief for planning spine batches (plan 0.3).

  python3 tools/spine/inventory.py [page.html] [--out repair/migration/spine/inventory.json] [--brief <id>]

Per brief: kind, title, shelf, bp, format (spine, typeC, legacy), words above the Practice header, item ids and
count, NBME item count, nids (resolved to AnKing cards, unresolved, and malformed tokens such as a UWorld QID;
NBME form refs such as psych-form-085f91 are listed apart),
claim maps (by primary_id) with their dropped-claim counts, the proposed entry type with the reason (a heuristic
the Lead confirms), owner candidates for each differential diagnosis (another brief whose title names it), and
a cluster key (first shelf + first body part). The output lives under repair/migration (local-only) because claim
map paths and card counts come from local-only files; the script itself holds no source text.
"""
import collections
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.dirname(HERE))
import pagelib as P  # noqa: E402

BANK = re.compile(r'<h5\b[^>]*class="[^"]*authored-hdr|<(?:div|ol)\b[^>]*\bclass="bank', re.I)
DRUG = re.compile(r'\b(effects?|therapy|drugs?|medications?|pharm\w*|toxicity|antibiotic|antipsychotic|lithium|ssri|anticoag\w*|insulin|vaccines?)\b', re.I)
SCREEN = re.compile(r'\b(screen\w*|prevention|preventive|surveillance|well[- ]child|immunization schedule)\b', re.I)
LOOKUP = re.compile(r'\b(milestones?|growth charts?|normal values|lab values|reference)\b', re.I)
PRESENT = re.compile(r'\b(pain|cough|fever|murmur|cyanosis|vomiting|diarrhea|stool|bleeding|mass|jaundice|rash|limp|'
                     r'headache|syncope|dyspnea|hypoxemia|polyuria|edema|bruising|hypotonia|weakness|seizure|'
                     r'constipation|dizziness|fatigue|voices|difficulty|delay|failure to thrive|lump|swelling)\b', re.I)


def words_above(inner):
    m = BANK.search(inner)
    return len(P.text(inner[:m.start()] if m else inner).split())


def fmt(b):
    if 'class="sp-step"' in b.inner:
        return 'spine'
    if 'class="scriptcard' in b.inner or 'authored-hdr' in b.inner:
        return 'typeC'
    return 'legacy'


def entry(b):
    t = b.title
    if fmt(b) == 'spine':
        m = re.search(r'data-entry="([a-z]+)"', b.inner[:600]) or re.search(r'data-entry="([a-z]+)"', ' '.join('%s="%s"' % kv for kv in b.attrs.items()))
        return (m.group(1) if m else 'spine'), 'already on the spine'
    if b.kind == 'aq':
        return 'presentation', 'Aquifer case workup (starts from a complaint)'
    if LOOKUP.search(t):
        return 'lookup', 'title names a reference table: %s' % LOOKUP.search(t).group(0)
    if SCREEN.search(t):
        return 'screen', 'title names screening or prevention: %s' % SCREEN.search(t).group(0)
    if DRUG.search(t):
        return 'drug', 'title names a drug or therapy: %s' % DRUG.search(t).group(0)
    if PRESENT.search(t):
        return 'presentation?', 'title names a complaint (%s); a hub only if it fans out to 3 or more owning briefs' % PRESENT.search(t).group(0)
    return 'disease', 'default'


def nid_tokens(b):
    toks = set(b.attrs.get('data-nid', '').split())
    for g in re.findall(r'data-nid="([^"]*)"', b.inner):
        toks |= set(g.split())
    return toks


def load_cards():
    p = os.path.join(WS, 'repair', 'sources', 'anki', 'anki_index.jsonl')
    have = {}
    if os.path.exists(p):
        for line in open(p, encoding='utf-8'):
            r = json.loads(line)
            if r.get('nid'):
                have[r['nid']] = len(r.get('hy', []))
    return have


def load_maps():
    maps = collections.defaultdict(list)
    for f in glob.glob(os.path.join(WS, 'repair', 'migration', '**', 'claim_map*.json'), recursive=True):
        try:
            d = json.load(open(f, encoding='utf-8'))
        except (ValueError, OSError):
            continue
        if not isinstance(d, dict) or not d.get('primary_id'):
            continue
        dropped = sum(1 for c in d.get('claims', []) if c.get('disposition') == 'dropped')
        maps[d['primary_id']].append({'path': os.path.relpath(f, WS), 'claims': len(d.get('claims', [])), 'dropped': dropped})
    return maps


def differential_rows(inner):
    m = BANK.search(inner)
    body = inner[:m.start()] if m else inner
    rows = []
    for t in re.finditer(r'<table\b.*?</table>', body, re.S):
        tbl = t.group(0)
        head = P.text(re.search(r'<tr>(.*?)</tr>', tbl, re.S).group(1)) if re.search(r'<tr>(.*?)</tr>', tbl, re.S) else ''
        cap = P.text((re.search(r'<caption>(.*?)</caption>', tbl, re.S) or [None, ''])[1])
        if re.search(r'look-alike|differential|which effect|mimic', cap + ' ' + head, re.I):
            rows += [P.text(c) for c in re.findall(r'<tr>\s*<td\b[^>]*>(.*?)</td>', tbl, re.S)]
    for btn in re.findall(r'<button\b[^>]*class="sp-drw"[^>]*>(.*?)</button>', body, re.S):
        rows.append(P.text(btn))
    return [r for r in dict.fromkeys(rows) if 2 < len(r) <= 80]


def main(argv):
    page = argv[0] if argv and not argv[0].startswith('--') else os.path.join(WS, 'index.html')
    out = argv[argv.index('--out') + 1] if '--out' in argv else os.path.join(WS, 'repair', 'migration', 'spine', 'inventory.json')
    only = argv[argv.index('--brief') + 1] if '--brief' in argv else None
    html = P.read_page(page)
    bl = P.briefs(html)
    items = collections.defaultdict(list)
    for it in P.items(html):
        items[it.brief_id].append(it)
    cards, maps = load_cards(), load_maps()
    titles = {b.id: b.title.lower() for b in bl}
    recs = []
    for b in bl:
        if only and b.id != only:
            continue
        toks = nid_tokens(b)
        nids = sorted(t for t in toks if re.fullmatch(r'1\d{12}', t))
        forms = sorted(t for t in toks if re.fullmatch(r'[a-z]+-form-[0-9a-f]+', t))   # NBME form item refs, not card ids
        bad = sorted(t for t in toks if t not in nids and t not in forms)
        resolved = [n for n in nids if int(n) in cards]
        et, why = entry(b)
        owners = []
        for dx in differential_rows(b.inner):
            low = dx.lower()
            hit = [bid for bid, t in titles.items() if bid != b.id and t and (t in low or (len(low) > 5 and low in t))]
            if hit:
                owners.append({'dx': dx, 'owners': hit[:3]})
        its = items.get(b.id, [])
        recs.append({
            'id': b.id, 'kind': b.kind, 'title': b.title,
            'shelf': b.attrs.get('data-shelf', '').split(), 'bp': b.attrs.get('data-bp', '').split(),
            'format': fmt(b), 'words': words_above(b.inner),
            'items': len(its), 'item_ids': [i.id for i in its],
            'nbme_items': sum(1 for i in its if i.attrs.get('data-src') == 'nbme'),
            'nids': nids, 'nids_resolved': resolved, 'card_statements': sum(cards[int(n)] for n in resolved),
            'nbme_form_refs': forms,
            'nid_problems': bad + [n for n in nids if int(n) not in cards],
            'claim_maps': maps.get(b.id, []),
            'entry': et, 'entry_reason': why,
            'owner_candidates': owners,
            'cluster': '%s/%s' % ((b.attrs.get('data-shelf', '').split() or ['-'])[0], (b.attrs.get('data-bp', '').split() or ['-'])[0]),
        })
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out + '.tmp', 'w', encoding='utf-8') as f:
        json.dump({'page': os.path.relpath(page, WS), 'count': len(recs), 'briefs': recs}, f, ensure_ascii=False, indent=1)
    os.replace(out + '.tmp', out)
    fm = collections.Counter(r['format'] for r in recs)
    en = collections.Counter(r['entry'] for r in recs if r['format'] != 'spine')
    print('inventory: %d briefs -> %s' % (len(recs), os.path.relpath(out, WS)))
    print('  format: %s' % dict(fm))
    print('  proposed entry (not yet on the spine): %s' % dict(en))
    print('  with a claim map: %d; with resolved cards: %d; with nid problems: %d' % (
        sum(1 for r in recs if r['claim_maps']), sum(1 for r in recs if r['nids_resolved']), sum(1 for r in recs if r['nid_problems'])))
    print('  words above the bank (not on the spine): median %d, over 1,300: %d' % (
        sorted(r['words'] for r in recs if r['format'] != 'spine')[len([r for r in recs if r['format'] != 'spine']) // 2],
        sum(1 for r in recs if r['format'] != 'spine' and r['words'] > 1300)))
    clusters = collections.Counter(r['cluster'] for r in recs if r['format'] != 'spine')
    print('  clusters (not on the spine): %s' % ', '.join('%s %d' % kv for kv in clusters.most_common(12)))


if __name__ == '__main__':
    main(sys.argv[1:])
