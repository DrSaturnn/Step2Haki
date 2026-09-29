#!/usr/bin/env python3
"""migrate_check.py: mechanical checks for one brief-migration cluster.

  python3 tools/migrate_check.py <old_briefs.html> <new_brief.html> <claim_map.json> [--json]
  python3 tools/migrate_check.py - <new_brief.html> - --topic="septic arthritis,transient synovitis"   (new brief, no migration)

Self-test first: python3 tools/test_migrate_check.py (golden brief passes, every known defect fails).
Rules and codes: tools/MIGRATION_CONTRACT.md.

old_briefs.html  the old brief blocks of the cluster, concatenated (as extracted from the page)
new_brief.html   the new Type C brief block
claim_map.json   {"cluster", "primary_id", "claims":[...], "items":[...]}

claims[]: {id, kind: claim|number|clue, source, text, role (clues: decides|localizes|supports|excludes|decoy),
           disposition: carried|moved|merged|dropped|corrected, new_text (carried/corrected: exact phrase
           that appears in the new brief), to (moved), merged_into (merged), reason (dropped/corrected)}
items[]:  {id, disposition: carried|moved|merged|archived|retired, to, merged_into, reason}

Exit 1 on any FAIL. WARN lines do not fail.
"""
import html as H
import json
import re
import sys

CLAIM_DISP = {'carried', 'moved', 'merged', 'dropped', 'corrected'}
ITEM_DISP = {'carried', 'moved', 'merged', 'archived', 'retired'}
ROLES = {'decides', 'localizes', 'supports', 'excludes', 'decoy'}


def norm(s):
    s = re.sub(r'</?(b|i|em|strong|sup|sub)\b[^>]*>', '', s or '')
    s = H.unescape(re.sub(r'<[^>]+>', ' ', s))
    s = s.replace('\u2013', '-').replace('\u2265', '>=')
    s = s.replace('→', '->').replace('’', "'")
    return re.sub(r'\s+', ' ', s).strip().lower()


def items_of(block):
    out = {}
    for m in re.finditer(r'<li ([^>]*data-item-id="(q_[0-9a-f]{20})"[^>]*)>(.*?)</li>', block, re.S):
        attrs = dict(re.findall(r'(data-[\w-]+)="([^"]*)"', m.group(1)))
        out[m.group(2)] = (attrs, m.group(3))
    return out



AGE_OPEN = re.compile(r'^(an? )?(\d+(\.\d+)?-(year|month|week|day|hour)-old|newborn|term newborn|preterm newborn)\b[^;,]{0,12}?\b(boy|girl|man|woman|infant|neonate|newborn|child|adolescent)', re.I)
SHORTHAND = re.compile(r'\b\d+\s*(yo|y/o|mo|wk|d/o)\b|\b\d+\s*(yo|mo)\s*[MF]\b|\byo [MF]\b', re.I)
PRIOR_DX = re.compile(r'\b(treated|drained|given|received|after (ivig|surgery|antibiotics|treatment)|diagnosed \w+ \w+ ago|was diagnosed|follow-up|well visit)\b', re.I)


QWORDS = {'always', 'never', 'only', 'especially', 'usually', 'rarely', 'most', 'least', 'all', 'none', 'not', 'must',
          'highest', 'lowest', 'wrong', 'excluded', 'required', 'contraindicated', 'unless', 'except'}


OBJ = re.compile(r'\bt \d|\bhr \d|\brr \d|\bbp \d|\d[\d,.]*\s*(mm|mg|g/dl|/mm|u/l|%|cm|/min|meq|mmol)|\bafebrile\b|well[ -]appearing|ultrasound shows|radiograph|echocardiogram shows|x-ray shows')
STOP = {'now', 'then', 'a', 'an', 'the', 'on', 'of', 'in', 'is', 'has', 'had', 'was', 'at', 'to', 'for', 'his', 'her', 'who', 'yo', 'm', 'f'}
NEG = {'not', 'never', 'none', 'no', 'without', 'absent', 'negative'}


