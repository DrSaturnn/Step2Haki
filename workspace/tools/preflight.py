#!/usr/bin/env python3
"""preflight.py: advisory checks for the content errors audits keep finding (Jonathan, 2026-10-05).

  python3 tools/preflight.py NEW.html [--base REV | --old OLD.html] [--sources DIR] [--all] [--json]

Compares a built page with the page at --base (default HEAD) and checks only what changed, so
the baseline never floods the report. Every check is a warning for a human or auditor to settle;
none of them proves an error. --all runs the item checks (P3 to P6) on every item instead of the
changed ones (calibration only).

  P1 hedge-loss       a number the old brief qualified ("up to 6 hours", "about 20%", "6 months
                      or more") now appears in that brief only without its qualifier; also a fall
                      in the brief's count of modal hedges (may, usually, typically, often ...)
  P2 sibling-left     a 6-word run whose page-wide count fell but did not reach zero: a claim
                      fixed in one place that survives in a table row, pearl or explanation
  P3 unexplained      a distractor whose explanation was cut, a relabeled distractor its
                      explanation does not name, or a new item's distractor named nowhere in the brief
  P4 same-key         two items in one bank with the same keyed answer, at least one new or changed
  P5 key-in-stem      a new or changed diagnosis item whose stem already holds the key's distinctive words
  P6 retell           a new or changed authored stem that shares most of its clue words and numbers
                      with one source stem (repair/sources/sNN_questions.md "Stem:" lines,
                      nbq_index.md); needs the local-only sources
  P7 vendor-orphan    run separately: tools/vendor_scan.py --page NEW.html (an old edit file that
                      the new wording leaves holding the only copy of a source run; s103)
"""
import html as H
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pagelib as pl

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STOP = set('''a an and are as at be been but by for from has have in into is it its of on or that the
their then there these this to was were which with without within after before than not no yes
patient patients year years old month months week weeks day days hour hours boy girl man woman
child infant newborn mother father most next step following likely appropriate diagnosis what
who whose when while also only both each other more less very over under about some any all
first second third new history examination exam normal shows show reports otherwise healthy
start obtain order check give treat treatment therapy test testing management start'''.split())
HEDGES = re.compile(r"\b(may|might|can|could|usually|typically|often|generally|commonly|"
                    r"frequently|rarely|sometimes|most|many|some|about|approximately|around|roughly|"
                    r"nearly|up to|at least|at most|or more|or less|or older|or younger|"
                    r"more than|less than|fewer than|under|over|within|by|before|after|until)\b", re.I)
NUM = re.compile(r"\b\d+(?:[.,]\d+)?(?:\s*(?:to|-|–)\s*\d+(?:[.,]\d+)?)?\s*"
                 r"(%|mg/dl|mg|g/dl|mmol/l|mcg|ml|cm|mm|kg|°c|hours?|h|days?|weeks?|months?|years?|"
                 r"minutes?|min|seconds?|cells?|percentile)?", re.I)
PRE_Q = re.compile(r"(up to|about|approximately|around|roughly|nearly|at least|at most|more than|"
                   r"less than|fewer than|under|over|within|by|before|after|until|older than|"
                   r"younger than|beyond|>=|<=|≥|≤|<|>)\s*$", re.I)
POST_Q = re.compile(r"^\s*(or more|or less|or older|or younger|or longer|or shorter|or above|or below|"
                    r"and older|and younger|and above|and up|plus)\b", re.I)


def words(t):
    return re.findall(r"[a-z0-9]+(?:[.'][a-z0-9]+)*", t.lower())


def content(t):
    return [w for w in words(t) if len(w) >= 4 and w not in STOP and not w.isdigit()]


def stem5(w):
    return w[:5]


def page_at(rev):
    return subprocess.run(['git', '-C', WS, 'show', '%s:./index.html' % rev],
                          capture_output=True, text=True, check=True).stdout


def brief_texts(html):
    out = {}
    for b in pl.briefs(html):
        # visible text plus option labels (attributes are visible as answer choices)
        opts = ' '.join(H.unescape(v) for k, v in re.findall(r'(data-d[12]|data-label-[a-z0-9]+)="([^"]*)"', b.inner))
        out[b.id] = vis(b.inner) + ' ' + opts
    return out


