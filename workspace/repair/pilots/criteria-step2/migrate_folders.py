#!/usr/bin/env python3
"""migrate_folders.py (s163 chunk 8, plan E7): bring the private repo's brief folders to the s163 step order, so a later
rebuild from a folder cannot restore the old order or the old wording.

  python3 repair/pilots/criteria-step2/migrate_folders.py [--private DIR] [--built FILE] [--write]

Without --write it only reports. For every outline.json under DIR/local-only (repair and local):
  - steps relabelled and renumbered with make_batch NEW (1:1, 5:2, 2:3, 3:4, 4:5, 6 to 8 the same), sorted, ids by
    new_id (B2); body h blocks get the same n and id;
  - the Criteria h block and its blocks up to the next h move to right after step 1's blocks (as on the page; a pause
    point that closes Workup stays with Workup);
  - every heading id renamed on the page is renamed in any outline string (links, fixes);
  - each s163 text op on that brief (20_wording, 40_labels, 50_masks) whose find text occurs verbatim in an outline
    string is replaced there; the rest are listed in local/s163/e7_misses.md (expected: wording the outline builds
    differently, and Recall masks, which the outline marks its own way);
  - check: the outline's h ids, in order, equal the built page's step heading ids for that brief.
For every 10_*_spine.json: a replace_brief html that equals the live page's brief is set to that brief's html on the
built s163 page; one that differs from the live page is stale and is listed, not touched.
"""
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(WS, 'tools'))
from pagelib import briefs, read_page  # noqa: E402
from make_batch import NEW, NAV, HEAD, new_id  # noqa: E402

OPS = ['20_wording.json', '40_labels.json', '50_masks.json']


def strings(x, fn):
    """Apply fn to every string in a JSON value; returns the new value."""
    if isinstance(x, str):
        return fn(x)
    if isinstance(x, list):
        return [strings(v, fn) for v in x]
    if isinstance(x, dict):
        return {k: strings(v, fn) for k, v in x.items()}
    return x


def page_heads(h):
    out, renamed = {}, set()
    for b in briefs(h):
        seg = h[b.start:b.end]
        if not NAV.search(seg):
            continue
        ids = [m.group(1) for m in HEAD.finditer(seg)]
        out[b.id] = ids
        renamed |= {i for i in ids if new_id(i) != i}
    return out, renamed


RESIDUAL = re.compile(r'How NBME framed it|\((?:see )?steps? \d[^)]*\)|\b[Ss]teps? [1-8]\b(?! CK)|\bowns\b|\bowned by\b')


def untag(s):
    return re.sub(r'<[^>]*>|^[^<>]*>|<[^<>]*$', '', s)


def trim(s):
    s = re.sub(r'^(?:\s*(?:<[^>]*>|[^<>]*>))+', '', s)
    return re.sub(r'(?:(?:<[^>]*>|<[^<>]*)\s*)+$', '', s)


def text_ops(o, ops, log):
    for op in ops:
        hit = [0]

        def rep(s, op=op, hit=hit):
            if op['find'] in s:
                hit[0] += s.count(op['find'])
                return s.replace(op['find'], op['with'])
            return s
        o = strings(o, rep)
        # the page op carries markup the outline string does not: retry with the outer markup trimmed (a wrapping
        # span or cell), then on the text alone; only where the text itself changes (a mask-only op changes no text
        # and stays a miss: the outline marks masks its own way)
        for cut in (trim, untag):
            if hit[0]:
                break
            ft, wt = cut(op['find']).strip(), cut(op['with']).strip()
            if ft and untag(ft) != untag(wt):
                o = strings(o, lambda s, ft=ft, wt=wt, hit=hit: (hit.__setitem__(0, hit[0] + s.count(ft)),
                                                                 s.replace(ft, wt))[1] if ft in s else s)
        if hit[0]:
            log['text_hit'] += 1
        else:
            log['misses'].append((o.get('brief'), op['note'], op['find'][:140]))
    # what a rebuild from this outline would still bring back: the old NBME label, step numbers, ownership words
    # (outline-only keys such as old_claims are history and skipped)
    keep = {k: v for k, v in o.items() if k not in ('old_claims', 'src', 'name', 'steps')}
    found = []
    strings(keep, lambda s: (found.extend('%s [..%s..]' % (m.group(0), s[max(0, m.start() - 90):m.end() + 30]) for m in RESIDUAL.finditer(s)), s)[1])
    if found:
        log['residual'].append((o.get('brief'), found))
    return o


