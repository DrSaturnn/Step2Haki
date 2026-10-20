#!/usr/bin/env python3
"""s148g (site layer, Jonathan 2026-10-20; claude/pending/SITE_S148G.md): writes repair/s148g/*.json from the live page.

  10_bold_bl.json    bottom lines bold their key words and criteria (data/bold_bl.json; bold only: removing the new <b>
                     tags gives back each bottom line exactly), one brief-scoped replace per brief
  20_firststep.json  First step split for the bands in data/pairs.json (lithium-effects, the renderer's proof): one row group
                     per order, each spanning only its own results; text, masks and hovers carried byte for byte
  40_site.json       page script patches (per-choice reasons in mcq(), the review session and the s148f Review; Open brief
                     on the preview's top row) and src/site_s148g.css + .js appended before </body>, after every layer
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(WS, 'tools'))
sys.path.insert(0, HERE)
from pagelib import read_page, briefs  # noqa: E402
import blbold  # noqa: E402
import w5split  # noqa: E402

NOTE = 's148g (site layer, Jonathan 2026-10-20)'

# ---- page script patches: (find, with, why); each find occurs exactly once in the live page
PATCHES = [
    # 1. mcq(): the choice's reason, from the item's data-key-why / data-d1-why / data-d2-why, inside its button
    ("        b.appendChild(document.createTextNode(optionDefs[oi].label));\n        o.appendChild(b);",
     "        b.appendChild(document.createTextNode(optionDefs[oi].label));\n"
     "        /* s148g: the choice's one-line reason, shown under it once the answer is revealed (Jonathan 2026-10-20) */\n"
     "        var rsn=norm(li.getAttribute(['data-key-why','data-d1-why','data-d2-why'][oi])||'');\n"
     "        if(rsn){ var rs=document.createElement('span'); rs.className='qx-rsn'; rs.textContent=rsn; b.appendChild(rs); box.classList.add('qx-hr'); }\n"
     "        o.appendChild(b);",
     'per-choice reasons in the question card'),
    # 2. the review session: the option label leaves the reason out; the reason shows after the answer
    ("    var c=b.cloneNode(true), k=c.querySelector('.k'); if(k) k.parentNode.removeChild(k);\n"
     "    var optionId=b.dataset.optionId||'';\n"
     "    return {optionId:optionId,text:c.textContent.trim(),right:correctId?optionId===correctId:i===ai};",
     "    var c=b.cloneNode(true), k=c.querySelector('.k'); if(k) k.parentNode.removeChild(k);\n"
     "    var rz=c.querySelector('.qx-rsn'), rw=rz?rz.textContent.trim():''; if(rz) rz.parentNode.removeChild(rz);\n"
     "    var optionId=b.dataset.optionId||'';\n"
     "    return {optionId:optionId,text:c.textContent.trim(),rw:rw,right:correctId?optionId===correctId:i===ai};",
     'review session: label without the reason'),
    ("    h+='<button type=\"button\" data-option-id=\"'+esc(o.optionId)+'\" data-r=\"'+(o.right?1:0)+'\"><span class=\"k\">'+'ABC'[i]+'</span>'+esc(o.text)+'</button>';",
     "    h+='<button type=\"button\" data-option-id=\"'+esc(o.optionId)+'\" data-r=\"'+(o.right?1:0)+'\"><span class=\"k\">'+'ABC'[i]+'</span>'+"
     "(o.rw?'<span class=\"qx-ol\">'+esc(o.text)+'<span class=\"qx-rsn\">'+esc(o.rw)+'</span></span>':esc(o.text))+'</button>';",
     'review session: the reason under its choice after the answer'),
    # 3. s148f Review rows: labels without the reason; the three choices with their reasons
    ("  function renderReview(bw){",
     "  function lab(b){ var c = b.cloneNode(true); Array.prototype.forEach.call(c.querySelectorAll('.k, .qx-rsn'), function(n){ n.parentNode.removeChild(n); }); return norm(c.textContent); }\n"
     "  function renderReview(bw){",
     'Review: option label helper'),
    ("        var ans = right ? txt(right).replace(/^[ABC]\\s*/, '') : txt(ansNode);\n"
     "        var rk = right ? right.querySelector('.k') : null; if(rk) ans = norm(right.textContent.slice(rk.textContent.length));\n"
     "        var picked = q.querySelector('.opts button.wrong'); var pk = picked ? picked.querySelector('.k') : null;",
     "        var ans = right ? lab(right) : txt(ansNode);\n"
     "        var picked = q.querySelector('.opts button.wrong');",
     'Review: key label without the reason'),
    ("        if(picked) r.querySelector('.qx-rc').textContent = 'You chose: ' + (pk ? norm(picked.textContent.slice(pk.textContent.length)) : txt(picked));",
     "        if(picked) r.querySelector('.qx-rc').textContent = 'You chose: ' + lab(picked);\n"
     "        if(q.classList.contains('qx-hr')){                         // s148g: the three choices, each with its reason\n"
     "          var ch = document.createElement('span'); ch.className = 'qx-rch';\n"
     "          Array.prototype.forEach.call(q.querySelectorAll('.opts button'), function(b){\n"
     "            var rs = b.querySelector('.qx-rsn'), key = b.dataset.correct === '1', mine = b === picked, row = document.createElement('span');\n"
     "            row.className = 'qx-rco' + (key ? ' k' : mine ? ' p' : '');\n"
     "            row.innerHTML = '<i aria-hidden=\"true\"></i><span><b></b></span>';\n"
     "            row.querySelector('i').textContent = key ? '\\u2713' : mine ? '\\u2715' : '\\u2022';\n"
     "            row.querySelector('b').textContent = lab(b);\n"
     "            if(rs) row.querySelector('span').appendChild(document.createTextNode(norm(rs.textContent)));\n"
     "            ch.appendChild(row);\n"
     "          });\n"
     "          r.querySelector('.qx-rb').appendChild(ch);\n"
     "        }",
     'Review: the choices with their reasons'),
    # 4. the linked-brief preview: Open brief moves to the card's top row (Jonathan 2026-10-20)
    ("    pv.innerHTML = '<span class=\"qx-pk\">Linked brief</span><span class=\"qx-pt\"></span>' + (q ? '<span class=\"qx-pq\"></span>' : '') +\n"
     "      '<button type=\"button\" class=\"qx-po\">Open brief</button>';",
     "    pv.innerHTML = '<span class=\"qx-ph\"><span class=\"qx-pk\">Linked brief</span><button type=\"button\" class=\"qx-po\">Open brief</button></span>' +\n"
     "      '<span class=\"qx-pt\"></span>' + (q ? '<span class=\"qx-pq\"></span>' : '');",
     'preview: Open brief on the top row'),
]


def gen(page_path=None, out_dir=None):
    s = read_page(page_path or os.path.join(WS, 'index.html'))
    out_dir = out_dir or HERE
    assert 'id="ax-s148g"' not in s, 'the page already carries s148g'
    B = {b.id: b for b in briefs(s)}

    # 10: bold in bottom lines
    spec = json.load(open(os.path.join(HERE, 'data', 'bold_bl.json'), encoding='utf-8'))
    E, nb = [], 0
    for bid in sorted(k for k in spec if not k.startswith('_')):
        h = s[B[bid].start:B[bid].end]
        a, b = blbold.region(h)
        old = h[a:b]
        new = blbold.apply(old, spec[bid])
        assert blbold.unbold_equal(old, new), bid
        assert h.count(old) == 1, bid
        nb += len(spec[bid])
        E.append({'op': 'replace', 'brief': bid, 'find': old, 'with': new, 'note': NOTE + ': bottom line key words bold (bold only)'})
    json.dump({'edits': E}, open(os.path.join(out_dir, '10_bold_bl.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)

    # 20: First step split
    pairs = json.load(open(os.path.join(HERE, 'data', 'pairs.json'), encoding='utf-8'))
    F = []
    for bid in sorted(k for k in pairs if not k.startswith('_')):
        h = s[B[bid].start:B[bid].end]
        for band, pair in pairs[bid]:
            old, new = w5split.split(h, band, pair)
            assert h.count(old) == 1
            F.append({'op': 'replace', 'brief': bid, 'find': old, 'with': new, 'note': NOTE + ': First step split, one row group per order'})
    json.dump({'edits': F}, open(os.path.join(out_dir, '20_firststep.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)

    # 40: script patches and the layer
    G = []
    for find, with_, why in PATCHES:
        assert s.count(find) == 1, 'patch anchor not unique (%d): %s' % (s.count(find), why)
        G.append({'op': 'replace_global', 'find': find, 'with': with_, 'note': NOTE + ': ' + why})
    css = open(os.path.join(HERE, 'src', 'site_s148g.css'), encoding='utf-8').read().strip()
    js = open(os.path.join(HERE, 'src', 'site_s148g.js'), encoding='utf-8').read().strip()
    assert '</script' not in js and '</style' not in css and s.count('</body>') == 1
    G.append({'op': 'replace_global', 'find': '</body>',
              'with': '<style id="ax-s148g">\n%s\n</style>\n<script id="ax-s148g-js">\n%s\n</script>\n</body>' % (css, js),
              'note': NOTE + ': per-choice reasons, card space, touch hover cards, linked-brief panel, First step split, timeline tile'})
    json.dump({'edits': G}, open(os.path.join(out_dir, '40_site.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print('gen s148g: %d bottom lines (%d bold phrases); %d First step splits; %d script patches + layer (%d B CSS, %d B JS)'
          % (len(E), nb, len(F), len(PATCHES), len(css), len(js)))


if __name__ == '__main__':
    gen()
