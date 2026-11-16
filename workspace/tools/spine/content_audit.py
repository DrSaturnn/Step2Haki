#!/usr/bin/env python3
"""content_audit.py (2026-11-08, plan for D-20261106-8 item 7): the POST_REFACTOR_LEDGER content audits rerun on a
page, as inventories the s170+ content batches build from. Read-only; writes OUT/ files and prints counts.

  python3 tools/spine/content_audit.py PAGE.html OUT_DIR [--base BASE.html]   (s170 T8: every content batch reruns it at B0)

Run from workspace/ (imports tools/pagelib and tools/spine/prose_lint). Files written:
  prose_by_brief.csv    per brief: section, entry, hits by pattern and by region (prose_lint.lint_brief)
  headers.csv           every header-region string with its count and the TEXTBOOK_STYLE H row it falls under
  hovers.csv            every hover body: brief, kicker, title, words, lines, longest line, break markup, source kicker
  in_practice.csv       every "In practice" line, with a flag when it names a source
  keypoints.csv         every key point line (div.dp): words, term-first colon, pronoun subject, prose hits
  nbme_blocks.csv       every NBME block outside the bank: kind, label, data-nbme, pause point or not, text hash
  step2.csv             every top-level block of step 2 (criteria) and each line's heuristic sort
  dx_rows.csv           every differential-table row: brief, caption, row label, row text hash
  dx_groups.md          row labels carried by two or more briefs, with the number of distinct wordings (N19)
  summary.json          the counts printed below
"""
import collections
import csv
import hashlib
import json
import os
import re
import sys

from bs4 import BeautifulSoup

WS = os.getcwd()
sys.path.insert(0, os.path.join(WS, 'tools'))
sys.path.insert(0, os.path.join(WS, 'tools', 'spine'))
from pagelib import briefs, read_page  # noqa: E402
import prose_lint as pl  # noqa: E402

SRC = re.compile(r"\b(?:AnKing|UWorld|NBME|AMBOSS|Amboss|First Aid|Pocket Medicine|UpToDate|Merck|MSD|label|Label|"
                 r"FDA|DailyMed|AAP|ACOG|USPSTF|CDC|guideline|Guideline|DSM)\b")
SRC_KICK = re.compile(r"^(?:AnKing|UWorld|NBME|Label|.*label|Merck|MSD|Source|Analogy|Board|In practice|Why|Mnemonic|"
                      r"More|Also|Order|Newborn|Receptors)$", re.I)
WORKUP = re.compile(r"\b(?:order|orders|ordered|obtain|check|measure|send|draw|repeat|confirm(?:ed|s)? (?:by|with)|"
                    r"imaging|ultrasound|ultrasonography|CT|MRI|radiograph|X-ray|x-ray|ECG|electrocardiogram|EEG|"
                    r"biopsy|culture|panel|level|levels|test|tests|testing|screen with|skip|not needed|no need)\b")
GRADE = re.compile(r"\b(?:mild|moderate|severe|grade|grading|stage|staging|class [IV]+|severity)\b", re.I)
MECH = re.compile(r"\b(?:mechanism|caused by|due to|types?|subtypes?|anatomy|pathophysiology)\b", re.I)
DIFF = re.compile(r"\b(?:versus|vs\.?|distinguish|differs?|unlike|in contrast)\b", re.I)
CRIT = re.compile(r"\b(?:criteria|criterion|at least|or more|of the following|≥|>=|score|points?|Wells|PERC|Centor|"
                  r"Kocher|ASCVD|PHQ|GAD-7|AUDIT|CAGE|EPDS|DSM|Jones|duration|for \d+|weeks?|months?|years?|cutoff|"
                  r"threshold|defin)\b", re.I)

