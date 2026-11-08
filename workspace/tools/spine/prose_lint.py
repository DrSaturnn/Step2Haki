#!/usr/bin/env python3
"""prose_lint.py (2026-11-06): prose register checks for the Step2Haki page (concise review-book register: First Aid,
AnKing, Pocket Medicine). Ported from the s164 audit prototype (v2 tuned patterns and region classifier) plus the
rhetorical patterns of the writing rules (contrast, branch, intensifier, reveal colon, trailing explainer).

Each brief is parsed from pagelib's Brief.inner, so lazy briefs wrapped in <template class="axl"> are linted too.
Practice items (ol.bank, div.nbq, div.vignette) are excluded. REPORT_ONLY patterns are printed in the totals but never
counted toward a brief's number, the baseline or --touched: header_wh_template, and the word caps header_long,
title_long and meta_words (headers and titles have no word cap, TEXTBOOK_STYLE rule 6, D-20261107-2).

Ratchet design: the current page has prose debt. The baseline file records each brief's hit count; a build fails
when any brief rises above its number or a brief missing from the baseline has hits. --tighten lowers numbers to the
current counts and never raises one. --touched holds every brief whose text changed since BASE_PAGE to zero hits;
a markup or attribute change leaves the text equal and is not a touch.

Usage:
  python3 prose_lint.py PAGE.html                        # per-pattern totals and the top 10 briefs
  python3 prose_lint.py PAGE.html --brief ID             # that brief's hits with their text
  python3 prose_lint.py PAGE.html --baseline B.json      # exit 1 if any brief rose above its baseline count
  python3 prose_lint.py PAGE.html --write-baseline B.json
  python3 prose_lint.py PAGE.html --tighten B.json       # rewrite B with min(baseline, current); drop gone briefs
  python3 prose_lint.py PAGE.html --touched BASE.html    # exit 1 if a brief whose text changed has any hit

Public API: lint_brief(inner_html) -> [{'pattern', 'region', 'text', 'match', 'tag'}]; page_counts(page_html) ->
{brief_id: hit_count}; text_key(inner_html) -> the brief's whole text, hover bodies included; changed_briefs(ref_html,
page_html) -> the briefs whose text_key differs from REF (new briefs included).
"""
import collections
import json
import os
import re
import sys

from bs4 import BeautifulSoup, NavigableString, Tag

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pagelib import briefs, read_page  # noqa: E402

FIX_LINE = 'rewrite per repair/efficiency/TEXTBOOK_STYLE.md'
REPORT_ONLY = {'header_wh_template', 'header_long', 'title_long', 'meta_words'}

# --------------------------------------------------------------------------------------------------------------------
# 1. Text extraction
# --------------------------------------------------------------------------------------------------------------------
SKIP_TAGS = {'script', 'style', 'svg', 'button', 'noscript', 'template'}
BLOCK_TAGS = {'div', 'p', 'ol', 'ul', 'li', 'br', 'tr', 'table', 'figure', 'h4', 'h5', 'small'}
# classed inline spans/bs that the page lays out as separate lines or cells
SEP_CLASSES = {'sl', 'si', 'ss', 'sd', 'pp-a', 'win', 'nm', 'when', 'sp-src', 'sp-cw', 'sp-nm', 'lbl', 'k', 'f', 'w',
               'trapwhy', 'pill', 'sk', 'sv', 'ld', 't', 'w5ol', 'tag', 'w5z', 'w5om'}
SEP_PARENTS = {'wl', 'wr2', 'sp-when', 'w5skip', 'wh'}


def _cls(el):
    return el.get('class') or []


def vis(el):
    """Visible text of el: no buttons (hover triggers), hover bodies, aria-hidden chart furniture, svg, section
    numbers. Block boundaries and classed cells become spaces."""
    out = []

    def walk(n):
        for c in n.children:
            if isinstance(c, NavigableString):
                if type(c).__name__ in ('Comment', 'Doctype'):
                    continue
                out.append(str(c))
            elif isinstance(c, Tag):
                cl = _cls(c)
                if (c.name in SKIP_TAGS and 'sp-a' not in cl) or 'sp-pop-b' in cl or 'sp-vl' in cl or 'sp-k' in cl \
                        or c.get('aria-hidden') == 'true' \
                        or 'sp-n' in cl or 'subq' in cl or 'alias' in cl or 'cap-sub' in cl:
                    continue
                if 'op' in cl:               # cause-and-effect arrow glyph
                    out.append(' -> ')
                    continue
                sep = c.name in BLOCK_TAGS or bool(SEP_CLASSES & set(cl)) or (
                    c.name in ('b', 'span') and c.parent is not None and bool(SEP_PARENTS & set(_cls(c.parent))))
                if sep:
                    out.append(' ')
                walk(c)
                if sep:
                    out.append(' ')
    walk(el)
    return re.sub(r'\s+', ' ', ''.join(out)).strip()


# --------------------------------------------------------------------------------------------------------------------
# 2. Region discovery
# --------------------------------------------------------------------------------------------------------------------
def _anc(el, pred):
    for p in el.parents:
        if isinstance(p, Tag) and pred(p):
            return True
    return False


def is_practice_container(t):
    cl = _cls(t)
    return (t.name == 'ol' and 'bank' in cl) or (t.name == 'div' and ('nbq' in cl or 'vignette' in cl))


def is_chrome(t):
    cl = _cls(t)
    return t.name == 'nav' or 'sp-chips' in cl or 'rail' in cl or 'rax' in cl or 'navsub' in cl


def is_mnemonic(t):
    """A mnemonic container: ul.mnem rows (class token mn or mnem*) or any element carrying data-mn-src."""
    return t.has_attr('data-mn-src') or any(c == 'mn' or c.startswith('mnem') for c in _cls(t))


