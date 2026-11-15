#!/usr/bin/env python3
"""B0 for a content rewrite batch: read the content_audit output, write the per-brief summary, the goldens and the
rewrite_lanes spec.  python3 repair/s176/b0.py <batch> <golden,golden> <id> <id> ...   (run from workspace/)"""
import csv, json, os, sys
WS = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.insert(0, os.path.join(WS, 'tools')); sys.path.insert(0, os.path.join(WS, 'tools', 'spine'))
import pagelib as P
import review_packet as RP
PRIV = os.environ.get('AX_PRIVATE', '/home/claude/step2haki-private')
batch, goldens, ids = sys.argv[1], sys.argv[2].split(','), sys.argv[3:]
L = os.path.join(WS, 'local', batch); A = os.path.join(L, 'audit')
rows = lambda f: list(csv.DictReader(open(os.path.join(A, f), encoding='utf-8')))
pb = {r['brief']: r for r in rows('prose_by_brief.csv')}
hv, nb, s2, ip = {}, {}, {}, {}
for r in rows('hovers.csv'): hv[r['brief']] = hv.get(r['brief'], 0) + 1
for r in rows('nbme_blocks.csv'):
    if r['pause'] == '0': nb.setdefault(r['brief'], []).append(r)
for r in rows('step2.csv'): s2.setdefault(r['brief'], []).append(r['step_name'])
for r in rows('in_practice.csv'):
    if r['names_source'] == '1': ip[r['brief']] = ip.get(r['brief'], 0) + 1
own = {}
for v in json.load(open(os.path.join(WS, 'repair/s170/anchors/anchor_own_pending.json'))).values():
    own[v['brief']] = own.get(v['brief'], 0) + 1
page = P.read_page(os.path.join(WS, 'index.html'))
G = os.path.join(L, 'goldens'); os.makedirs(G, exist_ok=True)
for g in goldens:
    b = P.brief_by_id(page, g)
    h = page[b.start:b.end]
    open(os.path.join(G, g + '.html'), 'w', encoding='utf-8').write(h)
    open(os.path.join(G, g + '.txt'), 'w', encoding='utf-8').write(RP.text_of(h))
GEN = ("Presentation hub: follow the shipped voices hub for line shapes, headers, table cells and hover layout: %s/voices.txt and its rewrite "
       "file %s/repair/migration/psych/HUB/voices/spine/rewrite_s170/rewrite_s170.json (grep it, never read whole); mdd (%s/mdd.txt) for key "
       "point and finding lines. Header list: %s/repair/efficiency/HEADERS.json; a header off the list is a NOTES.md row. Hover anchors: "
       "re-judge each hover's trigger under the contract's hover-anchor rules (the s172e KEEP verdicts are an open item for this rewrite); "
       "no label text is added. Lessons from the s171 to s174 review rounds: (1) a number, dose, age or duration stays exactly as its "
       "claim's quote gives it; never add, round or drop one; (2) when a line or hover line is split, each part carries the claim ids of "
       "the facts it holds; (3) text inside a study-mode mask stays inside it, and an unmasked line never names a masked answer; (4) no "
       "changed line copies 12 or more consecutive words of a source quote; (5) keep every hedge (may, can, usually, often, some, "
       "typically) or record lock_ok with its reason; (6) a raw unit that removes a wrapper names every claim the wrapper held, shared "
       "label claims included (a raw with \"claims\": [] drops them); (7) offered wrong options in a carried NBME fact are labeled with "
       "the header list's name, never with source words; (8) the lane shell refuses any command holding a '>' character: write files "
       "with the Write tool; (9) every changed line that states a fact carries at least one claim id whose quote holds it; a fact no "
       "quote in facts_before holds is not added, and a shipped line with no claim keeps its facts unchanged; (10) a table caption or "
       "block heading comes from the header list: a management ladder caption reads \"Stepwise management: <condition>\" (H12), with "
       "\"lock\": false and a lock_reason naming the header row, and its ladder rule kept as an sp-note line before the table; a "
       "differential table caption reads \"Differential diagnosis\" with any setting kept as a \"Setting:\" sp-note line; (11) no "
       "rowspan in any table (the study-mode gate refuses it): repeat the cell per row; (12) an abbreviation off "
       "%s/repair/efficiency/ABBREV.json is written out at first mention; (13) a contrast or negation in the shipped line that "
       "carries a fact (\"no fever\", \"not bilious\") is kept as a negative finding, never dropped with the contrast form. "
       "Plan your calls: INSTRUCTIONS.md, units.md by range, one Write of rewrite_%s.json, then check and fix; keep 4 calls for the "
       "last check and NOTES.md. ") % (G, WS, G, WS, WS, batch)
N5 = ("N5: one NBME %s block (nbme.md; %s). Apply the fence test (STANDING 'Pause point content': one stem detail flips the answer "
      "between two otherwise matching options). Not a fence case: state every fact the block carries (the deciding findings, the "
      "answer's action or mechanism, each offered option's separating detail) in body lines with the block's claim ids, then remove the "
      "block with carried_by; if the block or a child carries data-nbme, put that attribute on the carrying line (never on a div). An "
      "offered option whose separating detail has no claim id: search the cards first (python3 tools/spine/cards_search.py with two or "
      "three key terms), add a facts_local row for a card or the NBME source that states it, and never drop it unsearched. Fence case: "
      "say so in NOTES.md and leave the block for the lead. ")
out, tot, th, briefs = [], 0, 0, []
for i in ids:
    r = pb[i]; c = int(r['counted']); tot += c; th += hv.get(i, 0)
    out.append('%s %s %s hits %d hov %d nbme %s step2 %s ip_src %d own %d' % (i, r['entry'], r['kind'], c, hv.get(i, 0),
               [(x['kind'], x['label'], x['data_nbme']) for x in nb.get(i, [])], sorted(set(s2.get(i, []))), ip.get(i, 0), own.get(i, 0)))
    items = ['N1', 'N3', 'N4', 'N6'] + (['N5'] if nb.get(i) else []) + (['N10'] if s2.get(i) else [])
    n = ''
    for x in nb.get(i, []):
        n += N5 % ('question' if 'nbq' in x['kind'] else 'framing', ' '.join(x['text'].split()[3 if 'nbq' in x['kind'] else 2:][:22]))
    n += 'Hub: %d prose hits, %d hovers. ' % (c, hv.get(i, 0))
    if own.get(i):
        n += ('Deferred own-label rows for this brief in %s/repair/s170/anchors/anchor_own_pending.json: %d (judge each under the anchor '
              'rules). ') % (WS, own[i])
    briefs.append({'id': i, 'role': 'brief-rewrite', 'budget': 28 if c <= 15 else 32 if c <= 21 else 36, 'items': items,
                   'calls': ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C11'], 'notes': n + GEN})
out.append('total hits %d hovers %d call budget %d' % (tot, th, sum(b['budget'] for b in briefs)))
open(os.path.join(L, 'b0_summary.txt'), 'w').write('\n'.join(out) + '\n')
json.dump({'batch': batch, 'plan_step': batch, 'audit': 'local/%s/audit' % batch, 'plan': '%s/docs/batches/%s/PLAN.md' % (PRIV, batch),
           'briefs': briefs}, open(os.path.join(L, 'rewrite_spec.json'), 'w'), indent=1, ensure_ascii=False)
print('\n'.join(out))
