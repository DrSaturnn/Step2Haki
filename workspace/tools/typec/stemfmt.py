#!/usr/bin/env python3
"""stemfmt.py: scannable question stems and NBME question blocks for lean briefs (Jonathan 2026-10-01).

A stem is a list of lines, each (kind, text):
  'l'  lead line: age, sex and the complaint (opens the stem, I2)
  'i'  indented finding: one clause per line, drawn with the bottom line's indent rule
  's'  plain line: history or a pertinent negative
  'd'  data line (muted): vitals, labs, mental status, joined with ' &middot; '
Authored stems are 30 to 40 words (count_words). The page's mcq() clones the stem fragment, so the spans survive;
typec.css ("question stems") lays them out. Text stays plain words, so checks that read the stem still work."""
import re, html as H

KIND = {'l': 'sl', 'i': 'si', 's': 'ss', 'd': 'sd'}


def stem_html(lines):
    out = []
    for kind, text in lines:
        if kind == 'd' and isinstance(text, (list, tuple)):
            text = ' &middot; '.join(H.escape(t, quote=False) for t in text)
        else:
            text = H.escape(text, quote=False)
        out.append(f'<span class="{KIND[kind]}">{text}</span>')
    return '\n'.join(out)


def count_words(lines):
    t = ' '.join(' '.join(x) if isinstance(x, (list, tuple)) else x for _, x in lines)
    return len(t.split())


def restem(li, stem, explanation=None, bump=True):
    """Replace the stem of a bank <li> (text before the first ' &rarr; '), bump its version, optionally its explanation."""
    head, rest = li.split('>', 1)
    i = rest.index(' &rarr; ')
    if bump:
        v = int(re.search(r'data-item-version="(\d+)"', head).group(1))
        head = head.replace(f'data-item-version="{v}"', f'data-item-version="{v + 1}"')
    tail = rest[i:]
    if explanation is not None:
        j = tail.index(' &rarr; ', len(' &rarr; '))
        tail = tail[:j] + ' &rarr; ' + explanation + tail[tail.index('</li>'):]
    return head + '>' + stem + tail


def nbq(nid, n, stem, ask, competing, two, decider):
    """An NBME question in its framing block: compact stem with every clue, the competing answers (pull, then the
    masked reason it fails) and the final two (the masked decider). Not in the bank (Jonathan 2026-10-01)."""
    lis = ''.join(f'<li><b>{o}</b>: {pull} <span class="mask">{why}</span></li>' for o, pull, why in competing)
    return (f'<div class="pearls nbq" data-nbme="{nid}"><span class="lbl">How NBME framed it: question {n}</span>'
            f'<p class="nbstem">{stem}</p><p class="nbask">{ask}</p><span class="nbh">Competing answers</span><ul>{lis}</ul>'
            f'<p class="two"><b>Down to two:</b> {two} <span class="mask">{decider}</span></p></div>')


def relabel(li, role, label, taken):
    """Change one option's label and give it a new option id (gate id-immutable allows a new id only with a changed
    label and a bumped version; restem() bumps the version). role: 'key', 'd1' or 'd2'."""
    import os, sys
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
    from idgen import _mint
    iid = re.search(r'data-item-id="([^"]+)"', li).group(1)
    attr = {'key': 'data-key-id', 'd1': 'data-d1-id', 'd2': 'data-d2-id'}[role]
    new_id = _mint('o', 'o|%s|%s|%s|relabel-2026-10-01' % (role, label, iid), taken)
    li = re.sub(r'%s="[^"]+"' % attr, '%s="%s"' % (attr, new_id), li, count=1)
    if role == 'key':
        li = re.sub(r'(&rarr; <b>)(.*?)(</b> &rarr;)', lambda m: m.group(1) + H.escape(label, quote=False) + m.group(3), li, count=1)
    else:
        li = re.sub(r'data-%s="[^"]*"' % role, 'data-%s="%s"' % (role, H.escape(label)), li, count=1)
    return li
