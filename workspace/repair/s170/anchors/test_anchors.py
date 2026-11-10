#!/usr/bin/env python3
"""Offline tests for anchors.py row moves: python3 repair/s170/anchors/test_anchors.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import anchors as A  # noqa: E402

ROW = ('<table><tr><td>Alpha disease <span class="aka">(alpha)</span></td><td><span>Wrist pain</span></td>'
       '<td><span class="mask"><button type="button" class="sp-pop sp-a" aria-controls="p1">Sign positive</button> '
       '<span class="sp-pop-b" id="p1" hidden><span class="sp-ct">Alpha</span>Body.</span></span></td></tr>'
       '<tr><td><span class="mask">Beta</span> disease</td><td><button type="button" class="sp-pop sp-a" '
       'aria-controls="p2">x</button> <span class="sp-pop-b" id="p2" hidden>B</span></td></tr></table>')


def main():
    ok = 0
    pos = ROW.index('aria-controls="p1"')
    f = A.row_head_term(ROW, pos, 'Alpha disease')
    assert f and ROW[f[0]:f[1]] == 'Alpha disease' and f[0] < ROW.index('Wrist'), f
    ok += 1
    assert A.row_head_term(ROW, pos, 'Wrist pain') is None          # second cell is never searched
    ok += 1
    assert A.row_head_term(ROW, pos, 'alpha') is not None            # plain text inside a child tag counts
    ok += 1
    pos2 = ROW.index('aria-controls="p2"')
    assert A.row_head_term(ROW, pos2, 'Beta') is None                # a masked term is refused
    ok += 1
    assert A.row_head_term(ROW, pos2, 'disease') is not None
    ok += 1
    assert A.row_head_term('<p>' + ROW[ROW.index('<button'):ROW.index('</button>') + 9] + '</p>', 10, 'x') is None
    ok += 1
    print('test_anchors: %d passed, 0 failed' % ok)


if __name__ == '__main__':
    main()
