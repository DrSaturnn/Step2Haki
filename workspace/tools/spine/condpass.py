#!/usr/bin/env python3
"""Conditional PASS (Jonathan 2026-10-12, DECISIONS_DIGEST; claude/pending/POST_SHIP_R3.md section 2).

A reviewer with only LOW findings may write "Verdict: PASS-IF" and a Replacements block of exact text edits:

    Replacements:
    1. old: {{the exact text as it reads now}}
       new: {{the exact replacement text}}

verify.py counts such a receipt as PASS when the brief now differs from what the reviewer judged only by some of the
approved replacements. It replays them backwards (new text to old text) on every file the receipt depends on and
checks the hashes on the receipt's deps line.

Rules (enforced here):
  - text only: no markup and no study-mode masks, so neither old nor new may hold <, > or &;
  - no changed numbers; at most 8 replacements per receipt; at most 40 words of new text each;
  - a replacement the receipt itself approved always counts for it; one approved by another part counts only if it is
    wording-only: the same numbers, negations, hedge words (may, usually, often, can, rarely, about, consider),
    order and condition words (first, then, before, after, only, if, unless, except, until and the like) and
    diagnosis, drug and test names (repair/efficiency/ALIASES.json and ABBREV.json). Otherwise that part needs the
    normal follow-up review.
  - s148 fix 8 (Jonathan 2026-10-18): a replacement from another part whose only meaning change is ADDED hedge words
    still counts as wording-only when every added hedge word appears in a quote that the claim map cites for the line
    the replacement lands in (claim_map.json source_says, facts.json quote). Removing a hedge, or changing a number,
    a negation, an order or condition word or a name, still needs the normal follow-up review.
Item stems, keys, distractors and lead-ins are protected by verify's item check (a meaning change without a version bump
fails), so a replacement that lands there cannot make a brief READY.
"""
import html as H
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, '..', '..'))
MAX_N, MAX_WORDS = 8, 40
HEDGES = ('may', 'usually', 'often', 'can', 'rarely', 'about', 'consider', 'likely', 'typically')  # s148: + likely, typically
NEGATIONS = ('no', 'not', 'without', 'never', 'none', 'neither', 'nor', 'cannot')
# order and condition words carry meaning too (s133 replacement 6 dropped "first"; 7 added an "unless" exception)
QUALIFIERS = ('first', 'second', 'then', 'before', 'after', 'initial', 'initially', 'last', 'only',
              'if', 'unless', 'except', 'until')
NUM = re.compile(r'\d+(?:[.,]\d+)?')
REASON = re.compile(r'^\s*(key|d1|d2)\s*:\s*', re.I)   # s149: item-reason labels in receipts


def parse(txt):
    """the receipt's verdict ('PASS', 'PASS-IF', 'FAIL' or None) and its replacements [(n, old, new)]"""
    v = re.search(r'Verdict:\s*(PASS-IF|PASS|FAIL)', txt)
    reps = []
    blk = re.search(r'^Replacements:\s*$(.*?)(?=^\S[^\n]*:\s*$|\Z)', txt, re.M | re.S)
    if blk:
        for m in re.finditer(r'(\d+)\.\s*old:\s*\{\{(.*?)\}\}\s*new:\s*\{\{(.*?)\}\}', blk.group(1), re.S):
            reps.append((int(m.group(1)), m.group(2), m.group(3)))
        if not reps:  # s138: a receipt that drops the {{ }}: one line each, old and new on consecutive lines
            for m in re.finditer(r'^\s*(\d+)\.\s*old:[ \t]*(\S[^\n]*?)[ \t]*\n[ \t]*new:[ \t]*(\S[^\n]*?)[ \t]*$',
                                 blk.group(1), re.M):
                reps.append((int(m.group(1)), m.group(2), m.group(3)))
    return (v.group(1) if v else None), reps


def words(t):
    return re.findall(r"[A-Za-z]+(?:'[a-z]+)?", t.lower())


def stem_hedge(w):
    """hedge words are meaning: 'considered' counts as 'consider', 'usually' as itself"""
    for hdg in HEDGES:
        if w == hdg or (hdg == 'consider' and w.startswith('consider')) or (hdg == 'can' and w == "can't"):
            return hdg
    return None


def names():
    out = set()
    try:
        for e in json.load(open(os.path.join(WS, 'repair', 'efficiency', 'ALIASES.json'), encoding='utf-8'))['entries']:
            out |= {e['name']} | set(e['aliases'])
    except (OSError, ValueError, KeyError):
        pass
    try:
        ab = json.load(open(os.path.join(WS, 'repair', 'efficiency', 'ABBREV.json'), encoding='utf-8'))
        out |= set(ab.get('labs_imaging', {})) | set(ab.get('labs_imaging', {}).values())
    except (OSError, ValueError):
        pass
    return out


def names_in(t, table):
    low = t.lower()
    return sorted(n for n in table if re.search(r'(?<![A-Za-z])%s(?![A-Za-z])' % re.escape(n.lower()), low))


def hard_problems(old, new):
    """why a replacement may not be used at all (empty list when it may)"""
    bad = []
    if re.search(r'[<>&]', old + new):
        bad.append('markup or entity (text only, never markup or masks)')
    if sorted(NUM.findall(old)) != sorted(NUM.findall(new)):
        bad.append('a number changed')
    if len(new.split()) > MAX_WORDS:
        bad.append('new text over %d words' % MAX_WORDS)
    if not old.strip() or old == new:
        bad.append('empty or unchanged')
    return bad


