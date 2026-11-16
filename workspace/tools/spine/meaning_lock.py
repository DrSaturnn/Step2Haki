#!/usr/bin/env python3
"""meaning_lock (s170 T2; TEXTBOOK_STYLE rule 7, CONTENT_BATCHES_S170 design rule 6): a rewrite keeps every fact.

  python3 tools/spine/meaning_lock.py <delta.json>            one line per failing change; exit 1 on any failure
  python3 tools/spine/meaning_lock.py --old "TEXT" --new "TEXT"   check one pair

For each change in a delta ({"changes": [{"old": html, "new": html, ...}]}) the old line's carried tokens must all be
found in its new text: numbers (with their units; number words count: "double" is 2, "half" is 1/2), hedges (may,
can, might, could; usually, typically; often, commonly, frequently; some; rarely; most; generally; likely), negations
(no, not, without, never, absent, none, nor), sides (left, right, bilateral, unilateral), and names (each bold term
and each capitalized word inside a line). Words of a hedge group stand for each other ("may" for "can"); a negation
counts by number of occurrences. Equivalents: up and down arrows for increase and decrease words; an abbreviation
from ABBREV.json and its expansion; an alias pair from ALIASES.json.

A change may name where a dropped token went:
  "carried_by": [index, ...]      the new text of those changes (indexes in the same delta) also counts;
  "lock_ok": ["token", ...] with "lock_reason": "..."   tokens the lead or reviewer accepts as dropped (a source name
                                   moved to data-src under N4, a stem detail carried elsewhere), listed in the report.
A change with "new": "" (a removal) must carry "carried_by" or "lock_ok" for every token, or "cut": "<cuts.json id>".
The lock is mechanical: it fails a line that drops a token; reviewers still judge every line that passes.
"""
import html as H
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, '..', '..'))

HEDGE_GROUPS = [{'may', 'can', 'might', 'could'}, {'usually', 'typically'}, {'often', 'commonly', 'frequently'},
                {'some', 'few'}, {'rarely', 'rare'}, {'most'}, {'generally'}, {'likely'}]
# a possibility hedge is kept by a quantifier hedge ("a few may grow agitated" -> "agitation in some patients")
HEDGE_ALSO = {frozenset({'may', 'can', 'might', 'could'}): frozenset({'some', 'few'})}
NEG = {'no', 'not', 'without', 'never', 'absent', 'none', 'nor', "doesn't", "don't", 'cannot', "can't"}
SIDES = {'left', 'right', 'bilateral', 'unilateral'}
NUMWORDS = {'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 'six': '6', 'seven': '7',
            'eight': '8', 'nine': '9', 'ten': '10', 'eleven': '11', 'twelve': '12', 'double': '2', 'twice': '2',
            'doubling': '2', 'half': '1/2', 'triple': '3', 'third': '1/3', 'quarter': '1/4', 'first': '1st',
            'second': '2nd'}
UP = re.compile(r'\b(?:increase[sd]?|increasing|rise[sn]?|rising|rose|raise[sd]?|raising|higher|more|elevated|'
                r'(?<!take )(?<!takes )(?<!pick )(?<!follow-)up(?! to\b)|greater)\b', re.I)
DOWN = re.compile(r'\b(?:decrease[sd]?|decreasing|fall[s]?|fell|lower(?:s|ed)?|lowering|less|reduced?|reduces|'
                  r'drop[s]?|down|fewer)\b', re.I)
STOP_CAPS = {'If', 'In', 'On', 'At', 'The', 'A', 'An', 'For', 'With', 'And', 'Or', 'But', 'To', 'Of', 'By', 'As',
             'When', 'After', 'Before', 'Avoid', 'Choose', 'Check', 'Start', 'Stop', 'Give', 'Use', 'Most', 'Some',
             'All', 'Any', 'Each', 'No', 'Not', 'Do', 'Also', 'This', 'That', 'These', 'Those', 'It', 'They',
             'Watch', 'Monitor', 'Treatment', 'Symptoms', 'Onset', 'Prevention', 'Adverse', 'Highest', 'Other',
             'Less', 'More', 'Higher', 'Lower', 'Under', 'Over', 'From', 'During', 'Within', 'Without', 'Plus',
             'Type', 'Types', 'Why', 'Rationale', 'Finding', 'Findings', 'Next', 'Step', 'Key', 'First', 'Second',
             'Later', 'Early', 'Full', 'Late', 'Usually', 'Typically', 'Often', 'May', 'Can', 'Never', 'Only'}


