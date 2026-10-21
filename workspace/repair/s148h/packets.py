#!/usr/bin/env python3
"""s148h review packets (S4 plan in S148H.md): one merged file per brief and part, built from the batch page, because
tools/spine/review_packet.py renders a brief from its folder build and the folders do not carry the reasons or the
First step pairings (S148H.md "Carried"; packet gap found in the S4 chat, recorded in the batch file).

  python3 repair/s148h/packets.py --page <batch page> --live <live page> --out <packets dir>

Writes <out>/<brief>/<part>/ for acc, read, flags and display:
  deps.txt   "deps: s148h page <brief> live <sha> batch <sha>" and "brief-sha: <batch sha>" (page slices; the receipts'
             lines 2 and 3; no hook reads them, and this batch ships on approval, not READY);
  acc/reasons.md    the brief's changes besides the reasons (live against batch text, reasons stripped), then every item
                    as the learner reads it (stem, key, distractors, the three reasons) with each reason's source map
                    (best brief line and share, claims with their full text and cited ids, the lead's checks), each claim's
                    cited quotes cut to the sentences that share the most words with the reason (full quotes stay in
                    the folder's facts.json);
  flags/reasons.md  the reasons that state a number or a hedge or absolute word, or whose cited quotes hedge, each with
                    its claims and the quotes;
  read/sample.md    3 items per brief (the ones the lead's checks flag most), all three reasons each, then the
                    brief's changes besides the reasons (the First step split and prose lines) when it has any.
"""
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(WS, 'tools', 'spine'))
sys.path.insert(0, os.path.join(WS, 'tools'))
sys.path.insert(0, os.path.join(WS, 'tools', 'hooks'))
sys.path.insert(0, HERE)
import pagelib as P  # noqa: E402
import review_packet as RP  # noqa: E402
import ready_gate  # noqa: E402
import gen_s148h as G  # noqa: E402

ATTR = ('key', 'd1', 'd2')
HEDGE = re.compile(r'\b(may|might|can|could|usually|often|most|some|likely|unlikely|rarely|typically|generally|'
                   r'always|never|only|all|none|must|every)\b', re.I)
STOP = set('the a an of and or to in on for with is are be by as at from that this it its not no than then into'.split())


def words(t):
    return {w for w in re.findall(r'[a-z0-9]+', t.lower()) if w not in STOP and len(w) > 2}


def excerpt(quote, reason, n=2, cap=320):
    """The n sentences of a cited quote that share the most content words with the reason, each cut at cap chars, in
    quote order; the full quote stays in the folder's facts.json."""
    ss = [x.strip() for x in re.split(r'(?<=[.;:!?])\s+|\s+\.\.\.\s+', quote) if x.strip()]
    rw = words(reason)
    best = sorted(range(len(ss)), key=lambda i: -len(rw & words(ss[i])))[:n]
    return ' ... '.join(ss[i][:cap] for i in sorted(best) if rw & words(ss[i])) or ss[0][:cap] if ss else ''
NUM = re.compile(r'\d')
RSN = re.compile(r'; reasons: key: .*$')


def sha(s):
    return hashlib.sha1(s.encode()).hexdigest()[:10]


def slice_of(pg, bid):
    b = [x for x in P.briefs(pg) if x.id == bid]
    return pg[b[0].start:b[0].end] if b else ''


def item_blocks(txt):
    """{item id: block text} from text_of output: the [item ...] line and the lines up to the next item or heading."""
    out, cur, buf = {}, None, []
    for ln in txt.splitlines():
        m = re.match(r'\[item (\S+), type', ln)
        if m or (cur and (ln.startswith('#') or ln.startswith('== '))):
            if cur:
                out[cur] = '\n'.join(buf).strip()
            cur, buf = (m.group(1), [ln]) if m else (None, [])
            continue
        if cur:
            buf.append(ln)
    if cur:
        out[cur] = '\n'.join(buf).strip()
    return out


def source_map(bid):
    """{item id prefix (10 chars): {attr: [lines]}} from data/sources/<bid>.md."""
    out, item, attr = {}, None, None
    for ln in open(os.path.join(HERE, 'data', 'sources', bid + '.md'), encoding='utf-8').read().splitlines():
        m = re.match(r'## (\S+)  key:', ln)
        if m:
            item, attr = m.group(1), None
            out[item] = {}
            continue
        m = re.match(r'- (key|d1|d2) why:', ln)
        if m and item:
            attr = m.group(1)
            out[item][attr] = []
            continue
        if item and attr and ln.startswith('  - '):
            out[item][attr].append(ln[4:])
    return out


def claims_of(folder):
    if not folder:
        return {}
    cm = json.load(open(os.path.join(folder, 'claim_map.json'), encoding='utf-8'))
    return {c['id']: c for c in cm.get('claims', [])}


def checks_for(checks, bid):
    out = {}
    for c in checks['row_reuse']:
        if c['brief'] == bid:
            out.setdefault((c['item'], c['attr']), []).append(
                'lead check: reuses the %s row and adds: %s' % (c['choice'], ', '.join(c['words_not_in_row'])))
    for c in checks['wording']:
        if c['brief'] == bid:
            out.setdefault((c['item'], c['attr']), []).append(
                'lead check: words found nowhere in the brief: %s' % ', '.join(c['words_not_in_brief']))
    return out


