#!/usr/bin/env python3
"""Pre-review lint (s148 efficiency fix 6, Jonathan 2026-10-18). Advisory: verify --mech prints its findings as
"warn lint:" lines and never fails on them; the lead clears or answers each one in the S6 self-check (runbook section 4,
item 15) before any reviewer runs. It catches the categories that drew most s148 round-1 MEDs:

  next-step   a clue-table "Next best step" cell with no action (no verb, test or treatment term; "Not X" alone)
  alias       a diagnosis in repair/efficiency/ALIASES.json without its other name at first mention or in its row
  hedge       a claim whose closest cited quote carries a hedge word (may, usually, often, can, likely, typically,
              suggests) that the claim does not
  threshold   one decision with two thresholds: the same "past/after/within/under/over N unit" phrase with values that
              overlap but differ (backpain "past 4 to 6 weeks" against "past 6 weeks")
  number      a number in a claim that none of its cited quotes holds

  python3 tools/spine/lint.py <brief dir> [--quiet]     one "lint <check>: ..." line per finding; exit 0 always
"""
import html as H
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, '..', '..'))

LINT_HEDGES = ('may', 'usually', 'often', 'likely', 'typically', 'suggests', 'suggest')
# "can" (in the spec's list) is left out: in quotes it is almost always permission ("can be treated with", "MRI can be
# done"), not a hedge; measured on the nine s148 briefs it was most of the hedge noise. condpass keeps it as meaning.
NOT_HEDGE = re.compile(r'\b(?:most likely|the likely diagnosis|likely diagnosis)\b', re.I)
ACTION = set('''check order obtain get start begin give treat image refer consult reduce repair splint immobilize aspirate
tap drain measure test screen admit stop hold switch add observe reassure follow diagnose biopsy culture inject operate
decompress fix fixate fixation replace remove stabilize transfuse resuscitate monitor repeat recheck confirm exclude rule
continue taper raise lower lift reconsider avoid loosen rest ice brace sling cast elevate counsel educate discharge
send call examine palpate scan perform keep use offer prescribe dose withhold restart resume plan watch wait
mri ct ultrasound radiograph radiographs xray x-ray view views esr crp cbc bmp labs markers stain gram naat arthrocentesis
aspiration surgery surgical orif arthroplasty therapy physiotherapy nsaid nsaids acetaminophen glucocorticoid
glucocorticoids steroid steroids prednisone antibiotic antibiotics vancomycin ceftriaxone cefazolin analgesia analgesic
injection referral consultation incision debridement washout conservative care reduction catheter catheterization
voiding cystourethrogram vcug echocardiogram ecg ekg emg ultrasonography densitometry dexa bisphosphonate ppi
colchicine allopurinol methotrexate opioid opioids heat stretching exercise exercises strengthening factor level levels
hormone antibody antibodies panel assay count titer tsh a1c glucose drug drugs medication medications anti-ccp'''.split())
WEAK = ('look for', 'recognize', 'think of', 'consider it')
NUM = re.compile(r'(?<![\w.-])(\d+(?:[.,]\d+)?)(?![\w])')        # "beta-2" is a name, not a number
LABEL_NUM = re.compile(r'\b(?:rung|rungs|step|steps|card|cards|day|part|item|row)\s+(\d+)\b', re.I)
NUMWORDS = {'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 'six': '6', 'seven': '7', 'eight': '8',
            'nine': '9', 'ten': '10', 'eleven': '11', 'twelve': '12', 'twenty': '20', 'thirty': '30', 'forty': '40',
            'fifty': '50', 'hundred': '100'}
THR = re.compile(r'\b(past|after|beyond|within|under|over|longer than|more than|less than)\s+(\d+(?:\.\d+)?)'
                 r'(?:\s*(?:to|-|–)\s*(\d+(?:\.\d+)?))?\s*(minute|hour|day|week|month|year)s?\b', re.I)
SAME = {'past': 'past', 'after': 'past', 'beyond': 'past', 'longer than': 'past', 'more than': 'over', 'over': 'over',
        'within': 'within', 'under': 'under', 'less than': 'under'}


