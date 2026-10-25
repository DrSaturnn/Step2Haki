"""author_lib: compact authoring helpers for spine builds (from s152lib, made shared at the s152 close, 2026-10-25).

Each brief folder repair/migration/<system>/<id>/spine holds author.py, which does
    import os, sys; sys.path.insert(0, os.path.join(<workspace>, 'tools', 'spine')); from author_lib import *
and writes outline.json, live_src.json, facts_spec.json and the tail reasons. tools/spine/build_brief.py <folder> runs
author.py, facts_from_spec.py, outline_render.py and disp.py in order (BATCH_RUNBOOK section 2, S2 builder agents).
The batch id for live_src() comes from its batch argument or the AX_BATCH environment variable.
"""
import html as H
import json
import os
import re
import subprocess
import sys

WS = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.insert(0, os.path.join(WS, 'tools'))
import pagelib as PL  # noqa: E402


def ids(x):
    return x.split() if isinstance(x, str) else list(x)


def t(x, i, cur=None):
    """a sourced line; cur = currency for a number carried from the live brief (verified:<id> | stable | flagged)"""
    d = {'t': x, 'ids': ids(i)}
    if cur:
        d['currency'] = cur
    return d


def M(x):
    return {'M': x}


def p(c, cls=None):
    d = {'tag': 'p', 'c': c}
    if cls:
        d['cls'] = cls
    return d


def pop(trig, body, title=None):
    d = {'pop': trig, 'body': body}
    if title:
        d['title'] = title
    return d


def dr(bid, label):
    return {'drawer': bid, 'label': label}


def h(n, title, hid):
    return {'type': 'h', 'n': n, 'title': title, 'id': hid}


def table(caption, heads, rows, mask_cols=None, cls=None):
    d = {'type': 'table', 'caption': caption, 'heads': heads, 'rows': rows}
    if mask_cols:
        d['mask_cols'] = mask_cols
    if cls:
        d['cls'] = cls
    return d


def steps(prefix, used):
    lab = ['Script', 'Urgent', 'Differential', 'Workup', 'Criteria', 'Severity', 'Treatment', 'Follow-up']
    return [[n, lab[n - 1], ('%s-s%d' % (prefix, n)) if n in used else None] for n in range(1, 9)]


def live_src(bid, folder, batch=None):
    batch = batch or os.environ['AX_BATCH']
    d = json.load(open(os.path.join(WS, 'local', batch, 'live', bid + '.json'), encoding='utf-8'))
    cite = 'old brief %s (live page, %s baseline)' % (bid, batch)
    json.dump({k: [cite, v] for k, v in d.items()}, open(os.path.join(folder, 'live_src.json'), 'w', encoding='utf-8'),
              indent=1, ensure_ascii=False)
    return d


def bank(bid):
    pg = PL.read_page(os.path.join(WS, 'index.html'))
    b = PL.brief_by_id(pg, bid)
    t_ = pg[b.start:b.end]
    i = t_.find('<ol class="bank')
    return re.findall(r'<li data-type=.*?</li>', t_[i:], re.S)


def tail_fix(bid, reasons):
    """reasons {item id prefix: (key why, d1 why, d2 why)}; every bank item must have one"""
    out, seen = [], set()
    for li in bank(bid):
        iid = re.search(r'data-item-id="([^"]+)"', li).group(1)
        k = [k for k in reasons if iid.startswith(k)]
        assert len(k) == 1, ('reasons', bid, iid, k)
        seen.add(k[0])
        kw, w1, w2 = reasons[k[0]]
        if 'data-key-why=' in li:
            continue
        attrs = ' data-key-why="%s" data-d1-why="%s" data-d2-why="%s"' % tuple(H.escape(x, quote=True) for x in (kw, w1, w2))
        j = li.index('>')
        out.append([li, li[:j] + attrs + li[j:]])
    missing = set(reasons) - seen
    assert not missing, ('unused reasons', missing)
    return out + pairs_fix(bid)


