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
    s = H.unescape(re.sub(r'<[^>]+>', ' ', s or ''))
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

    # ---- items
    old_items = items_of(old)
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
    for a in dict.fromkeys(re.findall(r'\b([A-Z][A-Z0-9]{1,}(?:-[A-Z0-9]+)?)\b', text)):
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
        shared = shingles(new + ' ' + ' '.join(re.findall(r'data-(?:lead-in|d1|d2)="([^"]*)"', new))) & shingles(open(src_arg, encoding='utf-8').read())
        if shared:
            F(f'V2 {len(shared)} run(s) of 10 or more words copied from the vendor source, e.g. "{sorted(shared)[0]}"')

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
