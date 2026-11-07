"""style_card.py: the writing card from repair/efficiency/TEXTBOOK_STYLE.md (between <!-- card:start --> and
<!-- card:end -->), the one copy that tools/spine/build_lanes.py puts at the top of every builder's INSTRUCTIONS.md and
tools/spine/review_packet.py at the top of every reviewer's RULES.md (D-20261106-11).

  python3 tools/spine/style_card.py      print the card
"""
import os
import sys

WS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STYLE = os.path.join(WS, 'repair', 'efficiency', 'TEXTBOOK_STYLE.md')


def card():
    t = open(STYLE, encoding='utf-8').read()
    a, b = t.find('<!-- card:start -->'), t.find('<!-- card:end -->')
    if a < 0 or b < a:
        raise ValueError('TEXTBOOK_STYLE.md has no card markers')
    return t[a + len('<!-- card:start -->'):b].strip() + '\n'


if __name__ == '__main__':
    sys.stdout.write(card())
