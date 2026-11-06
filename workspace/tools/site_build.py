#!/usr/bin/env python3
"""site_build: builds the page's styles and scripts from workspace/site/ and writes them into the page.

  python3 tools/site_build.py PAGE [--out FILE] [--check] [--no-minify] [--no-index]

site/css/ORDER lists the style files, one per line as "<layer> <file>", in cascade order; site/js/ORDER lists the
script modules in run order. The page keeps its markup; every site style block and script block in it is replaced by
one <style id="ax-css"> in the head and one <script id="ax-js"> before </body>; JSON data blocks and styles inside
inline SVG stay. Comments are stripped and both bundles are minified (esbuild). HTML comments outside scripts and
styles are removed.

Each brief's inner HTML is wrapped in <template class="axl"> so the browser parses it without building it; the page
script builds a brief when it is opened or scrolled near (site/js/core.js AX.brief, site/js/06-load-near.js). The brief's
own tag and inner bytes do not change; an already wrapped page is unwrapped first. --eager writes the page unwrapped.

The search index (s164c, D-20261106-4): after writing a wrapped page, search.json is written beside it by
tools/search_index.js (the search record of every brief, read from the fully built page); the page fetches it after
load. --no-index skips it (a scratch candidate whose search is not under test); an --eager page needs none.

--check: exit 1 if PAGE's bundles differ from a fresh build (the gate runs this so the page never drifts from site/).
"""
import json, os, re, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pagelib  # noqa: E402

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(WS, 'site')
LAYERS = ('tokens', 'base', 'layout', 'components', 'themes')


def read(p):
    return open(p, encoding='utf-8').read()


def order(kind):
    rows = []
    for line in read(os.path.join(SITE, kind, 'ORDER')).splitlines():
        line = line.split('#', 1)[0].strip()
        if line:
            rows.append(line.split())
    return rows


def custom_media(css):
    names = dict(re.findall(r'@custom-media\s+(--[\w-]+)\s+([^;]+);', css))
    css = re.sub(r'@custom-media\s+--[\w-]+\s+[^;]+;\s*', '', css)

    def sub(m):
        q = m.group(1).strip()
        return '@media ' + ' and '.join(names[p.strip()[1:-1]] if re.fullmatch(r'\((--[\w-]+)\)', p.strip()) and p.strip()[1:-1] in names else p.strip()
                                        for p in re.split(r'\s+and\s+', q)) + '{'
    return re.sub(r'@media\s+([^{]+)\{', sub, css)


def esbuild(text, loader, minify=True):
    if not minify:
        return text
    js = ("const e=require('esbuild');let s='';process.stdin.on('data',d=>s+=d).on('end',()=>{"
          "const r=e.transformSync(s,{loader:%r,minify:true,legalComments:'none',target:'esnext',charset:'utf8'});"
          "process.stdout.write(r.code)})" % loader)
    r = subprocess.run(['node', '-e', js], input=text, capture_output=True, text=True, cwd=WS,
                       env=dict(os.environ, NODE_PATH=os.path.join(WS, 'node_modules')))
    if r.returncode:
        raise SystemExit('site_build: esbuild %s failed: %s' % (loader, r.stderr[:2000]))
    return r.stdout.strip()


def build_css(minify=True):
    rows = order('css')
    used = [l for l, _ in rows]
    bad = [l for l in used if l not in LAYERS]
    if bad:
        raise SystemExit('site_build: unknown layer %s in site/css/ORDER' % bad)
    media = read(os.path.join(SITE, 'css', 'media.css'))
    parts = ['@layer %s;' % ','.join(LAYERS)]
    for layer in LAYERS:
        body = '\n'.join(read(os.path.join(SITE, 'css', f)) for l, f in rows if l == layer)
        if body.strip():
            parts.append('@layer %s{\n%s\n}' % (layer, body))
    css = custom_media(media + '\n' + '\n'.join(parts))
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    return esbuild(css, 'css', minify)


