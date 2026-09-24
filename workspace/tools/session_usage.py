#!/usr/bin/env python3
"""session_usage.py: token usage per API call and in total from a Claude session transcript.

  python3 tools/session_usage.py <transcript.jsonl> [--since ISO] [--until ISO] [--summary] [--subagents]

Transcripts live in ~/.claude/projects/<cwd-slug>/<session>.jsonl (subagents under
<session>/subagents/*.jsonl). One API call is logged as several assistant records (one per
content block) sharing message.id; they are merged, keeping the largest usage numbers.
Columns: cached-read (cache_read_input_tokens), cache-write (cache_creation_input_tokens),
output, uncached input. --summary prints totals only. --subagents adds the session's
subagent transcripts as separate totals. Usage totals are a proxy, not billed cost.
"""
import glob
import json
import os
import sys

F = ('cache_read_input_tokens', 'cache_creation_input_tokens', 'output_tokens', 'input_tokens')


def calls(path, since=None, until=None):
    by = {}
    order = []
    with open(path, encoding='utf-8') as f:
        for line in f:
            try:
                d = json.loads(line)
            except ValueError:
                continue
            if d.get('type') != 'assistant':
                continue
            m = d.get('message') or {}
            u = m.get('usage')
            if not u:
                continue
            ts = d.get('timestamp', '')
            if since and ts < since:
                continue
            if until and ts > until:
                continue
            key = m.get('id') or d.get('requestId') or d.get('uuid')
            if key not in by:
                by[key] = {'ts': ts, 'model': m.get('model', '')}
                for k in F:
                    by[key][k] = 0
                order.append(key)
            for k in F:
                by[key][k] = max(by[key][k], int(u.get(k) or 0))
    return [by[k] for k in order]


def fmt(n):
    return '{:,}'.format(n)


def report(path, cs, summary, label):
    tot = {k: sum(c[k] for c in cs) for k in F}
    if not summary:
        print('%-4s %-24s %12s %12s %9s %7s' % ('#', 'timestamp', 'cached-read', 'cache-write', 'output', 'input'))
        for i, c in enumerate(cs, 1):
            print('%-4d %-24s %12s %12s %9s %7s' % (i, c['ts'][:23], fmt(c['cache_read_input_tokens']),
                  fmt(c['cache_creation_input_tokens']), fmt(c['output_tokens']), fmt(c['input_tokens'])))
    span = (cs[0]['ts'][:19] + ' to ' + cs[-1]['ts'][:19]) if cs else 'no calls'
    print('%s: %d calls | cached-read %s | cache-write %s | output %s | input %s | %s | %s'
          % (label, len(cs), fmt(tot['cache_read_input_tokens']), fmt(tot['cache_creation_input_tokens']),
             fmt(tot['output_tokens']), fmt(tot['input_tokens']), span, path))
    return tot


def main(argv):
    if not argv or argv[0].startswith('-'):
        print(__doc__)
        return 2
    path = argv[0]
    opt = lambda k: argv[argv.index(k) + 1] if k in argv else None  # noqa: E731
    since, until = opt('--since'), opt('--until')
    summary = '--summary' in argv
    report(path, calls(path, since, until), summary, 'total')
    if '--subagents' in argv:
        sub = os.path.join(os.path.splitext(path)[0], 'subagents')
        for p in sorted(glob.glob(os.path.join(sub, '*.jsonl'))):
            report(p, calls(p, since, until), True, 'subagent ' + os.path.basename(p)[:-6])
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