def migrate_outline(o, ops, renamed, built_ids, log):
    steps = o.get('steps')
    if not steps or len(steps) != 8:
        return text_ops(o, ops, log), 'no step rail (text only)'

    def nn(v):    # some outlines keep the step number as a string; keep its type
        return type(v)(NEW[int(v)])
    if [s[1] for s in sorted(steps, key=lambda s: int(s[0]))][1] == 'Criteria':
        return None, 'already migrated'
    # ids first, by token over the whole outline (steps, h blocks, links, fixes): a heading id renamed on the page,
    # or any -s2 to -s5 id of this brief's own prefix
    pfx = (o.get('prefix') or '') + '-s'
    tok = re.compile(r'(?<![\w-])([a-z][a-z0-9]*-s[2-5])(?![\w-])')
    o = strings(o, lambda s: tok.sub(
        lambda m: new_id(m.group(1)) if m.group(1) in renamed or m.group(1)[:-1] == pfx else m.group(1), s))
    o['steps'] = sorted([[nn(s[0])] + list(s[1:]) for s in o['steps']], key=lambda s: int(s[0]))
    body = o['body']
    hs = [i for i, x in enumerate(body) if isinstance(x, dict) and x.get('type') == 'h']
    crit = [i for i in hs if int(body[i]['n']) == 5]
    if crit:
        cs = crit[0]
        later = [i for i in hs if i > cs]
        ce = later[0] if later else len(body)
        block = body[cs:ce]
        rest = body[:cs] + body[ce:]
        h1 = [i for i, x in enumerate(rest) if isinstance(x, dict) and x.get('type') == 'h' and int(x['n']) == 1]
        after = [i for i, x in enumerate(rest) if isinstance(x, dict) and x.get('type') == 'h' and h1 and i > h1[0]]
        at = after[0] if after else len(rest)
        body = rest[:at] + block + rest[at:]
    for x in body:
        if isinstance(x, dict) and x.get('type') == 'h':
            x['n'] = nn(x['n'])
    o['body'] = body
    o = text_ops(o, ops, log)
    got =[x['id'] for x in o['body'] if isinstance(x, dict) and x.get('type') == 'h' and x.get('id')]
    if built_ids is not None and got != built_ids:
        return o, 'ORDER MISMATCH outline %s page %s' % (got, built_ids)
    return o, 'ok'


def main(argv):
    priv = '/home/claude/step2haki-private'
    built = os.path.join(WS, 'local', 's163', 'index.html')
    if '--private' in argv:
        priv = argv[argv.index('--private') + 1]
    if '--built' in argv:
        built = argv[argv.index('--built') + 1]
    write = '--write' in argv
    live_h, built_h = read_page(os.path.join(WS, 'index.html')), read_page(built)
    live = {b.id: live_h[b.start:b.end] for b in briefs(live_h)}
    new = {b.id: built_h[b.start:b.end] for b in briefs(built_h)}
    _, renamed = page_heads(live_h)
    built_heads, _ = page_heads(built_h)
    by_brief = {}
    for f in OPS:
        for op in json.load(open(os.path.join(WS, 'repair', 's163', f), encoding='utf-8'))['edits']:
            if op.get('brief') and 'find' in op:
                by_brief.setdefault(op['brief'], []).append(op)
    log = {'text_hit': 0, 'misses': [], 'residual': []}
    res = {}
    outs = sorted(glob.glob(os.path.join(priv, 'local-only', '**', 'outline.json'), recursive=True))
    for f in outs:
        o = json.load(open(f, encoding='utf-8'))
        bid = o.get('brief')
        n0 = len(log['misses'])
        o2, st = migrate_outline(o, by_brief.get(bid, []), renamed, built_heads.get(bid), log)
        res.setdefault(st.split(' outline')[0], []).append(os.path.relpath(f, priv))
        if st.startswith('ORDER'):
            print('  %s: %s' % (os.path.relpath(f, priv), st))
        if o2 is not None and write and not st.startswith('ORDER'):
            json.dump(o2, open(f, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
        del n0
    print('outline.json: %d files; %s' % (len(outs), {k: len(v) for k, v in res.items()}))
    sp = {'set': 0, 'done': 0, 'unchanged': 0, 'stale': [], 'unknown': []}
    for f in sorted(glob.glob(os.path.join(priv, 'local-only', '**', '10_*_spine.json'), recursive=True)):
        d = json.load(open(f, encoding='utf-8'))
        ch = False
        for op in d['edits']:
            if op.get('op') != 'replace_brief':
                continue
            bid = op['brief']
            if bid not in live:
                sp['unknown'].append(os.path.relpath(f, priv))
            elif bid in new and op['html'].strip() == new[bid].strip() and new[bid].strip() != live[bid].strip():
                sp['done'] += 1
            elif op['html'].strip() != live[bid].strip():
                sp['stale'].append(os.path.relpath(f, priv))
            elif new[bid].strip() == live[bid].strip():
                sp['unchanged'] += 1
            else:
                op['html'] = new[bid]
                sp['set'] += 1
                ch = True
        if ch and write:
            json.dump(d, open(f, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print('10_*_spine.json: set to the s163 html %d, already s163 %d, unchanged by s163 %d, stale (not touched) %d %s, unknown %d %s' % (
        sp['set'], sp['done'], sp['unchanged'], len(sp['stale']), sp['stale'], len(sp['unknown']), sp['unknown']))
    os.makedirs(os.path.join(WS, 'local', 's163'), exist_ok=True)
    with open(os.path.join(WS, 'local', 's163', 'e7_misses.md'), 'w', encoding='utf-8') as w:
        w.write('# E7 text misses (s163 op find text not verbatim in the outline)\n\n%d hits, %d misses\n\n' % (
            log['text_hit'], len(log['misses'])))
        for b, note, find in log['misses']:
            w.write('- %s | %s | %s\n' % (b, note, find.replace('\n', ' ')))
        w.write('\n## Residual in outlines after migration (old label, step numbers, ownership words)\n\n')
        for b, found in log['residual']:
            w.write('- %s: %s\n' % (b, found))
    print('text ops: %d replaced in outlines, %d misses; residual in %d outlines, %d hits (local/s163/e7_misses.md)%s' % (
        log['text_hit'], len(log['misses']), len(log['residual']), sum(len(f) for _, f in log['residual']),
        '' if write else '; dry run, nothing written'))
    return 1 if any(k.startswith('ORDER') for k in res) else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