def build_js(minify=True):
    out = []
    for row in order('js'):
        f = row[0]
        name = os.path.splitext(os.path.basename(f))[0]
        src = read(os.path.join(SITE, 'js', f))
        if f == 'core.js':
            out.append(src)
        else:
            out.append('AX.module(%s,function(AX){\n%s\n});' % (json.dumps(name), src))
    js = '\n'.join(out)
    return esbuild(js, 'js', minify) if minify else js


SVG_OPEN = re.compile(r'<svg\b', re.I)


def in_svg(html, pos):
    before = html[max(0, pos - 400):pos]
    return before.rfind('<svg') > before.rfind('</svg>')


def assemble(html, css, js):
    # remove site style blocks and script blocks (JSON data kept), then HTML comments outside them
    pieces, last, first_style = [], 0, None
    for m in re.finditer(r'<style\b[^>]*>.*?</style>\s*|<script\b([^>]*)>.*?</script>\s*', html, re.S):
        tag = m.group(0)
        if tag.startswith('<style'):
            if in_svg(html, m.start()):
                continue
            if first_style is None:
                first_style = sum(len(p) for p in pieces) + (m.start() - last)
            pieces.append(html[last:m.start()])
            last = m.end()
        else:
            if re.search(r'application/(?:ld\+)?json', m.group(1) or ''):
                continue
            pieces.append(html[last:m.start()])
            last = m.end()
    pieces.append(html[last:])
    page = ''.join(pieces)
    if first_style is None:
        first_style = page.find('</head>')
    page = page[:first_style] + '<style id="ax-css">' + css + '</style>\n' + page[first_style:]
    end = page.rfind('</body>')
    page = page[:end] + '<script id="ax-js">' + js + '</script>\n' + page[end:]
    # HTML comments outside scripts and styles
    out, last = [], 0
    for m in re.finditer(r'<(script|style)\b.*?</\1>|<!--.*?-->', page, re.S):
        if m.group(0).startswith('<!--'):
            out.append(page[last:m.start()])
            last = m.end()
    out.append(page[last:])
    return ''.join(out)


LAZY_OPEN, LAZY_CLOSE = '<template class="axl">', '</template>'


def unwrap(html):
    out, last = [], 0
    for b in pagelib.briefs(html):
        if b.lazy:
            out += [html[last:b.inner_start - len(LAZY_OPEN)], html[b.inner_start:b.inner_end]]
            last = b.inner_end + len(LAZY_CLOSE)
    out.append(html[last:])
    return ''.join(out)


def wrap(html):
    html = unwrap(html)
    out, last = [], 0
    for b in pagelib.briefs(html):
        out += [html[last:b.inner_start], LAZY_OPEN, html[b.inner_start:b.inner_end], LAZY_CLOSE]
        last = b.inner_end
    out.append(html[last:])
    return ''.join(out)


def bundles(html):
    c = re.search(r'<style id="ax-css">(.*?)</style>', html, re.S)
    j = re.search(r'<script id="ax-js">(.*?)</script>', html, re.S)
    return (c.group(1) if c else None), (j.group(1) if j else None)


def main(a):
    if not a:
        print(__doc__)
        return 2
    page = a[0]
    minify = '--no-minify' not in a
    html = read(page)
    css, js = build_css(minify), build_js(minify)
    if '--check' in a:
        c, j = bundles(html)
        ok = (c == css and j == js)
        print('site_build check: %s (css %s, js %s)' % ('PASS' if ok else 'FAIL', 'same' if c == css else 'differs',
                                                          'same' if j == js else 'differs'))
        return 0 if ok else 1
    new = assemble(unwrap(html) if '--eager' in a else wrap(html), css, js)
    out = a[a.index('--out') + 1] if '--out' in a else page
    open(out, 'w', encoding='utf-8').write(new)
    print('site_build: css %d, js %d chars; page %d > %d' % (len(css), len(js), len(html), len(new)))
    if '--eager' not in a and '--no-index' not in a:
        idx = os.path.join(os.path.dirname(os.path.abspath(out)), 'search.json')
        r = subprocess.run(['node', os.path.join(WS, 'tools', 'search_index.js'), out, idx], capture_output=True, text=True)
        if r.returncode:
            print('site_build: search index FAILED: ' + (r.stdout + r.stderr).strip()[:600])
            return 1
        print(r.stdout.strip())
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
