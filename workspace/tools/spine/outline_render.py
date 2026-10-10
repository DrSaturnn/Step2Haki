"""outline_render: render a brief's outline.json through spinelib (PHASE0_SCRIPTS item 1; replaces the filler role).

  python3 tools/spine/outline_render.py <dir>/outline.json            write brief.html, claim_map.json, 10_<id>_spine.json
  python3 tools/spine/outline_render.py <dir>/outline.json --compare <brief.html>
        render to a temp dir and diff against a reference brief (pop ids normalized); exit 1 on any difference

The architect writes outline.json; every learner-facing string is a {"t": text, "ids": [...]} part, so the claim map
is complete by construction and the page text is exactly the architect's text.

Top level:
  brief, prefix, entry (disease|drug|presentation|screen), lens (psych|peds|fm), name (cluster name), bank_id,
  tail_start (the live Practice header html), steps [[n, short label, id or null], ...],
  src [json files: either {"id": [citation, quote]} maps or facts.json files {"facts": [...]}] (paths relative to
  the outline's folder or to workspace/), tail_fix [[old, new], ...], head_fix [[old, new], ...],
  old_claims [[old text, disposition, where or reason], ...], body [blocks]

Rich text (anywhere text appears): a string, a part, or a list of them, concatenated.
  plain string        literal markup or punctuation (outline_check flags literal words: learner text needs ids)
  {"t", "ids"}        a sourced line (T)
  {"g": "A"|"P"|"NM"} arrow, plus, non-modifiable tag (" <span class=sp-nm>non-modifiable</span>")
  {"M": rich}         study-mode mask
  {"b": rich, "cls"}  <b class=...>
  {"tag": "p|span|div|i|small|ul|li|ol", "cls": "...", "id": "...", "c": rich}   a wrapper element
  {"drawer": brief-id, "label": rich}
  {"pop": rich, "body": rich, "title": str, "cls": str}      a hover card
  {"why": rich, "body": rich, "title": str}                  a "why" card (title defaults to "Why order it")
  {"chip": kind, "text": rich}
  {"commit": [cond rich, choice rich]}                       "If ..., choose ..."
Blocks (body items): a rich value (rendered as is), or {"type": ...}:
  h {n, title, id} | stepper | bottom {lines} | script2 {rows [[key, [lines]]]} | systems {title, small, rows [[key, finding, why]]}
  rows {rows [{src, finding, chips, commit [cond, choice], extra}]} | table {caption, heads, rows, mask_cols, cls}
  workup {steps [[when, [[name, [[finding, meaning]], extra]]]], end} | ladder {rungs [[n, tag, when, body]]}
  pause {text} | timeline {cells [[bold, rest]]}
"""
import difflib
import json
import os
import re
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(WS, 'repair', 'migration', 'spine'))
from spinelib import Spine  # noqa: E402

NM = ' <span class="sp-nm">non-modifiable</span>'
TAGS = {'p', 'span', 'div', 'i', 'small', 'ul', 'li', 'ol', 'b', 'em', 'strong'}


def load_src(o, base):
    src = {}
    for p in o.get('src', []):
        path = p if os.path.isabs(p) else (os.path.join(base, p) if os.path.exists(os.path.join(base, p)) else os.path.join(WS, p))
        d = json.load(open(path, encoding='utf-8'))
        if isinstance(d, dict) and 'facts' in d:
            for f in d['facts']:
                cite = '%s %s (fetched %s, cache %s; %s)' % (f.get('title', ''), f.get('url', f.get('local', '')), f.get('fetched', ''),
                                                              f.get('sha', ''), f.get('section', ''))
                src[f['id']] = (' '.join(cite.split()), f['quote'])
        else:
            for k, v in d.items():
                src[k] = tuple(v)
    return src