def text(h):
    h = re.sub(r'<button[^>]*>.*?</button>', ' ', h, flags=re.S)
    return re.sub(r'\s+', ' ', H.unescape(re.sub(r'<[^>]+>', ' ', h))).strip()


def words(t):
    return re.findall(r"[a-z]+(?:-[a-z]+)?", t.lower())


def body(brief_html):
    """the brief above the Practice bank"""
    m = re.search(r'<h5 class="[^"]*authored-hdr', brief_html)
    return brief_html[:m.start()] if m else brief_html


# ---- next-step
def has_action(cell):
    low = cell.lower()
    for w in WEAK:
        low = low.replace(w, ' ')
    ws = set(words(low)) | set(re.findall(r'[a-z]+', low))
    return bool(ws & ACTION)


def next_step_cells(brief_html):
    out = []
    for t in re.findall(r'<table[^>]*>.*?</table>', body(brief_html), re.S):
        heads = [text(x) for x in re.findall(r'<th[^>]*>(.*?)</th>', t, re.S)]
        if 'Next best step' not in heads:
            continue
        col = heads.index('Next best step')
        for row in re.findall(r'<tr>(.*?)</tr>', t, re.S):
            cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.S)
            if len(cells) > col:
                out.append((text(cells[0]), text(cells[col])))
    return out


def lint_next_step(brief_html):
    return ['next-step: row "%s": "%s" names no action (a verb, test or treatment)' % (c[:50], n[:80])
            for c, n in next_step_cells(brief_html) if not has_action(n)]


# ---- alias
def alias_table():
    try:
        return json.load(open(os.path.join(WS, 'repair', 'efficiency', 'ALIASES.json'), encoding='utf-8'))['entries']
    except (OSError, ValueError, KeyError):
        return []


def _find(name, t):
    return re.search(r'(?<![A-Za-z])%s(?![A-Za-z])' % re.escape(name.lower()), t.lower())


def lint_alias(brief_html, table=None):
    table = alias_table() if table is None else table
    b = body(brief_html)
    flat = text(b)
    rows = []
    for r in re.findall(r'<tr>(.*?)</tr>', b, re.S):
        c = re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', r, re.S)
        if c:
            rows.append((text(c[0]), text(r)))
    out = []
    for e in table:
        names = [e['name']] + list(e.get('aliases') or [])
        hits = [(m.start(), n) for n in names for m in [_find(n, flat)] if m]
        if not hits:
            continue
        pos, first = min(hits)
        window = flat[max(0, pos - 160):pos + len(first) + 160]
        if not any(n != first and _find(n, window) for n in names):
            out.append('alias: "%s" at first mention without its other name (%s)'
                       % (first, '; '.join(n for n in names if n != first)))
        for c0, r in rows:
            if any(_find(n, c0) for n in names) and sum(1 for n in names if _find(n, r)) < 2:
                out.append('alias: differential row "%s" names %s without its other name' % (c0[:50], e['name']))
    return out


# ---- hedge, number (claim map)
def hedges(t):
    return {w for w in words(NOT_HEDGE.sub(' ', t)) if w in LINT_HEDGES}


CLAIM_HEDGES = {'can', 'might', 'sometimes', 'some', 'probably', 'possible', 'possibly'}   # hedges on the claim side
STOPW = set('the a an of in on at to for with and or by as is are be was were from that this it its not no than then '
            'into over under after before about'.split())


def near_hedges(claim, quote, span=5):
    """hedge words of the quote that sit within span words of a content word the claim shares"""
    cw = {w for w in words(claim) if w not in STOPW and len(w) > 2}
    qw = words(NOT_HEDGE.sub(' ', quote))
    hits = [i for i, w in enumerate(qw) if w in cw]
    return {w for i, w in enumerate(qw) if w in LINT_HEDGES and any(abs(i - j) <= span for j in hits)}


