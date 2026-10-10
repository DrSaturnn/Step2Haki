"""numbers: the same fact given different numbers in different places (PHASE0_SCRIPTS item 4).

  python3 tools/spine/numbers.py [page.html] [--brief <id>] [--all] [--show N]

Reads every brief (body and practice bank separately) and records each time or percent value (minutes to years,
normalized to days, or %) with the one term it belongs to: the nearest term before it in the same clause (within 10
words; | ; and · end a clause), else one just after it, else the row's first cell. Terms come from the page itself:
brief titles, first cells of table rows, bold phrases, and "Long name (ACRONYM)" pairs (an upper-case ACRONYM maps to
the name); number phrases and generic words are not terms.
A NEAR MISS is reported when two places give the same term and unit values that overlap but differ (PSGN "1 to 3
weeks" against "2 to 4 weeks"; SCFE bilateral "18 to 50%" against "20 to 40%"): the typical copy that was updated in
one place only. Values that do not overlap (C3 back to normal by 6 to 8 weeks) are different facts and are not
reported. A range that contains the other (1 to 3 against "up to 6") is reported only with --all, except inside one brief, where
a body number that its own bank narrows or widens is reported too (SCFE bilateral 18 to 50% against 20 to 40%).

--brief limits the report to pairs that involve that brief (verify.py uses this) and exits 1 when any remain.
Accepted pairs go in tools/spine/numbers_allow.txt, one per line: term | brief | brief (order free), with a reason
after a #.
"""
import collections
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.dirname(HERE))
import pagelib as P  # noqa: E402

UNIT = {'minute': 1 / 1440, 'hour': 1 / 24, 'day': 1, 'week': 7, 'month': 30.4, 'year': 365}
NUM = r'(\d+(?:\.\d+)?)'
VAL = re.compile(r'(?<![\d.])' + NUM + r'(?:\s*(?:to|-|–|or)\s*' + NUM + r')?\s*(%|percent\b|(?:minute|hour|day|week|month|year)s?\b)', re.I)
BLOCK = re.compile(r'</?(?:p|li|div|tr|td|th|caption|h[1-6]|br|ul|ol|table|section|summary)\b[^>]*>', re.I)
STOP = set('the a an of in on at to for with and or by as is are be from after before within within up about usually '
           'often most more less than over under may can its their this that these those it not no new first'.split())
UNITW = {'minute', 'hour', 'day', 'week', 'month', 'year', 'percent', 'dose', 'time', 'onset', 'duration', 'age'}
GENERIC = set('patient patients child children adult adults treatment therapy management diagnosis symptoms symptom sign '
              'signs test tests risk risks follow up next step steps first line second line choice choose answer why '
              'when what how which who most likely typical classic key point points note clue clues finding findings '
              'start stop dose recheck repeat return daily weekly monthly yearly acute chronic mild moderate severe '
              'common rare better worse resolves resolve resolved infection infections attacks attack starting started stopping high low normal abnormal positive negative recurrence relapse response'.split())


def words(s):
    return re.findall(r'[a-z0-9]+', s.lower())


def vocabulary(html, briefs):
    terms, acr = set(), {}
    for b in briefs:
        if b.title:
            terms.add(' '.join(words(b.title)))
        for c in re.findall(r'<tr>\s*<td\b[^>]*>(.*?)</td>', b.inner, re.S):
            t = P.text(c)
            if 3 <= len(t) <= 60:
                terms.add(' '.join(words(t)))
        for c in re.findall(r'<b(?:\s[^>]*)?>(.*?)</b>', b.inner, re.S):
            t = P.text(c)
            if 4 <= len(t) <= 60 and len(t.split()) <= 6:
                terms.add(' '.join(words(t)))
        for long, short in re.findall(r'([A-Za-z][A-Za-z -]{6,60}?)\s*\(([A-Z][A-Za-z0-9]{1,7})\)', P.text(b.inner)):
            lw = words(long)
            pick = None
            for k in range(1, min(6, len(lw)) + 1):     # the acronym's letters pick how many trailing words name it
                cand = lw[-k:]
                if ''.join(w[0] for w in cand) == short.lower()[:len(cand)] or k == len(short):
                    pick = cand
                    break
            if pick is None:                            # PSGN: Poststreptococcal glomerulonephritis (letters inside words)
                for k in range(2, min(4, len(lw)) + 1):
                    if lw[-k][0] == short[0].lower() and lw[-k] not in STOP:
                        pick = lw[-k:]
                        break
            if pick:
                acr.setdefault(short.lower(), ' '.join(pick))
    def ok(t):
        ws = t.split()
        if not ws or any(any(ch.isdigit() for ch in w) or w.rstrip('s') in UNITW for w in ws):
            return False                     # a number phrase ("1 to 2 weeks") is a value, not a subject
        if not [w for w in ws if w not in STOP and w not in GENERIC]:
            return False
        return not (len(ws) == 1 and len(t) < 6 and t not in acr.values())
    cand = set(terms) | set(acr.values())
    for t in list(cand):                     # "Poststreptococcal glomerulonephritis (PSGN)" is the long name
        ws = t.split()
        if len(ws) > 1 and ws[-1] in acr:
            cand.discard(t)
            cand.add(' '.join(ws[:-1]))
    keep = {t for t in cand if ok(t)}
    acr = {a: l for a, l in acr.items() if ok(l)}
    return keep, acr


