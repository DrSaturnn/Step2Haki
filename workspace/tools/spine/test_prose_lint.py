#!/usr/bin/env python3
"""Offline tests for the prose lint (tools/spine/prose_lint.py). Positive cases are the TEXTBOOK_STYLE violations
(most from the live SSRI card); negative cases are its permitted near misses and the two known false-positive
sources from the s164 precision audit (mnemonic rows, ' · ' fragment lists).

  python3 tools/spine/test_prose_lint.py
"""
import contextlib
import io
import json
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import prose_lint as P  # noqa: E402

ok = bad = 0


def expect(name, cond):
    global ok, bad
    if cond:
        ok += 1
    else:
        bad += 1
        print('FAIL', name)


def pats(html, **kw):
    return [h['pattern'] for h in P.lint_brief(html, **kw)]


def catches(name, html, pattern):
    got = pats(html)
    expect('%s: %s caught (got %s)' % (name, pattern, got), pattern in got)


def clean(name, html):
    got = P.lint_brief(html)
    expect('%s: clean (got %s)' % (name, [(h['pattern'], h['match']) for h in got]), got == [])


def words(n):
    return ' '.join('word%d' % i for i in range(n))


# ---- every pattern catches a true example
catches('P9 it-and', '<div class="dp"><ul><li>Mirtazapine sedates and raises appetite and weight; it and bupropion '
        'cause no sexual dysfunction</li></ul></div>', 'pronoun_subject')
catches('P17 label', '<p>On the Zoloft label, newborns exposed to an SSRI late in the third trimester have needed '
        'prolonged hospital care</p>', 'source_narration')
catches('P17 appositive', '<p>Any SSRI late in pregnancy, paroxetine included, can cause persistent pulmonary '
        'hypertension of the newborn.</p>', 'appositive_included')
catches('X, not Y', '<p>Fix the class, not the instance.</p>', 'contrast')
catches('instead of', '<p>Prevent errors instead of inspecting for them.</p>', 'contrast')
catches('rather than', '<td>Recruit the alveoli rather than turning the oxygen up</td>', 'contrast')
catches('not just', '<p>Screen not just the mother.</p>', 'contrast')
catches('not only', '<td>Ewing sarcoma, not only osteomyelitis</td>', 'contrast')
catches("isn't X, it's", "<p>It isn't relapse, it's discontinuation.</p>", 'contrast')
catches('P15 article list', "<table><tr><td>Tramadol, linezolid, a triptan, dextromethorphan, ondansetron or St "
        "John's wort</td></tr></table>", 'article_list')
catches('P15 short article list', "<table><tr><td>A triptan, dextromethorphan, ondansetron or St John's wort</td>"
        "</tr></table>", 'article_list')
catches('repeated articles', '<table><tr><td>A tendon, a nerve or a vessel</td></tr></table>', 'article_list')
catches('N3 comma-by header', '<table><caption>Interactions, by result</caption><tr><td>x</td></tr></table>',
        'header_comma_by')
catches('N3 from-the header', '<figure class="lcw"><div class="ttl"><span>From the first dose</span></div></figure>',
        'header_from_the')
for nm, html, pt in (('long header', '<h5>Clues that change the answer</h5>', 'header_long'),
                     ('long title', '<h4>Panic Disorder and Other Anxiety</h4>', 'title_long'),
                     ('meta words', '<p>The stem mentions sleep.</p>', 'meta_words')):
    expect('%s is report-only: listed with report_only, never counted' % nm,
           pt in pats(html, report_only=True) and pt not in pats(html))
