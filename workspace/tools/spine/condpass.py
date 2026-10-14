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
HEDGES = ('may', 'usually', 'often', 'can', 'rarely', 'about', 'consider')
NEGATIONS = ('no', 'not', 'without', 'never', 'none', 'neither', 'nor', 'cannot')
# order and condition words carry meaning too (s133 replacement 6 dropped "first"; 7 added an "unless" exception)
QUALIFIERS = ('first', 'second', 'then', 'before', 'after', 'initial', 'initially', 'last', 'only',
              'if', 'unless', 'except', 'until')
NUM = re.compile(r'\d+(?:[.,]\d+)?')


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


def wording_only(old, new, table=None):
    """True when the replacement keeps numbers, negations, hedges and names: it may count for every part"""
    table = names() if table is None else table
    wo, wn = words(old), words(new)
    if sorted(NUM.findall(old)) != sorted(NUM.findall(new)):
        return False
    if sorted(w for w in wo if w in NEGATIONS or w.endswith("n't")) != sorted(w for w in wn if w in NEGATIONS or w.endswith("n't")):
        return False
    if sorted(filter(None, map(stem_hedge, wo))) != sorted(filter(None, map(stem_hedge, wn))):
        return False
    if sorted(w for w in wo if w in QUALIFIERS) != sorted(w for w in wn if w in QUALIFIERS):
        return False
    return names_in(old, table) == names_in(new, table)


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
        for fo_new, fo_old in zip(forms(new, kind), forms(old, kind)):
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


def pool(receipts, table=None):
    """receipts: {part: (verdict, reps)}. For each part, the replacements that may count for it:
    its own (passing the hard rules), plus other parts' that pass the hard rules and are wording-only."""
    table = names() if table is None else table
    ok = {p: [(n, o, w) for n, o, w in reps[:MAX_N] if not hard_problems(o, w)]
          for p, (v, reps) in receipts.items() if v == 'PASS-IF'}
    out = {}
    for part in receipts:
        mine = [(('%s.%d' % (part, n)), o, w) for n, o, w in ok.get(part, [])]
        other = [(('%s.%d' % (p, n)), o, w) for p, lst in ok.items() if p != part for n, o, w in lst
                 if wording_only(o, w, table)]
        seen, res = set(), []
        for rid, o, w in mine + other:          # the same edit approved by two parts is one replacement
            if (o, w) not in seen:
                seen.add((o, w))
                res.append((rid, o, w))
        out[part] = res
    return out
