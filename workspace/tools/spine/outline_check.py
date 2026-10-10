"""outline_check: the architect's outline against the spine rules, before anything is built (PHASE0_SCRIPTS item 2).

  python3 tools/spine/outline_check.py <dir>/outline.json [--cards <cards.md>] [--page index.html] [--quiet]

Reads outline.json, the facts.json files it cites (and <dir>/facts.json), <dir>/cards_disposition.json and the
card checklist (default repair/migration/spine/packets/<brief>/cards.md). Prints one line per finding:
  ERROR <rule> <where>: <what> -> <fix>      blocks the brief (exit 1)
  FLAG  <rule> <where>: <what>               for the auditor, written to <dir>/outline_flags.txt (exit 0)

Rules
  S1 steps      eight steps with the fixed labels in order; the entry type's absent steps are null (drug: 5 and 6;
                4 optional); every listed step has its h block (same n and id) and no h block is unlisted
  S2 schema     every block and rich part renders; every cited id is in SRC; a drawer names a brief or alias on
                the page; a plain string holds markup only (learner words go in {"t", "ids"})
  C1 cap        words above the Practice header: disease 1,300, drug 1,000, presentation 700
  C2 counts     bottom line 1 to 3 lines; Insights exactly two lines
  D1 tempting   a differential table (last head "Decides it") gives "tempting": one reason per row (FLAG on goldens)
  D2 decides    a Decides-it cell does not open with an action verb (give, treat, order...): it names what decides
  D3 decides    no two Decides-it cells in one table say the same thing
  L1 G2         an escalation rung (2nd line, add, relapse, refer, top...) has a trigger with a time or a named failure
  L2 G3         a Top or Refer rung is the last rung
  N1 currency   a line with a number that cites no facts.json fact carries "currency": verified:<fact id> | stable |
                flagged (contract N1)
  P1 population a peds brief citing an adult-only fact (or cirrhosis), or an FM brief citing a child-only fact, must
                name that population in the line itself
  X1 combined   a line citing facts from two pages or sections (FLAG: the auditor confirms each source's conditions)
  U1 labels     a qualifier label ("atypical features") used 3 or more times is defined somewhere: followed by a colon,
                dash or parenthesis, a hover title or trigger, or listed in "defined"
  O1 old claims every old claim is carried, corrected, moved or dropped, with where or why (3 words or more)
  K1 cards      every card checklist item has a disposition (covered:, owner:<brief>, scope:, not-topic, conflict:<fact>);
                owner names a brief on the page, conflict a fact id; a covered card's anchor or statement shares at
                least half its key words with the brief text
"""
import html as H
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import pagelib as P  # noqa: E402
import outline_render as OR  # noqa: E402

LABELS = ['Script', 'Urgent', 'Differential', 'Workup', 'Criteria', 'Severity', 'Treatment', 'Follow-up']
CAPS = {'disease': 1300, 'drug': 1000, 'presentation': 700, 'screen': 1000}
ACTION = re.compile(r'^(?:(?:give|treat|start|order|obtain|get|admit|prescribe|refer|stop|switch|begin|perform|do|send|'
                    r'draw|add|use|consult|operate)\b|(?:film|image|scan|biopsy|repeat|check|x-ray)\s+(?:the|a|an|both|it|them|for)\b)', re.I)
ESCALATE = re.compile(r'(2nd|3rd|second|third|add|relapse|refer|top|escalat|last|salvage|rescue)', re.I)
TOPTAG = re.compile(r'^\s*(top|refer|last)', re.I)
TRIGGER = re.compile(r'\d+\s*(?:to\s*\d+\s*)?(?:hour|day|week|month|year)s?|\bdespite\b|\bpersist|\bno response|'
                     r'\bnot (?:improv|respond|better|controlled)|\bno remission|\bfail|\brefractor|\brelapse|\brecur|'
                     r'\bexacerbation|\bdependen|\bintoleran|\bworse|\bstill\b|\buncontrolled|\binadequate|'
                     r'\bcontraindicat|\bresistan', re.I)
QUALIFIERS = ('atypical typical complicated uncomplicated high-risk low-risk red-flag significant frequent infrequent '
              'classic partial complete early late primary secondary severe mild moderate unstable stable '
              'steroid-sensitive steroid-resistant steroid-dependent persistent transient isolated').split()
STOP = set('the a an of in on at to for with and or by as is are be from after before within up about it its this that '
           'these those not no than then into over under more most less can may will which who what when how why '
           'have has had their there thus also often usually during occurs occur present presents initial initially '
           'year years olds old common commonly seen associated typically resulting result results increased decreased '
           'applied impacts range rapid periods early onset photo credit commons wikimedia cureus via'.split())


