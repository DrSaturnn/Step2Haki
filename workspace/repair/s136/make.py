"""make: build repair/s136/50_glance.json from src/glance.css, src/glance.js, tools/glance_accent.py and
tools/glance_dark.py.

  python3 repair/s136/make.py [page.html]     (default: the working page, workspace/index.html)

Run it on the page the batch builds on (after s135's edits): the accent rewrites anchor on whole rules, and the dark
theme repeats every color rule of that page.
"""
import colorsys, json, os, re, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(WS, 'tools'))
import glance_accent as GA  # noqa: E402
import glance_dark as GD  # noqa: E402

import glob  # noqa: E402
import apply_edits  # noqa: E402
OUT = '50_glance.json'
src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(WS, 'index.html')
page = open(src, encoding='utf-8').read()
# the page as the batch builds it up to this file: s135's briefs and site fixes (folded in 2026-10-14) come first
for f in sorted(glob.glob(os.path.join(HERE, '*.json'))):
    if os.path.basename(f) >= OUT:
        continue
    page, _ = apply_edits.apply(page, json.load(open(f, encoding='utf-8')))
tmpd = tempfile.mkdtemp()
page_path = os.path.join(tmpd, 'base.html')
open(page_path, 'w', encoding='utf-8').write(page)
tmp = os.path.join(tmpd, 'acc.json')
subprocess.run([sys.executable, os.path.join(WS, 'tools', 'glance_accent.py'), page_path, tmp], check=True)
acc = json.load(open(tmp))
css = open(os.path.join(HERE, 'src', 'glance.css')).read().replace('/*@TOKENS@*/', acc['tokens_css'])
js = open(os.path.join(HERE, 'src', 'glance.js')).read()

# the page's head CSS as it will be after the accent rewrites, plus the s136 block itself
after = page
for o in acc['edits']:
    after = after.replace(o['find'], o['with'], 1)
head = after[:after.index('</head>')]
head_css = ''.join(re.findall(r'<style[^>]*>(.*?)</style>', head, re.S)) + '\n' + css

# ---- dark tokens ----
MANUAL = {'--lt': 'rgba(255,255,255,.07)', '--lt-soft': 'rgba(255,255,255,.04)', '--dk': 'rgba(0,0,0,.6)',
          '--dk-soft': 'rgba(0,0,0,.42)', '--hair': 'rgba(255,255,255,.09)', '--row-tint': 'rgba(255,255,255,.045)',
          '--glass': 'rgba(30,31,36,.58)', '--glass-2': 'rgba(32,33,38,.94)',
          '--glass-edge': 'inset 0 1px 0 rgba(255,255,255,.10),0 0 0 1px rgba(255,255,255,.10),0 12px 36px rgba(0,0,0,.55)',
          '--glass-edge-2': 'inset 0 1px 0 rgba(255,255,255,.12),0 0 0 .5px rgba(255,255,255,.12),0 18px 48px rgba(0,0,0,.6)'}
tok = {}
for ctx, sel, body in GD.blocks(head_css):
    if sel.strip() != ':root' or ctx:
        continue
    for d in GD.split_top(body, ';'):
        p, _, v = d.partition(':')
        p, v = p.strip(), v.strip()
        if not p.startswith('--') or p.startswith(('--accent', '--acc-', '--axh-')):
            continue
        tok[p] = GD.map_shadow(v) if re.search(r'\dpx', v) else GD.map_colors(v)
tok.update(MANUAL)
dark_canvas = GD.invert([239, 240, 240]); dark_card = GD.invert([237, 238, 238])


def lighten_for_dark(h):
    r = [v / 255 for v in GA.rgb(h)]
    hh, l, s = colorsys.rgb_to_hls(*r)
    for k in range(0, 60):
        c = [v * 255 for v in colorsys.hls_to_rgb(hh, min(0.92, l + k * 0.01), s)]
        # 5.2:1 on the dark card, and 5.0:1 on the lightest tint accent text sits on: the accent's own --accent-bg and
        # the bottom-line panel in flat mode (#2E353D measured; S3 2026-10-14: slate labels were 4.11:1 there)
        bgs = [dark_card, [x * 0.82 + y * 0.18 for x, y in zip(dark_canvas, c)], [46, 53, 61]]
        if (GD.lum(c) + 0.05) / (GD.lum(dark_card) + 0.05) >= 5.2 and \
                all((GD.lum(c) + 0.05) / (GD.lum(g) + 0.05) >= 5.0 for g in bgs):
            return c
    return c


used = sorted(set(re.findall(r'--axh-([0-9A-F]{6})', acc['tokens_css'])))
acc_css = []
for key, name, h in GA.ACCENTS:
    a = lighten_for_dark(h)
    d = ['--accent:%s' % GD.fmt(a, 1), '--acc-rgb:%d,%d,%d' % tuple(round(v) for v in a),
         '--accent-bg:%s' % GD.fmt([c * 0.82 + x * 0.18 for c, x in zip(dark_canvas, a)], 1)]
    d += ['--axh-%s:%s' % (t, GD.fmt(GD.invert(GA.rgb(GA.follow('#' + t, h))), 1)) for t in used]
    sel = '[data-theme="dark"]' if key == 'slate' else '[data-theme="dark"][data-axa="%s"],[data-theme="dark"] [data-axa="%s"]' % (key, key)
    acc_css.append(sel + '{' + ';'.join(d) + '}')
dark = ('\n/* ---- dark theme (Jonathan 2026-10-14): tokens, then every color rule repeated for dark (tools/glance_dark.py) ---- */\n'
        '[data-theme="dark"]{color-scheme:dark;' + ';'.join('%s:%s' % kv for kv in tok.items()) + '}\n'
        + '\n'.join(acc_css) + '\n' + GD.dark_css(head_css) + '\n')
css = css + dark

note = 's136 site layout Phase 1 (claude/pending/S136.md; Jonathan 2026-10-13 and 14)'
edits = acc['edits'] + [
    {'op': 'replace_global', 'find': '</head>', 'with': '<style id="ax-s136">\n' + css + '</style>\n</head>', 'note': note + ': the glance style block'},
    {'op': 'replace_global', 'find': '</script>\n</body>', 'with': '</script>\n<script>\n' + js + '</script>\n</body>', 'note': note + ': the glance script block'},
]
json.dump({'edits': edits}, open(os.path.join(HERE, OUT), 'w'), indent=1)
print(OUT + ': %d edits (%d accent rule rewrites, style %d bytes of which dark %d, script %d bytes)' % (
    len(edits), len(acc['edits']), len(css), len(dark), len(js)))
