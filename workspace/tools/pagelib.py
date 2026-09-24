"""pagelib: offset-exact parsing and splicing for the AxBx index.html.

Everything here works on the page as a Python str read with newline='' so that
character offsets map 1:1 back to the file and a write reproduces every byte we
did not touch. Nothing here re-serializes a DOM.

Public API
  read_page(path) -> str            write_page(path, html)
  briefs(html) -> [Brief]           brief_by_id(html, id) -> Brief
  items(html)  -> [Item]            (every <li> carrying data-item-id)
  attrs(tag)   -> dict (raw, entity-encoded values, document order)
  split_arrows(inner_html) -> [raw segment html]  (direct-child arrows only)
  text(html)   -> visible text, tags stripped, entities decoded
  splice(html, [(start, end, new), ...]) -> html  (non-overlapping, any order)
  count(hay, needle), find_unique(hay, needle, what)
"""
import html as _html
import re
from dataclasses import dataclass, field

ATTR_RE = re.compile(r'([A-Za-z_:][-A-Za-z0-9_:.]*)(?:\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|([^\s>]+)))?')
DIV_TOKEN = re.compile(r'<!--.*?-->|<div\b[^>]*>|</div\s*>', re.S | re.I)
LI_TOKEN = re.compile(r'<!--.*?-->|<li\b[^>]*>|</li\s*>', re.S | re.I)
OPEN_BRIEF = re.compile(r'<div\b[^>]*\bclass="([^"]*)"[^>]*>', re.I)
ITEM_OPEN = re.compile(r'<li\b[^>]*\bdata-item-id="[^"]*"[^>]*>', re.I)
ARROW_RE = re.compile(r'→|&rarr;|&#8594;|&#x2192;', re.I)
ITEM_ATTRS = ['data-type', 'data-d1', 'data-d2', 'data-item-id', 'data-item-version',
              'data-item-status', 'data-key-id', 'data-d1-id', 'data-d2-id']
TYPES = {'next', 'dx', 'test', 'mech', 'avoid', 'screen', 'stage', 'claim'}
STATUSES = {'ready', 'needs_source', 'needs_repair'}
QID_RE = re.compile(r'^q_[0-9a-f]{20}$')
OID_RE = re.compile(r'^o_[0-9a-f]{20}$')


def read_page(path):
    with open(path, encoding='utf-8', newline='') as f:
        return f.read()


def write_page(path, html):
    with open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(html)


def attrs(tag):
    """Attributes of an opening tag, raw (entity-encoded) values, in order."""
    m = re.match(r'<\s*[A-Za-z0-9]+', tag)
    body = tag[m.end():] if m else tag
    body = body.rstrip('>').rstrip('/')
    out = {}
    for a in ATTR_RE.finditer(body):
        v = a.group(2) if a.group(2) is not None else (a.group(3) if a.group(3) is not None else (a.group(4) or ''))
        out[a.group(1).lower()] = v
    return out


def text(fragment):
    """Visible text: drop tags, decode entities once, collapse whitespace."""
    t = re.sub(r'<!--.*?-->', '', fragment, flags=re.S)
    t = re.sub(r'<[^>]+>', '', t)
    return re.sub(r'\s+', ' ', _html.unescape(t)).strip()


def _match_close(html, start, token_re, open_prefix):
    """Offset just past the close tag matching the open tag at `start`."""
    depth = 0
    for m in token_re.finditer(html, start):
        tok = m.group(0)
        if tok.startswith('<!--'):
            continue
        if tok.lower().startswith(open_prefix):
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                return m.end()
    raise ValueError('unclosed element at offset %d' % start)


@dataclass
class Brief:
    id: str
    kind: str            # brief | bs | aq
    classes: list
    attrs: dict
    start: int           # offset of '<div'
    end: int             # offset just past matching '</div>'
    open_end: int        # offset just past the opening tag
    inner_start: int
    inner_end: int       # offset of the matching '</div>'
    inner: str
    title: str = ''      # decoded <h4> text


def _script_zone(html):
    i = html.find('<script')
    return i if i >= 0 else len(html)


def briefs(html):
    """Every .brief (class token), depth-matched. Never a lazy regex."""
    out = []
    limit = _script_zone(html)
    for m in OPEN_BRIEF.finditer(html, 0, limit):
        classes = m.group(1).split()
        if 'brief' not in classes:
            continue
        a = attrs(m.group(0))
        end = _match_close(html, m.start(), DIV_TOKEN, '<div')
        inner_end = html.rfind('</div', m.start(), end)
        inner = html[m.end():inner_end]
        kind = 'aq' if 'aq' in classes else ('bs' if 'bs' in classes else 'brief')
        h = re.search(r'<h4\b[^>]*>(.*?)</h4>', inner, re.S)
        title = text(re.sub(r'<span class="nbmechip".*?</span>', '', h.group(1))) if h else ''
        out.append(Brief(a.get('id', ''), kind, classes, a, m.start(), end, m.end(),
                         m.end(), inner_end, inner, title))
    return out


