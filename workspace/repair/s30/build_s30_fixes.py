#!/usr/bin/env python3
"""build_s30_fixes.py: replayable generator for the s30 review fixes (run once from the workspace folder).

1. Manual review fixes, folded into the 04_voice_* op that produced the text so each op's claim map
   stays old -> final (bs-tef remaps, peds-constipation labels, rlq-pain wording, Kasai wording,
   fat-soluble stem fact, infant-stool opener).
2. Acronym pass with the reviewed placement: expansion immediately after the acronym at first use per
   block, inside the bold span when the acronym is bold (span declared in reworded_bold), brackets inside
   an existing parenthesis, plain in Pairs-with and p.sub. Expansions that fall inside a 04 op's text are
   folded into that op (with new_claims "expansion"); the rest become 05_acronyms.json.
Expansions come from tools/acronyms.json.
"""
import glob
import json
import os
import re
import sys

WS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(WS, 'tools'))
from pagelib import briefs, count, read_page, text  # noqa: E402
import apply_edits  # noqa: E402
import importlib.util  # noqa: E402
spec = importlib.util.spec_from_file_location('v', os.path.join(WS, 'tools', 'verify_edits.py'))
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)

ACR = json.load(open(os.path.join(WS, 'tools', 'acronyms.json'), encoding='utf-8'))
D, SKIP = ACR['expansions'], set(ACR['skip'])
TOK = re.compile(r'(?<![A-Za-z0-9-])(%s)(?![A-Za-z0-9])' % '|'.join(sorted(map(re.escape, D), key=len, reverse=True)))
S30 = os.path.join(WS, 'repair', 's30')
FILES = ['04_voice_%d.json' % i for i in range(1, 6)]
LOG = []


def load(f):
    return json.load(open(os.path.join(S30, f), encoding='utf-8'))


