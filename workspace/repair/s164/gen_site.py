"""s164 site layer: writes repair/s164/60_site.json (replace_global ops) from the live page.
Item 1 (phone rail, pilot repair/pilots/phone-rail/make_pilot.py, the same replacement).
Item 2 (window figures in the Differential drawer preview) and item 3 (matcher word forms): the s163 C4 preview code
(repair/pilots/criteria-step2/make_batch.py PV_JS, PV_CSS) as shipped, changed in place.
Usage: python3 repair/s164/gen_site.py [page]   (default index.html); prints the op count."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, 'repair', 'pilots', 'phone-rail'))
import make_pilot

PV = [
    # item 3: word forms the matcher missed (UTI, PTSD, depression for Major Depressive Disorder, tuberculous)
    ("  var PV_STOP = /^(a|an|the|of|in|and|or|with|for|to|on|at|by|vs|child|children|adult|adults|disease|disorder|syndrome|criteria|criterion|defining|diagnostic|diagnosis|classic|test)$/;\n",
     "  var PV_STOP = /^(a|an|the|of|in|and|or|with|for|to|on|at|by|vs|child|children|adult|adults|disease|disorder|syndrome|criteria|criterion|defining|diagnostic|diagnosis|classic|test)$/;\n"
     "  /* s164: word forms read as one word: an abbreviation as its words, an adjective as its noun (after the plural trim) */\n"
     "  var PV_FORMS = {uti: ['urinary', 'tract', 'infection'], ptsd: ['posttraumatic', 'stress'], mdd: ['major', 'depression'], depressive: ['depression'], tuberculou: ['tuberculosi']};\n",
     's164 item 3: preview matcher word forms'),
    ("      if(w && !PV_STOP.test(w) && o.indexOf(w) < 0) o.push(w);\n",
     "      (Object.prototype.hasOwnProperty.call(PV_FORMS, w) ? PV_FORMS[w] : [w]).forEach(function(w){ if(w && !PV_STOP.test(w) && o.indexOf(w) < 0) o.push(w); });\n",
     's164 item 3: preview matcher word forms'),
    # item 2: window figures (figure.lcw) in step 2 become tile candidates
    ("    var on = false, bl = [];\n"
     "    Array.prototype.forEach.call(t.querySelectorAll('h5.tsec, div.crit, div.sp-dx'), function(n){\n"
     "      if(n.tagName === 'H5') on = n === h; else if(on && !n.parentElement.closest('div.crit, div.sp-dx')) bl.push(n);\n"
     "    });\n"
     "    if(!bl.length) return null;\n",
     "    var on = false, bl = [], fg = [];   // s164: fg, the step's window figures (figure.lcw)\n"
     "    Array.prototype.forEach.call(t.querySelectorAll('h5.tsec, div.crit, div.sp-dx, figure.lcw'), function(n){\n"
     "      if(n.tagName === 'H5') on = n === h; else if(on && !n.parentElement.closest('div.crit, div.sp-dx, figure.lcw')) (n.tagName === 'FIGURE' ? fg : bl).push(n);\n"
     "    });\n"
     "    if(!bl.length && !fg.length) return null;\n",
     's164 item 2: window figures in the preview'),
    ("    var tt = pvToks((t.querySelector('h4') || {}).textContent || '');\n"
     "    return pvIn(tt, all) || pvIn(core, tt) ? bl[0] : null;\n",
     "    /* s164: a window figure one of whose rows names the row's diagnosis (Brief psychotic disorder, Delirium tremens) */\n"
     "    for(var f = 0; f < fg.length; f++){\n"
     "      var nm = fg[f].querySelectorAll('.wr .nm, .tr .nm');\n"
     "      for(var j = 0; j < nm.length; j++){\n"
     "        var x = nm[j].cloneNode(true); x.querySelectorAll('.mask-toggle, button').forEach(function(y){ y.remove(); });   // the Recall toggle's own words\n"
     "        var nt = pvToks(x.textContent); if(pvIn(core, nt) || pvIn(nt, all)) return fg[f];\n"
     "      }\n"
     "    }\n"
     "    var tt = pvToks((t.querySelector('h4') || {}).textContent || '');\n"
     "    return pvIn(tt, all) || pvIn(core, tt) ? (bl[0] || fg[0]) : null;\n",
     's164 item 2: window figures in the preview'),
    ("/* s163 C4: the linked brief's diagnostic criteria in a Differential row's preview */\n",
     "/* s163 C4: the linked brief's diagnostic criteria in a Differential row's preview */\n"
     "/* s164: a window figure (figure.lcw) in the tile reads as on the phone page: name and window over the bar, one row per block */\n"
     "html body .qx-pv > .brief.sp.qx-pc > figure.lcw{margin:0;max-width:none}\n"
     "html body .qx-pv > .brief.sp.qx-pc .lcw :is(.wr,.tr){display:block}\n"
     "html body .qx-pv > .brief.sp.qx-pc .lcw .wax{grid-template-columns:1fr}\n"
     "html body .qx-pv > .brief.sp.qx-pc .lcw .wsp{display:none}\n",
     's164 item 2: window figures in the preview'),
]


def ops(s):
    out = []
    make_pilot.PAIRS.clear()
    s = make_pilot.apply(s)
    for old, new in make_pilot.PAIRS:
        out.append({'op': 'replace_global', 'find': old, 'with': new, 'note': 's164 item 1: phone in-brief rail reading line'})
    for old, new, note in PV:
        assert s.count(old) == 1, (s.count(old), old[:70])
        s = s.replace(old, new)
        out.append({'op': 'replace_global', 'find': old, 'with': new, 'note': note})
    return out, s


if __name__ == '__main__':
    page = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, 'index.html')
    o, _ = ops(open(page, encoding='utf-8').read())
    json.dump({'edits': o}, open(os.path.join(HERE, '60_site.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print('60_site.json', len(o), 'ops')
