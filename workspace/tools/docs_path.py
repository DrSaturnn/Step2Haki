"""docs_path.py: where the internal documents live (the private repo DrSaturnn/Step2Haki-private, folder docs/).

DECISIONS_DIGEST, STANDING_DIRECTIONS, BATCH_RUNBOOK, STEP2HAKI_HANDOFF, RESUME, OPEN_WORK and ui/ (the UI refactor
plan, architecture and fit-to-screen notes) are kept out of the public repo. The private clone sits beside the public
clone (cloud: /home/claude/step2haki-private; Mac: ~/step2haki-private); S2H_PRIVATE overrides.

  from docs_path import doc        doc('DECISIONS_DIGEST.md') -> absolute path
"""
import os

WS = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
CANDIDATES = [os.environ.get('S2H_PRIVATE', ''),
              os.path.join(WS, '..', '..', 'step2haki-private'),
              '/home/claude/step2haki-private',
              os.path.expanduser('~/step2haki-private'),
              os.path.expanduser('~/step2haki-private-push')]


def private_root():
    for c in CANDIDATES:
        if c and os.path.isdir(os.path.join(c, 'docs')):
            return os.path.abspath(c)
    raise FileNotFoundError('docs_path: no private clone with docs/ found (set S2H_PRIVATE); tried ' +
                            ', '.join(c for c in CANDIDATES if c))


def docs_dir():
    return os.path.join(private_root(), 'docs')


def doc(name):
    return os.path.join(docs_dir(), name)


if __name__ == '__main__':
    print(docs_dir())
