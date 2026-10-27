#!/usr/bin/env python3
"""H6, context alarm (PostToolUse, every tool; Jonathan 2026-10-26 after s154f chat 3 ran to about 240k unnoticed).
Reads the lead's own transcript after each tool call and measures its current context (input + cache write + cache
read of the latest API call). Subagents are skipped.
  - below AX_CTX_WARN (default 200000): silent;
  - from AX_CTX_WARN: one warning per session (exit 2, so the lead sees it): finish the step in hand and write State;
  - from AX_CTX_STOP (default 225000, the runbook restart point): a stop notice after every call until the chat ends:
    rewrite the handoff State, commit and push both repos, send only the restart message.
State: <hook state>/ctx_<session>.json (whether the warning was shown).
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C  # noqa: E402

WARN = int(os.environ.get('AX_CTX_WARN', '200000'))
STOP = int(os.environ.get('AX_CTX_STOP', '225000'))


def current(path):
    """input + cache write + cache read of the transcript's latest assistant message with usage"""
    last = None
    try:
        for line in open(path, encoding='utf-8'):
            if '"usage"' not in line:
                continue
            d = json.loads(line)
            u = (d.get('message') or {}).get('usage') if d.get('type') == 'assistant' else None
            if u:
                last = u
    except (OSError, ValueError):
        return None
    if not last:
        return None
    return sum(int(last.get(k) or 0) for k in ('input_tokens', 'cache_creation_input_tokens', 'cache_read_input_tokens'))


def main():
    try:
        d = json.load(sys.stdin)
    except ValueError:
        return 0
    tp = d.get('transcript_path') or ''
    if d.get('agent_id') or '/subagents/' in tp or not tp:
        return 0
    n = current(tp)
    if n is None or n < WARN:
        return 0
    sid = d.get('session_id') or os.path.basename(tp).split('.')[0]
    sp = C.state('ctx_%s.json' % sid)
    seen = {}
    try:
        seen = json.load(open(sp, encoding='utf-8'))
    except (OSError, ValueError):
        pass
    if n >= STOP:
        sys.stderr.write('CONTEXT %dk: past the %dk restart point (runbook section 6). Start no new work: rewrite the handoff '
                         'State and the batch file (what is done, the exact next edit), commit and push both repos, then send '
                         'only "Context full. Paste into a fresh chat:" with the restart line alone in a code block.\n'
                         % (n // 1000, STOP // 1000))
        return 2
    if not seen.get('warned'):
        os.makedirs(os.path.dirname(sp), exist_ok=True)
        json.dump({'warned': n}, open(sp, 'w', encoding='utf-8'))
        sys.stderr.write('CONTEXT %dk: %dk left before the %dk restart point. Finish the step in hand, write its record to the '
                         'batch file and State, and plan to restart; no new surveys or whole-file reads.\n'
                         % (n // 1000, (STOP - n) // 1000, STOP // 1000))
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