def item_map(html):
    m = {}
    for it in pl.items(html):
        m[it.id] = it
    return m


def vis(frag):
    t = re.sub(r'<!--.*?-->', ' ', frag, flags=re.S)
    t = re.sub(r'<[^>]+>', ' ', t)
    return re.sub(r'\s+', ' ', H.unescape(t)).strip()


def norm_key(k):
    return ' '.join(words(re.sub(r'\(.*?\)', '', k)))


# ---------------------------------------------------------------- P1
def qualified_numbers(t):
    """number phrase -> (qualified occurrences, bare occurrences)."""
    res = defaultdict(lambda: [0, 0])
    for m in NUM.finditer(t):
        tok = re.sub(r'\s+', ' ', m.group(0).strip().lower())
        if not re.search(r'\d', tok) or len(tok) < 2:
            continue
        pre = t[max(0, m.start() - 20):m.start()]
        post = t[m.end():m.end() + 14]
        q = bool(PRE_Q.search(pre) or POST_Q.search(post))
        res[tok][0 if q else 1] += 1
    return res


def p1(old_b, new_b, changed):
    out = []
    for bid in changed:
        if bid not in old_b or bid not in new_b:
            continue
        o, n = qualified_numbers(old_b[bid]), qualified_numbers(new_b[bid])
        for tok, (oq, ob) in o.items():
            if oq and tok in n and n[tok][0] == 0 and n[tok][1] > 0:
                out.append({'brief': bid, 'msg': '"%s" was qualified %dx; now only bare (%dx)' % (tok, oq, n[tok][1])})
        ho = Counter(h.lower() for h in HEDGES.findall(old_b[bid]))
        hn = Counter(h.lower() for h in HEDGES.findall(new_b[bid]))
        lost = {h: ho[h] - hn.get(h, 0) for h in ho if ho[h] - hn.get(h, 0) > 0}
        modal = {h: v for h, v in lost.items() if h in ('may', 'might', 'can', 'could', 'usually', 'typically',
                                                       'often', 'generally', 'commonly', 'most', 'some',
                                                       'about', 'approximately', 'up to', 'at least')}
        if sum(modal.values()) >= 2:
            out.append({'brief': bid, 'msg': 'hedge words fell: ' + ', '.join('%s -%d' % kv for kv in sorted(modal.items()))})
    return out


# ---------------------------------------------------------------- P2
N2 = 6
VITALS = set('afebrile bp hr rr mm hg mg dl kg cm temperature pulse respirations spo2 oxygen saturation room air'.split())


def grams(t):
    w = words(t)
    return [' '.join(w[i:i + N2]) for i in range(len(w) - N2 + 1)]


def p2(old_b, new_b, changed):
    oc, nc, where = Counter(), Counter(), defaultdict(set)
    for bid, t in old_b.items():
        oc.update(grams(t))
    for bid, t in new_b.items():
        g = grams(t)
        nc.update(g)
        for x in set(g):
            where[x].add(bid)
    # only runs that the changed briefs lost
    lost_in_changed = set()
    for bid in changed:
        og = Counter(grams(old_b.get(bid, '')))
        ng = Counter(grams(new_b.get(bid, '')))
        lost_in_changed |= {g for g in og if ng[g] < og[g]}
    hits = {g for g in lost_in_changed if 0 < nc[g] < oc[g] and oc[g] <= 6
            and len([w for w in g.split() if w not in STOP and w not in VITALS and not w.isdigit()]) >= 3}
    # merge chained grams (each one word on from the last) into one phrase per location
    out, used = [], set()
    nxt = defaultdict(list)
    for g in hits:
        nxt[' '.join(g.split()[:-1])].append(g)
    for g in sorted(hits):
        if g in used:
            continue
        phrase, cur = g.split(), g
        used.add(g)
        while True:
            cand = [h for h in nxt.get(' '.join(cur.split()[1:]), []) if h not in used and where[h] == where[g]]
            if not cand:
                break
            cur = cand[0]; used.add(cur); phrase.append(cur.split()[-1])
        locs = sorted(where[g])
        out.append({'brief': ','.join(locs), 'msg': '"%s" fell %d -> %d; still in %s' % (' '.join(phrase), oc[g], nc[g], ', '.join(locs))})
    # drop phrases contained in a longer one already reported
    out = [o for o in out if not any(o is not p and o['brief'] == p['brief'] and o['msg'].split('"')[1] in p['msg'].split('"')[1] for p in out)]
    return out[:60]