# TEXTBOOK_STYLE header list rows, as regexes on the live string (anchored loosely)
HROWS = [
    ('H1', r'^Clues that change the answer'), ('H2', r'most tempting first'), ('H3', r'^Follow-up decisions'),
    ('H4', r'^Act now'), ('H5', r'^First treatment by situation'), ('H6', r'^Interactions(, by result)?$'),
    ('H7', r'^(Urgent findings|Red flags: act before)'),
    ('H8', r'^What (sets the outcome|raises the stakes|makes it severe|makes it dangerous)'),
    ('H9', r'^(History: what each answer|Examination: what each finding)'), ('H10', r'^(Finalists|What sets it apart)'),
    ('H11', r'^(Which effect is it|Manage by effect)'), ('H12', r'(lowest rung not yet tried|^Management ladder)'),
    ('H13', r'^Decides it$'), ('H14', r'^(Points to|What it points to)$'), ('H15', r'^(Next move|Next)$'),
    ('H16', r'^Clue$'), ('H17', r'^(Fingerprint|Illness script \+ buzzwords)$'), ('H18', r'^Do$'),
    ('H19', r'(NBME.{0,60}tell|^The tell$|^Tell$)'), ('H20', r'^(Combined with|Result|Rule)$'),
    ('H21', r'^(Excluded here by|Excluded by|Why less likely here)$'),
    ('H22', r'^(Hook|The picture|The company it keeps|What kills it|Why it tempts|Why it loses|Legitimate claim)$'),
    ('H23', r'^(Transferable rule|Pairs with|The decision point)$'), ('H24', r'^(Shows|Why)$'),
    ('H25', r'^(Decoy note|Decoys|Distractors|Common wrong answers)'),
    ('H26', r'^(Decision spine|Exit ramps|Gates|Boundary conditions|Tier fingerprint|The hierarchy to bank)'),
    ('H27', r'^Where the choice is made$'),
    ('H28', r'^(Papilledema forbids the tap|Occulta means hidden|Latency is a diagnostic variable|The vitals do most)'),
    ('H29', r'^From the first dose$'), ('H30', r'^Toxicity and withdrawal, from'),
    ('H31', r'^(Washout and diet limits|Limits after the last dose)'), ('H32', r'^Movement effects and NMS'),
    ('H33', r'^(When each reaction appears|After a dose or a stop)'), ('H34', r'^Titration and restart limits'),
    ('H35', r'^When each drug can start'), ('H36', r'^Clozapine, from the first dose'),
    ('H37', r'^Contraception on modafinil'), ('H38', r'^Time the psychosis'), ('H39', r'^Check it against mood'),
    ('H40', r'^(Time the episode|Name the disorder from its episodes)'), ('H41', r'^Time it, then name the fear'),
    ('H42', r'^(Time the confusion|Time alcohol withdrawal)'), ('H43', r'^\d+ .*\?$'),
    ('H44', r'^(Practice|Scenario bank)$'),
]
HROWS = [(k, re.compile(p)) for k, p in HROWS]
HEADER_SEL = ['caption', 'th', 'h5', 'figcaption', 'summary']


def norm(t):
    return re.sub(r'\s+', ' ', t or '').strip()


def h8(t):
    return hashlib.sha1(norm(t).encode()).hexdigest()[:10]


def hrow(t):
    for k, rx in HROWS:
        if rx.search(t):
            return k
    return ''


def step_regions(inner):
    """{step number: html of that step} for spine briefs (h5.tsec.sp-h with b.sp-n)."""
    heads = list(re.finditer(r'<h5 class="tsec sp-h" id="[^"]*"><b class="sp-n">(\d)</b>([^<]*)</h5>', inner))
    end_bank = inner.find('class="authored-hdr"')
    out = {}
    for i, m in enumerate(heads):
        stop = heads[i + 1].start() if i + 1 < len(heads) else (end_bank if end_bank > m.end() else len(inner))
        out[int(m.group(1))] = (m.group(2).strip(), inner[m.end():stop])
    return out