class Renderer:
    def __init__(self, o, base):
        self.o = o
        self.S = Spine(o['prefix'], load_src(o, base))

    def r(self, x):
        """rich text -> html"""
        S = self.S
        if x is None:
            return ''
        if isinstance(x, str):
            return x
        if isinstance(x, list):
            return ''.join(self.r(p) for p in x)
        if not isinstance(x, dict):
            raise ValueError('rich text must be str, list or dict: %r' % (x,))
        if 't' in x:
            return S.T(x['t'], *x.get('ids', []))
        if 'g' in x:
            return {'A': Spine.A, 'P': Spine.P, 'NM': NM}[x['g']]
        if 'M' in x:
            return S.M(self.r(x['M']))
        if 'b' in x:
            return '<b%s>%s</b>' % (' class="%s"' % x['cls'] if x.get('cls') else '', self.r(x['b']))
        if 'tag' in x:
            t = x['tag']
            if t not in TAGS:
                raise ValueError('wrapper tag not allowed: ' + t)
            attrs = ''.join(' %s="%s"' % (k, x[k]) for k in ('cls', 'id') if x.get(k)).replace(' cls=', ' class=')
            return '<%s%s>%s</%s>' % (t, attrs, self.r(x.get('c')), t)
        if 'drawer' in x:
            return S.drawer(x['drawer'], self.r(x['label']))
        if 'pop' in x:
            return S.pop(self.r(x['pop']), self.r(x['body']), x.get('title', ''), x.get('cls', ''))
        if 'why' in x:
            return S.why(self.r(x['why']), self.r(x['body']), x.get('title', 'Why order it'))
        if 'chip' in x:
            return S.chip(x['chip'], self.r(x['text']))
        if 'commit' in x:
            return S.commit(self.r(x['commit'][0]), self.r(x['commit'][1]))
        raise ValueError('unknown rich part: %s' % sorted(x))

    def block(self, b):
        S, r, o = self.S, self.r, self.o
        if not isinstance(b, dict) or 'type' not in b:
            return r(b)
        t = b['type']
        if t == 'h':
            return S.h(b['n'], b['title'], b['id'])
        if t == 'stepper':
            return S.stepper([tuple(s) for s in o['steps']], o['bank_id'])
        if t == 'bottom':
            return S.bottom([r(x) for x in b['lines']])
        if t == 'script2':
            return S.script2([(k, [r(x) for x in lines]) for k, lines in b['rows']])
        if t == 'systems':
            return S.systems(r(b['title']), r(b.get('small', '')), [(k, r(f), r(w)) for k, f, w in b['rows']])
        if t == 'rows':
            out = []
            for x in b['rows']:
                c = x.get('commit')
                out.append(S.row(x.get('src', ''), r(x['finding']), chips=r(x.get('chips')),
                                 commit=S.commit(r(c[0]), r(c[1])) if c else '', extra=r(x.get('extra'))))
            return '<div class="sp-rows">\n' + '\n'.join(out) + '\n</div>'   # as the goldens wrote it
        if t == 'table':
            return S.table(r(b['caption']), [r(h) for h in b['heads']], [tuple(r(c) for c in row) for row in b['rows']],
                           mask_cols=tuple(b.get('mask_cols', ())), cls=b.get('cls', 'sp-dx'))
        if t == 'workup':
            steps = [(r(when), [(r(name), [(r(a), r(z)) for a, z in rows], r(extra)) for name, rows, extra in tiles])
                     for when, tiles in b['steps']]
            return S.workup(steps, r(b['end']))
        if t == 'ladder':
            return S.ladder([S.rung(n, tag, r(when), r(body)) for n, tag, when, body in b['rungs']])
        if t == 'pause':
            return S.pause(r(b['text']))
        if t == 'timeline':
            return S.timeline([(r(x), r(y)) for x, y in b['cells']])
        raise ValueError('unknown block type: ' + t)


def render(outline_path, outdir=None):
    o = json.load(open(outline_path, encoding='utf-8'))
    base = os.path.dirname(os.path.abspath(outline_path))
    outdir = outdir or base
    R = Renderer(o, base)
    body = (o.get('joiner', '\n')).join(R.block(b) for b in o['body'])
    def fixer(key):
        # [old, new] pairs; new may be rich text (so a sourced subtitle keeps its ids). A pair whose old text is gone
        # and whose new text is already present was applied by an earlier ship: skip it (rebuilds stay re-runnable).
        ps = [(old, R.r(new)) for old, new in o.get(key, [])]
        if not ps:
            return None

        def f(s):
            for old, new in ps:
                if s.count(old) == 0 and new in s:
                    continue
                assert s.count(old) == 1, '%s anchor not found exactly once: %s' % (key, old[:60])
                s = s.replace(old, new)
            return s
        return f
    old = [tuple(x) for x in o.get('old_claims', [])]
    return R.S.finish(outdir, o['brief'], body, o['tail_start'], {'name': o['name'], 'entry': o['entry']},
                      tail_fix=fixer('tail_fix'), lens=o['lens'], old_claims=old, head_fix=fixer('head_fix'))


def norm(h):
    return re.sub(r'-pop-\d+', '-pop-N', h)


def main(argv):
    if not argv:
        sys.exit(__doc__.strip().splitlines()[2].strip())
    if '--compare' in argv:
        ref = argv[argv.index('--compare') + 1]
        tmp = tempfile.mkdtemp(prefix='orender-')
        try:
            new = render(argv[0], tmp)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        a, b = norm(open(ref, encoding='utf-8').read()), norm(new)
        if a == b:
            print('outline_render: IDENTICAL to %s (pop ids normalized)' % ref)
            return 0
        # show the first differences on a tag-split view
        sa, sb = re.sub(r'>', '>\n', a).split('\n'), re.sub(r'>', '>\n', b).split('\n')
        d = [l for l in difflib.unified_diff(sa, sb, 'reference', 'rendered', n=1, lineterm='')]
        print('outline_render: DIFFERS from %s (%d diff lines); first 40:' % (ref, len(d)))
        print('\n'.join(d[:40]))
        return 1
    render(argv[0])
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