def classify(el):
    """(region, tag) for a leaf-level text region, or None."""
    n = el.name
    cl = _cls(el)
    if n in ('h4', 'h5', 'caption', 'figcaption', 'th', 'summary'):
        return 'header', n
    if n == 'span' and 'lbl' in cl:
        return 'header', 'span.lbl'
    if n == 'p' and 'kick' in cl:
        return 'header', 'p.kick'
    if 'w5z' in cl and n in ('p', 'span'):
        return 'header', n + '.w5z'
    for tok in ('pill', 'sk', 'sp-src'):
        if n == 'span' and tok in cl:
            return 'header', 'span.' + tok
    for tok in ('pc-grp', 'wg'):
        if n == 'p' and tok in cl:
            return 'header', 'p.' + tok
    if n == 'span' and el.parent is not None and 'ttl' in _cls(el.parent):
        return 'header', 'div.ttl>span'
    if n == 'b' and 'pp-t' in cl:
        return 'header', 'b.pp-t'
    if n == 'td':
        return 'cell', 'td'
    if n == 'p' and 'sp-commit' in cl:
        return 'commit', 'p.sp-commit'
    if n in ('li', 'p') and el.find_parent('div', class_='dp') is not None:
        return 'keypoint', 'div.dp ' + n
    if _anc(el, lambda t: t.name == 'figure' and 'lcw' in _cls(t)):
        if 'nm' in cl and n == 'b':
            return 'timeline', 'figure.lcw b.nm'
        if 'win' in cl:
            return 'timeline', 'figure.lcw span.win'
        if n == 'p' and 'wl' in cl:
            return 'timeline', 'figure.lcw p.wl'
        if n == 'p' and 'rk' in cl:
            return None
    if n == 'li' and el.parent is not None and 'sp-trk' in _cls(el.parent):
        return 'timeline', 'figure.sp-course li'
    if n == 'em' and 'fl' in cl:
        return 'timeline', 'em.fl'
    if _anc(el, lambda t: t.name == 'div' and 'sp-pause' in _cls(t)):
        if n == 'p':
            return 'pause', 'sp-pause p'
        if n == 'span' and any(c in cl for c in ('sl', 'si', 'pp-a')) and not el.find_parent('span', class_=['si', 'pp-a', 'sl']):
            return 'pause', 'sp-pause span.' + [c for c in cl if c in ('sl', 'si', 'pp-a')][0]
    notes = ('pc-note', 'sp-note', 'system-note', 'pp-x', 'w5skip', 'pt-tx', 'sub')
    if n == 'p' and any(c in cl for c in notes):
        return 'note', 'p.' + [c for c in cl if c in notes][0]
    if n == 'span' and 'sp-note' in cl:
        return 'note', 'span.sp-note'
    if n == 'span' and 'trapwhy' in cl:
        return 'note', 'span.trapwhy'
    if n == 'div' and any(c in cl for c in ('rule', 'danger', 'crit', 'pearls')):
        return 'note', 'div.' + [c for c in cl if c in ('rule', 'danger', 'crit', 'pearls')][0]
    if n == 'b' and 'sp-f' in cl:
        return 'finding', 'b.sp-f'
    for tok in ('wr2', 'tn', 'sp-when'):
        if n == 'p' and tok in cl:
            return 'finding', 'p.' + tok
    if n == 'p' and el.parent is not None and 'sv' in _cls(el.parent):
        return 'finding', 'div.sv p'
    if n == 'div' and 'sv' in cl and not el.find('p'):
        return 'finding', 'div.sv'
    if n == 'span' and el.parent is not None and el.parent.parent is not None and 'sp-sysr' in _cls(el.parent.parent) \
            and any(c in cl for c in ('f', 'w')):
        return 'finding', 'sp-sysr span.' + [c for c in cl if c in ('f', 'w')][0]
    if n == 'div' and any(c in cl for c in ('w5c', 'w5m')):
        return 'finding', 'div.' + [c for c in cl if c in ('w5c', 'w5m')][0]
    if n == 'span' and 't' in cl and el.parent is not None and 'w5fd' in _cls(el.parent):
        return 'finding', 'w5fd span.t'
    if n == 'span' and 'w5om' in cl:
        return 'finding', 'span.w5om'
    if n == 'li' and any(c in cl for c in ('wr', 'cr', 'pt', 'wgb', 'tr')):
        return None
    if n in ('p', 'li'):
        return 'other', n
    if n == 'span' and 'when' in cl:
        return 'other', 'span.when'
    return None


SINGLE_LETTER_B = re.compile(r'<b\b[^>]*>\s*[A-Z]\s*</b>')


def mnemonic_fragments(el):
    """Visible text of each ' · ' fragment of el that spells a mnemonic inline (3+ single-letter bold capitals,
    eg 'WATER: <b>W</b>iskott-Aldrich, <b>T</b>hrombocytopenia ...')."""
    out = []
    for frag in re.split(r'&middot;|·|&#183;', str(el)):
        if len(SINGLE_LETTER_B.findall(frag)) >= 3:
            t = vis(BeautifulSoup(frag, 'lxml'))
            if t:
                out.append(t)
    return out


# --------------------------------------------------------------------------------------------------------------------
# 3. Patterns (v2 tuned set from the s164 audit, then the rhetorical set)
# --------------------------------------------------------------------------------------------------------------------
WORD = r"[A-Za-z][A-Za-z'’-]*"
SENT_SPLIT = re.compile(r'(?<=[.!?])\s+(?=[A-Z0-9"“(])')
ABBR = re.compile(r'\b(?:e\.g|i\.e|vs|Dr|approx|Fig|No|St|cf|eg|ie|ca|etc)\.$')
DOT_SPLIT = re.compile(r'\s+·\s+')


