"""content_rules.py: source-and-scope rules shared by every brief type.

One definition, used by tools/gate.py (every brief on the page: Type C, legacy, Part II, Aquifer)
and by tools/migrate_check.py (one brief). Rules: tools/MIGRATION_CONTRACT.md, "Every brief type".

  G1  no placeholder or note-to-self on the page ("study gap", "TBD", "trigger unknown", ...)
  G2  no hedged failure trigger ("if no improvement", "if no response") without a time or a number
  G3  every management-ladder row has an "Escalate when" cell; the last rung may say "Top rung"
  K3  every mnemonic names the widely taught source it comes from, with a locator a reviewer can open (data-mn-src); never invented

Each check returns a list of (code, key, message). Keys are stable so the gate allowlist can
baseline pre-existing briefs; a fixed brief makes its allowlist line stale, and the gate says so.
"""
import html as H
import re

PLACEHOLDER = re.compile(
    r'\bstudy gap\b|\btrigger unknown\b|\btbd\b|\btodo\b|\bplaceholder\b|\bcitation needed\b|'
    r'\bto be (?:determined|added|confirmed|verified)\b|\bxxx\b|\blorem\b|\?\?|\[\s*\?\s*\]', re.I)
# A failure-of-therapy trigger with no time or number is a hedge (board-brief Rule 8). Dosing phrases such as
# "as needed" (PRN) are not triggers, and a named failure ("if the enema fails") is a trigger, so neither is matched.
HEDGE = re.compile(r'\b(?:if|when|until) (?:there is )?(?:no (?:improvement|response)|not (?:improving|better|responding))\b', re.I)
TIMEBOUND = re.compile(r'\d|\b(?:hours?|days?|weeks?|months?|dose|doses|trial of)\b', re.I)

# Resources that teach mnemonics to medical students and clinicians. A URL to a teaching source also counts.
MN_SOURCES = ('first aid', 'anking', 'amboss', 'uworld', 'nbme', 'boards and beyond', 'boards & beyond', 'sketchy',
              'pixorize', 'pathoma', 'onlinemeded', 'online meded', 'step-up', 'step up to', 'case files', 'medbullets',
              'bootcamp', 'lecturio', 'osmosis', 'source explanation')
# The attribution must be checkable: a URL, or a card/page Jonathan pasted or keeps in the local sources.
CHECKABLE = re.compile(r'https?://|\bpasted\b|\blocal:|repair/sources/|source explanation', re.I)
MN_BAD = re.compile(r'\b(authored|invented|original|made up|claude|ai-generated|none|unknown|n/?a)\b', re.I)


def _text(fragment):
    return re.sub(r'\s+', ' ', H.unescape(re.sub(r'<[^>]+>', ' ', fragment or ''))).strip()


def _learner_html(inner):
    """Learner-facing part of a brief: drop comments and the hidden outside-the-brief notes."""
    s = re.sub(r'<!--.*?-->', '', inner, flags=re.S)
    return re.sub(r'<div class="(?:meta|outside)[^"]*"[^>]*>.*?</div>', '', s, flags=re.S)


def placeholders(bid, inner):
    out = []
    t = _text(_learner_html(inner))
    for m in PLACEHOLDER.finditer(t):
        out.append(('G1', '%s:%s' % (bid, m.group(0).lower().replace(' ', '_')),
                    '%s shows a placeholder "%s" (...%s...)' % (bid, m.group(0), t[max(0, m.start() - 40):m.end() + 20])))
    return out


def hedges(bid, inner):
    out = []
    t = _text(_learner_html(inner))
    for m in HEDGE.finditer(t):
        tail = t[m.end():m.end() + 50]
        tail = re.split(r'[.;·]', tail)[0]
        head = t[max(0, m.start() - 30):m.start()]
        if TIMEBOUND.search(tail) or TIMEBOUND.search(re.split(r'[.;·]', head)[-1]):
            continue
        out.append(('G2', '%s:%s' % (bid, m.group(0).lower().replace(' ', '_')),
                    '%s has a hedged trigger "%s" with no time or number (...%s...)' % (bid, m.group(0), t[max(0, m.start() - 40):m.end() + 30])))
    return out


