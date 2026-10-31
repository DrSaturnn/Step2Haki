"""s160 launch (lead): card shells from the live sedatives, adhd-meds and sud-meds banks (items verbatim, ids unchanged),
the sedatives retirement, and the s160 site layer (adhd-meds and sud-meds become card shells in place, keep their ids,
move into Psych Pharmacology; nav and counts). Run from workspace/: python3 repair/s160/make_shells.py"""
import json, sys, os
sys.path.insert(0, 'tools')
import pagelib as p

PAGE = '../discriminator-briefs-site/index.html'
h = p.read_page(PAGE)
live = {}
for it in p.items(h):
    if it.brief_id in ('sedatives', 'adhd-meds', 'sud-meds'):
        live.setdefault(it.brief_id, {})[it.id] = h[it.start:it.end]
nid_of = {b: p.attrs(h[p.brief_by_id(h, b).start:h.index('>', p.brief_by_id(h, b).start) + 1])['data-nid'].split()
          for b in ('adhd-meds', 'sud-meds')}

def shell(cid, nids, grp, title, sub, bank, ids, src):
    lis = '\n'.join(live[src][i] for i in ids)
    return ('<div class="brief sp pc" id="%s" data-shelf="psych" data-bp="behav" data-nid="%s">\n'
            '<p class="pc-grp">%s</p>\n<h4>%s</h4>\n<p class="sub">%s</p>\n'
            '<h5 class="authored-hdr" id="%s">Practice</h5>\n<ol class="bank authored">\n%s\n</ol>\n</div>'
            % (cid, ' '.join(nids), grp, title, sub, bank, lis))

G4 = '04 Anxiety and benzodiazepines <span>&middot;</span> class card'
G5 = '05 ADHD and sleep <span>&middot;</span> class card'
G6 = '06 Substance use and other <span>&middot;</span> class card'
D = ' &middot; '
NEW = {  # new cards: shells by new_brief (basepage pending shells)
 'BENZO': dict(cid='pc-benzo', after='pc-maoi|pc-antidep|pc-snri|#psych-pharm', bank='pcb-bank', grp=G4,
   title='Benzodiazepines', sub=D.join(['benzodiazepines', 'alprazolam', 'lorazepam', 'clonazepam', 'diazepam', 'chlordiazepoxide']),
   ids=['q_6d24488ee771f06c57d8', 'q_040b0fcf5fffc1646dd9', 'q_aa3df47ddbca173166dc', 'q_1dcb80e3ca4e2333a8c8'],
   nids='1484768396947 1522424066052 1522424264465 1522424293535 1484768639953 1484768625035 1484768616995 1484768607832 1484768590208 1484768467897 1484768634230 1484768629105 1485313553170 1522342829602 1571196998330 1541019852549 1484768571600 1484768559674 1484768412769'.split()),
 'ANXIO': dict(cid='pc-anxiety', after='pc-benzo|pc-maoi', bank='pcx-bank', grp=G4,
   title='Other anxiety agents', sub=D.join(['buspirone', 'hydroxyzine']),
   ids=['q_378c7bd3e3e86b2535ed'],
   nids='1485126664021 1485126687551 1485126691067 1485126694686 1485126682682 1474571677535'.split()),
 'SLEEPAG': dict(cid='pc-sleep', after='adhd-meds', bank='pcz-bank', grp=G5,
   title='Sleep agents', sub=D.join(['nonbenzodiazepine hypnotics (Z-drugs)', 'zolpidem', 'zaleplon', 'eszopiclone', 'ramelteon']),
   ids=['q_91f7d027a965fdd79033', 'q_0851fad94e92ca5f58e7'],
   nids='1484774449158 1484774453774 1484774462533 1484774485137 1484774503031 1484774431076 1484774507229 1484774515042 1484774529881 1484774523790 1484774475310'.split()),
 'OREXIN': dict(cid='pc-orexin', after='pc-sleep|adhd-meds', bank='pco-bank', grp=G5,
   title='Orexin antagonists', sub=D.join(['orexin receptor antagonists', 'suvorexant']),
   ids=['q_e0b108e984d1a6a011eb'],
   nids='1484774536659 1484774544152 1484774546391 1484774548427 1484774539040'.split()),
}
KEEP = {  # s157 briefs that map to one card keep their id: shell by replace_brief in the site layer
 'adhd-meds': dict(grp=G5, title='ADHD', sub=D.join(['stimulants', 'atomoxetine', 'alpha-2 agonists']), bank='adm-bank'),
 'sud-meds': dict(grp=G6, title='Substance use and cessation',
   sub=D.join(['naltrexone', 'acamprosate', 'disulfiram', 'buprenorphine', 'methadone', 'varenicline', 'nicotine replacement']), bank='sud-bank'),
}
used = set(i for s in NEW.values() for i in s['ids'])
assert used == set(live['sedatives']), (set(live['sedatives']) ^ used)
for k, s in NEW.items():
    d = 'repair/migration/pharm/%s/spine' % k
    os.makedirs(d, exist_ok=True)
    out = {'edits': [{'op': 'new_brief', 'after': s['after'],
        'html': shell(s['cid'], s['nids'], s['grp'], s['title'], s['sub'], s['bank'], s['ids'], 'sedatives'),
        'note': 's160 card shell: %s (%s), %d item(s) moved from sedatives, ids unchanged' % (s['cid'], s['title'], len(s['ids']))}]}
    json.dump(out, open('%s/05_%s_new.json' % (d, s['cid'].replace('-', '_')), 'w'), indent=1, ensure_ascii=False)