# headers TEXTBOOK_STYLE approves count no hit (T3, T12, H2-style lengths)
clean('approved header T3', '<h5>Other common adverse effects (sertraline)</h5>')
clean('approved header T12', '<h5>Line of therapy for pain and headache</h5>')
clean('even as concession', '<p>Mood improves even as sleep worsens.</p>')
clean('even with concession', '<p>Mortality is 20% even with treatment.</p>')
clean('above all three as quantity', '<p>Ferritin is above all three cutoffs.</p>')
expect('caption header text leaves out a nested timeline',
       [h['text'] for h in P.lint_brief('<table><caption>Follow-up<ol class="sp-trk"><li><b>under 4 wk</b>'
                                        '<span>too early to judge</span></li></ol></caption></table>', report_only=True)
        if h['region'] == 'header'] == [])
# s170 T3 to T5: header list, hover lines, source kickers
catches('retired header (H13)', '<table><tr><th>Decides it</th></tr></table>', 'header_retired')
catches('retired caption pattern (H2)', '<table><caption>Seizure mimics, most tempting first</caption></table>', 'header_retired')
catches('retired timeline tag (H24)', '<figure class="lcw"><p class="wl"><b>Shows</b>agitation in some patients</p></figure>', 'header_retired')
clean('approved header (C1)', '<table><tr><th>Distinguishing feature</th></tr></table>')
expect('new header counted only on a touched brief',
       'header_new' in [h['pattern'] for h in P.lint_brief('<table><tr><th>Zxq header</th></tr></table>', touched=True)]
       and 'header_new' not in [h['pattern'] for h in P.lint_brief('<table><tr><th>Zxq header</th></tr></table>')])
expect('known header passes on a touched brief',
       'header_new' not in [h['pattern'] for h in P.lint_brief('<table><tr><th>Diagnosis</th></tr></table>', touched=True)])
POPB = ('<p><button class="sp-pop" aria-controls="x1">Title</button><span class="sp-pop-b" id="x1" hidden>%s'
        '<span class="sp-ct">Title</span>%s</span></p>')
catches('hover line over 16 words', POPB % ('', '<span class="sp-l">%s</span>' % words(17)), 'hover_line_long')
clean('hover lines of 12 words', POPB % ('', '<span class="sp-l">%s</span><span class="sp-l">%s</span>' % (words(12), words(12))))
catches('hover sentence over 16 words, no lines', POPB % ('', words(18) + '.'), 'hover_line_long')
catches('source kicker', POPB % ('<span class="sp-k">Label</span>', '<span class="sp-l">Diarrhea, tremor</span>'), 'source_kicker')
clean('kicker naming no source', POPB % ('<span class="sp-k">Mnemonic</span>', '<span class="sp-l">Diarrhea, tremor</span>'))
ANC = ('<p>Nocturnal, eased by shaking; <button class="sp-pop sp-a" aria-controls="a1">%s</button><span class="sp-pop-b" '
       'id="a1" hidden><span class="sp-ct">Phalen and Tinel</span><span class="sp-l">Phalen: wrist flexion</span></span></p>')
catches('hover anchor: trigger shares no word with its card', ANC % 'Nocturnal', 'hover_anchor')
clean('hover anchor: trigger on the card term', ANC % 'Tinel and Phalen signs')
P._ANCHOR = {'Nocturnal|Phalen and Tinel'}
clean('hover anchor: allow-listed fit', ANC % 'Nocturnal')
P._ANCHOR = None
catches('wh header', '<h5>What raises the stakes</h5>', 'header_wh_word')
catches('P14 hedge', '<table><tr><td>A monoamine oxidase inhibitor (MAOI), or one stopped inside its washout</td>'
        '</tr></table>', 'hedged_narration')
catches('P11 hedge', '<p>A few may grow agitated.</p>', 'hedged_narration')
catches('long sentence', '<p>%s.</p>' % words(31), 'length_over_30')
catches('two semicolons', '<table><tr><td>Painful shallow ulcers with a gray base and red rim; they come back, often '
        'with stress; rarely in the pharynx.</td></tr></table>', 'multi_semicolon')
catches('hover paragraph', '<p>Term <button type="button" class="sp-pop" aria-controls="h1">More</button>'
        '<span class="sp-pop-b" id="h1" hidden><span class="sp-ct">More</span>%s.</span></p>' % words(32),
        'hover_no_break_over_30')
