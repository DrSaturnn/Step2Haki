#!/usr/bin/env python3
"""Rebuild the anchor allow list from the page: python3 repair/s172e/allow.py PAGE

Keeps a "trigger|title" pair only when a trigger on PAGE fails prose_lint's word test: every such pair on a term
trigger (class sp-a; all were judged in the anchor pass), and such pairs on label triggers that the list already
held. Lowers the count in tools/spine/allow_baseline.json.
"""
import json
import os
import re
import sys

WS = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.insert(0, os.path.join(WS, 'tools', 'spine'))
sys.path.insert(0, os.path.join(WS, 'tools'))
import pagelib as P  # noqa: E402
import prose_lint as L  # noqa: E402
import site_build  # noqa: E402

ALLOW = os.path.join(WS, 'repair', 'efficiency', 'ANCHOR_ALLOW.json')
BASE = os.path.join(WS, 'tools', 'spine', 'allow_baseline.json')


class Rec(set):
    def __init__(self):
        super().__init__()
        self.seen = set()

    def __contains__(self, k):
        self.seen.add(k)
        return False


def keys(page):
    r = Rec()
    L._ANCHOR = r
    for b in L.briefs(page):
        L.lint_brief(b.inner)
    return r.seen


def main():
    page = site_build.unwrap(P.read_page(sys.argv[1]))
    every = keys(page)
    term = keys(re.sub(r'(<button\b[^>]*\bclass="sp-pop(?! sp-a)[^"]*"[^>]*>)(.*?)(</button>)', r'\1\3', page, flags=re.S))
    cur = json.load(open(ALLOW))
    old = set(cur['fits'])
    label = every - term
    new = sorted(term | (label & old))
    cur['fits'] = new
    json.dump(cur, open(ALLOW, 'w'), indent=1, ensure_ascii=False)
    open(ALLOW, 'a').write('\n')
    b = json.load(open(BASE))
    b['repair/efficiency/ANCHOR_ALLOW.json']['count'] = len(new)
    json.dump(b, open(BASE, 'w'), indent=1)
    open(BASE, 'a').write('\n')
    print('allow list %d (was %d): term triggers %d, label triggers carried %d; label triggers failing and unlisted %d'
          % (len(new), len(old), len(term), len(label & old), len(label - old)))


if __name__ == '__main__':
    main()
