#!/usr/bin/env python3
"""rewrite_lanes (s170 T1; CONTENT_BATCHES_S170 T1, runbook 8b item 2): one rewrite lane per live brief for the content
batches (s170 to s180), where a lane rewrites lines under TEXTBOOK_STYLE and keeps every fact and claim id.
The lane contract is tools/spine/REWRITE_CONTRACT.md.

  python3 tools/spine/rewrite_lanes.py setup <spec.json> [--only id,id]
  python3 tools/spine/rewrite_lanes.py collect <batch> <id>      rewrite_<batch>/rewrite_<batch>.json -> delta_<batch>.json
                                                                 and facts_spec_<batch>.json
  python3 tools/spine/rewrite_lanes.py check <batch> <id>        collect, facts, build.py, then the meaning lock, prose lint
                                                                 (touched) and content_gate on the rebuilt brief; one line
                                                                 per failure, exit 1 on any (the lane runs this itself)

spec.json:
  {"batch": "s170", "plan_step": "s170", "audit": "local/s170/audit", "plan": "<private>/claude/pending/CONTENT_BATCHES_S170.md",
   "briefs": [{"id": "pc-snri", "role": "brief-build", "budget": 60, "items": ["N1", "N3", "N9"], "calls": ["C10"],
               "notes": "free text for this lane"}]}

setup, per brief (the s150e layout, so patch.py s3, review and verify work unchanged):
  <folder>/baseline_<batch>.html (the live brief), baseline_brief_text_<batch>.txt, claims_before_, facts_before_ and
  build_before_ copies (once), outline.json moved to outline_before_<batch>.json (pharm cards, so verify runs build.py),
  build.py calling repair/migration/spine/<batch>_delta.py, an empty facts_spec_<batch>.json; and <folder>/rewrite_<batch>/:
  units.json and units.md (every rewritable unit with its exact html, text, claim ids and prose hits), header_map.md,
  nbme.md, step2.md, items.md, INSTRUCTIONS.md (writing card + REWRITE_CONTRACT.md) and a rewrite_<batch>.json template.
  Launch prompt: local/<batch>/rewrite_prompts/<id>.txt.

Units (non-overlapping, outermost wins): p, li, tr, caption, figcaption, h5, span.lbl, span.sk, span.sp-src, b.sp-f,
b.nm, span.win, span.sp-pop-b; a p holding a hover is one unit with its hover. Excluded: the Practice section (from the
authored-hdr h5), script, style, nav.
"""
import csv
import glob
import html as H
import json
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, '..', '..'))
PRIV = os.environ.get('AX_PRIVATE', '/home/claude/step2haki-private')
sys.path.insert(0, os.path.join(WS, 'tools'))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(WS, 'repair', 'pilots', 's167c'))
import pagelib as P  # noqa: E402
from hovers import tree, walk  # noqa: E402  (offset tree, no DOM re-serialization)

UNIT = {'p': None, 'li': None, 'tr': None, 'caption': None, 'figcaption': None, 'h5': None,
        'span': {'lbl', 'sk', 'sp-src', 'win', 'sp-pop-b'}, 'b': {'sp-f', 'nm'}}
SKIP = {'script', 'style', 'nav'}
BUILD = '''#!/usr/bin/env python3
"""{batch} content rewrite replay on the shipped brief (tools/spine/REWRITE_CONTRACT.md). Prior builder archived as build_before_{batch}.py."""
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
WS=next(p for p in HERE.parents if (p/'repair/migration/spine').is_dir())
sys.path.insert(0,str(WS/'repair/migration/spine'))
from {batch}_delta import build
if __name__=='__main__':build(HERE)
'''


def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, cwd=WS)


def folder_of(bid):
    out = sh([sys.executable, os.path.join(HERE, 'folder_of.py'), bid]).stdout.split()
    if len(out) < 2:
        raise SystemExit('rewrite_lanes: no folder for %s' % bid)
    return os.path.join(WS, out[-1])


def plain(s):
    import meaning_lock as ML
    return ML.plain(s)


def key(s):
    return re.sub(r'\s+', '', s).lower()


def norm(s):
    return re.sub(r'\s+', ' ', s or '').strip()