def QUANT(s):
    w = set(re.findall(r"[a-z]+(?:-[a-z]+)*", norm(s)))
    out = {q for q in QWORDS if q in w}
    if out & NEG or w & NEG:
        out = (out - NEG) | {'(negation)'}
    return out


def item_contract(new, new_items, old_items, cmap, F, W):
    """Item style contract. Golden reference: the approved septic hip brief (local/pilot/hip3.html)."""
    topic = [t.lower() for t in cmap.get('topic_terms', [])]
    if not topic:
        F('I0 claim map has no topic_terms (the diagnosis names the stems must not give away)')
    bank = new[new.find('authored-hdr'):] if 'authored-hdr' in new else new
    order = [m for m in re.findall(r'data-src="(\w+)"', bank)]
    if 'nbme' in order and 'authored' in order and order.index('authored') < max(i for i, x in enumerate(order) if x == 'nbme'):
        F('I9 NBME items must come first in the bank')
    if 'nbme' in order and 'How NBME framed it' not in new:
        F('I9 NBME item without a "How NBME framed it" note')
    for iid, (a, body) in new_items.items():
        t = norm(body)
        parts = [x.strip() for x in t.split('->')]
        stem = parts[0]
        if a.get('data-src') not in ('nbme', 'authored'):
            F(f'I1 {iid}: data-src must be nbme or authored (got {a.get("data-src")!r})')
        li = a.get('data-lead-in', '')
        if not li:
            F(f'I1 {iid}: no explicit data-lead-in')
        elif not li.strip().endswith('?'):
            F(f'I1 {iid}: lead-in is not a question')
        if SHORTHAND.search(stem):
            F(f'I2 {iid}: shorthand in stem ("{SHORTHAND.search(stem).group(0)}"); write age and sex in full, e.g. "4-year-old boy"')
        if not AGE_OPEN.match(stem):
            F(f'I2 {iid}: stem does not open with age and sex ("{stem[:40]}")')
        if a.get('data-type') in ('dx', 'next', 'test', 'avoid', 'screen', 'stage') and not OBJ.search(stem):
            F(f'I8 {iid}: stem gives no objective data (a vital sign, a lab or imaging value with units, "afebrile" or "well appearing")')
        if len(parts) < 3 or not parts[2]:
            F(f'I3 {iid}: no companion after the key')
        key = norm(parts[1]) if len(parts) > 1 else ''
        opts = [key, norm(a.get('data-d1', '')), norm(a.get('data-d2', ''))]
        if len(set(opts)) < 3:
            F(f'I5 {iid}: options not distinct')
        typ = a.get('data-type')
        if key and len(key) > 3 and key in stem and typ in ('dx', 'mech', 'test', 'stage'):
            F(f'I4 {iid}: stem contains the keyed answer "{key}"')
        for term in topic:
            if term in stem:
                if typ in ('dx', 'test', 'stage') or not PRIOR_DX.search(stem):
                    F(f'I4 {iid}: stem names the topic diagnosis "{term}"; describe the findings instead')
        if iid in old_items:
            ostem = norm(old_items[iid][1]).split('->')[0].strip()
            ov = int(old_items[iid][0].get('data-item-version', '1'))
            nv = int(a.get('data-item-version', '1'))
            if ostem != stem and nv <= ov:
                F(f'I6 {iid}: stem changed but version not bumped ({ov} -> {nv})')
            ack = {r.get('id'): r.get('changed_options', []) for r in cmap.get('items', [])}.get(iid, [])
            for k in ('data-key-id', 'data-d1-id', 'data-d2-id'):
                if old_items[iid][0].get(k) != a.get(k) and k != 'data-key-id' and k not in ack:
                    W(f'I6 {iid}: {k} changed; allowed only when that option label changed meaning')
        if re.search(r'\bt\s*\d+(\.\d+)?\s*(°|deg)?\s*c\b', stem) is None and re.search(r'\bt\s*\d', stem):
            W(f'I7 {iid}: temperature without units')


