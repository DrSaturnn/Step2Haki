#!/usr/bin/env python3
"""offline tests for tools/style_surface.py (s170): text-only edits plan nothing; scoped rules plan only their combos."""
import os, sys, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
import style_surface as S

BASE_CSS = '.brief{color:#222}.hv{color:#333}#nav a{color:#111}'
BODY = ('<nav id="nav"><a>x</a></nav><section class="brief" id="b1"><p class="hv">one</p></section>'
        '<section class="brief" id="b2"><p>two</p><span class="tag">t</span></section>')


def page(css=BASE_CSS, body=BODY):
    f = tempfile.NamedTemporaryFile('w', suffix='.html', delete=False)
    f.write('<html><head><style>%s</style></head><body>%s</body></html>' % (css, body)); f.close()
    return f.name


def entry(p):
    return {'surface': S.pack(S.surface(p)[0]), 'label': 'base', 'date': 'd', 'views': 'desk,phone',
            'tools': {t: S.fdigest(t) for t in S.THEME_TOOLS}}


R = entry(page())
fails = 0


def check(name, cond):
    global fails
    print(('ok   ' if cond else 'FAIL ') + name)
    fails += not cond


def plan(p):
    sf, soup = S.surface(p)
    return S.plan_legib(sf, soup, R), S.theme_reasons(sf, R, 'desk,phone')


p, t = plan(page(body=BODY.replace('one', 'a new sentence')))
check('text-only edit: legib nothing', not p['runs']); check('text-only edit: theme nothing', not t)
p, t = plan(page(css=BASE_CSS + '#nav a{color:#000}'))
check('chrome-only paint rule: legib nothing', not p['runs']); check('chrome-only paint rule: theme runs', bool(t))
p, t = plan(page(css=BASE_CSS + '[data-theme=dark] .hv{color:#ddd}'))
combos = {(r['theme'], r['mode']) for r in p['runs']}
check('dark-scoped brief rule: dark and tinted only', {c[0] for c in combos} == {'dark', 'tinted'})
check('dark-scoped brief rule: brief b1 only', {b for r in p['runs'] for b in r['briefs']} == {'b1'})
check('dark-scoped brief rule: theme runs', bool(t))
p, t = plan(page(css=BASE_CSS + '@media (max-width:640px){.hv{font-size:12px}}'))
check('phone size-only rule: phone, light, sculpted', [(r['view'], r['theme'], r['mode']) for r in p['runs']] == [('phone', 'light', 'sculpted')])
check('size-only rule: theme nothing', not t)
p, t = plan(page(css=BASE_CSS + '.axm-study .hv:hover::after{color:red}'))
check('study-scoped hover rule: study mode only', {r['mode'] for r in p['runs']} == {'study'})
p, t = plan(page(css=BASE_CSS.replace('.hv{color:#333}', '')))
check('removed brief rule: planned from the record', {b for r in p['runs'] for b in r['briefs']} == {'b1'})
p, t = plan(page(body=BODY.replace('<span class="tag">', '<span class="tag new">')))
check('new class combination: its brief in every combo', {b for r in p['runs'] for b in r['briefs']} == {'b2'} and len(p['runs']) == 18)
check('new class combination: theme runs', bool(t))
p, t = plan(page(css=BASE_CSS + '@media print{.hv{color:#000}}'))
check('print rule: nothing', not p['runs'])
p, _ = plan(page(css=BASE_CSS + '[data-layout=two] .hv{color:#444}'))
check('Two-pane rule: desk and layout two only', {(r['view'], r['layout']) for r in p['runs']} == {('desk', 'two')})
sf, soup = S.surface(page())
check('no record: full sample audit', len(S.plan_legib(sf, soup, None)['runs']) == 18)
print('style_surface tests: %d failed' % fails)
sys.exit(1 if fails else 0)