def sentences(text):
    merged = []
    for p in SENT_SPLIT.split(text):
        if merged and ABBR.search(merged[-1]):
            merged[-1] += ' ' + p
        else:
            merged.append(p)
    return merged


def nwords(t):
    return len([w for w in re.split(r'\s+', t) if re.search(r'[A-Za-z0-9]', w)])


SRC_NAMES = r"AnKing|UWorld|NBME|Amboss|AMBOSS|First Aid|Pocket Medicine|UpToDate|Merck Manual|MSD Manual|Merck|MSD"
SOURCE = [
    ('label', re.compile(r"\bon the [A-Z][\w-]+ label\b|(?<!avoid )(?<!the term )\b(?:the|The) (?:[A-Z][\w-]+ |FDA |drug )?label\b|\b[A-Z][a-z]+ label (?:also|lists|says|warns|states|gives|reports|dose)\b|\bper (?:the )?label\b|\b\w+ labels (?:warn|list|say|give|state|report)\b")),
    ('board', re.compile(r"\b[Tt]he board (?:teaches|tests|keys|answer|wants|expects|asks|favou?rs)\b|\bas the board teaches\b|\bboard (?:answer|teaching)\b|\bStep 2 answer\b", re.I)),
    ('per', re.compile(r"\bper (?:the )?(?:AnKing|UWorld|NBME|Merck|MSD|UpToDate|First Aid)\b|\bAnKing (?:says|teaches|lists|cards?)\b|\b(?:UWorld|NBME) (?:says|teaches|answer|explanation|keys?)\b|\baccording to (?:the )?(?:" + SRC_NAMES + r")\b", re.I)),
    ('manual', re.compile(r"\b(?:the )?(?:Merck|MSD)(?: Sharp and Dohme)?(?: \(Merck Sharp and Dohme\))? Manual\b\s*(?:also |re-?|orders|lists|gives|says|puts|recommends|states|advises|and|\()|\b(?:the )?(?:Merck|MSD) Manual (?:and the CDC )?(?:also |re-?)?\w+s\b")),
]
APPOS_EXCL_PREV = set('''is are was were be been being also not that which often usually sometimes never if when who and or
then later may can will must should only rarely commonly as it they have has had already all both each these those most
many some other any no than so but even still just once now very more less first last well get gets got stays stay
remain remains remained whenever whether while until after before since because though although unless'''.split())
APPOS = re.compile(r"\b(" + WORD + r") included\b(?=\s*(?:[,.;:)\]]|$|->|\s(?:and|or|but|as|at)\b))")
HEDGE = re.compile(r"\ba few (?:may|can|will|might)\b|\bmay grow\b|\bor one stopped\b|\bcomes only after\b", re.I)
META = re.compile(r"\bthe (?:question|stem|vignette)\b|\bthe answer turns\b|\banswer turns\b", re.I)
META_QUESTION_IDIOM = re.compile(r"\b(?:answers?|answered|avoids?|is|becomes|settles?|begs|raises?|poses?|changes|beyond|asks)\s+the question\b", re.I)
# two or more comma-separated article-led items in one run ("a tendon, or a nerve")
ARTICLE_LIST = re.compile(r"(?<![\w-])(?:[Aa]n?) [A-Za-z0-9][\w-]*(?: [a-z0-9][\w-]*){0,2}, (?:(?:an?) [a-z0-9][\w-]*(?: [a-z0-9][\w-]*){0,2}, )*(?:or |and )?(?:an?) [a-z][\w-]*")
# a bare-noun list of three or more items where one item carries an article ("a triptan, dextromethorphan,
# ondansetron or St John's wort"); the review-book list drops it
_ITEM = r"(?:(?:an?) )?[A-Za-z0-9][\w'’-]*(?: [A-Za-z0-9][\w'’-]*){0,2}"
# The list must fill its whole clause (start of line or after : ; ( · – ->, end at . ; : ) · – -> or end of line),
# so a list that trails a verb or a preposition ("requires examination findings, pressure signs, or a change") is
# prose, not a bare list.
ARTICLE_MIXED = re.compile(r"(?:^|(?<=[:;(\u00b7–—] )|(?<=[:;(])|(?<=-> ))" + _ITEM + r"(?:, " + _ITEM + r"){2,}"
                           r"(?:,? (?:or|and) " + _ITEM + r")?(?=\s*(?:[.;:)\u00b7–—]|->|$))")
# a run whose first item follows one of these words is an introductory phrase plus a clause, not a list
INTRO_PREP = {'as', 'with', 'without', 'in', 'for', 'on', 'after', 'before', 'from', 'by', 'at', 'to', 'of', 'into',
              'under', 'over', 'like', 'during', 'once'}