def ladder_cells(bid, inner):
    out = []
    for tn, tm in enumerate(re.finditer(r'<table\b[^>]*>(.*?)</table>', inner, re.S)):
        heads = [_text(x).lower() for x in re.findall(r'<th\b[^>]*>(.*?)</th>', tm.group(1), re.S)]
        if not heads or heads[0] != 'tier' or 'escalate when' not in heads:
            continue
        col = heads.index('escalate when')
        body = re.search(r'<tbody\b[^>]*>(.*?)</tbody>', tm.group(1), re.S)
        rows = re.findall(r'<tr\b[^>]*>(.*?)</tr>', body.group(1) if body else tm.group(1), re.S)
        for rn, tr in enumerate(rows):
            cells = re.findall(r'<td\b[^>]*>(.*?)</td>', tr, re.S)
            if not cells:
                continue
            cell = _text(cells[col]) if col < len(cells) else ''
            if not cell or cell in ('-', '–', '—', 'n/a', 'none'):
                out.append(('G3', '%s:ladder%d:row%d' % (bid, tn + 1, rn + 1),
                            '%s ladder row %d ("%s") has no "Escalate when" trigger: write the sourced trigger, or "Top rung" '
                            'on the last row when the exam goes no further' % (bid, rn + 1, _text(cells[0])[:30])))
            elif cell.lower().startswith('top rung') and rn != len(rows) - 1:
                out.append(('G3', '%s:ladder%d:row%d:top' % (bid, tn + 1, rn + 1),
                            '%s ladder row %d says "Top rung" but is not the last row' % (bid, rn + 1)))
    return out


def mnemonic_blocks(inner):
    """Every mnemonic on a brief: highlighted lists (ul.plain with bold initials) and pearls labeled Mnemonic.
    Returns (label, open_tag) pairs."""
    out = []
    for mm in re.finditer(r'(?:<h5[^>]*>((?:(?!</?h5).)*)</h5>\s*)?(<ul class="plain(?: mnem)?"[^>]*>)(.*?)</ul>', inner, re.S):
        lis = re.findall(r'<li[^>]*>(.*?)</li>', mm.group(3), re.S)
        heads = [re.match(r'\s*<b(?: class="mn")?>([^<]{1,12})</b>', li) for li in lis]
        if lis and sum(1 for h in heads if h) >= max(2, len(lis) * 0.7):
            out.append((_text(mm.group(1) or '') or ''.join(h.group(1) for h in heads if h), mm.group(2)))
    for m in re.finditer(r'(<div class="[^"]*"[^>]*>)\s*<span class="lbl">\s*(Mnemonics?\b[^<]*)</span>', inner):
        out.append((_text(m.group(2)), m.group(1)))
    return out


def mnemonic_sources(bid, inner):
    out = []
    for label, tag in mnemonic_blocks(inner):
        src = (re.search(r'data-mn-src="([^"]*)"', tag) or [None, ''])[1].strip()
        key = '%s:%s' % (bid, re.sub(r'[^a-z0-9]+', '_', label.lower())[:40])
        if not src:
            out.append(('K3', key, '%s mnemonic "%s" does not name its source: add data-mn-src naming the widely taught '
                        'resource it comes from (First Aid, AnKing, AMBOSS, the source explanation, or a URL); '
                        'a mnemonic with no such source is removed, never invented' % (bid, label)))
        elif MN_BAD.search(src) or not (re.search(r'https?://', src) or any(s in src.lower() for s in MN_SOURCES)):
            out.append(('K3', key, '%s mnemonic "%s": data-mn-src="%s" is not a widely taught resource or a URL' % (bid, label, src)))
        elif not CHECKABLE.search(src):
            # R12 review: "First Aid Step 1" was named from memory and no reviewer could confirm it.
            out.append(('K3', key, '%s mnemonic "%s": data-mn-src="%s" names a resource but gives nothing a reviewer can open: add a URL '
                        'to a page that teaches it, or "pasted:" / "local:" for a card or page Jonathan supplied' % (bid, label, src)))
    return out


def check_brief(bid, inner):
    return placeholders(bid, inner) + hedges(bid, inner) + ladder_cells(bid, inner) + mnemonic_sources(bid, inner)
