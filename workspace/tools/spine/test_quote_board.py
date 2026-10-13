#!/usr/bin/env python3
"""s135: quote_check accepts brackets only in a kind "board" quote from the local AnKing text (the cloze answer is
bracketed in the card itself); any other bracketed quote still fails. Offline."""
import json, os, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, '..', '..'))
CARDS = 'repair/sources/anki/anki_cards.txt'
Q = 'First-line pharmacologic treatment of Tourette syndrome is [VMAT-2 inhibitors]'


def run(facts):
    with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as t:
        json.dump({'facts': facts}, t)
    r = subprocess.run([sys.executable, os.path.join(HERE, 'quote_check.py'), t.name], cwd=WS, capture_output=True, text=True)
    os.unlink(t.name)
    return r.returncode, r.stdout + r.stderr


def main():
    if not os.path.exists(os.path.join(WS, CARDS)):
        print('test_quote_board: SKIP (local AnKing text not restored)')
        return 0
    fails = 0
    rc, out = run([{'id': 'b1', 'local': CARDS, 'kind': 'board', 'quote': Q}])
    fails += rc != 0
    print('board cloze quote accepted:', rc == 0)
    rc, out = run([{'id': 'b2', 'local': CARDS, 'kind': 'fact', 'quote': Q}])
    fails += 'editorial brackets' not in out and 'AnKing card cited' not in out
    print('non-board bracketed quote refused:', 'editorial brackets' in out or 'AnKing card cited' in out)
    rc, out = run([{'id': 'b3', 'local': CARDS, 'kind': 'board', 'quote': 'First-line pharmacologic treatment of Tourette syndrome is [an alpha-2 agonist]'}])
    fails += rc == 0
    print('board quote with words not in the card refused:', rc != 0)
    print('test_quote_board: %d failed' % fails)
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