LIST_STOP = re.compile(r"\b(?:with|to|then|often|usually|on|in|for|from|at|by|as|such|than|the)\b", re.I)
# a verb within three words after the run means the last item opened a clause ("..., and an intervention is ranked")
ARTICLE_ITEM = re.compile(r"(?:^|, |(?:or|and) )(?:an?) ", re.I)
CLAUSE_WORD_IN_LIST = re.compile(r"\b(?:is|are|was|were|does|do|did|has|have|had|not|that|which|who|when|because|but|can|may|will|should)\b", re.I)
CLAUSE_VERBS = re.compile(r"\b(?:is|are|was|were|has|have|had|does|do|did|can|may|might|will|should|must|cannot|means?|shows?|causes?|brings?|carr(?:y|ies)|lasts?|suggests?|points?|explains?|fits?|reads?|gives?|needs?|requires?|makes?|leads?|stays?|remains?|rules?|allows?|works?|fails?|persists?|resolves?|produces?|reflects?|increases?|decreases?|raises?|lowers?|hurts?|relieves?|relieve|helps?|improves?|worsens?|falls?|rises?|occurs?|begins?|starts?|appears?|develops?|responds?|follows?|precedes?|predicts?|indicates?|supports?|excludes?|treats?|blocks?|crosses?|come|comes|goes|go|get|gets|become|becomes|sound|sounds|look|looks|feel|feels)\b|->", re.I)
PRON_SEMI = re.compile(r";\s+(?:it|they)\b", re.I)
PRON_ITAND = re.compile(r"(?:^|[;:(]\s*|,\s+|\b(?:and|but|while|so|because|if|when|whereas)\s+)(?:it|they) and [A-Za-z]+", re.I)
PRON_ITAND_NOT = re.compile(r"^(?:it|they) and (?:then|so|also|not|never|may|can|will|is|are|was|were|the|a|an|my|his|her|their|to)\b", re.I)
PRON_START = re.compile(r"^(?:It|They)\s")

# rhetorical set (writing rule 1), matched on visible prose regions only
CONTRAST = re.compile(
    r",\s+not (?!only\b|just\b)(?:(?:an?|the) )?[\w'’-]+(?: [\w'’-]+){0,3}(?=\s*(?:[.;:)!?]|$|->|·))"
    r"|\bnot (?:just|only) |\brather than\b|\binstead of\b|\bit isn['’]t\b|\bisn['’]t [^,.;]{1,40}, it['’]s\b", re.I)
# "otherwise" only as a branch (after , ; or opening a sentence); adjectival "otherwise normal" and "until proven
# otherwise" are not branches. "if not" only bare ("laparotomy if not;"), since "if not immune" is a clinical condition.
BRANCH = re.compile(r"(?:^|(?<=[,;] )|(?<=[.!?] ))[Oo]therwise\b|\b[Ii]f not\b(?=\s*(?:[,;.:)?]|$|->))")
INTENSIFIER = re.compile(r"\b(?:even|really|truly|actually|most of all|above all|crucially|importantly)\b", re.I)
REVEAL = re.compile(r"(?:^|(?<=[.!?]\s)|(?<=·\s)|(?<=->\s))(?:The (?:key|catch|pattern|trap|tell)|Bottom line):")
TRAILING = re.compile(r", making it\b|, meaning ")
RHETORIC = [('contrast', CONTRAST), ('branch', BRANCH), ('intensifier', INTENSIFIER), ('reveal_colon', REVEAL),
            ('trailing_explainer', TRAILING)]

# Permitted near misses. Each phrase is masked before the rhetorical patterns run, so a hit can never come from it.
ALLOW = [
    (r"\bunless (?:contraindicated|allergic)\b", 'standard clinical condition ("unless" is not in any pattern)'),
    (r"\b(?:the|an?) only\b", '"only" stating exclusivity ("only" is not in the intensifier set)'),
    (r"\bso that\b", 'purpose clause that carries information'),
    (r"^In practice:|(?<=[.!?]\s)In practice:", 'section label; a source named in that line still hits source_narration'),
    (r"\bno [a-z][\w-]*", 'negative finding stated as a fact ("no seizures")'),
    (r"\bwhether or not\b", 'fixed phrase, not a contrast'),
    (r"^(?:[\w'’ -]{1,30}, ){2,}not [\w'’-]+(?: [\w'’-]+)?(?:, [\w'’ -]{1,30})*$", 'negative finding as one item of a '
                                                                                'findings list ("weak, areflexic, alert, not dysmorphic")'),
    (r"\botherwise (?:an? )?(?:normal|healthy|well|intact|unremarkable|functioning|classic|ordinary|asymptomatic|uncomplicated)\b",
     'adverbial "otherwise" (in other respects), not a branch'),
    (r",\s+not (?:required|needed|necessary|both|pregnant|on purpose)\b", 'negated criterion stated as a fact '
                                                                         '("depression common, not required")'),
    (r"\bnot otherwise specified\b", 'fixed diagnostic phrase (NOS), not a contrast or branch'),
    (r"\beven(?=-)|\beven (?:if|though|when|as|with)\b", 'even-numbered, even if, even though, even as, even with: '
                                                          'arithmetic or a concession'),
    (r"\babove all (?:two|three|four|five|\d+|of)\b", 'quantity ("above all three"), not an intensifier'),
]
ALLOW_RX = [re.compile(p, re.I if not p.startswith('^In') else 0) for p, _ in ALLOW]
PROSE_REGIONS = {'keypoint', 'finding', 'note', 'commit', 'cell', 'timeline', 'pause', 'hover', 'other'}


def mask_allowed(text):
    for rx in ALLOW_RX:
        text = rx.sub(lambda m: '_' * len(m.group(0)), text)
    return text


def header_checks(text, tag):
    hits = []
    t = text.strip()
    if not t:
        return hits
    if re.search(r", by ", t):
        hits.append(('header_comma_by', ', by '))
    if re.match(r"From the\b", t):
        hits.append(('header_from_the', 'From the'))
    m = re.match(r"(What|How|Where|When)\b", t)
    if m:
        tmpl = tag == 'span.sk' or (tag == 'th' and len(t.split()) == 1)
        hits.append(('header_wh_template' if tmpl else 'header_wh_word', m.group(1)))
    wc = len([w for w in re.split(r'[\s/]+', t) if re.search(r'[A-Za-z0-9]', w)])
    if tag == 'h4':
        if wc > 4:
            hits.append(('title_long', '%d words' % wc))
    elif tag != 'p.pc-grp' and wc > 4:       # '01 Antidepressants - class card' is a catalogue tag, not a heading
        hits.append(('header_long', '%d words' % wc))
    return hits


