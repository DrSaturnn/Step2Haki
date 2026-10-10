"""passages: short passages from cached source pages, so no agent loads a whole page (plan 0.6).

  python3 tools/spine/passages.py <sha> "<term>" ["<term>" ...] [--context 1] [--max 8]
  python3 tools/spine/passages.py --all "<term>" ...        search every cached page

Prints each matching line (case-insensitive; a line is a block of the page) with --context lines either side,
under its nearest preceding heading-like line (short, no final period), and the sha to cite.
"""
import json
import os
import re
import sys

WS = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
CACHE = os.path.join(WS, 'repair', 'sources', 'web')


def heading(lines, i):
    for j in range(i - 1, max(-1, i - 40), -1):
        l = lines[j]
        if 3 < len(l) < 70 and not l.endswith('.'):
            return l
    return ''


def main(argv):
    if not argv:
        sys.exit(__doc__.strip().splitlines()[2].strip())
    ctx = int(argv[argv.index('--context') + 1]) if '--context' in argv else 1
    mx = int(argv[argv.index('--max') + 1]) if '--max' in argv else 8
    args = [a for i, a in enumerate(argv) if not a.startswith('--') and not (i and argv[i - 1] in ('--context', '--max'))]
    if '--all' in argv:
        shas, terms = [f[:-4] for f in os.listdir(CACHE) if f.endswith('.txt')], args
    else:
        shas, terms = [args[0]], args[1:]
    ix = json.load(open(os.path.join(CACHE, 'index.json'), encoding='utf-8'))
    pat = re.compile('|'.join(re.escape(t) for t in terms), re.I)
    shown = 0
    for sha in shas:
        lines = open(os.path.join(CACHE, sha + '.txt'), encoding='utf-8').read().split('\n')
        for i, l in enumerate(lines):
            if pat.search(l) and shown < mx:
                shown += 1
                print('--- %s (%s) under "%s"' % (sha, ix.get(sha, {}).get('title', '')[:50], heading(lines, i)))
                print('\n'.join(lines[max(0, i - ctx):i + ctx + 1]))
    if not shown:
        print('no passage matches', terms)


if __name__ == '__main__':
    main(sys.argv[1:])