def save(f, d):
    json.dump(d, open(os.path.join(S30, f), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)


def retarget(e, old_sent, new_sent):
    """Point claim quotes and new_claims text that used old_sent at new_sent."""
    o, n = v.norm_q(old_sent), v.norm_q(new_sent)
    for c in e.get('claims', []):
        for k in ('to', 'carried_by'):
            if c.get(k) and o in v.norm_q(c[k]):
                c[k] = v.norm_q(c[k]).replace(o, n)
    for c in e.get('new_claims', []):
        if o in v.norm_q(c.get('claim', '')):
            c['claim'] = v.norm_q(c['claim']).replace(o, n)


def sub_with(e, old, new):
    assert e['with'].count(old) == 1, (e['brief'], old[:60], e['with'].count(old))
    e['with'] = e['with'].replace(old, new)


# ---------------------------------------------------------------- 1. manual fixes
def manual(F):
    # bs-tef: the deleted "wrong options present at other ages" sentences are framing, not carried
    for n in (11, 14):
        e = F['04_voice_3.json']['edits'][n - 1]
        for c in e['claims']:
            if re.search(r'(wrong option|other options) (is|are) (a )?real disease', c['claim']):
                for k in ('to', 'carried_by'):
                    c.pop(k, None)
                c['dropped'] = 'framing about the answer options; not a clinical claim'
                LOG.append('bs-tef op %d: claim remapped as dropped (framing)' % n)
    # peds-constipation Tier fingerprint: restore the done / normal / bothered labels
    e = F['04_voice_3.json']['edits'][6]
    lab = re.findall(r'(<b>)?(done|normal|bothered)(</b>)?:', e['find'])
    L = {x[1]: '%s%s%s:' % x for x in lab}
    new = ('%s nothing has been tried yet &middot; %s growth, perineum and urinary function, and a nontender abdomen '
           '&middot; %s the child cries with every stool, so treat today rather than counsel and wait.' % (L['done'], L['normal'], L['bothered']))
    old = e['with']
    e['with'] = new
    for a, b in [('Nothing has been tried yet', 'done: nothing has been tried yet'),
                 ('growth, perineum and urinary function are normal, and the abdomen is nontender',
                  'normal: growth, perineum and urinary function, and a nontender abdomen'),
                 ('the child cries with every stool, so treat today rather than counsel and wait.',
                  'bothered: the child cries with every stool, so treat today rather than counsel and wait.')]:
        retarget(e, a, b)
    LOG.append('peds-constipation Tier fingerprint: done/normal/bothered labels restored')
    # rlq-pain: restore "is not an indication" (drop the added "for antibiotics")
    e = F['04_voice_4.json']['edits'][5]
    sub_with(e, 'is not an indication for antibiotics.', 'is not an indication.')
    retarget(e, 'is not an indication for antibiotics', 'is not an indication')
    LOG.append('rlq-pain pearls: "is not an indication" restored')
    # bs-galactosemia Kasai: plain exam-versus-evidence wording, every number kept
    e = F['04_voice_5.json']['edits'][19]
    sub_with(e, 'The exam keys <b>60 days</b> as the Kasai window; choose that number.',
             'Board questions use <b>60 days</b> as the Kasai cutoff.')
    retarget(e, 'The exam keys 60 days as the Kasai window; choose that number.', 'Board questions use 60 days as the Kasai cutoff.')
    sub_with(e, 'Treat 60 days as the keyed threshold, not as a deadline with room to spare.',
             'Use 60 days as the exam threshold, not as a deadline with room to spare.')
    retarget(e, 'Treat 60 days as the keyed threshold, not as a deadline with room to spare.',
             'Use 60 days as the exam threshold, not as a deadline with room to spare.')
    LOG.append('bs-galactosemia Kasai: "Board questions use 60 days as the Kasai cutoff"')
    # bs-fat-soluble-vitamins: state only what the stem says, and the explanation's inference as such
    e = F['04_voice_2.json']['edits'][9]
    old_s = 'This teen with CF stopped his enzymes and vitamins.'
    new_s = ('This teen with CF has not taken his prescribed medications; in CF these are usually pancreatic enzymes '
             'and fat-soluble vitamins.')
    sub_with(e, old_s, new_s)
    retarget(e, old_s, new_s)
    for c in e.get('new_claims', []):
        if 'stopped his enzymes' in c['claim']:
            c['claim'] = 'The teen has not taken his prescribed medications; in CF these are usually pancreatic enzymes and fat-soluble vitamins.'
    LOG.append('bs-fat-soluble-vitamins dp: stem fact restored (prescribed medications)')
    # infant-stool: no dangling "These"
    e = F['04_voice_2.json']['edits'][4]
    sub_with(e, '<p>These three benign stool complaints', '<p>Three benign stool complaints')
    retarget(e, 'These three benign stool complaints', 'Three benign stool complaints')
    LOG.append('infant-stool dp: opener "Three benign stool complaints occur in ..."')


# ---------------------------------------------------------------- 2. acronym pass
def spans(seg, pat):
    return [(m.start(), m.end()) for m in re.finditer(pat, seg, re.S)]


def expansions(html, s, t, lab):
    """[(abs_start, abs_end, replacement, acr, exp, bold_text_or_None)] for first uses in block html[s:t]."""
    seg = html[s:t]
    pairs = 'Pairs with' in seg[:80]
    lbls, bolds = spans(seg, r'<span class="lbl">.*?</span>'), spans(seg, r'<b>.*?</b>')
    vis_before = lambda i: v.norm_q(seg[:i]).lower()  # noqa: E731
    out, seen = [], set()
    for m in TOK.finditer(seg):
        a = m.group(1)
        lt, gt = seg.rfind('<', 0, m.start()), seg.rfind('>', 0, m.start())
        if lt > gt or a in seen or a in SKIP or any(x <= m.start() < y for x, y in lbls):
            continue
        inb = [(x, y) for x, y in bolds if x <= m.start() < y]
        if pairs and inb:
            continue  # partner title
        seen.add(a)
        exp = D[a]
        after = seg[m.end():m.end() + 12]
        if re.match(r'(</b>)?\s*[(\[]', after):
            continue  # already followed by a parenthesis (expansion or other)
        if re.match(r'\s*(—|&mdash;)', after) and not inb:
            continue  # mnemonic or plain term row: "HELLP — Hemolysis, ..."
        tail = v.norm_q(seg[(inb[0][1] if inb else m.end()):][:160]).lower()
        if re.match(r'\s*(—|&mdash;)', seg[(inb[0][1] if inb else m.end()):][:12]) and exp.split()[0].rstrip(',').lower() in tail[:60]:
            continue  # the definition after the dash already spells it out (mnemonic)
        if a != 'MR' and exp.lower() in vis_before(m.start()):
            continue  # written out earlier in the block
        pre = v.norm_q(seg[:m.start()])
        br = pre.count('(') > pre.count(')')
        par = (' [%s]' if br else ' (%s)') % exp
        if inb:
            x, y = inb[0]
            btxt = text(seg[x:y])
            if btxt == 'Repeat LFTs in 3 months':  # reviewed form: bold narrows to the acronym
                out.append((s + x, s + y, 'Repeat <b>LFTs</b>%s in 3 months' % par, a, exp, btxt))
            else:
                out.append((s + m.end(), s + m.end(), par, a, exp, btxt))
        elif pairs or lab.startswith('p.sub') or re.match(r'\s*(—|&mdash;)', after):
            out.append((s + m.end(), s + m.end(), par, a, exp, None))
        else:
            out.append((s + m.start(), s + m.end(), '<b>%s</b>%s' % (a, par), a, exp, None))
    return out


def gi_briefs(html):
    gs = html.find('<h3 class="system" id="gi"')
    ge = html.find('<h3 class="system"', gs + 10)
    return [b for b in briefs(html) if gs < b.start < ge]


def fold(F):
    """Apply 04 files op by op; expansions landing inside an op's new text are folded into that op."""
    html = read_page(os.path.join(WS, 'index.html'))
    for f in FILES:
        for n, e in enumerate(F[f]['edits'], 1):
            b = apply_edits._brief(html, e['brief'], n, 'replace')
            at = apply_edits._unique(html, b.start, b.end, e['find'], n, 'replace', b.id)
            html = apply_edits.apply_one(html, e, n, set(), [])
            lo, hi = at, at + len(e['with'])
            nb = [x for x in briefs(html) if x.id == e['brief']][0]
            reps = []
            for s, t, lab in v.voice_ranges(html, nb):
                if s <= lo <= t:
                    reps += [r for r in expansions(html, s, t, lab) if lo <= r[0] and r[1] <= hi]
            if not reps:
                continue
            w = e['with']
            for r in sorted(reps, key=lambda r: -r[0]):
                w = w[:r[0] - lo] + r[2] + w[r[1] - lo:]
            html = html[:lo] + w + html[hi:]
            e['with'] = w
            for r in reps:
                e.setdefault('new_claims', []).append({'claim': '%s stands for %s' % (r[3], r[4]), 'from': 'expansion'})
            old_b = {text(x) for x in re.findall(r'<b>(.*?)</b>', e['find'], re.S)}
            new_b = {text(x) for x in re.findall(r'<b>(.*?)</b>', w, re.S)}
            lost = sorted(x for x in old_b - new_b if x not in e.get('reworded_bold', []))
            if lost:
                e['reworded_bold'] = e.get('reworded_bold', []) + lost
            LOG.append('%s op %d (%s): folded %s' % (f, n, e['brief'], ', '.join(r[3] for r in reps)))
    return html


def fix_quotes(F, html):
    """Rewrite claim quotes to the literal final text when they differ only by expansions."""
    btext = {b.id: v.norm_q(b.inner) for b in gi_briefs(html)}
    fixed = 0
    for f in FILES:
        for e in F[f]['edits']:
            bt = btext[e['brief']]
            for c in e.get('claims', []):
                for k in ('to', 'carried_by'):
                    q = c.get(k)
                    if not q or v.norm_q(q) in bt:
                        continue
                    sq = v.strip_exp(v.norm_q(q))
                    # find the final sentence(s) whose stripped form contains the quote
                    for sent in re.split(r'(?<=[.;?!])\s+', bt):
                        if sq and sq in v.strip_exp(sent):
                            c[k] = sent
                            fixed += 1
                            break
    return fixed


def acronym_file(html):
    """05: expansions left in text no 04 op produced (first use per block, final placement rules)."""
    edits = []
    while True:
        done = True
        for b in gi_briefs(html):
            for s, t, lab in v.voice_ranges(html, b):
                reps = expansions(html, s, t, lab)
                if not reps:
                    continue
                r = reps[0]
                L, R = r[0], r[1]
                if r[5]:  # inside a bold span: the anchor covers the whole span so the bold rewrite is declared
                    L = html.rfind('<b>', s, r[0] + 1)
                    R = html.find('</b>', r[1] - 1) + len('</b>')
                elif L == R:
                    L, R = max(s, L - 12), min(t, R + 12)

                def untag(L, R):
                    while html.rfind('<', s, L) > html.rfind('>', s, L):  # never start inside a tag
                        L -= 1
                    while html.rfind('<', L, R) > html.rfind('>', L, R):  # never end inside a tag
                        R += 1
                    return L, R
                L, R = untag(L, R)
                while count(html[b.start:b.end], html[L:R]) != 1 or v.norm_q(html[L:R]) == '':
                    L, R = untag(max(s, L - 8), min(t, R + 8))
                    if L <= s and R >= t:
                        break
                find = html[L:R]
                withs = html[L:r[0]] + r[2] + html[r[1]:R]
                e = {'op': 'replace', 'brief': b.id, 'find': find, 'with': withs,
                     'note': 'acronym expansion at first use in %s: %s' % (lab, r[3]),
                     'claims': [{'claim': v.norm_q(find), 'to': v.norm_q(withs)}],
                     'new_claims': [{'claim': '%s stands for %s' % (r[3], r[4]), 'from': 'expansion'}]}
                if r[5]:
                    e['reworded_bold'] = [r[5]]
                html, _ = apply_edits.apply(html, {'edits': [e]})
                edits.append(e)
                done = False
                break
            if not done:
                break
        if done:
            return edits, html


def main():
    F = {f: load(f) for f in FILES}
    manual(F)
    html = fold(F)
    for f in FILES:
        save(f, F[f])
    a05, html = acronym_file(html)
    save('05_acronyms.json', {'batch': 's30', 'edits': a05})
    n = fix_quotes(F, html)
    for f in FILES:
        save(f, F[f])
    print('\n'.join(LOG))
    print('05_acronyms: %d ops | quotes rewritten to final text: %d' % (len(a05), n))


if __name__ == '__main__':
    main()