def _article_lists(text):
    out, spans = [], []
    for m in ARTICLE_LIST.finditer(text):
        g = m.group(0)
        after = ' '.join(text[m.end():].split()[:3])
        before = text[:m.start()].split()[-1:]
        if CLAUSE_WORD_IN_LIST.search(g) or CLAUSE_VERBS.search(after):
            continue
        if before and before[0].lower() in INTRO_PREP:
            continue                  # "As a rule, a pregnancy test", "without an emergency, a capable refusal"
        if g.count(',') == 1 and ', or ' in g:
            continue                  # two mutually exclusive alternatives keep "or" ("a LABA, or a medium-dose ICS")
        out.append(g)
        spans.append(m.span())
    for m in ARTICLE_MIXED.finditer(text):
        g = m.group(0)
        if CLAUSE_WORD_IN_LIST.search(g) or LIST_STOP.search(g) or not ARTICLE_ITEM.search(g):
            continue
        if any(a < m.end() and m.start() < b for a, b in spans):
            continue
        out.append(g)
    return out


def text_checks(text, region, tag='', mnemonic=False, mn_frags=()):
    """Pattern checks for one prose line. Returns [(pattern, match)]."""
    hits = []
    for m in PRON_SEMI.finditer(text):
        hits.append(('pronoun_subject', text[max(0, m.start() - 20):m.end() + 15]))
    for m in PRON_ITAND.finditer(text):
        g = m.group(0)
        core = re.sub(r"^.*?\b((?:it|they) and .*)$", r"\1", g, flags=re.I)
        if PRON_ITAND_NOT.match(core) or g.strip().startswith(';') or PRON_SEMI.search(g):
            continue
        hits.append(('pronoun_subject', g))
    if region in PROSE_REGIONS:
        for s in sentences(text):
            if PRON_START.match(s):
                hits.append(('pronoun_subject', s[:40]))
    for _, rx in SOURCE:
        for m in rx.finditer(text):
            hits.append(('source_narration', m.group(0)))
    for m in APPOS.finditer(text):
        if m.group(1).lower() not in APPOS_EXCL_PREV:
            hits.append(('appositive_included', text[max(0, m.start() - 15):m.end() + 12]))
    for m in HEDGE.finditer(text):
        hits.append(('hedged_narration', m.group(0)))
    if region in PROSE_REGIONS - {'hover'}:
        for g in _article_lists(text):
            hits.append(('article_list', g))
    if region in PROSE_REGIONS and not mnemonic:
        for s in [x for s0 in sentences(text) for x in DOT_SPLIT.split(s0)]:
            wc = nwords(s)
            if wc > 30 and not any(s in f for f in mn_frags):
                hits.append(('length_over_30', '%d words: %s...' % (wc, s[:50])))
    # counted per sentence and per ' · ' fragment (the page's row separator), so semicolons of separate entries in
    # one tile ("Pairs with" lists) are not summed; the fragment lists of div.pearls and div.crit use semicolons
    # between fragments of one item and are not counted at all
    if not (tag in ('div.pearls', 'div.crit') and '·' in text):
        for line in [x for s0 in sentences(text) for x in DOT_SPLIT.split(s0)]:
            if line.count(';') > 1:
                segs = line.split(';')
                if max(nwords(x) for x in segs) >= 9 and any(CLAUSE_VERBS.search(x) for x in segs):
                    hits.append(('multi_semicolon', '%d semicolons' % line.count(';')))
    for m in META.finditer(text):
        if m.group(0).lower() == 'the question' and META_QUESTION_IDIOM.search(text[max(0, m.start() - 14):m.end()]):
            continue                  # "answers the question", "is the question": clinical idiom, not the exam item
        hits.append(('meta_words', m.group(0)))
    if region in PROSE_REGIONS:
        masked = mask_allowed(text)
        for name, rx in RHETORIC:
            for m in rx.finditer(masked):
                hits.append((name, text[m.start():m.end()]))
    return hits



# --------------------------------------------------------------------------------------------------------------------
# 3b. s170: the header list as data (T3), hover lines (T4), source kickers (T5)
# --------------------------------------------------------------------------------------------------------------------
HEADERS_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                            'repair', 'efficiency', 'HEADERS.json')
STRUCT_TAGS = {'th', 'caption', 'figcaption', 'h5', 'span.lbl', 'span.sk', 'p.kick', 'p.w5z', 'span.w5z',
               'div.ttl>span', 'p.wg', 'summary', 'b.pp-t', 'p.wl>b'}
_HDR = None


def hnorm(t):
    return re.sub(r'\s+', ' ', (t or '').strip().lower())


def headers_data():
    global _HDR
    if _HDR is None:
        try:
            d = json.load(open(HEADERS_PATH, encoding='utf-8'))
        except (OSError, ValueError):
            d = {}
        _HDR = {'retired': {hnorm(x) for x in d.get('retired', [])},
                'patterns': [re.compile(p) for p in d.get('retired_patterns', [])],
                'ok': {hnorm(x) for x in d.get('allowed', []) + d.get('known', [])},
                'loaded': bool(d)}
    return _HDR


def retired_pattern(t, pats=None):
    pats = [re.compile(p) for p in pats] if pats is not None else headers_data()['patterns']
    return any(p.search(t or '') for p in pats)


