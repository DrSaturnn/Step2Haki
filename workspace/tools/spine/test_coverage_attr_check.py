#!/usr/bin/env python3
"""Offline tests for coverage_attr_check: attribute-only differences pass; any other difference fails."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import coverage_attr_check as c  # noqa: E402

REF = ('<div class="brief" id="a" data-bp="cv"><h4>A</h4><p>one</p></div>'
       '<div class="brief" id="b" data-bp="gi"><h4>B</h4><p>two</p></div>')


def run(page):
    same, attr_only, other = c.compare(page, REF)
    return same, len(attr_only), [x[0] for x in other]


def test_identical():
    assert run(REF) == (2, 0, [])


def test_tag_added():
    assert run(REF.replace('id="a" data-bp="cv"', 'id="a" data-bp="cv" data-bps="hf"')) == (1, 1, [])


def test_bp_changed():
    assert run(REF.replace('data-bp="gi"', 'data-bp="gi multi"')) == (1, 1, [])


def test_other_attribute_fails():
    assert run(REF.replace('id="a" data-bp="cv"', 'id="a" data-bp="cv" data-x="1"'))[2] == ['a']


def test_body_change_fails():
    assert run(REF.replace('<p>two</p>', '<p>three</p>'))[2] == ['b']


def test_new_and_missing_fail():
    assert sorted(run(REF.replace('id="b"', 'id="c"'))[2]) == ['b', 'c']


if __name__ == '__main__':
    n = 0
    for k, f in sorted(globals().items()):
        if k.startswith('test_'):
            f(); n += 1
    print('test_coverage_attr_check: %d passed' % n)
