#!/usr/bin/env python3
"""ui_retired.py: nothing in the Retired table of docs/ui/UI_MAP.md comes back (D-20261105-1; gate check ui-retired, s169).

  python3 tools/spine/ui_retired.py PAGE [UI_MAP.md]      prints each hit; exit 1 on any hit or unreadable entry

The table's first column is read entry by entry: a cell holds one or more items separated by commas; a note in
parentheses is dropped. An item is one of:
  --name          a custom property: no declaration or var() of it in the page's styles or scripts
  --prefix-*      custom properties starting with the prefix: none in the page's styles or scripts
  #id             an id: no element with that id in the markup, no "#id" in a style selector, no 'id' string in a script
  .prefix-*       a class prefix: no class starting with it in a style selector, the markup or a script string
  "Label"         visible text (in quotes, then any words describing it): not in the page text or a script string,
                  case ignored; the change log block and HTML comments are left out
  any selector    (lower case) no style rule selects it: the selector, whitespace normalized, is not part of any rule's selector
                  list at a compound boundary; and it matches no element in the markup (soupsieve)
Script-built elements are covered through their styles and, for ids and prefixes, through script strings; a retired
compound selector built only by script with no style is not detected.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.dirname(HERE))

AXLOG = re.compile(r'<script type="application/json" id="axlog">.*?</script>', re.S)
STYLE = re.compile(r'<style\b[^>]*>(.*?)</style>', re.S | re.I)
SCRIPT = re.compile(r'<script\b[^>]*>(.*?)</script>', re.S | re.I)
COMMENT = re.compile(r'<!--.*?-->', re.S)


def table_items(md):
    """[(cell, item)] from the Retired table's first column."""
    m = re.search(r'^## Retired\b.*?$(.*?)(?=^## |\Z)', md, re.S | re.M)
    if not m:
        raise ValueError('UI_MAP.md has no "## Retired" section')
    out = []
    for line in m.group(1).splitlines():
        if not line.startswith('|') or re.match(r'^\|\s*:?-{3,}', line) or 'Selector or id' in line:
            continue
        cell = line.strip('|').split('|')[0].strip()
        cell = re.sub(r'\([^()]*\)', '', cell)
        for it in split_items(cell):
            out.append((cell.strip(), it))
    return out


def split_items(cell):
    items, cur, depth, q = [], '', 0, False
    for ch in cell:
        if ch == '"':
            q = not q
        if ch in '([':
            depth += 1
        elif ch in ')]':
            depth -= 1
        if ch == ',' and depth == 0 and not q:
            items.append(cur.strip()); cur = ''
        else:
            cur += ch
    if cur.strip():
        items.append(cur.strip())
    return [i.strip('` ') for i in items if i.strip('` ')]


def norm(sel):
    sel = re.sub(r'\s*([>+~])\s*', r' \1 ', sel.strip())
    return re.sub(r'\s+', ' ', sel)


def css_selectors(css):
    """Every rule selector in the style text (inside @media, @layer and @supports blocks too), normalized."""
    import tinycss2
    out = []

    def walk(rules):
        for r in rules:
            if r.type == 'qualified-rule':
                for s in split_items(tinycss2.serialize(r.prelude)):
                    out.append(norm(s))
                if r.content:
                    inner = tinycss2.parse_rule_list(r.content, skip_comments=True, skip_whitespace=True)
                    if any(x.type == 'qualified-rule' for x in inner):
                        walk(inner)
            elif r.type == 'at-rule' and r.content is not None:
                walk(tinycss2.parse_rule_list(r.content, skip_comments=True, skip_whitespace=True))
    walk(tinycss2.parse_stylesheet(css, skip_comments=True, skip_whitespace=True))
    return out


def sel_hit(retired, selectors):
    """A selector in the list that contains the retired one at a compound boundary."""
    r = norm(retired)
    lead = r[0] in '.#[:'
    pat = re.compile((r'' if lead else r'(?:^|(?<=[\s>+~(]))') + re.escape(r) + r'(?![\w-])')
    for s in selectors:
        if pat.search(s):
            return s
    return None