def structural_headers(inner_html):
    """[(tag, text)] for the brief's structural headers: column heads, captions, step and tile labels, timeline titles
    and tags. Practice items and chrome excluded."""
    soup = BeautifulSoup(inner_html, 'lxml') if isinstance(inner_html, str) else inner_html
    out = []
    for el in (soup.body or soup).find_all(True):
        if is_practice_container(el) or _anc(el, is_practice_container) or 'sp-pop-b' in _cls(el) or \
                _anc(el, lambda t: 'sp-pop-b' in _cls(t)):
            continue
        if el.name == 'p' and 'wl' in _cls(el):
            lb = el.find('b')
            if lb is not None and lb.parent is el and el.contents and el.contents[0] is lb:
                out.append(('p.wl>b', vis(lb)))
            continue
        c = classify(el)
        if c is None or c[0] != 'header' or c[1] not in STRUCT_TAGS:
            continue
        el2 = el
        if c[1] in ('caption', 'figcaption') and el.find(['ol', 'ul', 'div', 'table', 'figure']):
            el2 = BeautifulSoup(str(el), 'lxml').find(c[1])
            for blk in el2.find_all(['ol', 'ul', 'div', 'table', 'figure']):
                blk.decompose()
        t = vis(el2)
        if t:
            out.append((c[1], t))
    return out


SRC_KICK = re.compile(r"^(?:Label|.*\blabel\b|AnKing|UWorld|NBME|Merck|MSD|StatPearls|First Aid|Pocket Medicine|"
                      r"UpToDate|Step 2 answer)", re.I)
ANCHOR_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                           'repair', 'efficiency', 'ANCHOR_ALLOW.json')
ANCHOR_STOP = set('a an the of and or to in on for with by at as is are be from that this its it into than then when if '
                  'not no after before over under per vs versus also only more most less first second why what which how'.split())
_ANCHOR = None


def anchor_allow():
    """keys 'trigger|title' judged to fit in the s170 anchor pass although they share no content word"""
    global _ANCHOR
    if _ANCHOR is None:
        try:
            _ANCHOR = set(json.load(open(ANCHOR_PATH, encoding='utf-8')).get('fits', []))
        except (OSError, ValueError):
            _ANCHOR = set()
    return _ANCHOR


def anchor_stems(t):
    return {w[:5] for w in re.findall(r'[a-z0-9][a-z0-9-]+', t.lower()) if w not in ANCHOR_STOP and len(w) > 2}


HOVER_LINE_MAX = 16          # TEXTBOOK_STYLE rule 6: hover line about 12 words; counted over 16


def hover_lines(copy):
    """the hover body's lines: span.sp-l elements when present, else its sentences."""
    ls = copy.find_all('span', class_='sp-l')
    if ls:
        return [re.sub(r'\s+', ' ', vis(x)).strip() for x in ls]
    return None