def main():
    page, out = sys.argv[1], sys.argv[2]
    base = sys.argv[sys.argv.index('--base') + 1] if '--base' in sys.argv else None
    os.makedirs(out, exist_ok=True)
    html = read_page(page)
    bl = briefs(html)
    S = collections.OrderedDict()
    S['briefs'] = len(bl)

    # 1 prose lint
    pats, regs = collections.Counter(), collections.Counter()
    with open(os.path.join(out, 'prose_by_brief.csv'), 'w', newline='') as f:
        w = csv.writer(f)
        allp = sorted({p for p in pl.REPORT_ONLY} | {'contrast', 'length_over_30', 'multi_semicolon', 'pronoun_subject',
                                                    'header_wh_word', 'hover_no_break_over_30', 'article_list',
                                                    'source_narration', 'intensifier', 'header_comma_by',
                                                    'appositive_included', 'branch', 'hedged_narration',
                                                    'trailing_explainer', 'reveal_colon', 'header_from_the'})
        rl = sorted(pl.PROSE_REGIONS | {'header'})
        w.writerow(['brief', 'title', 'sys', 'navgrp', 'entry', 'kind', 'counted'] + allp + ['r_' + r for r in rl])
        for b in bl:
            hits = pl.lint_brief(b.inner)
            pc = collections.Counter(h['pattern'] for h in hits)
            rc = collections.Counter(h['region'] for h in hits if h['pattern'] not in pl.REPORT_ONLY)
            counted = sum(v for k, v in pc.items() if k not in pl.REPORT_ONLY)
            pats.update(pc)
            regs.update(rc)
            w.writerow([b.id, b.title, b.attrs.get('data-sys', ''), b.attrs.get('data-navgrp', ''),
                        b.attrs.get('data-entry', ''), b.kind, counted] + [pc.get(p, 0) for p in allp] +
                       [rc.get(r, 0) for r in rl])
    S['prose_counted'] = sum(v for k, v in pats.items() if k not in pl.REPORT_ONLY)
    S['prose_by_region'] = dict(regs.most_common())

    hdr = collections.Counter()
    hdr_briefs = collections.defaultdict(set)
    hovers, inprac, keyp, nbme, step2, dxrows = [], [], [], [], [], []
    no_workup = []
    for b in bl:
        soup = BeautifulSoup(b.inner, 'lxml')
        for bank in soup.select('ol.bank'):
            bank.decompose()
        # 2 headers
        for el in soup.find_all(HEADER_SEL) + soup.select('span.lbl, span.sk, p.kick, b.pp-t, span.sp-ct, div.ttl > span'):
            t = norm(el.get_text(' '))
            if t and len(t) < 160 and not el.find_parent(class_='sp-pop-b'):
                hdr[(el.name + ('.' + el['class'][0] if el.get('class') else ''), t)] += 1
                hdr_briefs[t].add(b.id)
        # 3 hovers
        for pb in soup.select('span.sp-pop-b'):
            k = pb.find('span', class_='sp-k')
            ct = pb.find('span', class_='sp-ct')
            kick = norm(k.get_text()) if k else ''
            title = norm(ct.get_text()) if ct else ''
            body = BeautifulSoup(str(pb), 'lxml').find('span', class_='sp-pop-b')
            for x in body.find_all('span', class_=['sp-k', 'sp-ct']):
                x.decompose()
            breaks = len(body.find_all('br')) + len(body.find_all(['p', 'li', 'div']))
            parts = [norm(p) for p in re.split(r'<br\s*/?>|</p>|</li>|</div>', str(body)) if norm(BeautifulSoup(p, 'lxml').get_text(' '))]
            lines = [norm(BeautifulSoup(p, 'lxml').get_text(' ')) for p in parts] or [norm(body.get_text(' '))]
            words = [pl.nwords(x) for x in lines]
            trig = soup.find(attrs={'aria-controls': pb.get('id')}) if pb.get('id') else None
            hovers.append([b.id, pb.get('id', ''), kick, title, sum(words), len(lines), max(words or [0]), breaks,
                           int(bool(SRC_KICK.match(kick)) and bool(re.search(r'label|AnKing|UWorld|NBME|Merck|MSD|Source|Board', kick, re.I))),
                           int(bool(SRC.search(body.get_text(' ')))), norm(trig.get_text(' '))[:60] if trig else '',
                           int(bool(trig and kick and norm(trig.get_text(' ')) == kick))])
        # 4 In practice lines (visible and hover)
        for s in soup.find_all(string=re.compile(r'In practice')):
            par = s.find_parent(['p', 'li', 'td', 'span', 'div'])
            t = norm(par.get_text(' ')) if par else norm(s)
            inprac.append([b.id, int(bool(par and par.find_parent(class_='sp-pop-b'))) if par else 0,
                           int(bool(re.search(r'AnKing|UWorld|NBME|Merck|MSD|label|Label|UpToDate|First Aid', t))), t[:200]])
        # 5 key points
        for dp in soup.select('div.dp'):
            for li in dp.find_all(['li', 'p']):
                if li.find(['li', 'p']):
                    continue
                t = norm(pl.vis(li))
                if not t:
                    continue
                head = t.split(':')[0] if ':' in t else ''
                keyp.append([b.id, pl.nwords(t), int(bool(head) and pl.nwords(head) <= 6),
                             int(bool(re.match(r'^(It|They|This|These)\b', t) or re.search(r';\s+(it|they)\b', t))),
                             len(pl.text_checks(t, 'keypoint', 'div.dp li')), t[:220]])
        # 6 NBME blocks outside the bank
        seen = set()
        for el in soup.find_all(True):
            cl = el.get('class') or []
            lab = el.find('span', class_=['lbl', 'sp-ct', 'ex'], recursive=False)
            labt = norm(lab.get_text(' ')) if lab else ''
            is_nb = ('nbq' in cl or 'pc-nbq' in cl or 'pc-nbi' in cl or (el.name == 'div' and el.get('data-nbme') is not None)
                     or (el.name == 'div' and 'NBME' in labt))
            if not is_nb or any(id(p) in seen for p in el.parents):
                continue
            seen.add(id(el))
            pause = bool(el.find_parent('div', class_='sp-pause') or 'pp-b' in cl)
            nbme.append([b.id, el.name + '.' + '.'.join(cl), labt[:40], el.get('data-nbme', ''), int(pause),
                         pl.nwords(norm(el.get_text(' '))), h8(el.get_text(' ')), norm(el.get_text(' '))[:160]])
        # 7 step 2 and workup presence
        steps = step_regions(b.inner)
        if 2 in steps:
            name, reg = steps[2]
            rs = BeautifulSoup(reg, 'lxml').body or BeautifulSoup('', 'lxml')
            tops = [c for c in rs.children if getattr(c, 'name', None)]
            if 5 not in steps:
                no_workup.append(b.id)
            for i, blk in enumerate(tops):
                lines = [norm(pl.vis(x)) for x in blk.find_all(['li', 'p', 'tr', 'span'], class_=lambda c: True)
                         if x.name in ('li', 'p', 'tr') or 'sl' in (x.get('class') or []) or 'si' in (x.get('class') or [])]
                lines = [x for x in lines if x] or [norm(pl.vis(blk))]
                for ln in lines:
                    tag = ('workup' if WORKUP.search(ln) and not CRIT.search(ln) else
                           'mixed' if WORKUP.search(ln) else
                           'severity' if GRADE.search(ln) and not CRIT.search(ln) else
                           'script' if MECH.search(ln) and not CRIT.search(ln) else
                           'differential' if DIFF.search(ln) else 'criteria')
                    step2.append([b.id, name, i + 1, blk.name + '.' + '.'.join(blk.get('class') or []), tag, ln[:220]])
        # 8 differential rows
        for st, (name, reg) in steps.items():
            if not re.search(r'Differential', name):
                continue
            rsoup = BeautifulSoup(reg, 'lxml')
            for tb in rsoup.find_all('table'):
                cap = norm(tb.caption.get_text(' ')) if tb.caption else ''
                for tr in tb.select('tbody tr'):
                    tds = tr.find_all('td')
                    if not tds:
                        continue
                    td0 = BeautifulSoup(str(tds[0]), 'lxml')
                    for x in td0.select('.aka, .sp-chip'):
                        x.decompose()
                    lab = norm(td0.get_text(' ')).lower()
                    lab = re.sub(r'\s*\(.*?\)', '', lab).strip(' .')
                    rowt = ' | '.join(norm(pl.vis(td)) for td in tds[1:])
                    dxrows.append([b.id, cap[:80], lab[:80], len(tds), h8(rowt), rowt[:220]])

    def dump(name, head, rows):
        with open(os.path.join(out, name), 'w', newline='') as f:
            w = csv.writer(f)
            w.writerow(head)
            w.writerows(rows)

    hrows_c = collections.Counter()
    hrows_b = collections.defaultdict(set)
    hl = []
    for (tag, t), n in hdr.most_common():
        r = hrow(t)
        hl.append([tag, t, n, r, len(hdr_briefs[t])])
        if r:
            hrows_c[r] += n
            hrows_b[r] |= hdr_briefs[t]
    dump('headers.csv', ['tag', 'text', 'uses', 'hrow', 'briefs'], hl)
    S['header_strings'] = len(hdr)
    S['hrow_uses'] = {k: [hrows_c[k], len(hrows_b[k])] for k, _ in HROWS if hrows_c[k]}
    dump('hovers.csv', ['brief', 'pop', 'kicker', 'title', 'words', 'lines', 'longest_line', 'break_markup',
                        'source_kicker', 'source_in_body', 'trigger', 'label_trigger'], hovers)
    S['hovers'] = len(hovers)
    S['hovers_one_block'] = sum(1 for h in hovers if h[5] == 1)
    S['hovers_line_over_12'] = sum(1 for h in hovers if h[6] > 12)
    S['hovers_over_30_no_break'] = sum(1 for h in hovers if h[5] == 1 and h[4] > 30)
    S['hovers_label_trigger'] = sum(h[11] for h in hovers)
    S['hovers_source_kicker'] = sum(h[8] for h in hovers)
    S['hover_kickers'] = dict(collections.Counter(h[2] for h in hovers if h[2]).most_common(25))
    S['hovers_source_in_body'] = sum(h[9] for h in hovers)
    S['hover_briefs'] = len({h[0] for h in hovers})
    dump('in_practice.csv', ['brief', 'in_hover', 'names_source', 'text'], inprac)
    S['in_practice'] = [len(inprac), sum(r[2] for r in inprac), sum(r[1] for r in inprac)]
    dump('keypoints.csv', ['brief', 'words', 'term_colon', 'pronoun', 'prose_hits', 'text'], keyp)
    S['keypoint_lines'] = len(keyp)
    S['keypoint_term_colon'] = sum(r[2] for r in keyp)
    S['keypoint_pronoun'] = sum(r[3] for r in keyp)
    S['keypoint_over_15'] = sum(1 for r in keyp if r[1] > 15)
    S['keypoint_briefs'] = len({r[0] for r in keyp})
    dump('nbme_blocks.csv', ['brief', 'kind', 'label', 'data_nbme', 'pause', 'words', 'hash', 'text'], nbme)
    S['nbme_blocks'] = len(nbme)
    S['nbme_pause'] = sum(r[4] for r in nbme)
    S['nbme_briefs'] = len({r[0] for r in nbme})
    S['nbme_kinds'] = dict(collections.Counter(r[1] for r in nbme))
    dump('step2.csv', ['brief', 'step_name', 'block', 'block_tag', 'sort', 'line'], step2)
    S['step2_briefs'] = len({r[0] for r in step2})
    S['step2_blocks'] = len({(r[0], r[2]) for r in step2})
    S['step2_lines'] = len(step2)
    S['step2_sort'] = dict(collections.Counter(r[4] for r in step2))
    S['step2_no_workup_step'] = no_workup
    dump('dx_rows.csv', ['brief', 'caption', 'label', 'cols', 'hash', 'text'], dxrows)
    by = collections.defaultdict(list)
    for r in dxrows:
        by[r[2]].append(r)
    groups = [(k, v) for k, v in by.items() if len({r[0] for r in v}) >= 2 and k]
    groups.sort(key=lambda kv: -len({r[0] for r in kv[1]}))
    with open(os.path.join(out, 'dx_groups.md'), 'w') as f:
        f.write('# Differential rows carried by two or more briefs (N19)\n\n| Row label | Briefs | Wordings | Briefs |\n|---|---|---|---|\n')
        for k, v in groups:
            f.write('| %s | %d | %d | %s |\n' % (k, len({r[0] for r in v}), len({r[4] for r in v}),
                                               ', '.join(sorted({r[0] for r in v}))))
    S['dx_rows'] = len(dxrows)
    S['dx_tables'] = len({(r[0], r[1]) for r in dxrows})
    S['dx_shared_labels'] = len(groups)
    S['dx_shared_rows'] = sum(len(v) for _, v in groups)
    S['dx_shared_drifted'] = sum(1 for _, v in groups if len({r[4] for r in v}) > 1)
    S['dx_shared_briefs'] = len({r[0] for _, v in groups for r in v})
    if base:
        bh = read_page(base)
        S['text_changed_vs_base'] = sorted(pl.changed_briefs(bh, html))
    json.dump(S, open(os.path.join(out, 'summary.json'), 'w'), indent=1, ensure_ascii=False)
    for k, v in S.items():
        print(k, json.dumps(v, ensure_ascii=False)[:600])


if __name__ == '__main__':
    main()