def pairs_fix(bid):
    """s152 S3: a Pairs with block renders as an owner list only when it opens on a title (pointer_check); drop the
    "Part I" / "Part II" labels in front of each <b> title"""
    pg = PL.read_page(os.path.join(WS, 'index.html'))
    b = PL.brief_by_id(pg, bid)
    t_ = pg[b.start:b.end]
    out = []
    for m in re.finditer(r'<div class="pearls"[^>]*>\s*<span class="lbl">Pairs with</span>.*?</div>', t_, re.S):
        new = re.sub(r'Part II? (?=<b>)', '', m.group(0))
        new = re.sub(r'Ask: <([ib])>(.*?)</\1>', r'Ask: \2', new)   # a question is not a title row
        if new != m.group(0):
            out.append([m.group(0), new])
    return out


def cited(x, out=None):
    out = set() if out is None else out
    if isinstance(x, dict):
        if 'ids' in x:
            out |= set(x['ids'])
        for v in x.values():
            cited(v, out)
    elif isinstance(x, list):
        for v in x:
            cited(v, out)
    return out


def old_claims(live, o, disp):
    """every live line (L03 on) not cited by the outline needs a disposition: {Lnn: (disposition, where or why)}"""
    c = cited(o['body'])
    out = []
    for k, v in live.items():
        if k in ('L02',) or k in c:
            continue
        assert k in disp, ('old line needs a disposition', k, v[:80])
        out.append([v, disp[k][0], disp[k][1]])
    extra = set(disp) - set(live)
    assert not extra, extra
    return out


def auto_stable(x, out):
    """a part citing only live lines whose digits are names (22q11.2, 45,X, 100% oxygen) gets currency stable; listed"""
    if isinstance(x, dict):
        if 'ids' in x and 'currency' not in x and re.search(r'\d', x['t']) and all(i.startswith('L') for i in x['ids']):
            x['currency'] = 'stable'
            out.append(x['t'][:70])
        for v in x.values():
            auto_stable(v, out)
    elif isinstance(x, list):
        for v in x:
            auto_stable(v, out)


def write(folder, o):
    out = []
    auto_stable(o['body'], out)
    if out:
        open(os.path.join(folder, 'stable_numbers.txt'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
    json.dump(o, open(os.path.join(folder, 'outline.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)


def build(folder):
    """facts, render; print one line"""
    r = subprocess.run([sys.executable, os.path.join(WS, 'tools', 'spine', 'facts_from_spec.py'),
                        os.path.join(folder, 'facts_spec.json')], capture_output=True, text=True, cwd=WS)
    print('facts:', (r.stdout + r.stderr).strip()[-600:])
    if r.returncode:
        sys.exit(1)
    r = subprocess.run([sys.executable, os.path.join(WS, 'tools', 'spine', 'outline_render.py'),
                        os.path.join(folder, 'outline.json')], capture_output=True, text=True, cwd=WS)
    print('render:', (r.stdout + r.stderr).strip()[-1500:])
    return r.returncode


def claim_of(folder, phrase):
    """claim ids whose text holds the phrase (for covered: dispositions)"""
    cm = json.load(open(os.path.join(folder, 'claim_map.json'), encoding='utf-8'))
    norm = lambda s: ' '.join(H.unescape(s).lower().split())
    hit = [c['id'] for c in cm['claims'] if norm(phrase) in norm(c.get('new_text', ''))]
    return hit


def dispositions(folder, disp):
    """disp {card key: 'covered:@phrase1|phrase2 note' or any other disposition}; resolves @phrases to claim ids"""
    out, bad = {}, []
    for k, v in disp.items():
        if v.startswith('covered:@'):
            body = v[len('covered:@'):]
            phrases, _, note = body.partition(' ## ')
            got = []
            for ph in phrases.split('|'):
                c = claim_of(folder, ph)
                if not c:
                    bad.append((k, ph))
                got += c[:2]
            out[k] = 'covered:%s %s' % (','.join(dict.fromkeys(got)), note or phrases.split('|')[0][:60])
        else:
            out[k] = v
    json.dump(out, open(os.path.join(folder, 'cards_disposition.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    return bad


def card_keys(folder):
    """every card and statement key in cards.md"""
    keys = []
    for l in open(os.path.join(folder, 'cards.md'), encoding='utf-8'):
        m = re.match(r'## (?:candidate|must) (\S+)', l) or re.match(r'## card (\S+)', l)
        if m:
            keys.append(m.group(1))
        m = re.match(r'- \[([^\]]+)\]', l)
        if m:
            keys.append(m.group(1))
    return keys
