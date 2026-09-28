#!/usr/bin/env python3
"""migrate_check.py: mechanical checks for one brief-migration cluster.

  python3 tools/migrate_check.py <old_briefs.html> <new_brief.html> <claim_map.json> [--json]

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


def main():
    a = [x for x in sys.argv[1:] if not x.startswith('--')]
    as_json = '--json' in sys.argv
    old = open(a[0], encoding='utf-8').read()
    new = open(a[1], encoding='utf-8').read()
    cmap = json.load(open(a[2], encoding='utf-8'))
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
    unexp = []
    for a in dict.fromkeys(re.findall(r'\b([A-Z][A-Z0-9]{1,}(?:-[A-Z0-9]+)?)\b', text)):
        if a in ACR_OK or len(a) > 8:
            continue
        if not re.search(re.escape(a) + r'\s*\(|\(' + re.escape(a) + r'\)|' + re.escape(a) + r':\s', text):
            unexp.append(a)
    if unexp:
        W('acronyms never written out: ' + ', '.join(unexp))
    pre = new.split('class="authored-hdr"')[0]
    words = len(H.unescape(re.sub(r'<[^>]+>', ' ', pre)).split())
    if words > 1400:
        W(f'{words} words before the practice questions (cap about 1,300)')
    if len(new_items) < 12:
        W(f'{len(new_items)} practice questions (coverage list aims for 12 to 18)')

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