# ---------------------------------------------------------------- P3-P6
def changed_items(old_i, new_i, everything):
    if everything:
        return list(new_i.values())
    return [it for iid, it in new_i.items() if iid not in old_i or old_i[iid].inner != it.inner
            or old_i[iid].attrs != it.attrs]


def label(it, k):
    return H.unescape(it.attrs.get(k, ''))


EXTRA_ACR = {'LDH': 'lactate dehydrogenase', 'CK': 'creatine kinase', 'CBC': 'complete blood count',
             'ESR': 'erythrocyte sedimentation rate', 'CRP': 'C-reactive protein', 'UA': 'urinalysis',
             'ECG': 'electrocardiogram', 'EEG': 'electroencephalogram', 'VCUG': 'voiding cystourethrogram'}


def _acr():
    try:
        d = json.load(open(os.path.join(WS, 'tools', 'acronyms.json'), encoding='utf-8')).get('expansions', {})
    except Exception:
        d = {}
    d.update(EXTRA_ACR)
    return d


ACR = _acr()


def expand(t):
    for k, v in ACR.items():
        t = re.sub(r'\b%s\b' % re.escape(k), k + ' ' + v, t)
    return t


def named(it, k, expl):
    expl = expand(expl)
    cw = content(label(it, k))
    es = {stem5(w) for w in content(expl)}
    return not cw or any(stem5(w) in es for w in cw)


def p3(items, old_i, old_b, new_b):
    """A distractor that was explained (in its item or anywhere in its brief) and no longer is."""
    out = []
    for it in items:
        o = old_i.get(it.id)
        for k in ('data-d1', 'data-d2'):
            lab = label(it, k)
            if o is None:
                if not named(it, k, it.companion) and not named(it, k, new_b.get(it.brief_id, '').replace(lab, '')):
                    out.append({'brief': it.brief_id, 'item': it.id, 'msg': 'new item: "%s" is named nowhere else in the brief' % lab})
                continue
            if label(o, k) != lab:
                if not named(it, k, it.companion):
                    out.append({'brief': it.brief_id, 'item': it.id, 'msg': 'distractor relabeled to "%s" and its explanation does not name it' % lab})
            elif named(o, k, o.companion) and not named(it, k, it.companion):
                out.append({'brief': it.brief_id, 'item': it.id, 'msg': 'explanation used to address "%s" and no longer does' % lab})
    return out


def p4(items, new_i, old_i):
    by_brief = defaultdict(list)
    for it in new_i.values():
        by_brief[it.brief_id].append(it)
    touched = {it.id for it in items}
    out = []
    for bid, its in by_brief.items():
        seen = defaultdict(list)
        for it in its:
            k = norm_key(it.key)
            if k:
                seen[k].append(it)
        for k, grp in seen.items():
            if len(grp) > 1 and any(g.id in touched for g in grp):
                was = [g for g in grp if g.id in old_i and norm_key(old_i[g.id].key) == k]
                if len(was) < len(grp) or len(was) == len(grp) and not all(g.id in old_i for g in grp):
                    out.append({'brief': bid, 'item': ' '.join(g.id for g in grp),
                                'msg': '%d items keyed "%s"' % (len(grp), grp[0].key[:60])})
    return out


GENERIC_KEY = STOP | set('''disease disorder syndrome infection acute chronic primary secondary
reassurance observation repeat refer referral education counseling clinical fever pain rash cough
swelling bleeding failure deficiency anemia infection valve'''.split())