# s167c N7: a hover anchored on a term (button.sp-a) is line text; a short hover shown as a line (span.sp-vl) is linted
# as the hover it was; the old label kept as a kicker (span.sp-k) is neither
catches('anchor button text is line text', '<p>Toxicity <button type="button" class="sp-pop sp-a" aria-controls="h2">'
        'even</button> at usual doses<span class="sp-pop-b" id="h2" hidden>Card text here.</span></p>', 'intensifier')
catches('visible line linted as a hover', '<p>Term <span class="sp-vl"><span class="sp-k">More</span>%s.</span></p>'
        % words(32), 'hover_no_break_over_30')
clean('kicker and visible line stay out of the line', '<p>Lithium level <span class="sp-vl"><span class="sp-k">Why</span>'
      'Narrow window.</span></p>')
expect('text_key: aria-hidden chart furniture and tag-boundary spaces are not text',
       P.text_key('<p><b>Lithium</b>, renal (<i>x</i>)<span aria-hidden="true">0 1 wk</span></p>')
       == P.text_key('<p>Lithium, renal (x)</p>'))
catches('branch otherwise','<table><tr><td>Refer for airway surgery; otherwise reassure</td></tr></table>', 'branch')
catches('branch if not', '<p>Is it glomerular, and if not, does a symptom name the cause?</p>', 'branch')
catches('intensifier even', '<table><tr><td>Toxicity even at usual doses</td></tr></table>', 'intensifier')
for w in ('really', 'truly', 'actually', 'most of all', 'above all', 'crucially', 'importantly'):
    catches('intensifier %s' % w, '<p>Check the potassium %s before the dose.</p>' % w, 'intensifier')
catches('reveal key', '<table><tr><td>The key: a pull-or-twist fracture</td></tr></table>', 'reveal_colon')
catches('reveal bottom line in prose', '<p>Give fluids. Bottom line: no imaging.</p>', 'reveal_colon')
catches('trailing making it', '<p>Clearance is renal, making it risky in kidney failure.</p>', 'trailing_explainer')
catches('trailing meaning', '<p>May be considered for a complex febrile seizure, meaning one that is focal.</p>',
        'trailing_explainer')
catches('In practice still names a source', '<p>In practice: per UWorld, incubation 3 to 12 days</p>',
        'source_narration')
expect('wh template is report-only', 'header_wh_template' not in pats('<span class="sk">What it is</span>')
       and 'header_wh_template' in pats('<span class="sk">What it is</span>', report_only=True))
h = P.lint_brief('<p>Fix the class, not the instance.</p>')
expect('hit carries pattern, region and text', h and {'pattern', 'region', 'text'} <= set(h[0]) and h[0]['region'] == 'other'
       and h[0]['text'] == 'Fix the class, not the instance.')

# ---- permitted near misses and the two known false-positive sources pass clean
clean('unless contraindicated', '<p>Give aspirin unless contraindicated.</p>')
clean('unless allergic', '<p>Give penicillin unless allergic.</p>')
clean('only as exclusivity', '<p>Fluoxetine: the only FDA-approved drug for bulimia nervosa</p>')
clean('so that purpose clause', '<p>Taper slowly so that symptoms resolve.</p>')
clean('In practice label', '<p>In practice: incubation 3 to 12 days</p>')
clean('negative finding', '<table><tr><td>Fever and rash; no seizures</td></tr></table>')
clean('negative finding in a findings list', '<table><tr><td>Weak, areflexic, alert, not dysmorphic</td></tr></table>')
clean('negated criterion', '<p>Depression common, not required.</p>')
clean('whether or not', '<p>Treat whether or not cultures are positive.</p>')
clean('not otherwise specified', '<p>Psychotic disorder, not otherwise specified</p>')
clean('even-numbered', '<p>Even-numbered chromosomes pair.</p>')
clean('even if', '<p>Treat even if afebrile.</p>')
clean('adverbial otherwise', '<p>Papilledema, otherwise a normal neurologic exam</p>')
clean('until proven otherwise', '<p>Septic arthritis until proven otherwise.</p>')
clean('if not as a clinical condition', '<p>Hepatitis B vaccine if not immune.</p>')
clean('two exclusive alternatives keep or', '<p>Add a LABA, or a medium-dose ICS.</p>')
clean('Bottom line tile label', '<div class="rule"><span class="lbl">Bottom line</span> Give aspirin.</div>')
mn_row = ('<h5>DIGFAST</h5><ul class="plain mnem" id="x-dig" data-mn-src="PsychDB"><li><b class="mn">I</b>ndiscretion '
          '&ndash; %s</li></ul>' % words(33))