def chunks(inner):
    """(scope, text, subject) per sentence or table row; scope is 'body' or 'bank'; subject is a row's first cell"""
    m = re.search(r'<h5\b[^>]*class="[^"]*authored-hdr', inner)
    parts = [('body', inner[:m.start()] if m else inner), ('bank', inner[m.start():] if m else '')]
    out = []
    for scope, h in parts:
        for tr in re.findall(r'<tr\b[^>]*>(.*?)</tr>', h, re.S):
            cells = [P.text(c) for c in re.findall(r'<t[dh]\b[^>]*>(.*?)</t[dh]>', tr, re.S)]
            if len(cells) > 1:
                out.append((scope, ' | '.join(cells), cells[0]))
        h = re.sub(r'<tr\b[^>]*>.*?</tr>', ' ', h, flags=re.S)
        for block in BLOCK.split(h):
            t = P.text(block)
            for s in re.split(r'(?<=[.])\s+|\s+→\s+', t):
                if s.strip():
                    out.append((scope, s.strip(), ''))
    return out


SOFT = ('', -1, -1, ';')                 # a semicolon: the clause goes on, at a cost of 3 words


def tokens(text):
    """[(word, start, end)] plus clause breaks as None"""
    out = []
    for m in re.finditer(r'[A-Za-z0-9]+|[|;·]', text):
        out.append(None if m.group(0) in '|·' else SOFT if m.group(0) == ';' else (m.group(0).lower(), m.start(), m.end(), m.group(0)))
    return out


def find_terms(text, vocab, acr, maxn=6):
    """[(term, word index)] with clause breaks counted as positions, so distance stops at them"""
    tk = tokens(text)
    found = []
    i = 0
    while i < len(tk):
        if tk[i] is None or tk[i] is SOFT:
            i += 1
            continue
        hit = None
        for n in range(maxn, 0, -1):
            seg = tk[i:i + n]
            if len(seg) < n or any(x is None or x is SOFT for x in seg):
                continue
            g = ' '.join(x[0] for x in seg)
            if g in vocab:
                hit = (g, n)
                break
            if n == 1 and g in acr and seg[0][3].isupper() and len(seg[0][3]) > 1:   # PSGN, not the word 'or'
                hit = (acr[g], 1)
        if hit:
            found.append((hit[0], i, i + hit[1] - 1, tk[i][1]))
            i += hit[1]
        else:
            i += 1
    return found, tk


def owner(terms, tk, pos, window=10):
    """the term a value at character pos belongs to: the nearest term before it in the same clause (within window
    words), else the nearest after it within 4 words; None when no term is that close"""
    vi = next((k for k, x in enumerate(tk) if x is not None and x is not SOFT and x[1] >= pos), len(tk))
    best = None
    for t, a, z, _ in terms:
        if z < vi:
            span = tk[z + 1:vi]
            d = len(span) + 2 * sum(1 for x in span if x is SOFT)
            if any(x is None for x in span) or d > window:
                continue
        else:
            span = tk[vi:a]
            if any(x is None or x is SOFT for x in span) or len(span) > 4:
                continue
            d = len(span) + 0.5
        if best is None or d < best[0]:
            best = (d, t)
    return best[1] if best else None


def values(text):
    out = []
    for m in VAL.finditer(text):
        a, b, u = float(m.group(1)), float(m.group(2)) if m.group(2) else None, m.group(3).lower().rstrip('s')
        if u in ('%', 'percent'):
            kind, k = '%', 1
        else:
            kind, k = 'time', UNIT[u]
        lo, hi = a * k, (b if b is not None else a) * k
        if re.search(r'up to (?:about )?$', text[max(0, m.start() - 16):m.start()].lower()):
            lo = 0
        out.append((kind, lo, hi, m.group(0), m.start()))
    return out


