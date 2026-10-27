#!/usr/bin/env python3
"""H6, context alarm (PostToolUse, every tool; Jonathan 2026-10-26 after s154f chat 3 ran to about 240k unnoticed;
rebased 2026-10-27, Jonathan: "yes lets make those changes", after the lead reported that a fresh chat already measured
129k before any batch work, so the fixed 200k/225k marks left about 70k of working room and would force a restart
in the middle of a review round).
Reads the lead's own transcript after each tool call and measures its current context (input + cache write + cache
read of the latest API call). Subagents are skipped. The first reading in a session is its base (the system prompt and
tools); the marks are relative to it:
  - below base + AX_CTX_WARN_ADD (default 150000): silent;
  - from there: one warning per session: finish the step in hand and keep State current;
  - from base + AX_CTX_END_ADD (default 200000): one finish notice: finish the step in hand (a review round counts as
    one step), write State and the batch file, commit and push, then restart; a reminder after each further
    AX_CTX_REMIND (default 50000). Never a notice on every call.
AX_CTX_WARN / AX_CTX_STOP, if set, are absolute marks that override the relative ones.
State: <hook state>/ctx_<session>.json (base, and the marks already shown).
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C  # noqa: E402

WARN_ADD = int(os.environ.get('AX_CTX_WARN_ADD', '150000'))
END_ADD = int(os.environ.get('AX_CTX_END_ADD', '200000'))
REMIND = int(os.environ.get('AX_CTX_REMIND', '50000'))
ABS_WARN = os.environ.get('AX_CTX_WARN')
ABS_STOP = os.environ.get('AX_CTX_STOP')


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
    if n is None:
        return 0
    sid = d.get('session_id') or os.path.basename(tp).split('.')[0]
    sp = C.state('ctx_%s.json' % sid)
    st = {}
    try:
        st = json.load(open(sp, encoding='utf-8'))
    except (OSError, ValueError):
        pass
    if 'base' not in st:
        st['base'] = n
    base = st['base']
    warn = int(ABS_WARN) if ABS_WARN else base + WARN_ADD
    end = int(ABS_STOP) if ABS_STOP else base + END_ADD
    msg = None
    if n >= end:
        step = (n - end) // REMIND          # 0 at the finish mark, then one more per REMIND tokens
        if st.get('ended', -1) < step:
            st['ended'] = step
            msg = ('CONTEXT %dk (started at %dk): past the %dk finish mark. Finish the step in hand (a review round is one '
                   'step), then rewrite the handoff State and the batch file (what is done, the exact next edit), commit and '
                   'push both repos, and send "Context full. Paste into a fresh chat:" with the restart line alone in a '
                   'code block. Start no new chunk.' % (n // 1000, base // 1000, end // 1000))
    elif n >= warn and not st.get('warned'):
        st['warned'] = n
        msg = ('CONTEXT %dk (started at %dk): %dk left before the %dk finish mark. Finish the step in hand and keep the '
               'batch file and State current; no new surveys or whole-file reads.' % (n // 1000, base // 1000, (end - n) // 1000, end // 1000))
    os.makedirs(os.path.dirname(sp), exist_ok=True)
    json.dump(st, open(sp, 'w', encoding='utf-8'))
    if msg:
        sys.stderr.write(msg + '\n')
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