clean('mnemonic row over 30 words', mn_row)
clean('mnemonic row by data-mn-src alone', mn_row.replace('class="plain mnem" ', ''))
clean('inline mnemonic fragment in pearls', '<div class="pearls"><span class="lbl">Pearls</span> <b>Wiskott-Aldrich '
      'syndrome</b> &ndash; WATER: <b>W</b>iskott-Aldrich, <b>T</b>hrombocytopenia with small platelets, <b>E</b>czema, '
      '<b>R</b>ecurrent infections, %s &middot; <b>Ataxia-telangiectasia</b> &ndash; DNA repair defect</div>' % words(25))
PEARL_APART = ('<div class="pearls"><span class="lbl">Pearls</span> Lithium &ndash; the level is drawn at 12 hours '
               'after the last dose; narrow window &middot; Valproate &ndash; it causes liver failure in children under '
               'two years; teratogenic &middot; Carbamazepine &ndash; inducer</div>')
PEARL_ONE = ('<div class="pearls"><span class="lbl">Pearls</span> Lithium &ndash; the level is drawn at 12 hours after '
             'the last dose; narrow window; renal clearance &middot; Valproate &ndash; hepatotoxic &middot; '
             'Carbamazepine &ndash; inducer</div>')
clean('pearls: three fragments, two semicolons apart', PEARL_APART)
clean('pearls: three fragments, two semicolons in one', PEARL_ONE)
expect('control: the same two-semicolon line outside pearls hits',
       'multi_semicolon' in pats(PEARL_ONE.replace('<div class="pearls">', '<div class="x"><p>').replace('</div>', '</p></div>')))
expect('control: the mnemonic row outside a mnemonic list hits',
       'length_over_30' in pats(mn_row.replace('class="plain mnem" ', '').replace(' data-mn-src="PsychDB"', '')))
clean('crit list with semicolons', '<div class="crit"><span class="lbl">Criteria</span> A &ndash; 2 weeks; 5 of 9 '
      '&middot; B &ndash; distress; impairment &middot; C &ndash; no substance</div>')
clean('practice bank excluded', '<ol class="bank"><li>Fix the class, not the instance; it and that; the stem; %s</li>'
      '</ol>' % words(35))
clean('nbq and vignette excluded', '<div class="nbq"><p>The stem: fix the class, not the instance.</p></div>'
      '<div class="vignette"><p>Otherwise, the vignette really says it.</p></div>')

# ---- page_counts, lazy template briefs and the CLI ratchet
def brief(bid, body, lazy=False):
    inner = '<h4>T</h4>' + body
    if lazy:
        inner = '<template class="axl">' + inner + '</template>'
    return '<div class="brief" id="%s">%s</div>' % (bid, inner)


def page(*bs):
    return '<!doctype html><html><body>%s</body></html>' % ''.join(bs)


BAD1 = '<p>Fix the class, not the instance.</p>'
BAD2 = BAD1 + '<p>Prevent errors instead of inspecting for them.</p>'
OK = '<p>Give aspirin.</p>'
expect('page_counts reads a lazy template brief',
       P.page_counts(page(brief('a', BAD1, lazy=True), brief('b', OK))) == {'a': 1, 'b': 0})

