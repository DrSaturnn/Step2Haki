#!/usr/bin/env python3
"""s159 site layer (Psych Pharmacology section, batch 1 of 4): writes repair/s159/01_pharm_section.json from the live
page, using the approved mockup v3 (repair/pilots/psych-pharm/: pc_nav.html, pc_css.html) minus its review furniture.
  python3 repair/s159/gen_section.py
Live cards in B1: pc-snri, pc-antidep, pc-maoi; the other 15 are greyed planned entries (CARD_SPEC.md section 6)."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, '..', '..'))
LIVE = {'SNRIs': 'pc-snri', 'Other antidepressants': 'pc-antidep', 'MAOIs': 'pc-maoi'}
GROUPS = [('01 Antidepressants', ['SSRIs', 'SNRIs', 'Other antidepressants', 'TCAs', 'MAOIs']),
          ('02 Antipsychotics', ['Atypical antipsychotics', 'Typical antipsychotics', 'Anticholinergic', 'Tardive dyskinesia agents']),
          ('03 Mood and cognition', ['Lithium and anticonvulsants', 'Cognitive agents']),
          ('04 Anxiety and benzodiazepines', ['Benzodiazepines', 'Other anxiety agents']),
          ('05 ADHD and sleep', ['ADHD', 'Sleep agents', 'Orexin antagonists']),
          ('06 Substance use and other', ['Substance use and cessation', 'Other agents'])]


def nav():
    out = ['    <div class="sect pc-sect">Psych Pharmacology <span class="count">%d</span></div>' % len(LIVE)]
    for g, cards in GROUPS:
        out.append('    <div class="navsub">%s</div>' % g)
        for c in cards:
            if c in LIVE:
                out.append('    <a href="#%s">%s</a>' % (LIVE[c], c))
            else:
                out.append('    <a href="#psych-pharm" class="pc-plan" title="Planned card">%s</a>' % c)
    return '\n'.join(out)


CSS = """<style id="ax-s159">
/* ============ s159: Psych Pharmacology class cards (CARD_SPEC.md; mockup v3, page tokens only) ============ */
#navlinks .pc-sect{color:var(--accent)}
html body #nav #navlinks a.pc-plan{color:var(--faint)!important;-webkit-text-fill-color:var(--faint);opacity:.75;font-weight:400}
.brief.pc .pc-grp{margin:0 0 6px;font-size:12px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--accent)}
.brief.pc .pc-grp span{color:var(--faint);padding:0 4px}
.brief.pc .pc-tn{color:var(--muted);font-size:.92em;padding-left:4px}
.brief.pc .pc-uv{display:inline-block;margin-left:6px;font-size:12px;font-weight:500;color:var(--caution);background:var(--caution-bg);border-radius:var(--r-chip);padding:1px 7px}
.brief.pc .pc-blocks{margin-top:18px}
.brief.pc .pc-note{margin:6px 0 0;font-size:14px;color:var(--muted)}
.brief.pc .pc-tbl{margin-top:18px}
.brief.pc .pc-lcw{margin-top:18px}
.brief.pc .pc-owners{margin:20px 0 0;padding:12px 18px;border-radius:var(--r-sub);background:var(--recess);box-shadow:var(--inner-2)}
.brief.pc .pc-owners .lbl{display:block;font-size:12px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--accent);margin-bottom:4px}
.brief.pc .pc-owners p{margin:6px 0;color:var(--ink-2)}
.brief.pc .pc-nbq{margin-top:20px}
</style>
"""

HEAD = ('\n\n<!-- =================== PSYCH PHARM =================== -->\n'
        '<h3 class="system" id="psych-pharm">Psych Pharmacology <span class="n">%d of 18 class cards</span></h3>\n'
        '<p class="system-note">One short card per drug class, grouped as in the pharm documents. Each card holds what the '
        'drug does; the disease briefs keep the choice of drug.</p>' % len(LIVE))

PROV = '\n\n<div style="margin:70px 0 0;padding:22px 0 0;border-top:2px solid var(--rule)'
NAV_END = '    <a href="#ipv">Intimate Partner Violence</a>\n  </div>\n</aside>'


def main():
    page = open(os.path.join(WS, 'index.html'), encoding='utf-8').read()
    for a in (PROV, NAV_END, '</body>'):
        assert page.count(a) == 1, a[:60]
    spec = {'marker': 'id="psych-pharm"',
            'note': 's159 site layer: the Psych Pharmacology sidebar section and page section (CARD_SPEC.md section 6)',
            'edits': [
                {'op': 'replace_global', 'find': NAV_END,
                 'with': '    <a href="#ipv">Intimate Partner Violence</a>\n' + nav() + '\n  </div>\n</aside>',
                 'note': 's159: Psych Pharmacology sidebar section after Psychiatry; planned cards greyed'},
                {'op': 'replace_global', 'find': PROV, 'with': HEAD + PROV,
                 'note': 's159: Psych Pharmacology page section after the Psychiatry briefs'},
                {'op': 'replace_global', 'find': '</body>', 'with': CSS + '</body>',
                 'note': 's159: class card styles on theme tokens'}]}
    json.dump(spec, open(os.path.join(HERE, '01_pharm_section.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print('01_pharm_section.json: %d ops' % len(spec['edits']))


if __name__ == '__main__':
    main()