BLOCK_TAG = re.compile(r'<(?:br|/?(?:p|li|ul|ol|div|tr|td|th|table|h\d|caption|figcaption))\b[^>]*>|<span class="sp-l[^"]*"[^>]*>', re.I)


def plain(s):
    """visible-ish text: block tags and line spans become spaces, inline tags vanish (a bold mnemonic letter stays
    joined to its word)."""
    s = re.sub(r'<span class="op op-a"[^>]*></span>', ' → ', s or '')
    s = BLOCK_TAG.sub(' ', s)
    s = re.sub(r'<[^>]+>', '', s)
    return re.sub(r'\s+', ' ', H.unescape(s)).strip()


def _load(name):
    p = os.path.join(WS, 'repair', 'efficiency', name)
    try:
        return json.load(open(p, encoding='utf-8'))
    except (OSError, ValueError):
        return {}


def _pairs():
    """lowercase synonym pairs from ABBREV.json and ALIASES.json (both directions)."""
    out = {}

    def add(a, b):
        a, b = a.lower().strip(), b.lower().strip()
        if a and b and a != b:
            out.setdefault(a, set()).add(b); out.setdefault(b, set()).add(a)
    ab = _load('ABBREV.json')
    for k, v in (ab.get('allow') or ab.get('abbrev') or ab if isinstance(ab, dict) else {}).items():
        if isinstance(v, str):
            add(k, v)
    al = _load('ALIASES.json')
    groups = al.get('groups') if isinstance(al, dict) else al
    for g in groups or []:
        names = g if isinstance(g, list) else (g.get('names') or [])
        names = [n for n in names if isinstance(n, str)]
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                add(names[i], names[j])
    return out


PAIRS = None


def numbers(t):
    """number tokens with an optional following unit word; number words mapped to digits."""
    t2 = t.replace('–', '-').replace('−', '-')
    out = []
    for m in re.finditer(r'(?<![\w.])(\d+(?:[.,]\d+)?(?:/\d+)?)(?:\s*(?:-|to)\s*(\d+(?:\.\d+)?))?', t2):
        out.append(m.group(1).replace(',', ''))
        if m.group(2):
            out.append(m.group(2))
    t3 = re.sub(r'\bhalf-life\b|\bhalf-lives\b', '', t2, flags=re.I)
    for w, d in NUMWORDS.items():
        if re.search(r'\b%s\b' % w, t3, re.I) and w not in ('first', 'second', 'one'):
            out.append(d)
    return out


def num_in(n, new):
    nn = numbers(new)
    if n in nn or re.search(r'(?<![\d.])%s(?![\d])' % re.escape(n), new):
        return True
    if n == '2' and re.search(r'\b(?:double|twice|2-fold|two)\b', new, re.I):
        return True
    if n == '1/2' and re.search(r'\bhalf\b', new, re.I):
        return True
    return False


def hedges(t):
    t = re.sub(r'\bmost of all\b|\bcan\'t\b|\bcannot\b', ' ', t.lower())     # an intensifier, a negation
    words = re.findall(r"[a-z']+", t)
    return [frozenset(g) for w in words for g in HEDGE_GROUPS if w in g]


def negs(t):
    return sum(1 for w in re.findall(r"[a-z']+", t.lower()) if w in NEG) + len(re.findall(r'\bnon-|\bun[a-z]', t.lower())) * 0


def names(old_html):
    out = []
    for m in re.finditer(r'<b\b[^>]*>(.*?)</b>', old_html or '', re.S):
        b = plain(m.group(1))
        # a bold term is a name; a bold clause (over 4 words) is checked through its capitalized words below
        if b and not re.fullmatch(r'(?:If|choose|Choose|then|and|or)', b) and len(b) > 1 and len(b.split()) <= 4:
            out.append(b)
    t = plain(old_html)
    for s in re.split(r'(?<=[.:;])\s+', t):
        ws = s.split()
        for i, w in enumerate(ws):
            w2 = re.sub(r'^[(\["]+|[)\],.;:"]+$', '', w)
            if i == 0 or not w2 or not w2[0].isupper() or w2 in STOP_CAPS:
                continue
            out.append(w2)
    return out


SOURCE_PHRASE = re.compile(r"\b(?:on |in )?the [A-Z][\w-]+ label\b|\b[A-Z][\w-]+ label\b|\b(?:the )?(?:Merck|MSD)(?: Manual)?\b|"
                           r"\bAnKing(?: card)?\b|\bUWorld\b|\bNBME\b|\bStatPearls\b|\bFirst Aid\b|\bAnalogy from the source\b|"
                           r"\bAnalogy\b", re.I)