# --------------------------------------------------------------------------------------------------------------------
# 4. Brief and page API
# --------------------------------------------------------------------------------------------------------------------
def lint_brief(inner_html, report_only=False, touched=False):
    """Hits for one brief's inner HTML: [{'pattern', 'region', 'text', 'match', 'tag'}]. Practice items are excluded.
    report_only=True also returns the uncounted header_wh_template hits. touched=True (the brief's text changed: the
    prose-touched check and verify.py) adds header_new, a structural header in neither HEADERS.json allowed nor known."""
    soup = BeautifulSoup(inner_html, 'lxml')
    for t in soup(['style', 'script']):
        t.decompose()
    hits = []
    claimed = set()

    def emit(region, tag, text, pairs):
        for pat, m in pairs:
            if pat in REPORT_ONLY and not report_only:
                continue
            hits.append({'pattern': pat, 'region': region, 'text': text, 'match': m, 'tag': tag})

    def claim(el):
        claimed.add(id(el))
        for d in el.descendants:
            if isinstance(d, Tag):
                claimed.add(id(d))

    root = soup.body or soup
    for el in root.find_all(True):
        if id(el) in claimed:
            continue
        if is_practice_container(el) or is_chrome(el) or 'sp-pop-b' in _cls(el):
            claim(el)                 # practice items, navigation chrome and hover bodies (checked below)
            continue
        c = classify(el)
        if c is None:
            continue
        region, tag = c
        txt = vis(el)
        if tag == 'summary':
            txt = re.sub(r'\s+', ' ', ''.join(x for x in el.find_all(string=True) if x.parent.name != 'small')).strip()
        if tag in ('caption', 'figcaption') and el.find(['ol', 'ul', 'div', 'table', 'figure']):
            cp = BeautifulSoup(str(el), 'lxml').find(tag)
            for blk in cp.find_all(['ol', 'ul', 'div', 'table', 'figure']):
                blk.decompose()
            txt = vis(cp)             # the caption's own words; a timeline or chart nested in it is not the header
        if tag == 'figure.lcw p.wl':
            lb = el.find('b')
            if lb is not None and lb.parent is el:
                txt = txt[len(vis(lb)):].strip()
        if tag in ('figure.sp-course li', 'p.sp-when'):
            kids = [vis(k) for k in el.find_all(['b', 'span'], recursive=False)]
            txt = ': '.join(k for k in kids if k) or txt
        if not txt:
            claimed.add(id(el))
            continue
        lbl = None
        if region == 'note' and tag.startswith('div.'):
            lbl = el.find('span', class_='lbl')
            if lbl is not None:
                lt = vis(lbl)
                if txt.startswith(lt):
                    txt = txt[len(lt):].strip()
                if lt:                # the tile's own label is a header region
                    emit('header', 'span.lbl', lt, header_checks(lt, 'span.lbl') +
                         [(p, m) for p, m in text_checks(lt, 'header') if p in ('source_narration', 'meta_words', 'hedged_narration')])
        if region == 'header':
            pairs = header_checks(txt, tag) + [(p, m) for p, m in text_checks(txt, region)
                                               if p in ('source_narration', 'meta_words', 'hedged_narration')]
        else:
            mn = is_mnemonic(el) or _anc(el, is_mnemonic)
            frags = mnemonic_fragments(el) if tag in ('div.pearls', 'div.crit') else ()
            pairs = text_checks(txt, region, tag, mnemonic=mn, mn_frags=frags)
        emit(region, tag, txt, pairs)
        for sub in el.find_all(class_=['cap-sub', 'subq']):
            st = re.sub(r'\s+', ' ', sub.get_text()).strip()
            if st:
                stag = 'span.' + [c for c in _cls(sub) if c in ('cap-sub', 'subq')][0]
                emit('note', stag, st, text_checks(st, 'note', stag))
        claim(el)

    # hover cards: title is a header, body is prose
    pops = {e.get('id'): e for e in soup.select('span.sp-pop-b')}
    # s167c: a short hover shown as a visible line (span.sp-vl) is linted as the hover it was
    pairs = [(b, pops.get(b.get('aria-controls'))) for b in soup.select('button.sp-pop')] + \
            [(v, v) for v in soup.select('span.sp-vl')]
    for btn, body in pairs:
        if body is None or _anc(btn, is_practice_container) or 'nbd' in _cls(btn):
            continue
        ct = body.find('span', class_='sp-ct')
        htitle = vis(ct) if ct is not None else ''
        copy = BeautifulSoup(str(body), 'lxml').find('span', class_=body.get('class'))
        first = copy.find('span', class_='sp-ct')
        if first is not None:
            first.decompose()
        for k in copy.find_all('span', class_='sp-k'):   # s167c: the old trigger label, kept as the card's kicker
            kt = vis(k)
            if SRC_KICK.match(kt) and not _anc(btn, is_practice_container):
                emit('hover_title', 'span.sp-k', kt, [('source_kicker', kt)])    # s170 T5 (N4, C7)
            k.decompose()
        hl = hover_lines(copy)
        # s170 A1 (D-20261108-5): the trigger names what its card explains; a trigger sharing no content word with the
        # card's title, kicker or first line is counted unless the anchor pass judged it a fit (ANCHOR_ALLOW.json)
        if btn.name == 'button':
            trig = vis(btn)
            kick = ' '.join(vis(k) for k in body.find_all('span', class_='sp-k'))
            first_l = vis(hl[0]) if hl and not isinstance(hl[0], str) else (hl[0] if hl else vis(copy)[:160])
            if trig and not (anchor_stems(trig) & anchor_stems(htitle + ' ' + kick + ' ' + first_l)) and \
                    (trig + '|' + htitle) not in anchor_allow():
                emit('hover_title', 'button.sp-pop', trig, [('hover_anchor', '%s -> %s' % (trig[:40], htitle[:40]))])
        parts = []

        def walkb(n):
            for c in n.children:
                if isinstance(c, NavigableString):
                    parts.append(str(c))
                elif isinstance(c, Tag):
                    if c.name in SKIP_TAGS:
                        continue
                    if 'op' in _cls(c):
                        parts.append(' -> ')
                        continue
                    blk = c.name in BLOCK_TAGS or 'sp-why-l' in _cls(c) or 'sp-l' in _cls(c)
                    # a hover line (span.sp-l) ends its sentence: ' · ' is the line boundary DOT_SPLIT splits on, so
                    # the length check counts each line, not lines joined without a period (s170 pc-snri lane)
                    end = ' · ' if 'sp-l' in _cls(c) else ' '
                    if blk:
                        parts.append(' ')
                    walkb(c)
                    if blk:
                        parts.append(end)
        walkb(copy)
        btxt = re.sub(r'\s+', ' ', ''.join(parts)).strip()
        has_break = bool(copy.find(['br', 'div', 'p', 'ol', 'ul', 'li']) or copy.find(class_=['sp-why-l', 'sp-l']))
        if htitle:
            emit('hover_title', 'span.sp-ct', htitle, header_checks(htitle, 'span.sp-ct') +
                 [(p, m) for p, m in text_checks(htitle, 'header') if p in ('source_narration', 'meta_words')])
        emit('hover', 'span.sp-pop-b', btxt, text_checks(btxt, 'hover', 'span.sp-pop-b'))
        if nwords(btxt) > 30 and not has_break:
            emit('hover', 'span.sp-pop-b', btxt, [('hover_no_break_over_30', '%d words, no break' % nwords(btxt))])
        # s170 T4: one idea per hover line, about 12 words; a line over 16 words is counted (sentences when the body
        # has no span.sp-l lines)
        for ln in (hl if hl is not None else [x for s0 in sentences(btxt) for x in DOT_SPLIT.split(s0)]):
            if nwords(ln) > HOVER_LINE_MAX:
                emit('hover', 'span.sp-pop-b', btxt, [('hover_line_long', '%d words: %s...' % (nwords(ln), ln[:50]))])

    # s170 T3: structural headers against repair/efficiency/HEADERS.json
    hd = headers_data()
    if hd['loaded']:
        for tag, t in structural_headers(soup):
            n = hnorm(t)
            if n in hd['retired'] or retired_pattern(t):
                emit('header', tag, t, [('header_retired', t)])
            elif touched and n not in hd['ok']:
                emit('header', tag, t, [('header_new', t)])
    return hits