def relation(x, y):
    """'same' | 'near' (overlap, differ) | 'contains' | 'apart'"""
    (lo1, hi1), (lo2, hi2) = x, y
    tol = 0.12 * max(hi1, hi2, 1e-9)
    if abs(lo1 - lo2) <= tol and abs(hi1 - hi2) <= tol:
        return 'same'
    if min(hi1, hi2) - max(lo1, lo2) <= tol:     # no overlap, or only a shared end ("up to 6" and "6 to 8")
        return 'apart'
    if (lo1 <= lo2 and hi2 <= hi1) or (lo2 <= lo1 and hi1 <= hi2):
        return 'contains'
    return 'near'


def load_allow():
    p = os.path.join(HERE, 'numbers_allow.txt')
    allow = set()
    if os.path.exists(p):
        for line in open(p, encoding='utf-8'):
            line = line.split('#')[0].strip()
            if line.count('|') == 2:
                t, a, b = [x.strip() for x in line.split('|')]
                allow.add((t, frozenset((a, b))))
    return allow


def main(argv):
    page = argv[0] if argv and not argv[0].startswith('--') else os.path.join(WS, 'index.html')
    only = argv[argv.index('--brief') + 1] if '--brief' in argv else None
    show_all = '--all' in argv
    show = int(argv[argv.index('--show') + 1]) if '--show' in argv else 40
    html = P.read_page(page)
    briefs = P.briefs(html)
    vocab, acr = vocabulary(html, briefs)
    rec = collections.defaultdict(list)          # (term, kind) -> [(place, lo, hi, raw, sentence)]
    for b in briefs:
        for scope, s, subj in chunks(b.inner):
            vals = values(s)
            if not vals:
                continue
            terms, tk = find_terms(s, vocab, acr)
            row = [t for t, *_ in find_terms(subj, vocab, acr)[0]] if subj else []
            for kind, lo, hi, raw, pos in vals:
                t = owner(terms, tk, pos)
                # the row's subject only when nothing in the cell is closer; with neither, the brief itself, so a
                # body number can still meet its own bank (SCFE bilateral "18 to 50%" against "20 to 40%")
                for x in ([t] if t else row[:1] or ['@' + b.id]):
                    rec[(x, kind)].append(('%s/%s' % (b.id, scope), lo, hi, raw, s))
    allow = load_allow()
    flags = []
    for (t, kind), rs in rec.items():
        places = collections.defaultdict(list)
        for r in rs:
            places[r[0]].append(r)
        names = sorted(places)
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                A, B = places[names[i]], places[names[j]]
                ba, bb = names[i].split('/')[0], names[j].split('/')[0]
                if only and only not in (ba, bb):
                    continue
                if (t, frozenset((ba, bb))) in allow:
                    continue
                for ra in A:
                    rels = [(relation((ra[1], ra[2]), (rb[1], rb[2])), rb) for rb in B]
                    if any(r == 'same' for r, _ in rels):
                        continue
                    for r, rb in rels:
                        if r == 'near' or (r == 'contains' and (show_all or ba == bb)):   # one brief: body against its bank
                            if not any(r2 == 'same' for r2 in [relation((rb[1], rb[2]), (x[1], x[2])) for x in A]):
                                flags.append((r, t, names[i], ra, names[j], rb))
    seen, out = set(), []
    for f in flags:
        key = (f[1], f[2], f[3][3], f[4], f[5][3])
        if key not in seen:
            seen.add(key)
            out.append(f)
    out.sort(key=lambda f: (f[0] != 'near', f[1]))
    print('numbers: %d terms with values, %d near misses%s%s' % (
        len(rec), sum(1 for f in out if f[0] == 'near' or f[2].split('/')[0] == f[4].split('/')[0]), (', %d containments' % sum(1 for f in out if f[0] == 'contains')) if show_all else '',
        (' involving %s' % only) if only else ''))
    for r, t, pa, ra, pb, rb in out[:show]:
        print('  %s  "%s": %s says "%s"; %s says "%s"' % (r.upper(), t, pa, ra[3], pb, rb[3]))
        print('      %s | %s' % (ra[4][:110], rb[4][:110]))
    return 1 if (only and any(f[0] == 'near' or f[2].split('/')[0] == f[4].split('/')[0] for f in out)) else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