def is_unit(n):
    if n.tag not in UNIT:
        return False
    want = UNIT[n.tag]
    return want is None or bool(want & set(n.cls()))


def units_of(outer):
    """[{uid, step, step_name, sel, start, end, html, text}] for one brief's outer html."""
    stop = outer.find('<h5 class="authored-hdr')
    stop = len(outer) if stop < 0 else stop
    heads = [(m.start(), int(m.group(1)), m.group(2).strip()) for m in
             re.finditer(r'<h5 class="tsec sp-h" id="[^"]*"><b class="sp-n">(\d)</b>([^<]*)</h5>', outer)]
    root = tree(outer)
    out = []

    def visit(n):
        for k in n.kids:
            if k.tag == '#text' or k.s >= stop:
                continue
            if k.tag in SKIP:
                continue
            if is_unit(k) and k.cs is not None:
                h = outer[k.s:k.e]
                t = plain(h)
                if t:
                    st = [x for x in heads if x[0] <= k.s]
                    out.append({'start': k.s, 'end': k.e, 'html': h, 'text': t, 'sel': k.tag + ''.join('.' + c for c in k.cls()),
                                'step': st[-1][1] if st else 0, 'step_name': st[-1][2] if st else 'Header'})
                continue
            visit(k)
    visit(root)
    for i, u in enumerate(out):
        u['uid'] = 'U%03d' % (i + 1)
    return out


def claims_for(units, cm):
    """claim ids per unit: 'in' (the claim's text sits inside the unit) and 'part' (the unit's text sits inside a longer
    claim of 4+ words); keys ignore whitespace."""
    ck = [(c['id'], key(c.get('new_text', ''))) for c in cm.get('claims', []) if c.get('new_text')]
    for u in units:
        uk = key(u['text'])
        u['claims_in'] = [cid for cid, k in ck if k and k in uk]
        u['claims_part'] = [cid for cid, k in ck if len(u['text'].split()) >= 4 and uk in k and k not in uk]


def hits_for(units, inner):
    import prose_lint as pl
    hits = pl.lint_brief(inner, touched=True)
    left = []
    for h in hits:
        hk = key(h['text'])[:80]
        u = next((u for u in units if hk and hk in key(u['text'])), None)
        if u is None:
            hk2 = key(h.get('match', ''))
            u = next((u for u in units if hk2 and len(hk2) > 6 and hk2 in key(u['text'])), None)
        if u is None:
            left.append(h)
        else:
            u.setdefault('hits', []).append('%s (%s): %s' % (h['pattern'], h['region'], h['match'][:60]))
    return hits, left


def audit_rows(audit, name, bid):
    p = os.path.join(audit, name)
    if not os.path.exists(p):
        return None
    return [r for r in csv.DictReader(open(p, encoding='utf-8')) if r.get('brief') == bid]


def md_table(rows, cols):
    if not rows:
        return '(none)\n'
    out = '| ' + ' | '.join(cols) + ' |\n|' + '---|' * len(cols) + '\n'
    for r in rows:
        out += '| ' + ' | '.join(str(r.get(c, '')).replace('|', '/').replace('\n', ' ') for c in cols) + ' |\n'
    return out


HDR_SEL = 'caption, th, h5, span.lbl, span.sk, span.sp-ct, span.sp-k, b.pp-t, p.kick, div.ttl > span'


def header_strings(outer):
    """normalized texts of the brief's header elements (an h5 without its step number)."""
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(outer, 'lxml')
    for n in soup.select('b.sp-n'):
        n.decompose()
    return {norm(e.get_text(' ')) for e in soup.select(HDR_SEL)}


def header_map(outer):
    hd = json.load(open(os.path.join(WS, 'repair', 'efficiency', 'HEADERS.json'), encoding='utf-8'))
    have = header_strings(outer)
    text = '\n'.join(sorted(have))
    rows = []
    for r in hd.get('rows', []):
        for s in r.get('live', []):
            if s and norm(s) in have:
                rows.append({'id': r['id'], 'kind': r.get('kind', ''), 'live': s, 'name': r.get('name', ''), 'status': r.get('status', '')})
    pats = [p for p in hd.get('retired_patterns', []) if re.search(p, text, re.M)]
    out = '# Header map for this brief (repair/efficiency/HEADERS.json rows whose live string occurs here)\n\n'
    out += 'Rename each live string to its approved name. A header you write must be an approved name, an allowed header or one\n'
    out += 'the page already carries (prose_lint header_new on a touched brief). "Result" is renamed only in interaction tables (H20).\n\n'
    out += md_table(rows, ['id', 'kind', 'live', 'name', 'status'])
    if pats:
        out += '\nRetired patterns that match a line here: ' + '; '.join('`%s`' % p for p in pats) + '\n'
    return out


