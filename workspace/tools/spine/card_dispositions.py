#!/usr/bin/env python3
"""card_dispositions (s146b, Jonathan 2026-10-17): every AnKing card a brief's board terms reach gets a recorded
disposition, so a skipped board fact is caught mechanically rather than left to the lead's judgment.

  python3 tools/spine/card_dispositions.py make <brief-id> <brief folder> [--cap 90]
      runs card_checklist.py with the brief's terms from repair/efficiency/board_terms.json (cards linked by note id,
      plus up to --cap Step 2 candidates, default 90) and writes <folder>/cards.md (card text: local-only, never committed)
  python3 tools/spine/card_dispositions.py check <brief folder> [--page index.html] [--quiet]
      every card in cards.md needs an entry in <folder>/cards_disposition.json:
        covered:S012[,S040] <where>  (claim ids from claim_map.json, or practice item ids q_..., that teach it)
        owner:<brief id>             (a live brief on the page teaches it)
        scope:<reason>               (in the topic but deliberately not taught; the reason is required)
        not-topic[:<reason>]         (the search term matched, the card is about something else)
        conflict:<fact id> <note>    (a source opened that day disagrees; the board answer is taught)
      A high-yield statement inherits its card's disposition unless it has its own entry ("<nid>.<key>").
      Exit 1 on any error; a covered statement whose key words are absent from the brief is listed as a warning.
verify.py runs the check whenever a folder holds cards.md (G-MECH), and review_packet.py gives the acc part both files.
"""
import html as H
import json
import os
import re
import subprocess
import tempfile
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, '..', '..'))
KINDS = ('covered', 'owner', 'scope', 'not-topic', 'conflict')
STOP = set('with from that this have been their which when what does into than then also more most less only some '
           'such other these those after before over under about there where while being because patient patients '
           'cause causes caused associated typically usually often common commonly due'.split())


def parse_cards(path):
    """[(card id, anchor, statements [(stmt id, text)])] from a card_checklist cards.md"""
    cards, cur = [], None
    for line in open(path, encoding='utf-8'):
        m = re.match(r'## (card|candidate) (\S+)', line)
        if m:
            cur = [m.group(2), '', '', []]
            cards.append(cur)
            continue
        if not cur:
            continue
        m = re.match(r'- anchor \(cloze\): (.*)', line)
        if m:
            cur[1] = m.group(1).strip()
        m = re.match(r'- card text: (.*)', line)
        if m:
            cur[2] = m.group(1).strip()
        m = re.match(r'- \[(\S+?\.[0-9a-f]+)\] (.*)', line)
        if m:
            cur[3].append((m.group(1), m.group(2).strip()))
    return cards


def words(s):
    return [w for w in re.findall(r'[a-z0-9]{4,}', s.lower()) if w not in STOP]