def _same_but_hedges(old, new, table):
    """numbers, negations, order and condition words and names unchanged (hedges not compared)"""
    wo, wn = words(old), words(new)
    if sorted(NUM.findall(old)) != sorted(NUM.findall(new)):
        return False
    if sorted(w for w in wo if w in NEGATIONS or w.endswith("n't")) != sorted(w for w in wn if w in NEGATIONS or w.endswith("n't")):
        return False
    if sorted(w for w in wo if w in QUALIFIERS) != sorted(w for w in wn if w in QUALIFIERS):
        return False
    return names_in(old, table) == names_in(new, table)


def added_hedges(old, new):
    """the hedge words new adds over old (a multiset difference), or None when new drops any hedge old had"""
    from collections import Counter
    ho, hn = Counter(filter(None, map(stem_hedge, words(old)))), Counter(filter(None, map(stem_hedge, words(new))))
    if ho - hn:
        return None
    return sorted((hn - ho).elements())


def wording_only(old, new, table=None, quotes=None):
    """True when the replacement keeps numbers, negations, hedges and names: it may count for every part.
    quotes (s148 fix 8): the quotes the claim map cites for the line the replacement lands in; a replacement that only
    ADDS hedge words is wording-only when every added hedge word appears in one of them."""
    table = names() if table is None else table
    if not _same_but_hedges(old, new, table):
        return False
    add = added_hedges(old, new)
    if add is None:
        return False
    if not add:
        return True
    qw = set(filter(None, map(stem_hedge, words(' '.join(quotes or [])))))
    return all(h in qw for h in add)


def claim_quotes(folder):
    """a function text -> the quotes cited for every claim whose text holds it (claim_map.json new_text; its sources'
    source_says and the facts.json quote of each source id)"""
    try:
        cm = json.load(open(os.path.join(folder, 'claim_map.json'), encoding='utf-8'))
    except (OSError, ValueError):
        return lambda t: []
    try:
        fx = {f['id']: f.get('quote', '') for f in json.load(open(os.path.join(folder, 'facts.json'), encoding='utf-8'))['facts']}
    except (OSError, ValueError, KeyError, TypeError):
        fx = {}
    claims = []
    for c in cm.get('claims', []) if isinstance(cm, dict) else cm:
        text = c.get('new_text') or c.get('text') or ''
        qs = []
        for s in c.get('sources') or []:
            if isinstance(s, dict):
                qs += [s.get('source_says') or '', fx.get(s.get('id'), '')]
        qs += [fx.get(i, '') for i in c.get('derived_from') or [] if isinstance(i, str)]
        claims.append((H.unescape(text), [q for q in qs if q]))

    def find(t):
        t = H.unescape(t)
        return [q for text, qs in claims if t and t in text for q in qs]
    return find


def forms(t, kind):
    """how a learner-text string appears in each dependency file"""
    from html.entities import codepoint2name
    named = ''.join('&%s;' % codepoint2name[ord(c)] if ord(c) > 127 and ord(c) in codepoint2name else c for c in t)
    out = [t, H.escape(t, quote=False), named]
    if kind == 'json':
        out = [json.dumps(x, ensure_ascii=False)[1:-1] for x in out] + out
    seen, res = set(), []
    for x in out:
        if x not in seen:
            seen.add(x)
            res.append(x)
    return res


def undo(text, reps, kind):
    """replay the replacements backwards on one file's text. Returns (text, applied ids, problem or None).
    A replacement whose new text is absent was not applied; one whose new text occurs more than once is ambiguous."""
    applied = []
    for n, old, new in reps:
        hit = None
        pairs = list(zip(forms(new, kind), forms(old, kind)))
        m_new, m_old = REASON.match(new), REASON.match(old)
        if m_new and m_old and m_new.group(1).lower() == m_old.group(1).lower():
            # s149: an item reason quoted as "d1: ..." lives in data-d1-why without its label; quote-escaped there
            bn, bo = new[m_new.end():], old[m_old.end():]
            pairs += list(zip(forms(bn, kind), forms(bo, kind)))
            pairs += [(H.escape(bn, quote=True), H.escape(bo, quote=True))]
        for fo_new, fo_old in pairs:
            c = text.count(fo_new)
            if c > 1:
                return text, applied, 'replacement %s is ambiguous (its new text occurs %d times)' % (n, c)
            if c == 1:
                hit = (fo_new, fo_old)
                break
        if hit:
            text = text.replace(hit[0], hit[1], 1)
            applied.append(n)
    return text, applied, None


def pool(receipts, table=None, quotes=None):
    """receipts: {part: (verdict, reps)}. For each part, the replacements that may count for it:
    its own (passing the hard rules), plus other parts' that pass the hard rules and are wording-only.
    quotes: text -> cited quotes (claim_quotes); looked up by the replacement's new text, then its old text."""
    table = names() if table is None else table
    q = quotes or (lambda t: [])
    ok = {p: [(n, o, w) for n, o, w in reps[:MAX_N] if not hard_problems(o, w)]
          for p, (v, reps) in receipts.items() if v == 'PASS-IF'}
    out = {}
    for part in receipts:
        mine = [(('%s.%d' % (part, n)), o, w) for n, o, w in ok.get(part, [])]
        other = [(('%s.%d' % (p, n)), o, w) for p, lst in ok.items() if p != part for n, o, w in lst
                 if wording_only(o, w, table, q(w) or q(o))]
        seen, res = set(), []
        for rid, o, w in mine + other:          # the same edit approved by two parts is one replacement
            if (o, w) not in seen:
                seen.add((o, w))
                res.append((rid, o, w))
        out[part] = res
    return out