def plan_rows(plan, items, calls):
    if not plan or not os.path.exists(plan):
        return '(plan file not found: %s)\n' % plan
    t = open(plan, encoding='utf-8').read().splitlines()
    out = ['# Items and calls for this lane (from %s)\n' % os.path.relpath(plan, PRIV) if plan.startswith(PRIV) else plan, '']
    for n in items:
        rows = []
        for i, l in enumerate(t):
            if re.match(r'^- %s\b' % re.escape(n), l):
                rows.append(l)
                for l2 in t[i + 1:]:
                    if not l2.startswith('  ') or not l2.strip():
                        break
                    rows.append(l2)
        out += ['## %s' % n] + (rows or ['(no "- %s" line in the plan)' % n]) + ['']
    out += ['## Calls (as adopted)', '']
    for c in calls:
        rows = [l for l in t if l.startswith('| %s |' % c)]
        out += rows or ['(no row for %s)' % c]
    return '\n'.join(out) + '\n'


def write_units_md(path, bid, units, left):
    out = ['# Units of %s (rewrite one unit by writing its new html in rewrite_*.json; leave the rest alone)' % bid, '']
    step = None
    for u in units:
        if u['step'] != step:
            step = u['step']
            out += ['', '## Step %s %s' % (u['step'], u['step_name']), '']
        tags = []
        if u['claims_in']:
            tags.append('claims ' + ','.join(u['claims_in']))
        if u['claims_part']:
            tags.append('part of ' + ','.join(u['claims_part']))
        if u.get('hits'):
            tags.append('HITS: ' + ' | '.join(u['hits']))
        out.append('- **%s** `%s` %s%s' % (u['uid'], u['sel'], u['text'][:300], ('  [' + '; '.join(tags) + ']') if tags else ''))
    if left:
        out += ['', '## Prose hits not mapped to a unit (find the line and name the unit it sits in)', '']
        out += ['- %s (%s, %s): %s' % (h['pattern'], h['region'], h['tag'], h['text'][:160]) for h in left]
    open(path, 'w', encoding='utf-8').write('\n'.join(out) + '\n')


def delta_tool(batch):
    """s171: build.py imports repair/migration/spine/<batch>_delta.py; copy the newest content-batch delta tool
    (s170 on) and rename it when the batch has none, since the lanes cannot write outside their folders."""
    sd = os.path.join(WS, 'repair', 'migration', 'spine')
    dst = os.path.join(sd, '%s_delta.py' % batch)
    if os.path.exists(dst):
        return 'delta tool: %s_delta.py present' % batch
    num = lambda n: int(re.match(r's(\d+)', n).group(1))
    cands = sorted((n for n in os.listdir(sd) if re.fullmatch(r's\d+_delta\.py', n) and num(n) >= 170
                    and num(n) < num(batch)), key=num)
    if not cands:
        return 'delta tool: none to copy (write %s_delta.py by hand)' % batch
    src = cands[-1][:-len('_delta.py')]
    open(dst, 'w', encoding='utf-8').write(open(os.path.join(sd, cands[-1]), encoding='utf-8').read().replace(src, batch))
    return 'delta tool: %s_delta.py written from %s' % (batch, cands[-1])


