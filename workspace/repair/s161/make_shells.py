"""s161 launch (lead): card shells for the four new B3 cards (empty banks: Q4 keep, no item moves from ssri-effects,
tca-tox, lithium-effects or dementia), and the s161 site layer (mood-anticonv becomes the Lithium and anticonvulsants
card shell in place, keeps its id and its 9 items, moves into Psych Pharmacology after pc-maoi; nav and counts).
Run from workspace/: python3 repair/s161/make_shells.py"""
import json, sys, os
sys.path.insert(0, 'tools')
import pagelib as p

PAGE = '../discriminator-briefs-site/index.html'
h = p.read_page(PAGE)
live = {}
for it in p.items(h):
    if it.brief_id == 'mood-anticonv':
        live.setdefault(it.brief_id, {})[it.id] = h[it.start:it.end]
b0 = p.brief_by_id(h, 'mood-anticonv')
nid_mac = p.attrs(h[b0.start:h.index('>', b0.start) + 1])['data-nid'].split()
for bank in ('pcssri-bank', 'pctca-bank', 'pccog-bank', 'pcoth-bank'):
    assert ('id="%s"' % bank) not in h, bank

def shell(cid, nids, grp, title, sub, bank, lis):
    nid = (' data-nid="%s"' % ' '.join(nids)) if nids else ''
    return ('<div class="brief sp pc" id="%s" data-shelf="psych" data-bp="behav"%s>\n'
            '<p class="pc-grp">%s</p>\n<h4>%s</h4>\n<p class="sub">%s</p>\n'
            '<h5 class="authored-hdr" id="%s">Practice</h5>\n<ol class="bank authored">\n%s\n</ol>\n</div>'
            % (cid, nid, grp, title, sub, bank, lis))

G1 = '01 Antidepressants <span>&middot;</span> class card'
G3 = '03 Mood and cognition <span>&middot;</span> class card'
G6 = '06 Substance use and other <span>&middot;</span> class card'
D = ' &middot; '
NEW = {
 'SSRI': dict(cid='pc-ssri', after='#psych-pharm', bank='pcssri-bank', grp=G1, title='SSRIs',
   sub=D.join(['selective serotonin reuptake inhibitors', 'citalopram', 'escitalopram', 'fluoxetine', 'fluvoxamine', 'paroxetine', 'sertraline'])),
 'TCA': dict(cid='pc-tca', after='pc-antidep|pc-snri|pc-ssri|#psych-pharm', bank='pctca-bank', grp=G1, title='TCAs',
   sub=D.join(['tricyclic antidepressants', 'amitriptyline', 'clomipramine', 'desipramine', 'doxepin', 'imipramine', 'nortriptyline', 'protriptyline'])),
 'COG': dict(cid='pc-cog', after='mood-anticonv|pc-maoi', bank='pccog-bank', grp=G3, title='Cognitive agents',
   sub=D.join(['cholinesterase inhibitors', 'donepezil', 'rivastigmine', 'galantamine', 'memantine'])),
 'OTHER': dict(cid='pc-other', after='sud-meds|pc-orexin', bank='pcoth-bank', grp=G6, title='Other agents',
   sub=D.join(['modafinil', 'armodafinil', 'phentermine'])),
}
for k, s in NEW.items():
    d = 'repair/migration/pharm/%s/spine' % k
    os.makedirs(d, exist_ok=True)
    out = {'edits': [{'op': 'new_brief', 'after': s['after'],
        'html': shell(s['cid'], [], s['grp'], s['title'], s['sub'], s['bank'], ''),
        'note': 's161 card shell: %s (%s); Q4 keep, no item moved' % (s['cid'], s['title'])}]}
    json.dump(out, open('%s/05_%s_new.json' % (d, s['cid'].replace('-', '_')), 'w'), indent=1, ensure_ascii=False)

def nav_line(t, href=None):
    return '    <a href="#psych-pharm" class="pc-plan" title="Planned card">%s</a>' % t if href is None else '    <a href="#%s">%s</a>' % (href, t)
MAC_SUB = D.join(['lithium', 'valproate', 'carbamazepine', 'oxcarbazepine', 'lamotrigine', 'topiramate'])
ed = [{'op': 'replace_brief', 'brief': 'mood-anticonv', 'ledger': 'repair/s161/S161.md',
       'html': shell('mood-anticonv', nid_mac, G3, 'Lithium and anticonvulsants', MAC_SUB, 'mac-bank', '\n'.join(live['mood-anticonv'].values())),
       'note': 's161: mood-anticonv becomes the Lithium and anticonvulsants card shell in place (id kept; %d items carried)' % len(live['mood-anticonv'])},
      {'op': 'move_brief', 'brief': 'mood-anticonv', 'after': 'pc-maoi'},
      {'op': 'replace_global', 'find': '    <a href="#mood-anticonv">Anticonvulsant Mood Stabilizers</a>\n', 'with': ''},
      {'op': 'replace_global', 'find': 'Psychiatry &amp; Behavioral Health <span class="count">30</span>', 'with': 'Psychiatry &amp; Behavioral Health <span class="count">29</span>'}]
for t, href in [('SSRIs', 'pc-ssri'), ('TCAs', 'pc-tca'), ('Lithium and anticonvulsants', 'mood-anticonv'),
                ('Cognitive agents', 'pc-cog'), ('Other agents', 'pc-other')]:
    ed.append({'op': 'replace_global', 'find': nav_line(t) + '\n', 'with': nav_line(t, href) + '\n'})
ed.append({'op': 'replace_global', 'find': 'Psych Pharmacology <span class="count">9</span>', 'with': 'Psych Pharmacology <span class="count">14</span>'})
ed.append({'op': 'replace_global', 'find': 'Psych Pharmacology <span class="n">9 of 18 class cards</span>', 'with': 'Psych Pharmacology <span class="n">14 of 18 class cards</span>'})
for e in ed:
    if e['op'] == 'replace_global':
        assert h.count(e['find']) == 1, e['find']
json.dump({'marker': '<a href="#pc-ssri">SSRIs</a>',
           'note': 's161 site layer: mood-anticonv becomes the Lithium and anticonvulsants card shell in place and moves into Psych Pharmacology; nav links and counts for the five B3 cards',
           'edits': ed}, open('repair/s161/01_pharm_s161.json', 'w'), indent=1, ensure_ascii=False)
print('shells', len(NEW), 'site edits', len(ed), 'mac items', len(live['mood-anticonv']), 'nids', len(nid_mac))