def p5(items):
    out = []
    for it in items:
        if it.attrs.get('data-type') not in ('dx', 'stage'):
            continue
        kw = [w for w in content(it.key) if w not in GENERIC_KEY and len(w) >= 5]
        if not kw:
            continue
        st = {stem5(w) for w in content(it.stem)}
        hit = [w for w in kw if stem5(w) in st]
        if hit and len(hit) >= max(1, (len(kw) + 1) // 2):
            out.append({'brief': it.brief_id, 'item': it.id,
                        'msg': 'stem holds key words %s (key "%s")' % (', '.join(hit), it.key[:60])})
    return out


def source_stems(src):
    out = []
    if not os.path.isdir(src):
        return None
    for f in sorted(os.listdir(src)):
        if not (re.match(r's\d+[a-z]?_questions\.md$', f) or f == 'nbq_index.md'):
            continue
        for line in open(os.path.join(src, f), encoding='utf-8', errors='replace'):
            m = re.match(r'\s*(?:[-*]\s*)?(?:\*\*)?(?:Stem|Vignette)(?:\*\*)?\s*:\s*(.+)', line, re.I)
            if m and len(m.group(1)) > 80:
                out.append((f, m.group(1)))
    return out


def clue_set(t):
    nums = set(re.findall(r'\b\d+(?:\.\d+)?\b', t))
    return {stem5(w) for w in content(t)} | {'#' + n for n in nums}


def p6(items, src):
    stems = source_stems(src)
    if stems is None:
        return [{'brief': '', 'msg': 'skipped: no local-only sources at %s' % src}]
    sets = [(f, s, clue_set(s)) for f, s in stems]
    out = []
    for it in items:
        if it.attrs.get('data-src', 'authored') != 'authored':
            continue
        c = clue_set(it.stem)
        if len(c) < 8:
            continue
        best = max(((len(c & S) / len(c), f, s) for f, s, S in sets), default=(0, '', ''))
        nums = {x for x in c if x.startswith('#')}
        bnums = clue_set(best[2]) if best[1] else set()
        shared_nums = len(nums & bnums)
        if best[0] >= 0.6 or (best[0] >= 0.45 and shared_nums >= 3):
            out.append({'brief': it.brief_id, 'item': it.id,
                        'msg': '%.0f%% of stem clues and %d numbers match a stem in %s' % (100 * best[0], shared_nums, best[1])})
    return out


def main(argv):
    if not argv or argv[0].startswith('-'):
        print(__doc__)
        return 2
    new = open(argv[0], encoding='utf-8', newline='').read()

    def opt(k, d=None):
        return argv[argv.index(k) + 1] if k in argv else d
    old = open(opt('--old'), encoding='utf-8', newline='').read() if opt('--old') else page_at(opt('--base', 'HEAD'))
    src = opt('--sources', os.path.join(WS, 'repair', 'sources'))
    everything = '--all' in argv
    ob, nb = brief_texts(old), brief_texts(new)
    changed = sorted(b for b in nb if ob.get(b) != nb[b])
    oi, ni = item_map(old), item_map(new)
    items = changed_items(oi, ni, everything)
    res = {'P1 hedge-loss': p1(ob, nb, changed), 'P2 sibling-left': p2(ob, nb, changed),
           'P3 unexplained': p3(items, oi, ob, nb), 'P4 same-key': p4(items, ni, oi),
           'P5 key-in-stem': p5(items), 'P6 retell': p6(items, src)}
    if '--json' in argv:
        print(json.dumps(res, indent=1))
        return 0
    total = sum(len(v) for v in res.values())
    print('preflight: %d changed brief(s), %d new or changed item(s) | %d warning(s): %s' % (
        len(changed), len(items), total, ', '.join('%s %d' % (k.split()[0], len(v)) for k, v in res.items())))
    for k, v in res.items():
        for r in v[:25]:
            print('  %-16s %-22s %s%s' % (k, r.get('brief', '')[:22], (r['item'][:22] + ' ') if r.get('item') else '', r['msg']))
        if len(v) > 25:
            print('  %-16s ... %d more' % (k, len(v) - 25))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
