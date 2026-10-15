"""s141 helper: exact-text patches on a brief's build.py or outline.json (the s140 conventions: arrows for high and
low measured values, bold cutoffs with condition hovers, underline-only hovers). Each old string must occur exactly
once; a miss or a repeat stops the run before anything is written."""
import sys


def apply(path, pairs, tag):
    s = open(path, encoding='utf-8').read()
    assert tag not in s, '%s already applied to %s' % (tag, path)
    for old, new in pairs:
        n = s.count(old)
        if n != 1:
            sys.exit('conv: %r occurs %d times in %s; nothing written' % (old[:80], n, path))
        s = s.replace(old, new)
    s = s.rstrip('\n') + '\n# %s: %d patches (repair/s141/conv.py)\n' % (tag, len(pairs))
    open(path, 'w', encoding='utf-8').write(s)
    print('%s: %d patches applied to %s' % (tag, len(pairs), path))