def text_key(inner_html):
    """The brief's whole text (hover bodies and labels included, markup and attributes ignored), whitespace collapsed."""
    soup = BeautifulSoup(inner_html, 'lxml')
    for t in soup(['style', 'script']):
        t.decompose()
    for t in soup.find_all(attrs={'aria-hidden': 'true'}):   # chart furniture (axis labels, arrows) is not text (s167c)
        t.decompose()
    t = re.sub(r'\s+', ' ', soup.get_text(' ')).strip()
    # tag boundaries add a space before closing punctuation and after an opening parenthesis (s167c anchors); not text
    return re.sub(r'\( ', '(', re.sub(r' ([;:,.!?)])', r'\1', t))


def changed_briefs(ref_html, page_html):
    """Briefs on page_html whose text differs from ref_html, plus briefs new since ref_html."""
    ref = {}
    for b in briefs(ref_html):
        ref[b.id] = ref.get(b.id, '') + text_key(b.inner)
    cur = collections.OrderedDict()
    for b in briefs(page_html):
        cur.setdefault(b.id, []).append(b)
    return [b for bid, bs in cur.items() if ref.get(bid) != ''.join(text_key(x.inner) for x in bs) for b in bs]


def page_counts(page_html):
    """{brief_id: counted hit total} for every brief on the page (zero included)."""
    out = {}
    for b in briefs(page_html):
        out[b.id] = out.get(b.id, 0) + len(lint_brief(b.inner))
    return out


# --------------------------------------------------------------------------------------------------------------------
# 5. CLI
# --------------------------------------------------------------------------------------------------------------------
def _arg(a, flag):
    i = a.index(flag)
    if i + 1 >= len(a):
        raise SystemExit('%s needs a value' % flag)
    return a[i + 1]


def _load_baseline(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def _save_baseline(path, counts):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(dict(sorted(counts.items())), f, indent=1)   # flat {brief_id: n}, the shape tools/gate.py reads
        f.write('\n')


def _print_hits(bid, hs):
    for h in hs:
        print('  %s %-22s %-10s %s | %s' % (bid, h['pattern'], h['region'], h['match'][:60], h['text'][:160]))


def main(a):
    if not a or a[0].startswith('-'):
        print(__doc__)
        return 2
    page = read_page(a[0])
    bl = briefs(page)

    if '--brief' in a:
        bid = _arg(a, '--brief')
        found = [b for b in bl if b.id == bid]
        if not found:
            print('PROSE-LINT: no brief %r on the page' % bid)
            return 2
        hs = [h for b in found for h in lint_brief(b.inner, report_only=True)]
        print('%s (%s): %d hits (%d report-only)' % (bid, found[0].title, sum(h['pattern'] not in REPORT_ONLY for h in hs),
                                                      sum(h['pattern'] in REPORT_ONLY for h in hs)))
        _print_hits(bid, hs)
        return 0

    if '--touched' in a:
        bad = 0
        for b in changed_briefs(read_page(_arg(a, '--touched')), page):
            hs = lint_brief(b.inner, touched=True)
            if hs:
                bad += 1
                print('PROSE-LINT touched brief %s has %d hits:' % (b.id, len(hs)))
                _print_hits(b.id, hs)
        if bad:
            print('PROSE-LINT FAIL: %d changed brief(s) with prose hits; %s' % (bad, FIX_LINE))
            return 1
        print('PROSE-LINT touched: clean')
        return 0

    counts = {}
    for b in bl:
        counts[b.id] = counts.get(b.id, 0) + len(lint_brief(b.inner))

    if '--write-baseline' in a:
        _save_baseline(_arg(a, '--write-baseline'), counts)
        print('PROSE-LINT baseline written: %d briefs, %d hits' % (len(counts), sum(counts.values())))
        return 0

    if '--tighten' in a:
        path = _arg(a, '--tighten')
        old = _load_baseline(path)
        new = {k: min(v, counts[k]) for k, v in old.items() if k in counts}
        lowered = {k: (old[k], new[k]) for k in new if new[k] < old[k]}
        dropped = sorted(k for k in old if k not in counts)
        _save_baseline(path, new)
        print('PROSE-LINT baseline tightened:', lowered if lowered else '(no change)',
              ('dropped %s' % dropped) if dropped else '')
        return 0

    if '--baseline' in a:
        base = _load_baseline(_arg(a, '--baseline'))
        worse = []
        for k, n in sorted(counts.items()):
            if k in base and n > base[k]:
                worse.append('%s: %d -> %d' % (k, base[k], n))
            elif k not in base and n > 0:
                worse.append('%s: new brief with %d hits' % (k, n))
        if worse:
            print('PROSE-LINT FAIL: prose hits rose above the baseline:')
            for w in worse:
                print('  ' + w)
            print('fix: %s; then run prose_lint.py PAGE --brief ID to list the hits' % FIX_LINE)
            return 1
        print('PROSE-LINT ok: %d hits, no brief above its baseline' % sum(counts.values()))
        return 0

    # report
    per = collections.Counter()
    report_only = collections.Counter()
    for b in bl:
        for h in lint_brief(b.inner, report_only=True):
            (report_only if h['pattern'] in REPORT_ONLY else per)[h['pattern']] += 1
    titles = {b.id: b.title for b in bl}
    print('PROSE-LINT %s: %d briefs, %d hits, %d briefs with zero hits' % (
        a[0], len(counts), sum(counts.values()), sum(1 for n in counts.values() if n == 0)))
    for p, n in per.most_common():
        print('  %-24s %d' % (p, n))
    for p, n in report_only.items():
        print('  %-24s %d (report-only, not counted)' % (p, n))
    print('top 10 briefs:')
    for k, n in sorted(counts.items(), key=lambda x: -x[1])[:10]:
        print('  %4d  %s  %s' % (n, k, titles.get(k, '')))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