tmp = tempfile.mkdtemp()


def run(args):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        rc = P.main(args)
    return rc, out.getvalue()


def write(name, html):
    path = os.path.join(tmp, name)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    return path


try:
    base = write('base.html', page(brief('a', BAD1), brief('b', OK)))
    bl = os.path.join(tmp, 'b.json')
    rc, _ = run([base, '--write-baseline', bl])
    expect('write-baseline', rc == 0 and json.load(open(bl)) == {'a': 1, 'b': 0})
    rc, _ = run([base, '--baseline', bl])
    expect('baseline: equal counts pass', rc == 0)
    rc, out = run([write('rise.html', page(brief('a', BAD2), brief('b', OK))), '--baseline', bl])
    expect('baseline: a rise fails and names the brief and the fix', rc == 1 and 'a: 1 -> 2' in out
           and 'rewrite per repair/efficiency/TEXTBOOK_STYLE.md' in out)
    rc, out = run([write('new.html', page(brief('a', BAD1), brief('b', OK), brief('c', BAD1))), '--baseline', bl])
    expect('baseline: a new brief with hits fails', rc == 1 and 'c: new brief' in out)
    rc, _ = run([write('newok.html', page(brief('a', BAD1), brief('b', OK), brief('c', OK))), '--baseline', bl])
    expect('baseline: a new clean brief passes', rc == 0)
    rc, _ = run([write('fall.html', page(brief('a', OK), brief('b', OK))), '--baseline', bl])
    expect('baseline: a fall passes', rc == 0)

    tb = os.path.join(tmp, 't.json')
    with open(tb, 'w') as f:
        json.dump({'a': 5, 'b': 0, 'gone': 3}, f)
    rc, _ = run([write('t.html', page(brief('a', BAD2), brief('b', BAD2))), '--tighten', tb])
    got = json.load(open(tb))
    expect('tighten: lowers to current, never raises, drops gone briefs (got %s)' % got,
           rc == 0 and got == {'a': 2, 'b': 0})
    rc, _ = run([write('t2.html', page(brief('a', BAD2 + BAD2), brief('b', BAD2))), '--tighten', tb])
    expect('tighten: a rise leaves the number alone', json.load(open(tb)) == {'a': 2, 'b': 0})

    base2 = write('base2.html', page(brief('a', BAD1), brief('b', BAD1)))
    rc, out = run([write('touch.html', page(brief('a', BAD1), brief('b', BAD1 + OK))), '--touched', base2])
    expect('touched: a changed brief with hits fails', rc == 1 and 'touched brief b' in out and 'brief a' not in out)
    rc, _ = run([base2, '--touched', base2])
    expect('touched: an unchanged brief with hits passes', rc == 0)
    rc, _ = run([write('touch_ok.html', page(brief('a', BAD1), brief('b', OK))), '--touched', base2])
    expect('touched: a changed clean brief passes', rc == 0)
    attr = write('attr.html', page(brief('a', BAD1), brief('b', BAD1.replace('<p>', '<p class="x" data-k="1">'))))
    rc, _ = run([attr, '--touched', base2])
    expect('touched: a markup or attribute change with equal text is not a touch', rc == 0)
    rc, out = run([write('hov.html', page(brief('a', BAD1), brief('b', BAD1.replace('</p>', '<span class="sp-pop-b">new</span></p>')))),
                   '--touched', base2])
    expect('touched: a hover text change is a touch', rc == 1 and 'touched brief b' in out)
    rc, out = run([base, '--brief', 'a'])
    expect('--brief lists the hit text', rc == 0 and 'Fix the class, not the instance.' in out)
finally:
    shutil.rmtree(tmp)

print('test_prose_lint: %d passed, %d failed' % (ok, bad))
sys.exit(1 if bad else 0)