json.dump({'edits': [{'op': 'retire_brief', 'brief': 'sedatives', 'alias_before': 'pc-benzo', 'ledger': 'repair/s160/S160.md'}]},
          open('repair/migration/pharm/BENZO/spine/06_sedatives_retire.json', 'w'), indent=2)

def nav_line(t, href=None):
    return '    <a href="#psych-pharm" class="pc-plan" title="Planned card">%s</a>' % t if href is None else '    <a href="#%s">%s</a>' % (href, t)
ed = []
for bid, s in KEEP.items():
    ed.append({'op': 'replace_brief', 'brief': bid, 'ledger': 'repair/s160/S160.md',
               'html': shell(bid, nid_of[bid], s['grp'], s['title'], s['sub'], s['bank'], list(live[bid]), bid),
               'note': 's160: %s becomes the %s card shell in place (id kept; %d items carried)' % (bid, s['title'], len(live[bid]))})
ed.append({'op': 'move_brief', 'brief': 'adhd-meds', 'after': 'pc-maoi'})
ed.append({'op': 'move_brief', 'brief': 'sud-meds', 'after': 'adhd-meds'})
ed.append({'op': 'replace_global', 'find': '    <a href="#adhd-meds">ADHD Medications</a>\n    <a href="#sud-meds">Medications for Substance Use Disorders</a>\n', 'with': ''})
ed.append({'op': 'replace_global', 'find': 'Psychiatry &amp; Behavioral Health <span class="count">33</span>', 'with': 'Psychiatry &amp; Behavioral Health <span class="count">31</span>'})
for t, href in [('Benzodiazepines', 'pc-benzo'), ('Other anxiety agents', 'pc-anxiety'), ('ADHD', 'adhd-meds'),
                ('Sleep agents', 'pc-sleep'), ('Orexin antagonists', 'pc-orexin'), ('Substance use and cessation', 'sud-meds')]:
    ed.append({'op': 'replace_global', 'find': nav_line(t) + '\n', 'with': nav_line(t, href) + '\n'})
ed.append({'op': 'replace_global', 'find': 'Psych Pharmacology <span class="count">3</span>', 'with': 'Psych Pharmacology <span class="count">9</span>'})
ed.append({'op': 'replace_global', 'find': 'Psych Pharmacology <span class="n">3 of 18 class cards</span>', 'with': 'Psych Pharmacology <span class="n">9 of 18 class cards</span>'})
for e in ed:
    if e['op'] == 'replace_global':
        assert h.count(e['find']) == 1, e['find']
json.dump({'marker': '<a href="#pc-benzo">Benzodiazepines</a>',
           'note': 's160 site layer: adhd-meds and sud-meds become card shells in place and move into Psych Pharmacology; nav links and counts for the six B2 cards',
           'edits': ed}, open('repair/s160/01_pharm_s160.json', 'w'), indent=1, ensure_ascii=False)
print('shells', len(NEW), 'keep', len(KEEP), 'site edits', len(ed))
