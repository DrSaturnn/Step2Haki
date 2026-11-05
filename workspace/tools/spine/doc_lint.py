"""doc_lint.py (draft, 2026-11-05): keeps DECISIONS_DIGEST and STANDING_DIRECTIONS from holding two live answers to one question.
Proposed home: tools/spine/doc_lint.py, run at batch launch (the launch gate) and before any doc commit.

Conventions it enforces, for every digest line written from 2026-11-05 on (older lines get ids in the refactor's audit):
- the line starts "- YYYY-MM-DD [D-YYYYMMDD-n] {topic}" ; topic is a short tag (workup, sidebar, fit, motion, theme ...);
- a line that changes an earlier decision says "supersedes D-..." ; the earlier line must then end "(superseded by D-...)";
- STANDING_DIRECTIONS cites digest ids as [D-...] ; citing a superseded id fails.

Usage:
  python3 doc_lint.py DIGEST.md STANDING.md            # fail (exit 1) on broken supersession or stale citations
  python3 doc_lint.py DIGEST.md STANDING.md --topic workup   # every live decision on one topic, newest first
"""
import re, sys

LINE = re.compile(r'^- (\d{4}-\d{2}-\d{2}) \[(D-\d{8}-\d+)\] \{([\w-]+)\}(.*)$')

def parse(digest):
    out = {}
    for raw in open(digest, encoding='utf-8').read().splitlines():
        m = LINE.match(raw)
        if m:
            date, did, topic, rest = m.groups()
            out[did] = {'date': date, 'topic': topic, 'text': rest.strip(),
                        'supersedes': re.findall(r'supersedes (D-\d{8}-\d+)', rest),
                        'superseded_by': re.findall(r'\(superseded by (D-\d{8}-\d+)\)', rest)}
    return out

def main(a):
    if len(a) < 2: print(__doc__); return 2
    d = parse(a[0]); standing = open(a[1], encoding='utf-8').read(); errs = []
    for did, e in d.items():
        for t in e['supersedes']:
            if t not in d: errs.append(f'{did} supersedes {t}, which is not in the digest')
            elif did not in d[t]['superseded_by']: errs.append(f'{t} is superseded by {did} but not marked "(superseded by {did})"')
    for cited in set(re.findall(r'\[(D-\d{8}-\d+)\]', standing)):
        if cited in d and d[cited]['superseded_by']:
            errs.append(f'STANDING_DIRECTIONS cites {cited}, superseded by {d[cited]["superseded_by"][0]}: update the line')
        if cited not in d: errs.append(f'STANDING_DIRECTIONS cites {cited}, which is not in the digest')
    if '--topic' in a:
        t = a[a.index('--topic') + 1]
        live = sorted([(e['date'], k, e['text']) for k, e in d.items() if e['topic'] == t and not e['superseded_by']], reverse=True)
        print(f'live decisions on {{{t}}}, newest first:'); [print(' ', x[0], x[1], x[2][:160]) for x in live]
    if errs: print('DOC-LINT FAIL'); [print(' ', x) for x in errs]; return 1
    print(f'DOC-LINT PASS ({len(d)} ids checked)'); return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