def parts(html):
    html = AXLOG.sub('', html)
    css = '\n'.join(STYLE.findall(html))
    js = '\n'.join(s for s in SCRIPT.findall(html))
    markup = COMMENT.sub('', SCRIPT.sub('', STYLE.sub('', html)))
    markup = re.sub(r'</?template\b[^>]*>', '', markup)
    return css, js, markup


def check(html, md):
    """[(cell, item, where)] for every item that is back, and [(cell, item, 'unreadable')] for one that is not an item."""
    from bs4 import BeautifulSoup
    css, js, markup = parts(html)
    sels = css_selectors(css)
    soup = BeautifulSoup(markup, 'lxml')
    text = soup.get_text(' ').lower()
    strings = re.findall(r'"((?:[^"\\]|\\.)*)"|\'((?:[^\'\\]|\\.)*)\'', js)
    strings = [a or b for a, b in strings]
    hits = []
    for cell, it in table_items(md):
        if it.startswith('"'):
            m = re.match(r'"([^"]+)"', it)
            label = m.group(1).lower() if m else ''
            if not label:
                hits.append((cell, it, 'unreadable')); continue
            if label in text:
                hits.append((cell, it, 'page text'))
            elif any(label in s.lower() for s in strings):
                hits.append((cell, it, 'script string'))
            continue
        if re.fullmatch(r'--[\w-]+\*', it):
            if re.search(re.escape(it[:-1]) + r'[\w-]*', css + '\n' + js):
                hits.append((cell, it, 'custom property prefix in styles or scripts'))
            continue
        if it.startswith('--'):
            name = re.match(r'--[\w-]+', it).group(0)
            if re.search(re.escape(name) + r'(?![\w-])', css + '\n' + js):
                hits.append((cell, it, 'custom property in styles or scripts'))
            continue
        if re.fullmatch(r'\.[\w-]+\*', it):
            pre = it[1:-1]
            rx = re.compile(r'(?<![\w-])' + re.escape(pre) + r'[\w-]*')
            if any(re.search(r'\.' + re.escape(pre), s) for s in sels):
                hits.append((cell, it, 'style selector'))
            elif soup.find(class_=lambda c: c and any(x.startswith(pre) for x in c.split())):
                hits.append((cell, it, 'markup class'))
            elif any(rx.fullmatch(t) for s in strings for t in s.split()):
                hits.append((cell, it, 'script string'))
            continue
        if re.fullmatch(r'#[\w-]+', it):
            name = it[1:]
            if soup.find(id=name):
                hits.append((cell, it, 'markup id'))
            elif sel_hit(it, sels):
                hits.append((cell, it, 'style selector ' + sel_hit(it, sels)))
            elif name in strings or ('#' + name) in strings:
                hits.append((cell, it, 'script string'))
            continue
        if not re.match(r'^[\w.#\[:*>+~ -]', it) or re.search(r'[A-Z]', it):
            hits.append((cell, it, 'unreadable')); continue
        h = sel_hit(it, sels)
        if h:
            hits.append((cell, it, 'style selector ' + h)); continue
        try:
            if soup.select_one(it):
                hits.append((cell, it, 'markup element'))
        except Exception:
            hits.append((cell, it, 'unreadable'))
    return hits


def ui_map_path():
    import docs_path
    return docs_path.doc(os.path.join('ui', 'UI_MAP.md'))


def main(argv):
    if not argv:
        sys.exit(__doc__)
    md_path = argv[1] if len(argv) > 1 else ui_map_path()
    hits = check(open(argv[0], encoding='utf-8').read(), open(md_path, encoding='utf-8').read())
    for cell, it, where in hits:
        print('RETIRED %-40s %s' % (it, where))
    n = len(table_items(open(md_path, encoding='utf-8').read()))
    print('UI-RETIRED %s (%d items, %d back or unreadable)' % ('FAIL' if hits else 'PASS', n, len(hits)))
    return 1 if hits else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