def main(argv):
    page, live, out = (argv[argv.index(k) + 1] for k in ('--page', '--live', '--out'))
    pg, lv = P.read_page(page), P.read_page(live)
    reasons = json.load(open(os.path.join(HERE, 'data', 'reasons.json'), encoding='utf-8'))
    checks = json.load(open(os.path.join(HERE, 'data', 'checks.json'), encoding='utf-8'))
    folders = ready_gate.folders()
    rows = []
    for bid in G.ORDER:
        new_h, old_h = slice_of(pg, bid), slice_of(lv, bid)
        new_t, old_t = RP.text_of(new_h), RP.text_of(old_h)
        strip = lambda t: [RSN.sub('', x) for x in t.splitlines()]  # noqa: E731
        ch = RP.since_diff(strip(old_t), strip(new_t)).replace('your last review', 'the live page').replace(
            'the version you last reviewed', 'the live page')
        blocks = item_blocks(new_t)
        smap = source_map(bid)
        folder = folders.get(bid)
        cl = claims_of(folder)
        chk = checks_for(checks, bid)
        deps = 'deps: s148h page %s live %s batch %s\nbrief-sha: %s\n' % (bid, sha(old_h), sha(new_h), sha(new_h))
        acc = ['# %s: per-choice reasons and other changes (s148h)' % bid, '',
               'Folder: %s' % (os.path.relpath(folder, WS) if folder else 'none (non-spine brief; page text only)'), '',
               ch.replace('# Changes since', '## Changes besides the reasons, since'), '## Items', '',
               'Each item as the learner reads it ([item id, type], lead-in, distractors, then "reasons: key | d1 | d2", '
               'then the stem, the answer and the explanation chain); under each reason, its source map: the best '
               'brief line (share of the reason\'s content words found on it), the claims (S### ids, full text, cited '
               'fact ids) and the lead\'s checks.', '']
        flags = ['# %s: reasons with a number, a hedge or an absolute word, or hedged quotes (s148h)' % bid, '']
        quotes, sample, seen = {}, [], set()
        n_f = 0
        for iid, rs in reasons[bid].items():
            if iid.startswith('_'):
                continue
            blk = blocks.get(iid, '(item not found on the batch page: %s)' % iid)
            acc.append(blk)
            m = smap.get(iid[:10], {})
            fl_item = []
            score = 0
            for k, r in enumerate(rs):
                a = ATTR[k]
                ids = re.findall(r'\b(S\d{3})\b', ' '.join(x for x in m.get(a, []) if x.startswith('claims:')))[:2]
                acc.append('- %s reason: "%s"' % (a, r))
                for x in m.get(a, []):
                    if x.startswith('best line'):
                        acc.append('  - ' + x)
                lines, ex = [], {}
                for i in ids:
                    c = cl.get(i)
                    if not c:
                        continue
                    srcs = c.get('sources', [])
                    lines.append('  - claim %s [%s]: %s' % (i, ', '.join(x['id'] for x in srcs), (c.get('new_text') or '')[:240]))
                    rw = words(r)
                    for x in sorted(srcs, key=lambda x: -len(rw & words(x.get('source_says', ''))))[:2]:
                        quotes[x['id']] = x
                        e = excerpt(x.get('source_says', ''), r, n=1, cap=260)
                        ex[x['id']] = e
                        key = (x['id'], e)
                        lines.append('    - %s says: %s' % (x['id'], '(same line as above)' if key in seen else '"%s"' % e))
                        seen.add(key)
                acc += lines
                for x in chk.get((iid, 'data-%s-why' % a), []):
                    acc.append('  - ' + x)
                    score += 1
                lost = not HEDGE.search(r) and any(HEDGE.search(x) for x in ex.values())
                if NUM.search(r) or HEDGE.search(r) or lost:
                    fl_item.append('- %s reason: "%s"%s' % (a, r, '' if lines else ' (no claim matched; judge against '
                                                            'the item explanation)'))
                    fl_item += lines
                    n_f += 1
            acc.append('')
            if fl_item:
                flags += ['## ' + blk.splitlines()[0]] + blk.splitlines()[1:2] + fl_item + ['']
            sample.append((score, iid, blk))
        acc += ['Sources by id: ' + '; '.join('%s %s' % (q, s.get('source', '')[:70]) for q, s in sorted(quotes.items()))]
        top = sorted(sample, key=lambda x: -x[0])[:3]
        rd = ['# %s: 3 sample items, all three reasons each' % bid, ''] + [b for _, _, b in top] + ['']
        if 'No change.' not in ch:
            rd += [ch.replace('# Changes since', '## %s: changes besides the reasons, since' % bid)]
        for part, body in (('acc', acc), ('flags', flags), ('read', rd), ('display', None)):
            d = os.path.join(out, bid, part)
            os.makedirs(d, exist_ok=True)
            open(os.path.join(d, 'deps.txt'), 'w').write(deps)
            if body is not None:
                name = 'sample.md' if part == 'read' else 'reasons.md'
                open(os.path.join(d, name), 'w', encoding='utf-8').write('\n'.join(body) + '\n')
        nch = ch.count('\n+') + ch.count('\n-')
        rows.append((bid, len([k for k in reasons[bid] if not k.startswith('_')]), n_f, nch,
                     len('\n'.join(acc)), len('\n'.join(flags))))
    for r in rows:
        print('%-20s items %2d  flags reasons %2d  changed lines %2d  acc %6d chars  flags %6d chars' % r)
    print('packets: %d briefs, acc %d chars, flags %d chars' % (len(rows), sum(r[4] for r in rows), sum(r[5] for r in rows)))


if __name__ == '__main__':
    main(sys.argv[1:])
