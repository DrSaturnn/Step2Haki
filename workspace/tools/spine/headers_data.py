#!/usr/bin/env python3
"""headers_data (s170 T3): writes repair/efficiency/HEADERS.json, the TEXTBOOK_STYLE header list as data.

  python3 tools/spine/headers_data.py [PAGE]      (PAGE: the page whose header strings become "known"; default index.html)

HEADERS.json:
  rows: the header list H1 to H45 (TEXTBOOK_STYLE.md): kind, live strings, the approved name, status;
  retired: live strings of approved rows, which no brief may show once touched (prose_lint header_retired, counted);
  retired_patterns: regexes for the families ("..., most tempting first", question titles);
  allowed: approved names and approved new headings; known: every structural header on PAGE when the list was made,
  minus retired. A touched brief's structural headers must be in allowed or known (prose_lint header_new, counted on
  touched briefs): a header that is in neither is new and needs the owner's approval (TEXTBOOK_STYLE rule 6), which adds
  it to allowed. C6 (D-20261108-2): a block heading that is the plain name of a drug, disease, syndrome, exposure or
  test already named in the brief needs no separate approval; block headings are listed in the batch report.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(WS, 'tools'))

A = 'approved D-20261108-2 (C1 to C6)'
P = 'applied in s170 under TEXTBOOK_STYLE; approved with the s170 ship'
ROWS = [
    ('H1', 'caption', ['Clues that change the answer'], 'Key findings', P),
    ('H2', 'caption', ['Look-alikes, most tempting first', 'Which look-alike, most tempting first'], 'Differential diagnosis', P),
    ('H3', 'caption', ['Follow-up decisions'], 'Follow-up', P),
    ('H4', 'caption', ['Act now'], 'Emergencies', P),
    ('H5', 'caption', ['First treatment by situation', 'First drug by situation'], 'Initial treatment', P),
    ('H6', 'caption', ['Interactions, by result', 'Interactions'], 'Drug interactions', P),
    ('H7', 'caption', ['Urgent findings', 'Red flags: act before the full history'], 'Red flags', P),
    ('H8', 'caption', ['What sets the outcome', 'What raises the stakes', 'What makes it severe', 'What makes it dangerous'], 'Prognosis or Severity, by content', P),
    ('H9', 'caption', ['History: what each answer points to', 'Examination: what each finding points to'], 'History; Physical examination', P),
    ('H10', 'caption', ['Finalists', 'What sets it apart'], 'Leading diagnoses; Distinguishing features', P),
    ('H11', 'caption', ['Which effect is it, most tempting first', 'Manage by effect'], 'Differential of adverse effects; Management by adverse effect', P),
    ('H12', 'caption', ['Management ladder'], 'Stepwise management', P),
    ('H13', 'th', ['Decides it'], 'Distinguishing feature', A),
    ('H14', 'th', ['Points to', 'What it points to'], 'Interpretation', A),
    ('H15', 'th', ['Next move', 'Next'], 'Next step', A),
    ('H16', 'th', ['Clue'], 'Finding', A),
    ('H17', 'th', ['Fingerprint', 'Illness script + buzzwords'], 'Key features', P),
    ('H18', 'th', ['Do'], 'Management', P),
    ('H19', 'th', ['The NBME tell', 'The tell', 'Tell'], 'Classic finding', P),
    ('H20', 'th', ['Combined with', 'Rule'], 'Drug; Effect; Management', P),   # "Result" also heads lab tables: renamed by the lanes in interaction tables, not retired
    ('H21', 'th', ['Excluded here by', 'Excluded by', 'Why less likely here'], 'Findings against the diagnosis', P),
    ('H22', 'th', ['Hook', 'The picture', 'The company it keeps', 'What kills it', 'Why it tempts', 'Why it loses', 'Legitimate claim'], 'Rewrite per table', P),
    ('H23', 'lbl', ['Transferable rule', 'Pairs with', 'The decision point'], 'General rule; Related topics; Key decision', P),
    ('H24', 'tag', ['Shows', 'Why'], 'Finding or action line (Shows dropped); Rationale', A),
    ('H25', 'lbl', ['Decoy note', 'Decoys', 'Distractors'], 'Common wrong answers', P),
    ('H26', 'lbl', ['Decision spine', 'Exit ramps', 'Gates', 'Boundary conditions', 'Tier fingerprint', 'The hierarchy to bank'], 'Remove or rewrite per content', P),
    ('H27', 'lbl', ['Where the choice is made'], 'Drug choice by condition', P),
    ('H28', 'lbl', ['Papilledema forbids the tap', 'Occulta means hidden', 'Latency is a diagnostic variable', 'The vitals do most of the eliminating'], 'Noun labels per content', P),
    ('H29', 'timeline', ['From the first dose'], 'Treatment response timeline', P),
    ('H30', 'timeline', ['Toxicity and withdrawal, from the exposure or the last dose'], 'Toxicity and withdrawal timeline', P),
    ('H31', 'timeline', ['Washout and diet limits, from the last dose', 'Limits after the last dose'], 'Washout periods and dietary restrictions', P),
    ('H32', 'timeline', ['Movement effects and NMS, from a start or dose increase'], 'Onset of extrapyramidal effects and neuroleptic malignant syndrome', P),
    ('H33', 'timeline', ['When each reaction appears, from the start', 'After a dose or a stop: which effect, and when'], 'Onset of adverse and withdrawal effects', P),
    ('H34', 'timeline', ['Titration and restart limits, from the last dose change'], 'Titration and restart limits', P),
    ('H35', 'timeline', ['When each drug can start'], 'Timing of initiation', P),
    ('H36', 'timeline', ['Clozapine, from the first dose'], 'Clozapine adverse effects timeline', P),
    ('H37', 'timeline', ['Contraception on modafinil or armodafinil, from the last dose'], 'Contraception with modafinil, armodafinil', P),
    ('H38', 'timeline', ['Time the psychosis'], 'Psychotic disorders by duration', P),
    ('H39', 'timeline', ['Check it against mood episodes'], 'Psychosis and mood episodes', P),
    ('H40', 'timeline', ['Time the episode', 'Name the disorder from its episodes'], 'Episode duration; Mood disorders by episode', P),
    ('H41', 'timeline', ['Time it, then name the fear'], 'Anxiety disorders by duration and focus of fear', P),
    ('H42', 'timeline', ['Time the confusion', 'Time alcohol withdrawal from the last drink'], 'Confusion timeline; Alcohol withdrawal timeline', P),
    ('H43', 'workup', [], 'Plain test or topic name', P),
    ('H44', 'section', ['Scenario bank'], 'Practice', P),
    ('H45', 'block', [], 'SNRI discontinuation syndrome; Citalopram QT precautions; Bupropion; Late-pregnancy SSRI exposure', A),
]
RETIRED_PATTERNS = [r', most tempting first$', r': start on the lowest rung not yet tried$', r'^Management ladder:',
                    r'^\d+\s.*\?$']


def main(a):
    import pagelib
    import prose_lint as PL
    page = pagelib.read_page(a[0] if a else os.path.join(WS, 'index.html'))
    retired = sorted({s for r in ROWS for s in r[2]})
    allowed = set()
    for r in ROWS:
        if r[3].startswith(('Rewrite', 'Remove', 'Noun labels', 'Plain test', 'Finding or action')):
            if r[0] == 'H24':
                allowed.add('Rationale')
            continue
        for n in r[3].split('; '):
            if ' or ' in n and ', by content' in n:
                allowed.update(x.strip() for x in n.replace(', by content', '').split(' or '))
            else:
                allowed.add(n)
    known = set()
    for b in pagelib.briefs(page):
        for _, t in PL.structural_headers(b.inner):
            known.add(t)
    rk = {PL.hnorm(x) for x in retired}
    known = sorted(k for k in known if PL.hnorm(k) not in rk and not PL.retired_pattern(k, RETIRED_PATTERNS))
    out = {'_doc': __doc__.split('\n\n', 1)[1].strip(),
           'rows': [{'id': r[0], 'kind': r[1], 'live': r[2], 'name': r[3], 'status': r[4]} for r in ROWS],
           'retired': retired, 'retired_patterns': RETIRED_PATTERNS, 'allowed': sorted(allowed), 'known': known}
    p = os.path.join(WS, 'repair', 'efficiency', 'HEADERS.json')
    json.dump(out, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(p, 'a').write('\n')
    print('HEADERS.json: %d rows, %d retired, %d allowed, %d known' % (len(ROWS), len(retired), len(allowed), len(known)))


if __name__ == '__main__':
    main(sys.argv[1:])