def lane(spec, b, page):
    batch, bid = spec['batch'], b['id']
    f = folder_of(bid)
    rd = os.path.join(f, 'rewrite_%s' % batch)
    os.makedirs(rd, exist_ok=True)
    br = P.brief_by_id(page, bid)
    if not br:
        return '%s: not on the page' % bid
    import site_build   # s164c pages wrap each brief's inner html in <template class="axl">; the baseline is unwrapped
    outer = site_build.unwrap(page[br.start:br.end])
    title = re.sub(r'<[^>]+>', '', (re.search(r'<h4[^>]*>(.*?)</h4>', outer, re.S) or [None, bid])[1]).strip()
    note = []
    bh = os.path.join(f, 'brief.html')
    if os.path.exists(bh) and open(bh, encoding='utf-8').read() != outer:
        note.append('brief.html differs from live (baseline is the live brief)')
    import review_packet as RP
    open(os.path.join(f, 'baseline_%s.html' % batch), 'w', encoding='utf-8').write(outer)
    open(os.path.join(f, 'baseline_brief_text_%s.txt' % batch), 'w', encoding='utf-8').write(RP.text_of(outer) + '\n')
    for a, c in (('claim_map.json', 'claims_before_%s.json'), ('facts.json', 'facts_before_%s.json'), ('build.py', 'build_before_%s.py')):
        if os.path.exists(os.path.join(f, a)) and not os.path.exists(os.path.join(f, c % batch)):
            shutil.copy(os.path.join(f, a), os.path.join(f, c % batch))
    if not os.path.exists(os.path.join(f, 'facts_before_%s.json' % batch)):
        json.dump({'facts': []}, open(os.path.join(f, 'facts_before_%s.json' % batch), 'w'))
    if os.path.exists(os.path.join(f, 'outline.json')):
        os.replace(os.path.join(f, 'outline.json'), os.path.join(f, 'outline_before_%s.json' % batch))
        note.append('outline.json moved to outline_before_%s.json' % batch)
    open(os.path.join(f, 'build.py'), 'w').write(BUILD.replace('{batch}', batch))
    fs = os.path.join(f, 'facts_spec_%s.json' % batch)
    if not os.path.exists(fs):
        json.dump({'out': os.path.relpath(os.path.join(f, 'facts_%s.json' % batch), WS), 'population': 'as in the brief'},
                  open(fs, 'w'), ensure_ascii=False, indent=1)
    cm = json.load(open(os.path.join(f, 'claims_before_%s.json' % batch), encoding='utf-8'))
    units = units_of(outer)
    claims_for(units, cm)
    hits, left = hits_for(units, br.inner)
    json.dump({'brief': bid, 'batch': batch, 'units': units}, open(os.path.join(rd, 'units.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    write_units_md(os.path.join(rd, 'units.md'), bid, units, left)
    open(os.path.join(rd, 'header_map.md'), 'w', encoding='utf-8').write(header_map(outer))
    audit = os.path.join(WS, spec.get('audit', 'local/%s/audit' % batch))
    if not os.path.exists(os.path.join(audit, 'summary.json')):
        sh([sys.executable, os.path.join(HERE, 'content_audit.py'), os.path.join(WS, 'index.html'), audit])
    nb = audit_rows(audit, 'nbme_blocks.csv', bid)
    s2 = audit_rows(audit, 'step2.csv', bid)
    open(os.path.join(rd, 'nbme.md'), 'w', encoding='utf-8').write(
        '# NBME blocks outside the bank in %s (content_audit nbme_blocks.csv; pause = 1 sits in a pause point)\n\n' % bid
        + 'A changed brief keeps none outside a pause point (gate nbme-block): carry each block\'s separating stem details into\n'
        + 'the brief\'s lines, then remove the block (new "" with carried_by), unless items.md says to keep it.\n\n'
        + (md_table(nb, ['kind', 'label', 'pause', 'words', 'hash', 'text']) if nb is not None else '(audit missing)\n'))
    open(os.path.join(rd, 'step2.md'), 'w', encoding='utf-8').write(
        '# Step 2 (criteria) lines in %s with their heuristic sort (content_audit step2.csv)\n\n' % bid
        + 'Step 2 holds criteria only; a workup ladder there fails gate step2-workup. A block you move to another step needs a\n'
        + 'row in repair/%s/step_moves.json (brief, hash, from, to, class, reason), written by the lead from your notes.\n\n' % batch
        + (md_table(s2, ['block', 'block_tag', 'sort', 'line']) if s2 is not None else '(audit missing)\n'))
    open(os.path.join(rd, 'items.md'), 'w', encoding='utf-8').write(
        plan_rows(spec.get('plan'), b.get('items', []), b.get('calls', [])) + ('\n## Lead notes\n\n%s\n' % b['notes'] if b.get('notes') else ''))
    tpl = os.path.join(rd, 'rewrite_%s.json' % batch)
    if not os.path.exists(tpl):
        json.dump({'brief': bid, 'units': [], 'raw': [], 'new_claims': [], 'facts_local': {}}, open(tpl, 'w'), indent=1)
    import style_card
    fill = {'batch': batch, 'bid': bid, 'title': title, 'folder': os.path.relpath(f, WS), 'rd': os.path.relpath(rd, WS),
            'role': b.get('role', 'brief-rewrite'), 'budget': b.get('budget', 40), 'n_units': len(units), 'n_hits': len(hits),
            'style': os.path.join('repair', 'efficiency', 'TEXTBOOK_STYLE.md')}
    t = open(os.path.join(HERE, 'REWRITE_CONTRACT.md'), encoding='utf-8').read()
    for k, v in fill.items():
        t = t.replace('{%s}' % k, str(v))
    leftover = sorted(set(re.findall(r'\{([a-z_]+)\}', t)))
    if leftover:
        return '%s: contract placeholders unfilled: %s' % (bid, ', '.join(leftover))
    open(os.path.join(rd, 'INSTRUCTIONS.md'), 'w', encoding='utf-8').write(style_card.card() + '\n---\n\n' + t)
    pdir = os.path.join(WS, 'local', batch, 'rewrite_prompts')
    os.makedirs(pdir, exist_ok=True)
    open(os.path.join(pdir, bid + '.txt'), 'w', encoding='utf-8').write(
        'Role: %s\nPlan step: %s\nLane: %s\nBudget: %d\n\nRead rewrite_%s/INSTRUCTIONS.md in your lane first.\n'
        % (fill['role'], spec.get('plan_step', batch), f, fill['budget'], batch))
    return '%s: lane ready (%s; %d units, %d prose hits, %d unmapped; nbme %s; claims %d)%s' % (
        bid, fill['rd'], len(units), len(hits), len(left), len([r for r in (nb or []) if r.get('pause') == '0']),
        len(cm.get('claims', [])), ('; ' + '; '.join(note)) if note else '')


# ---------------------------------------------------------------- collect
def collect(batch, bid):
    """rewrite_<batch>.json -> delta_<batch>.json + facts_spec_<batch>.json. Returns a list of problems (empty = ok)."""
    f = folder_of(bid)
    rd = os.path.join(f, 'rewrite_%s' % batch)
    rw = json.load(open(os.path.join(rd, 'rewrite_%s.json' % batch), encoding='utf-8'))
    U = {u['uid']: u for u in json.load(open(os.path.join(rd, 'units.json'), encoding='utf-8'))['units']}
    base = open(os.path.join(f, 'baseline_%s.html' % batch), encoding='utf-8').read()
    cm = json.load(open(os.path.join(f, 'claims_before_%s.json' % batch), encoding='utf-8'))
    claim_text = {c['id']: norm(c.get('new_text', '')) for c in cm.get('claims', [])}
    # s171 fix (round 1 systemic finding 1): a claim whose text sits in more than one unit (one-word labels such as
    # "Borderline") is owned by none of them; the last rewritten unit used to take it over. Such a claim moves only
    # when a unit or raw names it in "claims"; check() fails when its text leaves the rebuilt brief.
    owners = {}
    for u in U.values():
        for cid in u.get('claims_in', []):
            owners[cid] = owners.get(cid, 0) + 1
    shared = {cid for cid, n in owners.items() if n > 1}
    ck = [(c['id'], key(c.get('new_text', ''))) for c in cm.get('claims', []) if c.get('new_text')]
    probs, changes = [], []
    seen = set()
    for x in rw.get('units', []):
        uid = x.get('uid')
        if uid not in U:
            probs.append('unit %s is not in units.json' % uid)
            continue
        if uid in seen:
            probs.append('unit %s listed twice' % uid)
            continue
        seen.add(uid)
        if 'new' not in x:
            probs.append('unit %s has no "new"' % uid)
            continue
        u = U[uid]
        changes.append({'uid': uid, 'old': u['html'], 'new': x['new'], 'start': u['start'], 'end': u['end'], 'x': x, 'u': u})
    for i, x in enumerate(rw.get('raw', [])):
        old = x.get('old', '')
        n = base.count(old) if old else 0
        if n != 1:
            probs.append('raw %d: "old" must occur once in baseline_%s.html (found %d): %s' % (i, batch, n, old[:60]))
            continue
        s = base.index(old)
        ok_ = key(plain(old))
        auto = [cid for cid, k in ck if k and k in ok_ and cid not in shared and base.count(old) == 1]
        changes.append({'uid': x.get('uid') or 'R%02d' % (i + 1), 'old': old, 'new': x.get('new', ''), 'start': s, 'end': s + len(old),
                        'x': x, 'u': {'claims_in': x.get('claims') or auto, 'text': plain(old),
                              'claims_part': [cid for cid, k in ck if len(plain(old).split()) >= 4 and ok_ in k and k not in ok_]}})
    changes.sort(key=lambda c: c['start'])
    for a, b in zip(changes, changes[1:]):
        if b['start'] < a['end']:
            probs.append('%s overlaps %s' % (a['uid'], b['uid']))
    idx = {c['uid']: i for i, c in enumerate(changes)}
    # a shared claim whose text survives in the spliced brief stays as it is; one whose text is gone follows the first
    # changed unit that held it (s171 fix)
    parts, pos = [], 0
    for c in changes:
        if c['start'] >= pos:
            parts.append(base[pos:c['start']]); parts.append(c['new']); pos = c['end']
    parts.append(base[pos:])
    spliced = key(plain(''.join(parts)))
    keep = {cid for cid, k in ck if cid in shared and k and k in spliced}
    taken = set()
    out = []
    for c in changes:
        x, u = c['x'], c['u']
        d = {'uid': c['uid'], 'old': c['old'], 'new': c['new'], 'start': c['start'], 'ids': [], 'lines': c['uid']}
        cb = []
        for j in x.get('carried_by', []):
            if isinstance(j, int):
                cb.append(j)
            elif j in idx:
                cb.append(idx[j])
            else:
                probs.append('%s carried_by %s: not a changed unit' % (c['uid'], j))
        if cb:
            d['carried_by'] = cb
        for k in ('lock_ok', 'lock_reason', 'cut', 'note'):
            if x.get(k):
                d[k] = x[k]
        new_plain = norm(plain(c['new']))
        old_plain = norm(u.get('text') or plain(c['old']))
        # an empty "claims" list counts as unset: dropping a claim takes "cut" (s171: lanes wrote "claims": [] on raws)
        cin = x.get('claims') or [cid for cid in u.get('claims_in', []) if cid not in keep and cid not in taken]
        taken.update(cid for cid in cin if cid in shared)
        ups, cuts = [], []
        for cid in cin:
            if cid not in claim_text:
                probs.append('%s names claim %s, not in claims_before_%s.json' % (c['uid'], cid, batch))
                continue
            if c['new'] == '':
                if x.get('cut'):
                    cuts.append({'id': cid, 'cut': x['cut']})
                elif cb:
                    claim_text[cid] = norm(plain(changes[cb[0]]['new']))
                    ups.append({'id': cid, 'new_text': claim_text[cid]})
            else:
                claim_text[cid] = new_plain
                ups.append({'id': cid, 'new_text': new_plain})
        for cid in ([] if x.get('claims') else u.get('claims_part', [])):
            t = claim_text.get(cid, '')
            rx = re.compile(r'\s*'.join(re.escape(ch) for ch in old_plain.replace(' ', ''))) if old_plain else None
            if old_plain and old_plain in t:
                claim_text[cid] = t.replace(old_plain, new_plain, 1)
                ups.append({'id': cid, 'new_text': claim_text[cid]})
            elif rx and rx.search(t):
                claim_text[cid] = norm(rx.sub(lambda m: ' ' + new_plain + ' ', t, count=1))
                ups.append({'id': cid, 'new_text': claim_text[cid]})
            elif c['uid'].startswith('R') and 'uid' not in x:
                pass  # a raw inside a longer claim whose spacing differs: the rebuilt-brief claim check decides
            else:
                probs.append('%s: part of claim %s, but its old text no longer sits in the claim text; name the claim in "claims"' % (c['uid'], cid))
        if ups:
            d['claim_updates'] = ups
        if cuts:
            d['claim_cuts'] = cuts
        out.append(d)
    delta = {'brief': bid, 'meaning_lock': True, 'changes': out, 'new_claims': rw.get('new_claims', [])}
    json.dump(delta, open(os.path.join(f, 'delta_%s.json' % batch), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    fl = rw.get('facts_local') or {}
    if isinstance(fl, list):
        d2 = {}
        for r in fl:
            d2.setdefault(r.get('kind', 'web'), []).append(r.get('row'))
        fl = d2
    spec = {'out': os.path.relpath(os.path.join(f, 'facts_%s.json' % batch), WS), 'population': rw.get('population', 'as in the brief')}
    spec.update({k: v for k, v in fl.items() if k in ('cards', 'web', 'local', 'relayed') and v})
    json.dump(spec, open(os.path.join(f, 'facts_spec_%s.json' % batch), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return probs, len(out)


def check(batch, bid):
    probs, n = collect(batch, bid)
    f = folder_of(bid)
    if not probs:
        r = sh([sys.executable, os.path.join(HERE, 'facts_from_spec.py'), os.path.join(f, 'facts_spec_%s.json' % batch)])
        if r.returncode:
            probs.append('facts_from_spec: ' + (r.stdout + r.stderr).strip()[-300:])
    if not probs:
        r = sh([sys.executable, os.path.join(f, 'build.py')])
        if r.returncode:
            probs.append('build.py: ' + (r.stdout + r.stderr).strip()[-400:])
    if not probs:
        import meaning_lock as ML
        import prose_lint as pl
        import content_gate as CG
        d = json.load(open(os.path.join(f, 'delta_%s.json' % batch), encoding='utf-8'))
        for i, miss in ML.check_delta(d):
            probs.append('meaning_lock %s drops %s' % (d['changes'][i]['uid'], ', '.join('%s %s' % m for m in miss)))
        new_outer = open(os.path.join(f, 'brief.html'), encoding='utf-8').read()
        m = re.match(r'<div[^>]*>', new_outer)
        inner = new_outer[m.end():new_outer.rfind('</div>')]
        for h in pl.lint_brief(inner, touched=True):
            probs.append('prose %s (%s): %s' % (h['pattern'], h['region'], h['text'][:100]))
        base = open(os.path.join(f, 'baseline_%s.html' % batch), encoding='utf-8').read()
        for code, k, msg in CG.check(base, new_outer, {bid}):
            probs.append('%s: %s' % (code, msg))
        # every claim's text must sit in the rebuilt brief (catches a shared claim whose only wording was rewritten)
        bk = key(plain(inner))
        b0 = key(plain(base))
        cmp_ = os.path.join(f, 'claim_map.json')
        if os.path.exists(cmp_):
            cut = {c['id'] for ch in d['changes'] for c in ch.get('claim_cuts', [])}
            for c in json.load(open(cmp_, encoding='utf-8')).get('claims', []):
                t = key(c.get('new_text', ''))
                if t and c['id'] not in cut and c.get('disposition') != 'cut' and t in b0 and t not in bk:
                    probs.append('claim %s text is not in the rebuilt brief: %s' % (c['id'], c.get('new_text', '')[:80]))
    return probs, n


def main(argv):
    if not argv or argv[0] not in ('setup', 'collect', 'check'):
        sys.exit(__doc__.strip().splitlines()[4].strip())
    if argv[0] == 'setup':
        spec = json.load(open(argv[1], encoding='utf-8'))
        only = set(argv[argv.index('--only') + 1].split(',')) if '--only' in argv else None
        page = P.read_page(os.path.join(WS, 'index.html'))
        print(delta_tool(spec['batch']))
        for b in spec['briefs']:
            if not only or b['id'] in only:
                print(lane(spec, b, page))
        print('prompts: local/%s/rewrite_prompts/<id>.txt (agent lean-builder; model from tools/hooks/roles.json by role)' % spec['batch'])
        return 0
    batch, bid = argv[1], argv[2]
    probs, n = (collect if argv[0] == 'collect' else check)(batch, bid)
    for p in probs:
        print('FIX ' + p)
    print('%s %s %s: %d change(s), %d problem(s)' % (argv[0], batch, bid, n, len(probs)))
    return 1 if probs else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
