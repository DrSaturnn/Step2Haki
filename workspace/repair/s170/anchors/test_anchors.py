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


def span_tests():
    line = ('<div class="brief"><p><b><button type="button" class="sp-pop sp-a" aria-controls="q1">Alpha</button></b> beta, '
            'gamma <span class="sp-pop-b" id="q1" hidden>Body alpha beta.</span> delta <span class="mask">eps</span></p></div>')
    out, why = A.span_move(line, 'q1', 'Alpha beta')
    assert not why and '<button type="button" class="sp-pop sp-a" aria-controls="q1"><b>Alpha</b> beta</button>' in out, (out, why)
    assert A.txt(out) == A.txt(line)
    out, why = A.span_move(line, 'q1', 'delta')
    assert not why and 'aria-controls="q1">delta</button>' in out and '<b>Alpha</b>' in out
    assert A.span_move(line, 'q1', 'Body alpha')[1]            # card text is never a target
    assert A.span_move(line, 'q1', 'delta eps')[1]             # a mask boundary is never crossed
    line2 = '<div><p>A <button type="button" class="sp-pop sp-a" aria-controls="q2">hot</button> <b>cat (old)</b> sat <span class="sp-pop-b" id="q2" hidden>x</span></p></div>'
    assert A.span_move(line2, 'q2', 'hot cat')[1]              # cutting through a tag is refused
    out, why = A.span_move(line2, 'q2', 'hot cat (old)')
    assert not why and '>hot <b>cat (old)</b></button>' in out
    print('test_anchors span: 6 passed, 0 failed')


if __name__ == '__main__':
    span_tests()
