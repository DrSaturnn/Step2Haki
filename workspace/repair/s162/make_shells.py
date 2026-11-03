"""s162 launch (lead): card shells for the four B4 cards of 02 Antipsychotics (empty banks: Q4 keep, no item moves from
antipsych-effects or tca-tox), and the s162 site layer (nav links live for the four cards, Psych Pharmacology counts
14 -> 18, "18 of 18 class cards"). Shells go after pc-maoi, before mood-anticonv, in sidebar order.
Run from workspace/: python3 repair/s162/make_shells.py"""
import json, sys, os
sys.path.insert(0, 'tools')
import pagelib as p

PAGE = '../discriminator-briefs-site/index.html'
h = p.read_page(PAGE)
for bank in ('pcatyp-bank', 'pctyp-bank', 'pcachol-bank', 'pctd-bank'):
    assert ('id="%s"' % bank) not in h, bank
for cid in ('pc-atypical', 'pc-typical', 'pc-antichol', 'pc-td'):
    assert ('id="%s"' % cid) not in h, cid

def shell(cid, grp, title, sub, bank):
    return ('<div class="brief sp pc" id="%s" data-shelf="psych" data-bp="behav">\n'
            '<p class="pc-grp">%s</p>\n<h4>%s</h4>\n<p class="sub">%s</p>\n'
            '<h5 class="authored-hdr" id="%s">Practice</h5>\n<ol class="bank authored">\n\n</ol>\n</div>'
            % (cid, grp, title, sub, bank))

G2 = '02 Antipsychotics <span>&middot;</span> class card'
D = ' &middot; '
NEW = {
 'ATYP': dict(cid='pc-atypical', after='pc-maoi', bank='pcatyp-bank', title='Atypical antipsychotics',
   sub=D.join(['second-generation antipsychotics', 'aripiprazole', 'asenapine', 'brexpiprazole', 'cariprazine', 'clozapine',
               'iloperidone', 'lumateperone', 'lurasidone', 'olanzapine', 'paliperidone', 'quetiapine', 'risperidone', 'ziprasidone'])),
 'TYP': dict(cid='pc-typical', after='pc-atypical|pc-maoi', bank='pctyp-bank', title='Typical antipsychotics',
   sub=D.join(['first-generation antipsychotics', 'chlorpromazine', 'fluphenazine', 'haloperidol', 'loxapine', 'molindone',
               'perphenazine', 'pimozide', 'thioridazine', 'thiothixene', 'trifluoperazine'])),
 'ACHOL': dict(cid='pc-antichol', after='pc-typical|pc-atypical|pc-maoi', bank='pcachol-bank', title='Anticholinergic',
   sub=D.join(['anticholinergics for antipsychotic movement effects', 'benztropine', 'diphenhydramine', 'trihexyphenidyl'])),
 'TD': dict(cid='pc-td', after='pc-antichol|pc-typical|pc-atypical|pc-maoi', bank='pctd-bank', title='Tardive dyskinesia agents',
   sub=D.join(['VMAT2 inhibitors', 'valbenazine', 'deutetrabenazine'])),
}
for k, s in NEW.items():
    d = 'repair/migration/pharm/%s/spine' % k
    os.makedirs(d, exist_ok=True)
    out = {'edits': [{'op': 'new_brief', 'after': s['after'],
        'html': shell(s['cid'], G2, s['title'], s['sub'], s['bank']),
        'note': 's162 card shell: %s (%s); Q4 keep, no item moved' % (s['cid'], s['title'])}]}
    json.dump(out, open('%s/05_%s_new.json' % (d, s['cid'].replace('-', '_')), 'w'), indent=1, ensure_ascii=False)

def nav_line(t, href=None):
    return '    <a href="#psych-pharm" class="pc-plan" title="Planned card">%s</a>' % t if href is None else '    <a href="#%s">%s</a>' % (href, t)
ed = []
for t, href in [('Atypical antipsychotics', 'pc-atypical'), ('Typical antipsychotics', 'pc-typical'),
                ('Anticholinergic', 'pc-antichol'), ('Tardive dyskinesia agents', 'pc-td')]:
    ed.append({'op': 'replace_global', 'find': nav_line(t) + '\n', 'with': nav_line(t, href) + '\n'})
ed.append({'op': 'replace_global', 'find': 'Psych Pharmacology <span class="count">14</span>', 'with': 'Psych Pharmacology <span class="count">18</span>'})
ed.append({'op': 'replace_global', 'find': 'Psych Pharmacology <span class="n">14 of 18 class cards</span>', 'with': 'Psych Pharmacology <span class="n">18 of 18 class cards</span>'})
for e in ed:
    assert h.count(e['find']) == 1, e['find']
json.dump({'marker': '<a href="#pc-atypical">Atypical antipsychotics</a>',
           'note': 's162 site layer: nav links and counts for the four B4 cards (02 Antipsychotics); no planned card left',
           'edits': ed}, open('repair/s162/01_pharm_s162.json', 'w'), indent=1, ensure_ascii=False)
print('shells', len(NEW), 'site edits', len(ed))