def brief_by_id(html, bid):
    hits = [b for b in briefs(html) if b.id == bid]
    if len(hits) != 1:
        raise KeyError('brief id %r found %d times' % (bid, len(hits)))
    return hits[0]


@dataclass
class Item:
    id: str
    attrs: dict
    start: int
    end: int
    open_end: int
    inner_start: int
    inner_end: int
    inner: str
    brief_id: str = ''
    segments: list = field(default_factory=list)

    @property
    def stem(self):
        return text(self.segments[0]) if self.segments else text(self.inner)

    @property
    def key(self):
        """Keyed answer = arrow segment 2 (never 'the first <b>')."""
        return text(self.segments[1]) if len(self.segments) > 1 else ''

    @property
    def companion(self):
        return ' → '.join(text(s) for s in self.segments[2:])


def split_arrows(inner):
    """Split on arrows in direct-child text only; nested markup is content."""
    segs, depth, last, pos = [], 0, 0, 0
    tag_re = re.compile(r'<!--.*?-->|<(/?)([A-Za-z0-9]+)\b[^>]*?(/?)>', re.S)
    voids = {'br', 'img', 'wbr', 'hr', 'input', 'meta', 'link', 'source'}
    while pos < len(inner):
        tm = tag_re.search(inner, pos)
        chunk_end = tm.start() if tm else len(inner)
        if depth == 0:
            for am in ARROW_RE.finditer(inner, pos, chunk_end):
                segs.append(inner[last:am.start()])
                last = am.end()
        if not tm:
            break
        if not tm.group(0).startswith('<!--'):
            name = tm.group(2).lower()
            if tm.group(1):
                depth = max(0, depth - 1)
            elif not tm.group(3) and name not in voids:
                depth += 1
        pos = tm.end()
    segs.append(inner[last:])
    return segs


def items(html, with_briefs=True):
    """Every <li> with data-item-id, with offsets and arrow segments."""
    bl = briefs(html) if with_briefs else []
    out = []
    limit = _script_zone(html)
    for m in ITEM_OPEN.finditer(html, 0, limit):
        a = attrs(m.group(0))
        end = _match_close(html, m.start(), LI_TOKEN, '<li')
        inner_end = html.rfind('</li', m.start(), end)
        inner = html[m.end():inner_end]
        owner = ''
        for b in bl:
            if b.start < m.start() < b.end:
                owner = b.id
                break
        out.append(Item(a.get('data-item-id', ''), a, m.start(), end, m.end(), m.end(),
                        inner_end, inner, owner, split_arrows(inner)))
    return out


def splice(html, edits):
    """Apply (start, end, replacement) edits by offset. Edits must not overlap."""
    edits = sorted(edits, key=lambda e: (e[0], e[1]))
    for a, b in zip(edits, edits[1:]):
        if b[0] < a[1]:
            raise ValueError('overlapping edits at %d-%d and %d-%d' % (a[0], a[1], b[0], b[1]))
    parts, last = [], 0
    for s, e, new in edits:
        if not (0 <= s <= e <= len(html)):
            raise ValueError('edit out of range %d-%d' % (s, e))
        parts.append(html[last:s])
        parts.append(new)
        last = e
    parts.append(html[last:])
    return ''.join(parts)


def count(hay, needle):
    n, i = 0, hay.find(needle)
    while i >= 0:
        n += 1
        i = hay.find(needle, i + 1)
    return n


def find_unique(hay, needle, what='anchor'):
    """Offset of needle, asserting it occurs exactly once (overlaps counted)."""
    if not needle:
        raise ValueError('%s is empty' % what)
    n = count(hay, needle)
    if n != 1:
        raise ValueError('%s occurs %d times (must be exactly 1): %r' % (what, n, needle[:80]))
    return hay.find(needle)


def set_attr_in_tag(tag, name, value):
    """Return tag with attribute name set to value (raw, already escaped).
    Replaces in place when present, else appends before '>'. Byte-minimal."""
    pat = re.compile(r'(\s' + re.escape(name) + r'=")([^"]*)(")')
    if pat.search(tag):
        return pat.sub(lambda m: m.group(1) + value + m.group(3), tag, count=1)
    close = tag.rfind('>')
    return tag[:close] + ' %s="%s"' % (name, value) + tag[close:]


def esc_attr(s):
    return s.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')


if __name__ == '__main__':
    import sys
    h = read_page(sys.argv[1] if len(sys.argv) > 1 else 'index.html')
    bl, it = briefs(h), items(h)
    from collections import Counter
    print('briefs', len(bl), dict(Counter(b.kind for b in bl)), '| items', len(it))