def main():
    a = [x for x in sys.argv[1:] if not x.startswith('--')]
    as_json = '--json' in sys.argv
    old = '' if a[0] == '-' else open(a[0], encoding='utf-8').read()
    new = open(a[1], encoding='utf-8').read()
    cmap = {'claims': [], 'items': []} if a[2] == '-' else json.load(open(a[2], encoding='utf-8'))
    for x in sys.argv[1:]:
        if x.startswith('--topic='):
            cmap['topic_terms'] = [t.strip() for t in x[8:].split(',') if t.strip()]
    fails, warns = [], []
    F = fails.append
    W = warns.append
    newn = norm(new)

    # ---- claims
    claims = cmap.get('claims', [])
    ids = [c.get('id') for c in claims]
    if len(ids) != len(set(ids)):
        F('claim ids are not unique')
    byid = {c.get('id'): c for c in claims}
    nclue = 0
    for c in claims:
        cid, disp, kind = c.get('id'), c.get('disposition'), c.get('kind')
        if disp not in CLAIM_DISP:
            F(f'{cid}: bad disposition {disp!r}')
            continue
        if kind == 'clue':
            nclue += 1
            if c.get('role') not in ROLES:
                F(f'{cid}: clue without a valid role ({c.get("role")!r})')
            if disp == 'dropped':
                F(f'{cid}: clue dropped: {c.get("text", "")[:70]}')
        if disp in ('carried', 'corrected'):
            nt = norm(c.get('new_text', ''))
            if not nt:
                F(f'{cid}: {disp} without new_text')
            elif nt not in newn:
                F(f'{cid}: new_text not found in new brief: {c.get("new_text")[:70]!r}')
        if disp == 'moved' and not c.get('to'):
            F(f'{cid}: moved without a destination')
        if disp == 'merged':
            tgt = byid.get(c.get('merged_into'))
            if not tgt or tgt.get('disposition') not in ('carried', 'corrected'):
                F(f'{cid}: merged into {c.get("merged_into")!r}, which is not a carried claim')
            elif kind == 'clue' and tgt.get('role') != c.get('role'):
                F(f'{cid}: clue merged into a claim with a different role')
        if disp == 'carried' and c.get('text') and c.get('new_text') and not c.get('qualifier_ok'):
            lost = QUANT(c['text']) - QUANT(c['new_text'])
            if lost:
                F(f'Q1 {cid}: qualifier(s) {sorted(lost)} dropped from a carried claim ({c["text"][:50]!r}); keep them, use a sourced corrected row, or give qualifier_ok with the reason the meaning is unchanged')
        if disp == 'carried' and c.get('text') and c.get('new_text') and not c.get('qualifier_ok'):
            ot, nt2 = set(re.findall(r'[a-z]+', norm(c['text']))), set(re.findall(r'[a-z]+', norm(c['new_text'])))
            if 'and' in ot and 'or' not in ot and 'or' in nt2:
                F(f'Q1 {cid}: "and" became "or" in a carried claim ({c["text"][:50]!r}); conditions that were all required now read as alternatives')
        if kind == 'clue' and re.search(r'nbme|uworld|source', (c.get('source') or '').lower()):
            rb = c.get('role_basis')
            if rb not in ('source', 'inferred'):
                F(f'R1 {cid}: source clue needs role_basis source|inferred (is the role stated by the source explanation?)')
            elif rb == 'inferred' and disp == 'carried':
                row = next((r for r in re.findall(r'<tr>.*?</tr>|<li[^>]*>.*?</li>', new, re.S) if norm(c.get('new_text', '')) in norm(r)), '')
                if row and not re.search(r'\u26a0|&#x26A0;|&#9888;', row, re.I):
                    F(f'R1 {cid}: inferred role not marked with the warning flag where it appears')
        if disp == 'corrected' and kind == 'number':
            if not c.get('stale_patterns'):
                F(f'S1 {cid}: corrected number without stale_patterns (old wordings that must not remain anywhere)')
            for pat in c.get('stale_patterns', []):
                if norm(pat) in newn:
                    F(f'S1 {cid}: the corrected old value "{pat}" still appears in the new brief')
        if kind == 'number' and disp in ('carried', 'corrected'):
            cur = c.get('currency')
            if cur not in ('verified', 'flagged', 'stable'):
                F(f'N1 {cid}: number row needs currency verified|flagged|stable (checked against current guidance?)')
            elif cur == 'verified' and not (c.get('source') or c.get('reason')):
                F(f'N1 {cid}: verified number without a source')
        if disp in ('dropped', 'corrected') and not c.get('reason'):
            F(f'{cid}: {disp} without a reason')

    # ---- C1 clue census: every fragment of every old bank stem is covered by a clue row
    old_items = items_of(old)
    def cn(x):
        return norm(x).replace('\u00b0', ' ').replace('  ', ' ')
    clue_texts = [cn(c.get('text', '')) for c in claims if c.get('kind') == 'clue']
    for iid, (_, body) in old_items.items():
        stem = cn(body).split('->')[0]
        for frag in re.split(r'[,;]| and | with ', stem):
            frag = frag.strip(' .')
            toks = set(re.findall(r'[a-z0-9./]+', frag)) - STOP
            if len(frag) > 3 and toks and not any(toks <= set(re.findall(r'[a-z0-9./]+', t)) or (len(t) > 3 and t in frag) for t in clue_texts):
                F(f'C1 {iid}: stem clue "{frag}" has no clue row in the claim map')

    # ---- items
    new_items = items_of(new)
    inv = {i.get('id'): i for i in cmap.get('items', [])}
    for iid, (attrs, _) in old_items.items():
        r = inv.get(iid)
        if not r:
            F(f'old item {iid} not accounted for')
            continue
        d = r.get('disposition')
        if d not in ITEM_DISP:
            F(f'{iid}: bad item disposition {d!r}')
        if d == 'carried':
            if iid not in new_items:
                F(f'{iid}: carried but not in the new brief')
            else:
                ov = int(attrs.get('data-item-version', '1'))
                nv = int(new_items[iid][0].get('data-item-version', '1'))
                if nv < ov:
                    F(f'{iid}: version went down ({ov} -> {nv})')
                if new_items[iid][0].get('data-key-id') != attrs.get('data-key-id'):
                    F(f'{iid}: key id changed; a new key needs a new item')
        if d in ('moved',) and not r.get('to'):
            F(f'{iid}: moved without a destination')
        if d in ('retired', 'archived') and not r.get('reason'):
            F(f'{iid}: {d} without a reason')
        if attrs.get('data-src') == 'uworld' and d == 'carried':
            F(f'{iid}: UWorld item carried onto the page; archive it and write a new item')

    # ---- new brief structure
    if 'data-src="uworld"' in new:
        F('new brief contains a data-src="uworld" item')
    if 'class="vignette"' in new:
        F('new brief contains a .vignette block')
    if re.search(r'class="brief bs"', new):
        F('new brief uses the board-style class')
    for iid, (attrs, body) in new_items.items():
        for k in ('data-type', 'data-d1', 'data-d2', 'data-key-id', 'data-d1-id', 'data-d2-id', 'data-item-version'):
            if not attrs.get(k):
                F(f'{iid}: missing {k}')
        stem = norm(body)
        if re.match(r'(same|the same) (patient|child|boy|girl|infant)', stem):
            F(f'{iid}: stem depends on another item ("{stem[:30]}")')
        if stem.count('->') < 1:
            F(f'{iid}: no arrow chain')
    for tgt in re.findall(r'<nav class="jump">(.*?)</nav>', new, re.S):
        for h in re.findall(r'href="#([^"]+)"', tgt):
            if f'id="{h}"' not in new:
                F(f'jump link #{h} has no target')
    rep = re.search(r'data-replaces="([^"]*)"', new)
    if rep:
        for rid in rep.group(1).split():
            if f'<span class="alias" id="{rid}"' not in new:
                F(f'replaced id {rid} has no alias span')
    for t in re.findall(r'<table[^>]*>', new):
        pass
    # M1 table masks (study-page-builder "Wrappers and captions")
    for tm in re.finditer(r'<table([^>]*)>(.*?)</table>', new, re.S):
        mask = re.search(r'data-mask="([^"]*)"', tm.group(1))
        heads = [norm(h) for h in re.findall(r'<th[^>]*>(.*?)</th>', tm.group(2))]
        first = heads[0] if heads else ''
        want = None
        if first == 'tier':
            if mask:
                F(f'M1 Tier table carries data-mask="{mask.group(1)}"; Tier tables carry no data-mask (the transform masks the intervention column)')
            continue
        if heads[:2] == ['diagnosis', 'the stem shows']:
            want = '3'
        elif heads[:2] == ['test', 'order']:
            want = '4'
        elif first in ('clue', 'finding'):
            want = 'none'
        if want and (not mask or mask.group(1) != want):
            F(f'M1 table "{" | ".join(heads[:3])}" needs data-mask="{want}"')
    tables = len(re.findall(r'<table', new))
    wrapped = len(re.findall(r'<div class="tw">\s*<table', new))
    caps = len(re.findall(r'<table[^>]*>\s*<caption>', new))
    if wrapped < tables:
        F(f'{tables - wrapped} table(s) not in a .tw wrapper')
    if caps < tables:
        W(f'{tables - caps} table(s) without a caption as first child')
    text = H.unescape(re.sub(r'<[^>]+>', ' ', new))
    if '—' in text:
        F('em dash in learner-facing text')
    for bad in ('separates nothing', 'separate nothing', 'noise'):
        if bad in text.lower():
            F(f'banned wording: "{bad}"')
    ACR_OK = {'CRASH', 'ST', 'GI', 'COVID-19', 'SARS', 'II', 'III', 'HR', 'RR', 'BP', 'COVID', 'US', 'IV', 'NBME', 'OK'}
    unexp, late = [], []
    LOWER_ABBR = ['hpf', 'lpf', 'prn']
    cands = re.findall(r'\b([A-Z][A-Z0-9]{1,}(?:-[A-Z0-9]+)?)\b', text) + re.findall(r'\b((?:Ig|Hb)[A-Z0-9][A-Za-z0-9]*)\b', text) \
        + [w for w in re.findall(r'\b([a-z]{3})\b', text) if w in LOWER_ABBR]
    for a in dict.fromkeys(cands):
        if a in ACR_OK or len(a) > 8:
            continue
        m0 = re.search(r'\b' + re.escape(a) + r'\b', text)
        at_first = re.match(r'\s*\(', text[m0.end():]) or (text[:m0.start()].rstrip().endswith('(') and text[m0.end():].lstrip().startswith(')')) \
            or re.match(r':\s', text[m0.end():])
        if not re.search(re.escape(a) + r'\s*\(|\(' + re.escape(a) + r'\)|' + re.escape(a) + r':\s', text):
            unexp.append(a)
        elif not at_first:
            late.append(a)
    if unexp:
        F('V1 acronyms never written out: ' + ', '.join(unexp))
    if late:
        F('V1 acronyms used before they are written out (write out at first use): ' + ', '.join(late))
    pre = new.split('class="authored-hdr"')[0]
    words = len(H.unescape(re.sub(r'<[^>]+>', ' ', pre)).split())
    if words > 1400:
        W(f'{words} words before the practice questions (cap about 1,300)')
    if len(new_items) < 12:
        W(f'{len(new_items)} practice questions (coverage list aims for 12 to 18)')

    # ---- item contract (tools/ITEM_CONTRACT.md); codes I1-I9, A1
    item_contract(new, new_items, old_items, cmap, F, W)
    old_exp = {a: e for a, e in re.findall(r'\b([A-Z][A-Za-z0-9-]*[A-Z])\s*\(([A-Za-z][^()]{3,80})\)', H.unescape(re.sub(r'<[^>]+>', ' ', old)))
               if re.search(r'[a-z]{3}', e)}
    for acr, exp in old_exp.items():
        if re.search(r'\b' + re.escape(acr) + r'\b', text) and not re.search(re.escape(acr) + r'\s*\(|\(' + re.escape(acr) + r'\)|' + re.escape(acr) + r':\s', text):
            F(f'A1 old brief wrote out {acr} ({exp}); the new brief uses {acr} without it')

    # ---- V2 vendor text (needs --source=<local source file>): no 10-word run copied from the source
    src_arg = next((x[9:] for x in sys.argv[1:] if x.startswith('--source=')), None)
    if src_arg:
        def shingles(x):
            w = re.findall(r"[a-z0-9]+", H.unescape(re.sub(r'<[^>]+>', ' ', x)).lower())
            return {' '.join(w[i:i + 10]) for i in range(len(w) - 9)}
        # NBME lead-ins may be exact (board-brief Rule 11), so the lead-in attribute is not scanned; stems and options are
        shared = shingles(new + ' ' + ' '.join(re.findall(r'data-(?:d1|d2)="([^"]*)"', new))) & shingles(open(src_arg, encoding='utf-8').read())
        if shared:
            F(f'V2 {len(shared)} run(s) of 10 or more words copied from the vendor source, e.g. "{sorted(shared)[0]}"')

    # ---- K1 mnemonics carried and highlighted; K2 scale references resolve
    def mnems(html_):
        out = []
        for mm in re.finditer(r'(?:<h5[^>]*>(.*?)</h5>\s*)?<ul class="(plain(?: mnem)?)"([^>]*)>(.*?)</ul>', html_, re.S):
            lis = re.findall(r'<li[^>]*>(.*?)</li>', mm.group(4), re.S)
            heads = [re.match(r'\s*<b(?: class="mn")?>([^<]{1,12})</b>', li) for li in lis]
            if lis and sum(1 for h in heads if h) >= max(2, len(lis) * 0.7):
                out.append({'title': norm(mm.group(1) or ''), 'id': (re.search(r'id="([^"]+)"', mm.group(3)) or [None, None])[1],
                            'initials': [h.group(1) if h else '' for h in heads],
                            'bolds': [norm(b) for li in lis for b in re.findall(r'<b(?: class="mn")?>(.*?)</b>', li)[1:]],
                            'hl': 'mnem' in mm.group(2) and all(re.match(r'\s*<b class="mn">', li) for li in lis),
                            'seps': all(re.search(r'\s[\u2014\u2013]\s|\s&ndash;\s', H.unescape(li)) or re.search(r'\s&ndash;\s', li) for li in lis),
                            'n': len(lis)})
        return out
    newm = mnems(new)
    for om in mnems(old):
        match = next((x for x in newm if x['initials'] == om['initials']), None)
        label = om['title'] or '/'.join(om['initials'])
        if not match:
            F(f'K1 mnemonic "{label}" is not carried as a highlighted mnemonic block (ul.plain, each line opening with its bold letter: {"".join(om["initials"])})')
            continue
        if not match['hl']:
            F(f'K1 mnemonic "{label}" is not highlighted: use <ul class="plain mnem"> and open each line with <b class="mn">letter</b>')
        if om['title'] and om['title'] not in newn:
            F(f'K1 mnemonic name "{om["title"]}" is missing from the new brief')
        if not match['seps']:
            F(f'K1 mnemonic "{label}": every line needs " &ndash; " between the term and its meaning (the page renders it as a masked mnemonic)')
        lost = [b for b in om['bolds'] if b not in match['bolds']]
        if lost:
            F(f'K1 mnemonic "{label}": highlighted phrases lost: {lost[:4]}')
    for blk in re.findall(r'<div class="[^"]*"><span class="lbl">([^<]*[Mm]nemonic[^<]*)</span>(.*?)</div>', old, re.S):
        for b in re.findall(r'<b>(.*?)</b>', blk[1]):
            if norm(b) and not re.search(r'<b[^>]*>\s*' + re.escape(b.strip()) + r'\s*</b>', new):
                F(f'K1 mnemonic block "{norm(blk[0])}": highlighted term "{norm(b)}" is not carried in bold')
    for sc in re.findall(r'class="scaleref"[^>]*data-scale="([^"]+)"', old):
        if f'data-scale="{sc}"' not in new:
            F(f'K2 scale reference to #{sc} (the criteria tile\'s link to its mnemonic or table) was dropped')
    for sc in re.findall(r'class="scaleref"[^>]*data-scale="([^"]+)"', new):
        if f'id="{sc}"' not in new:
            F(f'K2 scale reference #{sc} has no target in the new brief')

    # ---- H1 inbound titles (needs --page=index.html)
    page_arg = next((x[7:] for x in sys.argv[1:] if x.startswith('--page=')), None)
    old_h4 = [norm(h) for h in re.findall(r'<h4[^>]*>(.*?)</h4>', old, re.S)]
    new_h4 = norm((re.findall(r'<h4[^>]*>(.*?)</h4>', new, re.S) or [''])[0])
    if page_arg:
        pg = open(page_arg, encoding='utf-8').read()
        refs = {}
        for pb in re.findall(r'<span class="lbl">Pairs with</span>(.*?)</div>', pg, re.S):
            for b in re.findall(r'<b>(.*?)</b>', pb, re.S):
                refs[norm(b)] = refs.get(norm(b), 0) + 1
        nav = [norm(x) for x in re.findall(r'<a href="#[^"]+">(.*?)</a>', pg)]
        rewrites = {norm(x) for x in cmap.get('inbound_rewrites', [])}
        for h in old_h4:
            if h and h != new_h4 and (refs.get(h) or h in nav) and h not in rewrites:
                F(f'H1 title changed from "{h}" to "{new_h4}" but {refs.get(h, 0)} Pairs-with reference(s) and the sidebar still name it; keep the title or list it in claim_map inbound_rewrites and rewrite them')
    if page_arg:
        h4s = {norm(h) for h in re.findall(r'<h4[^>]*>(.*?)</h4>', pg, re.S)} | {new_h4}
        for pb in re.findall(r'<span class="lbl">Pairs with</span>(.*?)</div>', new, re.S):
            for b in re.findall(r'<b>(.*?)</b>', pb, re.S):
                if norm(b) not in h4s:
                    F(f'P1 Pairs-with partner "{norm(b)}" is not an <h4> on the page (use <i> for a partner not on the page)')
    elif old_h4 and new_h4 not in old_h4:
        W('H1 title changed; run with --page=index.html to check inbound references')

    summary = {'claims': len(claims), 'clues': nclue, 'old_items': len(old_items), 'new_items': len(new_items),
               'words_before_bank': words, 'fails': fails, 'warns': warns}
    if as_json:
        print(json.dumps(summary, indent=1))
    else:
        print(f"migrate_check: {'FAIL' if fails else 'PASS'} | claims {len(claims)} (clues {nclue}) | "
              f"old items {len(old_items)} | new items {len(new_items)} | words before bank {words}")
        for f in fails:
            print('  FAIL', f)
        for w in warns:
            print('  WARN', w)
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
