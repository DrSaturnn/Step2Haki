#!/usr/bin/env python3
"""apply_edits.py: apply an edits.json (format: tools/EDITS.md) to the page by offset splices.

  python3 tools/apply_edits.py <edits.json> [page] [--out FILE] [--quiet]
Writes in place unless --out. Ops run in order; each op sees the result of the previous
one. Every anchor must occur exactly once inside its scope (the brief, or one item);
the first failing op aborts with a message and a fix, and nothing is written.
Never re-serializes the DOM: bytes outside the spliced ranges are untouched.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pagelib import (TYPES, STATUSES, briefs, count, esc_attr, items, read_page,  # noqa: E402
                     set_attr_in_tag, splice, split_arrows, text, write_page, attrs)
from idgen import new_item_ids, taken_ids  # noqa: E402

OPS = {
    'replace': ({'brief', 'find', 'with'}, {'item', 'note'}),
    'insert_before': ({'brief', 'anchor', 'html'}, {'item', 'note'}),
    'insert_after': ({'brief', 'anchor', 'html'}, {'item', 'note'}),
    'add_item': ({'brief', 'type', 'stem', 'answer', 'd1', 'd2'},
                 {'companion', 'lead_in', 'status', 'src', 'nid', 'after_item', 'attrs', 'bold_answer', 'note'}),
    'set_attr': ({'target', 'attr', 'value'}, {'note'}),
    'new_brief': ({'after', 'html'}, {'nav', 'note'}),
}
IDENTITY = {'id', 'data-item-id', 'data-key-id', 'data-d1-id', 'data-d2-id'}


class EditError(Exception):
    def __init__(self, n, op, msg, fix):
        super().__init__('edit %d (%s): %s\n      fix: %s' % (n, op, msg, fix))
        self.n, self.op, self.msg, self.fix = n, op, msg, fix


def validate(spec):
    """Schema check of the whole file. Returns a list of (n, op, msg, fix)."""
    errs = []
    if not isinstance(spec, dict) or not isinstance(spec.get('edits'), list):
        return [(0, 'file', 'top level must be {"edits": [...]}', 'wrap the ops in {"edits": [ ... ]}')]
    for n, e in enumerate(spec['edits'], 1):
        op = e.get('op') if isinstance(e, dict) else None
        if op not in OPS:
            errs.append((n, str(op), 'unknown op', 'use one of ' + ', '.join(OPS)))
            continue
        req, opt = OPS[op]
        miss = sorted(req - set(e))
        extra = sorted(set(e) - req - opt - {'op'})
        if miss:
            errs.append((n, op, 'missing field(s) ' + ', '.join(miss), 'see tools/EDITS.md for the %s example' % op))
        if extra:
            errs.append((n, op, 'unknown field(s) ' + ', '.join(extra), 'remove them; allowed: ' + ', '.join(sorted(req | opt))))
        for k in req | opt:
            if k in e and k not in ('attrs', 'nav', 'bold_answer', 'companion') and not isinstance(e[k], str):
                errs.append((n, op, 'field %s must be a string' % k, 'quote it'))
        if op == 'add_item':
            if e.get('type') not in TYPES:
                errs.append((n, op, 'type %r not in %s' % (e.get('type'), sorted(TYPES)), 'pick the type the three options are'))
            if e.get('status', 'ready') not in STATUSES:
                errs.append((n, op, 'status %r' % e.get('status'), 'ready, needs_source or needs_repair'))
            for k in ('stem', 'answer', 'companion'):
                v = e.get(k)
                if isinstance(v, str) and len(split_arrows(v)) > 1:
                    errs.append((n, op, '%s contains a top-level arrow' % k, 'the applier writes the arrows; remove "→" from %s' % k))
            a = e.get('attrs', {})
            if not isinstance(a, dict) or any(k in IDENTITY or k in ('data-item-version', 'data-type', 'data-d1', 'data-d2') for k in a):
                errs.append((n, op, 'attrs must be a dict without id/type/option attributes', 'ids come from idgen; use the named fields'))
        if op == 'set_attr':
            if e.get('attr') in IDENTITY:
                errs.append((n, op, 'identity attribute %s is immutable' % e.get('attr'), 'never edit ids'))
            if not re.match(r'^[a-z][a-z0-9-]*$', e.get('attr', '') or ''):
                errs.append((n, op, 'bad attribute name %r' % e.get('attr'), 'lowercase data-* name'))
        if op == 'new_brief' and 'nav' in e:
            nav = e['nav']
            if not isinstance(nav, dict) or not {'after_link', 'title'} <= set(nav):
                errs.append((n, op, 'nav must be {"after_link": <brief id>, "title": <short title>}', 'see tools/EDITS.md'))
    return errs


def _brief(html, bid, n, op):
    hits = [b for b in briefs(html) if b.id == bid]
    if len(hits) != 1:
        raise EditError(n, op, 'brief %r found %d times' % (bid, len(hits)),
                        'use an existing brief id exactly (see the brief list); ids never change')
    return hits[0]


def _item(html, qid, n, op):
    hits = [i for i in items(html) if i.id == qid]
    if len(hits) != 1:
        raise EditError(n, op, 'item %r found %d times' % (qid, len(hits)), 'use an existing data-item-id exactly')
    return hits[0]


def _scope(html, e, n, op):
    b = _brief(html, e['brief'], n, op)
    s, t = b.start, b.end
    if e.get('item'):
        it = _item(html, e['item'], n, op)
        if it.brief_id != b.id:
            raise EditError(n, op, 'item %s is in brief %s, not %s' % (it.id, it.brief_id, b.id), 'fix brief or item')
        s, t = it.start, it.end
    return s, t, b


def _unique(html, s, t, needle, n, op, where):
    if not needle:
        raise EditError(n, op, 'empty anchor', 'give a verbatim, unique snippet of the current HTML')
    seg = html[s:t]
    c = count(seg, needle)
    if c != 1:
        raise EditError(n, op, 'anchor occurs %d times in %s (must be exactly 1): %r' % (c, where, needle[:90]),
                        'copy the anchor verbatim from the brief HTML (entities included)' if c == 0 else
                        'lengthen the anchor with neighbouring text until it is unique inside %s' % where)
    return s + seg.find(needle)


def apply_one(html, e, n, taken, log):
    op = e['op']
    if op in ('replace', 'insert_before', 'insert_after'):
        s, t, b = _scope(html, e, n, op)
        where = 'item %s' % e['item'] if e.get('item') else 'brief %s' % b.id
        needle = e['find'] if op == 'replace' else e['anchor']
        at = _unique(html, s, t, needle, n, op, where)
        if op == 'replace':
            if b.start == at and needle.startswith('<div'):
                raise EditError(n, op, 'replace may not rewrite the brief opening tag', 'use set_attr for brief attributes')
            html = splice(html, [(at, at + len(needle), e['with'])])
        elif op == 'insert_before':
            html = splice(html, [(at, at, e['html'])])
        else:
            html = splice(html, [(at + len(needle), at + len(needle), e['html'])])
        log.append('%s in %s' % (op, where))
        return html
    if op == 'add_item':
        b = _brief(html, e['brief'], n, op)
        m = re.search(r'<ol\b[^>]*class="bank\b[^"]*"[^>]*>', b.inner)
        if not m or len(re.findall(r'<ol\b[^>]*class="bank\b', b.inner)) != 1:
            raise EditError(n, op, 'brief %s has %s ol.bank' % (b.id, 'no' if not m else 'more than one'),
                            'add the bank with insert_after first (h5.authored-hdr + ol.bank authored)')
        ol_start = b.inner_start + m.start()
        ol_end = html.find('</ol>', ol_start)
        stem, ans = e['stem'].strip(), e['answer'].strip()
        comp = (e.get('companion') or '').strip()
        ids = new_item_ids(text(ans), text(stem), text(e['d1']), text(e['d2']), taken)
        at = [('data-type', e['type']), ('data-d1', esc_attr(e['d1'])), ('data-d2', esc_attr(e['d2'])),
              ('data-item-id', ids['data-item-id']), ('data-item-version', '1'),
              ('data-item-status', e.get('status', 'ready')), ('data-key-id', ids['data-key-id']),
              ('data-d1-id', ids['data-d1-id']), ('data-d2-id', ids['data-d2-id'])]
        if e.get('lead_in'):
            at.append(('data-lead-in', esc_attr(e['lead_in'])))
        if e.get('src'):
            at.append(('data-src', esc_attr(e['src'])))
        if e.get('nid'):
            at.append(('data-nid', esc_attr(e['nid'])))
        for k, v in (e.get('attrs') or {}).items():
            at.append((k, esc_attr(str(v))))
        body = stem + ' → ' + ('<b>%s</b>' % ans if e.get('bold_answer', True) else ans)
        if comp:
            body += ' → ' + comp
        li = '<li %s>%s</li>' % (' '.join('%s="%s"' % kv for kv in at), body)
        if e.get('after_item'):
            it = _item(html, e['after_item'], n, op)
            if it.brief_id != b.id:
                raise EditError(n, op, 'after_item %s is not in brief %s' % (it.id, b.id), 'name an item of this brief')
            html = splice(html, [(it.end, it.end, '\n' + li)])
        else:
            pre = html[:ol_end]
            ins = li + '\n' if pre.endswith('\n') else '\n' + li + '\n'
            html = splice(html, [(ol_end, ol_end, ins)])
        log.append('add_item %s to %s' % (ids['data-item-id'], b.id))
        return html
    if op == 'set_attr':
        tgt, name, val = e['target'], e['attr'], e['value']
        if tgt.startswith('q_'):
            it = _item(html, tgt, n, op)
            s, oe = it.start, it.open_end
        else:
            b = _brief(html, tgt, n, op)
            s, oe = b.start, b.open_end
        tag = html[s:oe]
        cur = attrs(tag)
        if name == 'data-item-version' and val == '+1':
            val = str(int(cur.get('data-item-version', '1')) + 1)
        new = set_attr_in_tag(tag, name, esc_attr(val))
        html = splice(html, [(s, oe, new)])
        log.append('set_attr %s %s=%s' % (tgt, name, val))
        return html
    if op == 'new_brief':
        after = _brief(html, e['after'], n, op)
        nb = e['html'].strip()
        found = briefs(nb)
        if len(found) != 1 or found[0].start != 0 or found[0].end != len(nb):
            raise EditError(n, op, 'html must be exactly one complete <div class="brief ..."> block',
                            'balance the <div>s; one brief per new_brief op')
        nid = found[0].id
        if not nid or re.search(r'\sid="%s"' % re.escape(nid), html):
            raise EditError(n, op, 'new brief id %r is empty or already used on the page' % nid, 'choose a new short lowercase id')
        html = splice(html, [(after.end, after.end, '\n\n' + nb)])
        nav = e.get('nav')
        if nav:
            ns = html.find('<div id="navlinks">')
            m = re.search(r'<a\b[^>]*href="#%s"[^>]*>.*?</a>' % re.escape(nav['after_link']), html[ns:])
            if not m:
                raise EditError(n, op, 'nav after_link #%s not found' % nav['after_link'], 'name a brief whose nav link exists')
            kind = found[0].kind
            cls = nav.get('class', 'bs' if kind == 'bs' else ('aq' if kind == 'aq' else ''))
            link = '\n    <a %shref="#%s">%s</a>' % ('class="%s" ' % cls if cls else '', nid, nav['title'])
            p = ns + m.end()
            html = splice(html, [(p, p, link)])
            if not cls:
                sec_start = html.rfind('<div class="sect">', 0, p)
                cm = re.compile(r'<span class="count">(\d+)</span>').search(html, sec_start)
                html = splice(html, [(cm.start(1), cm.end(1), str(int(cm.group(1)) + 1))])
        log.append('new_brief %s after %s' % (nid, after.id))
        return html
    raise EditError(n, op, 'unknown op', 'see tools/EDITS.md')


def apply(html, spec):
    errs = validate(spec)
    if errs:
        n, op, msg, fix = errs[0]
        raise EditError(n, op, msg + ('' if len(errs) == 1 else ' (+%d more schema errors)' % (len(errs) - 1)), fix)
    taken = taken_ids(html)
    log = []
    for n, e in enumerate(spec['edits'], 1):
        html = apply_one(html, e, n, taken, log)
    return html, log


def main(argv):
    out, quiet, pos = None, False, []
    i = 0
    while i < len(argv):
        if argv[i] == '--out':
            out = argv[i + 1]
            i += 2
        elif argv[i] == '--quiet':
            quiet = True
            i += 1
        else:
            pos.append(argv[i])
            i += 1
    if not pos:
        print(__doc__)
        return 2
    page = pos[1] if len(pos) > 1 else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'index.html')
    spec = json.load(open(pos[0], encoding='utf-8'))
    html = read_page(page)
    try:
        new, log = apply(html, spec)
    except EditError as ex:
        print('apply_edits: FAIL %s' % ex)
        return 1
    write_page(out or page, new)
    if not quiet:
        print('apply_edits: OK %d op(s) -> %s (%+d chars): %s' % (len(log), out or page, len(new) - len(html), '; '.join(log)))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