def rx(s):
    return re.sub(r'\s+', ' ', H.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()


class Check:
    def __init__(self, path, page, cards):
        self.path, self.dir = path, os.path.dirname(os.path.abspath(path))
        self.o = json.load(open(path, encoding='utf-8'))
        self.page, self.cards_path = page, cards
        self.errors, self.flags = [], []
        self.facts = {}
        files = [os.path.join(self.dir, 'facts.json')] + [os.path.join(self.dir, p) if os.path.exists(os.path.join(self.dir, p))
                                                         else os.path.join(WS, p) for p in self.o.get('src', [])]
        for f in files:
            if os.path.exists(f):
                d = json.load(open(f, encoding='utf-8'))
                if isinstance(d, dict) and 'facts' in d:
                    for x in d['facts']:
                        self.facts[x['id']] = x
        self.golden = bool(self.o.get('golden'))

    def err(self, rule, where, what, fix):
        self.errors.append('ERROR %s %s: %s -> %s' % (rule, where, what, fix))

    def flag(self, rule, where, what):
        self.flags.append('FLAG  %s %s: %s' % (rule, where, what))

    # ---- walking the outline
    def parts(self):
        """every {"t", "ids"} part with a where label"""
        out = []

        def walk(x, where):
            if isinstance(x, dict):
                if 't' in x and 'ids' in x:
                    out.append((where, x))
                    return
                for k, v in x.items():
                    walk(v, where)
            elif isinstance(x, list):
                for v in x:
                    walk(v, where)
        for k, b in enumerate(self.o['body']):
            walk(b, 'body[%d]%s' % (k, ':' + b['type'] if isinstance(b, dict) and 'type' in b else ''))
        return out

    def plain_strings(self):
        out = []
        skip = {'ids', 'type', 'id', 'cls', 'tag', 'title', 'drawer', 'chip', 'g', 'n', 'mask_cols', 'src', 'tempting',
                'currency', 'pop_ok', 'note', 'label'}

        def walk(x, where, key=None):
            if isinstance(x, str):
                t = rx(x)
                n = len(re.findall(r'[A-Za-z]{2,}', t))
                if n >= 5 or (n and re.search(r'\d', t)):   # a short label ("Why first", "Confirm") is structure
                    out.append((where, t))
            elif isinstance(x, dict):
                if 't' in x and 'ids' in x:
                    return
                for k, v in x.items():
                    if k not in skip:
                        walk(v, where, k)
            elif isinstance(x, list):
                for v in x:
                    walk(v, where)
        for k, b in enumerate(self.o['body']):
            if isinstance(b, dict) and b.get('type') == 'h':
                continue
            if isinstance(b, dict) and b.get('type') == 'ladder':        # rung tags are line-of-therapy labels
                for n, tag, when, body in b['rungs']:
                    walk([when, body], 'body[%d]:ladder' % k)
                continue
            if isinstance(b, dict) and b.get('type') == 'script2':        # row keys are the fixed script labels
                for key, lines in b['rows']:
                    walk(lines, 'body[%d]:script2' % k)
                continue
            if isinstance(b, dict) and b.get('type') == 'systems':
                walk([b.get('title'), b.get('small')] + [[f, w] for _, f, w in b['rows']], 'body[%d]:systems' % k)
                continue
            if isinstance(b, dict) and b.get('type') == 'table':           # captions and heads are plain labels
                walk(b['rows'], 'body[%d]:table' % k)
                continue
            if isinstance(b, dict) and b.get('type') == 'workup':
                walk([[tiles] for when, tiles in b['steps']] + [b.get('end')], 'body[%d]:workup' % k)
                continue
            walk(b, 'body[%d]' % k)
        return out

    # ---- rules
    def s1(self):
        o, steps = self.o, self.o['steps']
        if [s[1] for s in steps] != LABELS or [str(s[0]) for s in steps] != [str(i) for i in range(1, 9)]:
            self.err('S1', 'steps', 'labels or numbers are not 1..8 %s' % LABELS, 'use the fixed stepper labels in order')
        present = {int(s[0]) for s in steps if s[2]}
        need = {'disease': set(range(1, 9)) - {2, 6}, 'drug': {1, 3, 7, 8}}.get(o['entry'])
        never = {'drug': {5, 6}}.get(o['entry'], set())
        if need and not need <= present:
            self.err('S1', 'steps', '%s entry lacks step(s) %s' % (o['entry'], sorted(need - present)), 'add the step or justify it in the spec')
        if present & never:
            self.err('S1', 'steps', '%s entry has step(s) %s' % (o['entry'], sorted(present & never)), 'pass null for them')
        hs = [(b['n'], b['id']) for b in o['body'] if isinstance(b, dict) and b.get('type') == 'h']
        listed = {(int(s[0]), s[2]) for s in steps if s[2]}
        for n, i in hs:
            if (int(n), i) not in listed:
                self.err('S1', 'h %s' % i, 'h block not in steps (or a different number)', 'list it in steps with its number')
        for n, i in listed - {(int(n), i) for n, i in hs}:
            self.err('S1', 'step %d' % n, 'listed step %s has no h block' % i, 'add {"type": "h", "n": %d, "id": "%s"}' % (n, i))
        if [n for n, _ in hs] != sorted(n for n, _ in hs):
            self.err('S1', 'steps', 'h blocks out of order', 'order the body by step')

    def s2(self, ids_on_page):
        try:
            R = OR.Renderer(self.o, self.dir)
            self.html = '\n'.join(R.block(b) for b in self.o['body'])
        except AssertionError as ex:
            self.html = ''
            self.err('S2', 'render', 'unsourced or unknown id: %s' % ex, 'cite an id that is in facts.json or the claim map')
            return
        except (ValueError, KeyError, TypeError) as ex:
            self.html = ''
            self.err('S2', 'render', str(ex)[:160], 'use a block or part type from outline_render.py')
            return
        for where, t in self.plain_strings():
            self.err('S2', where, 'learner words outside a sourced part: "%s"' % t[:60], 'wrap them as {"t": ..., "ids": [...]}')
        for m in re.finditer(r'"drawer": "([^"]+)"', json.dumps(self.o)):
            if ids_on_page is not None and m.group(1) not in ids_on_page:
                self.err('S2', 'drawer', 'no brief or alias "%s" on the page' % m.group(1), 'use a live brief id')

    def c1c2(self):
        o = self.o
        words = len(H.unescape(re.sub('<[^>]+>', '', self.html)).split()) if self.html else 0
        cap = CAPS.get(o['entry'])
        if cap and words > cap * 1.02:          # the caps are "about" (Jonathan 2026-10-10): 2% slack, then an error
            self.err('C1', 'body', '%d words above the Practice header, cap about %d' % (words, cap), 'cut, or move guideline-only detail into a hover')
        elif cap and words > cap:
            self.flag('C1', 'body', '%d words, just over the cap of about %d' % (words, cap))
        self.words = words
        for k, b in enumerate(o['body']):
            if isinstance(b, dict) and b.get('type') == 'bottom' and not 1 <= len(b['lines']) <= 3:
                self.err('C2', 'body[%d]:bottom' % k, '%d bottom-line lines' % len(b['lines']), 'keep 1 to 3')
            if isinstance(b, dict) and b.get('type') == 'script2':
                ins = [lines for key, lines in b['rows'] if key == 'Insights']
                if len(ins) != 1 or len(ins[0]) != 2:
                    self.err('C2', 'body[%d]:script2' % k, 'Insights must be one row of exactly two lines', 'two Insights lines')

    def d(self):
        R = OR.Renderer(self.o, self.dir) if self.html else None
        for k, b in enumerate(self.o['body']):
            if not (isinstance(b, dict) and b.get('type') == 'table' and b['heads'] and rx(R.r(b['heads'][-1]) if R else '') == 'Decides it'):
                continue
            where = 'body[%d]:table "%s"' % (k, rx(R.r(b['caption']))[:40])
            tb = b.get('tempting')
            if not tb or len(tb) != len(b['rows']) or not all(isinstance(x, str) and len(x.split()) >= 2 for x in tb):
                what = 'no "tempting" reason for every row (rows ordered by temptation need the reason)'
                if self.golden:
                    self.flag('D1', where, what + '; golden outline, written before the rule')
                else:
                    self.err('D1', where, what, 'add "tempting": one reason per row, in row order')
            seen = {}
            for i, row in enumerate(b['rows']):
                cell = rx(R.r(row[-1]))
                if ACTION.match(cell):
                    self.err('D2', '%s row %d' % (where, i + 1), 'Decides-it opens with an action: "%s"' % cell[:50],
                             'name the finding or timeline that decides; the action belongs in Treatment')
                key = re.sub(r'[^a-z0-9 ]', '', cell.lower())
                if key in seen:
                    self.err('D3', '%s rows %d and %d' % (where, seen[key] + 1, i + 1), 'same Decides-it text', 'each row needs its own decider')
                seen.setdefault(key, i)

    def l(self):
        R = OR.Renderer(self.o, self.dir)
        for k, b in enumerate(self.o['body']):
            if not (isinstance(b, dict) and b.get('type') == 'ladder'):
                continue
            rungs = b['rungs']
            for j, (n, tag, when, body) in enumerate(rungs):
                w = rx(R.r(when))
                if j > 0 and ESCALATE.search(tag) and not TRIGGER.search(w):
                    self.err('L1', 'body[%d]:ladder rung %s' % (k, n), 'escalation "%s" has no time or named failure: "%s"' % (tag, w[:50]),
                             'say when (after 2 weeks, despite..., no response to...)')
                if TOPTAG.match(tag) and j != len(rungs) - 1:
                    self.err('L2', 'body[%d]:ladder rung %s' % (k, n), '"%s" is not the last rung' % tag, 'move it to the end')

    def n1p1x1(self):
        lens = self.o.get('lens')
        for where, p in self.parts():
            t = rx(p['t'])
            fids = [i for i in p['ids'] if i in self.facts]
            if re.search(r'\d', t) and not fids:
                c = p.get('currency', '')
                if not (c == 'stable' or c == 'flagged' or (c.startswith('verified:') and c[9:] in self.facts)):
                    self.err('N1', where, 'a number from a carried source with no currency: "%s"' % t[:60],
                             'cite a fetched fact, or add "currency": "verified:<fact id>" | "stable" | "flagged"')
            for i in fids:
                pop = self.facts[i].get('population', '')
                adult = re.search(r'adult|cirrho', pop, re.I) and not re.search(r'child|all ages|adolesc|infant|pediatric', pop, re.I)
                child = re.search(r'child|infant|pediatric|neonat', pop, re.I) and not re.search(r'adult|all ages', pop, re.I)
                if lens == 'peds' and adult and not re.search(r'adult|cirrho', t, re.I) and not p.get('pop_ok'):
                    self.err('P1', where, 'fact %s is for "%s" in a peds line: "%s"' % (i, pop, t[:50]),
                             'cite a pediatric source, or say "in an adult" in the line')
                if lens == 'fm' and child and not re.search(r'child|infant|pediatric|newborn|neonat|adolesc', t, re.I) and not p.get('pop_ok'):
                    self.err('P1', where, 'fact %s is for "%s" in an FM line: "%s"' % (i, pop, t[:50]),
                             'cite an adult source, or name the child in the line')
            srcs = {(self.facts[i].get('sha') or self.facts[i].get('url'), self.facts[i].get('section')) for i in fids}
            if len(srcs) > 1:
                self.flag('X1', where, 'combined %d sources (%s): "%s"' % (len(srcs), ', '.join(fids), t[:70]))

    def u1(self):
        if not self.html:
            return
        text = rx(self.html).lower()
        defined = {d.lower() for d in self.o.get('defined', [])}
        heads = ' | '.join(rx(c).lower() for c in re.findall(r'<tr>\s*<td\b[^>]*>(.*?)</td>', self.html, re.S)
                           + re.findall(r'<b\b[^>]*>(.*?)</b>', self.html, re.S)
                           + re.findall(r'data-title="([^"]*)"', self.html))
        done = set()
        for q in QUALIFIERS:
            for m in re.findall(r'\b%s ([a-z][a-z-]{3,})' % re.escape(q), text):
                label = '%s %s' % (q, m)
                if m in STOP or label in done or label in defined:
                    continue
                done.add(label)
                n = len(re.findall(r'\b%s\b' % re.escape(label), text))
                if n < 3:
                    continue
                # defined: a row header, a bold term or a hover title holds it; or a colon, dash or "means" follows it
                if re.search(r'(?:^| \| )%s\b' % re.escape(label), heads) or re.search(r'\b%s\b' % re.escape(label), heads) \
                        or re.search(r'\b%s\s*(?::|–|\(|means|is defined|are defined)' % re.escape(label), text):
                    continue
                self.err('U1', 'body', '"%s" used %d times and never defined' % (label, n),
                         'define it once (a colon, dash, row or hover), or list it in "defined" if the course already defines it')

    def o1(self):
        for k, x in enumerate(self.o.get('old_claims', [])):
            if len(x) < 3 or x[1] not in ('carried', 'corrected', 'moved', 'dropped') or len(str(x[2]).split()) < 3:
                self.err('O1', 'old_claims[%d]' % k, 'disposition %r' % (x[1:2],), 'carried | corrected | moved | dropped, with where or why')

    def k1(self, ids_on_page):
        bid = self.o['brief']
        cp = self.cards_path or os.path.join(WS, 'repair', 'migration', 'spine', 'packets', bid, 'cards.md')
        dp = os.path.join(self.dir, 'cards_disposition.json')
        if not os.path.exists(cp):
            self.flag('K1', 'cards', 'no card checklist at %s' % os.path.relpath(cp, WS))
            return
        items, cand = {}, set()
        cur = None
        for line in open(cp, encoding='utf-8'):
            m = re.match(r'## (card|candidate) (\d+)', line)     # must cards and --terms candidates alike
            if m:
                cur = m.group(2)
                items[cur] = ''
                if m.group(1) == 'candidate':
                    cand.add(cur)
                continue
            m = re.match(r'- anchor \(cloze\): (.*)', line)
            if m and cur:
                items[cur] = m.group(1).strip()
            m = re.match(r'- \[(\d+\.[0-9a-f]+)\] (.*)', line)
            if m:
                items[m.group(1)] = m.group(2).strip()
        disp = json.load(open(dp, encoding='utf-8')) if os.path.exists(dp) else {}
        text = rx(self.html).lower() if self.html else ''
        stems = {w[:5] for w in re.findall(r'[a-z0-9]+', text)}
        for i, txt in items.items():
            d = disp.get(i)
            if not d:
                self.err('K1', 'card %s' % i, 'no disposition', 'add it to cards_disposition.json')
                continue
            kind, _, rest = d.partition(':')
            kind = kind.strip()
            if kind not in ('covered', 'owner', 'scope', 'not-topic', 'conflict'):
                self.err('K1', 'card %s' % i, 'unknown disposition "%s"' % d[:40], 'covered:, owner:, scope:, not-topic, conflict:')
            elif kind == 'owner' and ids_on_page is not None and rest.strip().split()[0] not in ids_on_page:
                self.err('K1', 'card %s' % i, 'owner "%s" is not a brief on the page' % rest.strip()[:30], 'name a live brief id')
            elif kind == 'conflict' and rest.strip().split()[0] not in self.facts:
                self.err('K1', 'card %s' % i, 'conflict fact "%s" not in facts' % rest.strip()[:30], 'name the fact id that conflicts')
            elif kind == 'covered' and text:
                keys = [w for w in re.findall(r'[a-z0-9]+', txt.lower()) if len(w) >= 4 and w not in STOP]
                hit = [w for w in keys if w[:5] in stems]
                if keys and len(hit) * 2 < len(keys):
                    miss = 'marked covered but the brief lacks %s' % ', '.join(sorted(set(keys) - set(hit)))[:80]
                    if '.' in i or i in cand:   # an Extra statement or a candidate card: a paraphrase may cover it, so a reader settles it
                        self.flag('K1', 'card %s' % i, miss)
                    else:                 # the card's anchor (its cloze answer): the tested fact itself
                        self.err('K1', 'card %s' % i, miss, 'cover it, or change the disposition')
        for i in disp:
            if i not in items:
                self.flag('K1', 'card %s' % i, 'disposition for an item not on the checklist')

    def run(self):
        ids_on_page = None
        if self.page and os.path.exists(self.page):
            h = P.read_page(self.page)
            ids_on_page = set(re.findall(r'class="brief[^"]*" id="([^"]+)"', h)) | set(re.findall(r'class="alias" id="([^"]+)"', h))
        self.html = ''
        self.s1()
        self.s2(ids_on_page)
        self.c1c2()
        self.d()
        self.l()
        self.n1p1x1()
        self.u1()
        self.o1()
        self.k1(ids_on_page)
        return self


def main(argv):
    if not argv:
        sys.exit(__doc__.strip().splitlines()[2].strip())
    opt = lambda k, d=None: argv[argv.index(k) + 1] if k in argv else d
    c = Check(argv[0], opt('--page', os.path.join(WS, 'index.html')), opt('--cards')).run()
    if c.flags:
        open(os.path.join(c.dir, 'outline_flags.txt'), 'w', encoding='utf-8').write('\n'.join(c.flags) + '\n')
    print('outline_check %s: %d error(s), %d flag(s), %d words%s' % (
        c.o['brief'], len(c.errors), len(c.flags), getattr(c, 'words', 0), ' (flags in outline_flags.txt)' if c.flags else ''))
    for e in c.errors:
        print(e)
    if '--quiet' not in argv:
        for f in c.flags[:8]:
            print(f)
    return 1 if c.errors else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
