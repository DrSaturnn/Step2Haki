"""shingle_check: 10-word copy check of one rewritten brief against its own source quotes and every vendor source.

  python3 tools/spine/shingle_check.py <brief.html> <claim_map.json> [--bank <bank-id>] [--show N]

Replaces the per-brief /tmp ovl_*.py scripts. Checks the learner-facing text above the Practice header (the
<h5> whose id is the bank id; default: the first h5.authored-hdr) against:
  - every source_says quote in the claim map (any depth), and
  - every vendor source file under repair/sources (question files, Aquifer text, and the AnKing card text
    anki/anki_cards.txt), chosen by vendor_scan.is_vendor so the indexes and databases are not read.
Prints the shared 10-word runs and the longest run; exit 1 when any run is shared (fix by rewording).
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import vendor_scan as v  # noqa: E402


def quotes(o, out):
    if isinstance(o, dict):
        for k, x in o.items():
            if k == 'source_says' and isinstance(x, str):
                out.append(x)
            else:
                quotes(x, out)
    elif isinstance(o, list):
        for x in o:
            quotes(x, out)
    return out


def above_bank(h, bank):
    if bank:
        m = re.search(r'<h5\b[^>]*\bid="%s"' % re.escape(bank), h)
    else:
        m = re.search(r'<h5\b[^>]*class="[^"]*authored-hdr', h)
    if not m:
        sys.exit('shingle_check: Practice header not found (pass --bank <bank-id>)')
    return h[:m.start()]


def main(argv):
    if len(argv) < 2:
        sys.exit(__doc__.strip().splitlines()[2].strip())
    brief, cmap = argv[0], argv[1]
    bank = argv[argv.index('--bank') + 1] if '--bank' in argv else None
    show = int(argv[argv.index('--show') + 1]) if '--show' in argv else 15
    ws = os.path.abspath(os.path.join(HERE, '..', '..'))
    body = above_bank(open(brief, encoding='utf-8').read(), bank)
    src = {}
    for q in quotes(json.load(open(cmap, encoding='utf-8')), []):
        for s in v.shingles(v.words(q)):
            src.setdefault(s, 'claim map quote')
    sdir = os.path.join(ws, 'repair', 'sources')
    for root, _, fs in os.walk(sdir):
        for f in fs:
            rel = os.path.relpath(os.path.join(root, f), sdir)
            if v.is_vendor(rel):
                for s in v.shingles(v.words(open(os.path.join(root, f), encoding='utf-8', errors='replace').read())):
                    src.setdefault(s, rel)
    bw = v.words(body)
    sh = v.shingles(bw)
    hit = sh & src.keys()
    print('shingle_check: %d brief shingles, %d shared, longest shared run %d words' % (len(sh), len(hit), v.longest_run(bw, hit)))
    for x in sorted(hit)[:show]:
        print('  [%s] %s' % (src[x], x))
    return 1 if hit else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