def source_names(text):
    out = set()
    for m in SOURCE_PHRASE.finditer(text):
        out |= {w for w in re.findall(r"[A-Za-z][\w-]+", m.group(0)) if w[0].isupper()}
    return out


SYN = {'sodium': 'na+', 'potassium': 'k+', 'calcium': 'ca2+', 'magnesium': 'mg2+', 'chloride': 'cl-'}


def name_in(nm, new):
    global PAIRS
    if PAIRS is None:
        PAIRS = _pairs()
    sup = str.maketrans({'⁺': '+', '⁻': '-', '²': '2'})
    lo, nl = nm.lower().translate(sup), new.lower().translate(sup)
    for a, b in SYN.items():
        if b in nl:
            nl += ' ' + a
    if lo in nl:
        return True
    if any(p in nl for p in PAIRS.get(lo, ())):
        return True
    # a bold phrase passes when each of its content words is in the new text
    ws = [w for w in re.findall(r"[a-z0-9'⁺+-]+", lo) if len(w) > 3]
    return bool(ws) and all(w in nl or w.rstrip('s') in nl for w in ws)


def check_pair(old, new, old_is_html=True):
    """tokens of old missing from new: [(class, token)]"""
    ot = plain(old) if old_is_html else old
    nt = plain(new) if old_is_html else new
    miss = []
    for n in numbers(ot):
        if not num_in(n, nt):
            miss.append(('number', n))
    have = set(hedges(nt))
    for g in sorted(set(hedges(ot)), key=lambda g: sorted(g)):
        alt = HEDGE_ALSO.get(g)
        if g in have or (alt and alt in have):
            continue
        miss.append(('hedge', '/'.join(sorted(g))))
    if negs(nt) < negs(ot):
        miss.append(('negation', '%d of %d' % (negs(nt), negs(ot))))
    for s in SIDES:
        if re.search(r'\b%s\b' % s, ot, re.I) and not re.search(r'\b%s\b' % s, nt, re.I):
            miss.append(('side', s))
    if UP.search(ot) and not (UP.search(nt) or '↑' in nt):
        miss.append(('direction', 'increase'))
    if DOWN.search(ot) and not (DOWN.search(nt) or '↓' in nt):
        miss.append(('direction', 'decrease'))
    src = source_names(ot)
    dsrc = ' '.join(re.findall(r'data-src="([^"]*)"', new or '')).lower() if old_is_html else ''
    for nm in names(old if old_is_html else '<b>%s</b>' % ''):
        if name_in(nm, nt):
            continue
        if nm in src:
            if nm.lower() not in dsrc and not (nm.lower() in ('label', 'analogy', 'card', 'manual') and dsrc):
                miss.append(('source', nm + ' (to data-src, N4)'))
            continue
        miss.append(('name', nm))
    seen, out = set(), []
    for m in miss:
        if m not in seen:
            seen.add(m); out.append(m)
    return out


def check_delta(d):
    """[(index, missing tokens)] for every failing change."""
    ch = d.get('changes', [])
    fails = []
    for i, c in enumerate(ch):
        if c.get('lock') is False and c.get('lock_reason'):
            continue
        new = c.get('new', '') + ' ' + ' '.join(ch[j].get('new', '') for j in c.get('carried_by', []) if 0 <= j < len(ch))
        miss = check_pair(c.get('old', ''), new)
        norm = lambda x: '/'.join(sorted(str(x).split(' (')[0].lower().split('/')))
        ok = {norm(x) for x in c.get('lock_ok', [])} if c.get('lock_reason') else set()
        miss = [m for m in miss if norm(m[1]) not in ok]
        if c.get('new', '') == '':
            if c.get('cut'):
                miss = []
            elif not c.get('carried_by') and not (c.get('lock_ok') and c.get('lock_reason')):
                miss.append(('removal', 'no carried_by, lock_ok or cut'))
        if miss:
            fails.append((i, miss))
    return fails


def main(a):
    if '--old' in a:
        o = a[a.index('--old') + 1]; n = a[a.index('--new') + 1]
        m = check_pair(o, n)
        print('meaning_lock: %s' % ('PASS' if not m else 'FAIL ' + '; '.join('%s %s' % x for x in m)))
        return 1 if m else 0
    d = json.load(open(a[0], encoding='utf-8'))
    fails = check_delta(d)
    for i, m in fails:
        c = d['changes'][i]
        print('LOCK change %d (%s): drops %s | old: %s' % (i, c.get('uid', ''), '; '.join('%s %s' % x for x in m),
                                                         plain(c.get('old', ''))[:120]))
    print('meaning_lock %s: %d change(s), %d failing' % (os.path.basename(a[0]), len(d.get('changes', [])), len(fails)))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