def claim_rows(cm, facts):
    for c in cm.get('claims', []) if isinstance(cm, dict) else cm:
        t = H.unescape(re.sub(r'<[^>]+>', ' ', c.get('new_text') or c.get('text') or ''))
        qs = []
        for s in c.get('sources') or []:
            if isinstance(s, dict):
                qs += [s.get('source_says') or '', facts.get(s.get('id'), '')]
        qs += [facts.get(i, '') for i in c.get('derived_from') or [] if isinstance(i, str)]
        yield c.get('id', '?'), t, [q for q in qs if q]


def lint_hedge(rows):
    out = []
    for cid, t, qs in rows:
        if not qs or hedges(t) or set(words(t)) & CLAIM_HEDGES or len(words(t)) < 6:      # a short label is not an assertion
            continue
        tw = {w for w in words(t) if w not in STOPW}
        best = max(qs, key=lambda q: len(tw & set(words(q))))
        lost = near_hedges(t, best)
        if lost and len(tw & set(words(best))) >= 3:
            out.append('hedge: %s "%s" drops "%s" from its quote "%s"' % (cid, t[:70], '", "'.join(sorted(lost)), best[:80]))
    return out


def lint_number(rows):
    out = []
    for cid, t, qs in rows:
        q = ' '.join(qs).replace(',', '')
        q += ' ' + ' '.join(NUMWORDS[w] for w in re.findall(r'[a-z]+', q.lower()) if w in NUMWORDS)
        have = set(NUM.findall(q))
        labels = set(LABEL_NUM.findall(t))
        miss = [n for n in NUM.findall(t.replace(',', '')) if n not in have and n not in labels and n not in ('0', '1')]
        if miss and qs:
            out.append('number: %s "%s": %s in no cited quote' % (cid, t[:70], ', '.join(sorted(set(miss)))))
    return out


# ---- threshold
def lint_threshold(brief_html):
    flat = text(body(brief_html))
    seen = {}
    for m in THR.finditer(flat):
        lo = float(m.group(2))
        hi = float(m.group(3)) if m.group(3) else lo
        key = (SAME[m.group(1).lower()], m.group(4).lower())
        seen.setdefault(key, []).append((lo, hi, m.group(0)))
    out = []
    for key, vals in seen.items():
        for i, (a1, b1, s1) in enumerate(vals):
            for a2, b2, s2 in vals[i + 1:]:
                if (a1, b1) != (a2, b2) and a1 <= b2 and a2 <= b1:
                    out.append('threshold: "%s" against "%s": one decision, two thresholds?' % (s1, s2))
    return sorted(set(out))


def lint(folder, facts_dir=None):
    out = []
    bh = os.path.join(folder, 'brief.html')
    if os.path.exists(bh):
        brief_html = open(bh, encoding='utf-8').read()
        out += lint_next_step(brief_html) + lint_alias(brief_html) + lint_threshold(brief_html)
    try:
        cm = json.load(open(os.path.join(folder, 'claim_map.json'), encoding='utf-8'))
    except (OSError, ValueError):
        cm = {}
    try:
        facts = {f['id']: f.get('quote', '') for f in json.load(open(os.path.join(facts_dir or folder, 'facts.json'), encoding='utf-8'))['facts']}
    except (OSError, ValueError, KeyError, TypeError):
        facts = {}
    rows = list(claim_rows(cm, facts))
    return out + lint_hedge(rows) + lint_number(rows)


def main(argv):
    if not argv:
        sys.exit(__doc__.strip().splitlines()[-1].strip())
    found = lint(argv[0])
    if '--quiet' not in argv:
        for f in found:
            print('lint ' + f)
    counts = {}
    for f in found:
        counts[f.split(':')[0]] = counts.get(f.split(':')[0], 0) + 1
    print('lint %s: %d warning(s)%s' % (os.path.basename(os.path.dirname(os.path.abspath(argv[0]))) or argv[0], len(found),
                                         (' (' + ', '.join('%s %d' % kv for kv in sorted(counts.items())) + ')') if counts else ''))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