def check(folder, page_path, quiet=False):
    cp, dp = os.path.join(folder, 'cards.md'), os.path.join(folder, 'cards_disposition.json')
    errs, warns = [], []
    if not os.path.exists(cp):
        return ['no cards.md (run: card_dispositions.py make <brief> <folder>)'], []
    disp = json.load(open(dp, encoding='utf-8')) if os.path.exists(dp) else {}
    cm = json.load(open(os.path.join(folder, 'claim_map.json'), encoding='utf-8'))
    claim_ids = {c['id'] for c in cm.get('claims', [])}
    facts = set()
    fp = os.path.join(folder, 'facts.json')
    if os.path.exists(fp):
        facts = {f['id'] for f in json.load(open(fp, encoding='utf-8'))['facts']}
    page = open(page_path, encoding='utf-8').read()
    live = set(re.findall(r'<div class="brief[^"]*" id="([^"]+)"', page))
    bp = os.path.join(folder, 'brief.html')
    bhtml = open(bp, encoding='utf-8').read() if os.path.exists(bp) else ''
    hov = ' '.join(re.findall(r'data-(?:body|title)="([^"]*)"', bhtml))     # hover cards teach too
    btxt = H.unescape(re.sub(r'<[^>]+>', ' ', bhtml) + ' ' + hov).lower()
    bstems = {w[:6] for w in re.findall(r'[a-z0-9]+', btxt)}
    cards = parse_cards(cp)
    n = {k: 0 for k in KINDS}
    for cid, anchor, text, stmts in cards:
        d = disp.get(cid)
        if not d:
            errs.append('card %s: no disposition (%s)' % (cid, (text or anchor)[:70]))
            continue
        kind, _, rest = d.partition(':')
        kind, rest = kind.strip(), rest.strip()
        if kind not in KINDS:
            errs.append('card %s: unknown disposition %r' % (cid, d[:40]))
            continue
        n[kind] += 1
        if kind == 'covered':
            ids = re.findall(r'\bS\d{3}\b', rest)
            qids = re.findall(r'\bq_[0-9a-f]{20}\b', rest)      # a practice item that teaches it
            if not ids and not qids:
                errs.append('card %s: covered names no claim id (S###) or item id (q_...)' % cid)
            for i in ids:
                if i not in claim_ids:
                    errs.append('card %s: covered claim %s not in claim_map.json' % (cid, i))
            for q in qids:
                if 'data-item-id="%s"' % q not in bhtml:
                    errs.append('card %s: covered item %s not in the brief' % (cid, q))
        elif kind == 'owner':
            o = rest.split()[0] if rest else ''
            if o not in live:
                errs.append('card %s: owner %r is not a live brief' % (cid, o))
        elif kind == 'scope' and len(rest) < 8:
            errs.append('card %s: scope needs a reason' % cid)
        elif kind == 'conflict':
            f = rest.split()[0] if rest else ''
            if f not in facts:
                errs.append('card %s: conflict fact %r not in facts.json' % (cid, f))
        for sid, st in stmts:
            sd = disp.get(sid, d)
            sk = sd.partition(':')[0].strip()
            if sk not in KINDS:
                errs.append('statement %s: unknown disposition %r' % (sid, sd[:40]))
            elif sk == 'covered' and not re.search(r'photo credit|image\(s\) provided|image licensed|pathoma rules', st.lower()):
                ws = words(st)
                miss = [w for w in ws if w[:6] not in bstems]
                if ws and len(miss) > len(ws) / 2:
                    warns.append('statement %s inherits "covered" but most key words are absent: %s' % (sid, st[:90]))
    if not quiet:
        print('card_dispositions: %s: %d cards (%s); %d error(s), %d warning(s)' % (
            os.path.relpath(folder, WS), len(cards), ', '.join('%s %d' % kv for kv in n.items() if kv[1]), len(errs), len(warns)))
        for e in errs[:40]:
            print('  ERROR ' + e)
        for w in warns[:40]:
            print('  warn  ' + w)
    return errs, warns


def make(bid, folder, cap):
    terms = json.load(open(os.path.join(WS, 'repair', 'efficiency', 'board_terms.json'), encoding='utf-8')).get(bid, [])
    args = [sys.executable, os.path.join(HERE, 'card_checklist.py'), bid, '--cap', str(cap),
            '--out', os.path.join(folder, 'cards.md')]
    if terms:
        args[3:3] = ['--terms', ','.join(terms)]
    import basepage as BP   # s148e: a brief new in its batch has its shell in the folder (05_*_new.json)
    if BP.shells(folder):
        args += ['--page', BP.base_page_path(folder, tempfile.mkdtemp(prefix='cards-'))]
    r = subprocess.run(args, capture_output=True, text=True, cwd=WS)
    print((r.stdout + r.stderr).strip())
    return r.returncode


def main(argv):
    if len(argv) < 2 or argv[0] not in ('make', 'check'):
        sys.exit(__doc__)
    if argv[0] == 'make':
        cap = int(argv[argv.index('--cap') + 1]) if '--cap' in argv else 90
        sys.exit(make(argv[1], os.path.abspath(argv[2]), cap))
    page = argv[argv.index('--page') + 1] if '--page' in argv else os.path.join(WS, 'index.html')
    errs, _ = check(os.path.abspath(argv[1]), page, '--quiet' in argv)
    sys.exit(1 if errs else 0)


if __name__ == '__main__':
    main(sys.argv[1:])
