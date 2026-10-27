"""offline tests for shingle_check.drop_descriptions (s154g)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shingle_check as S

SHORT = 'bilateral nystagmus when the physician moves a strip of paper with vertical stripes'
LONG = ' '.join(['word%d' % i for i in range(30)])


def test_short_description_dropped():
    h = '<td>FND <span class="nbd-w" data-nbme-src="psych-cms-a92643">%s</span></td>' % SHORT
    assert 'nystagmus' not in S.drop_descriptions(h)


def test_button_and_hover_line_dropped():
    h = ('<button type="button" class="sp-pop nbd" data-nbme-src="x">%s</button>'
         '<span class="nbd-h" data-nbme-src="x"><b>Label:</b> %s</span>' % (SHORT, SHORT))
    out = S.drop_descriptions(h)
    assert 'nystagmus' not in out and out.count('\u2016') == 2


def test_long_description_kept():
    h = '<span class="nbd-h" data-nbme-src="x">%s</span>' % LONG
    assert S.drop_descriptions(h) == h


def test_plain_text_kept():
    h = '<td>%s</td>' % SHORT
    assert S.drop_descriptions(h) == h


def test_nested_span_kept():
    h = '<span class="nbd-w" data-nbme-src="x"><span class="nbd-k">k</span> %s</span>' % SHORT
    assert 'nystagmus' in S.drop_descriptions(h)
