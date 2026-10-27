#!/usr/bin/env python3
"""What a continuation chat reads, and nothing more (Jonathan 2026-10-26, after s154f chat 3 ran past the restart point
reading whole docs). Run once after the clone, before anything else:

  python3 /home/claude/Step2Haki/workspace/tools/spine/resume.py [batch]

Prints: the handoff State; the open batch's file as an outline (headings with line ranges) plus its chunk table; the
DIGEST lines that name the batch; and the reading rules. Then read only the batch-file section the State names as next,
by line range (sed -n A,Bp). The batch defaults to the first "**sNNN OPEN**" in the State.
"""
import os
import re
import sys

WS = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
EFF = os.path.join(WS, 'repair', 'efficiency')

RULES = '''Reading rules (runbook "Continuation chats"; the context hook H6 warns at 200k and stops at 225k):
- Do not read the runbook, the handoff, STANDING_DIRECTIONS or DECISIONS_DIGEST whole, in the repo or the project.
  Grep them for the topic of the edit in hand (a display or content rule may live in STANDING or an older DIGEST line).
- Read the batch file by the line ranges above; read briefs only through scripts (pagelib, review_packet, w5 helpers,
  lint, mentions), never as raw HTML in the chat.
- A survey (several briefs, or output over about 3k tokens) writes to local/<batch>/survey_<topic>.md and prints counts;
  read that file by section.
- End every chunk by writing the next chunk's exact edits into the batch file, so the next chat starts at the edits.'''


def section(text, head):
    m = re.search(r'^## %s\b.*?(?=^## |\Z)' % re.escape(head), text, re.S | re.M)
    return m.group(0).rstrip() if m else ''


def main(argv):
    hand = open(os.path.join(EFF, 'STEP2HAKI_HANDOFF.md'), encoding='utf-8').read()
    st = section(hand, 'State')
    st = st.split('\n- **s', 1)[0] + ''.join('\n- **s' + p for p in st.split('\n- **s')[1:2])  # the open batch and the next item
    print(st, '\n')
    m = re.search(r'\*\*(s\d+[a-z]?) OPEN\*\*', st)
    batch = argv[0] if argv else (m.group(1) if m else None)
    if not batch:
        print('No open batch in the State: a launch reads the full runbook read order.')
        print(RULES)
        return 0
    bf = os.path.join(WS, 'repair', batch, batch.upper() + '.md')
    if os.path.exists(bf):
        lines = open(bf, encoding='utf-8').read().split('\n')
        heads = [(i + 1, l) for i, l in enumerate(lines) if l.startswith('## ')]
        print('Batch file %s (%d lines), sections:' % (os.path.relpath(bf, WS), len(lines)))
        for k, (n, l) in enumerate(heads):
            end = heads[k + 1][0] - 1 if k + 1 < len(heads) else len(lines)
            print('  %4d-%-4d %s' % (n, end, l[3:][:110]))
        tab = [l for l in lines if l.startswith('| C') or l.startswith('| Chunk')]
        if tab:
            print('\n' + '\n'.join(tab))
    else:
        print('No batch file at %s: the State is the batch record.' % os.path.relpath(bf, WS))
    dg = [l for l in open(os.path.join(EFF, 'DECISIONS_DIGEST.md'), encoding='utf-8').read().split('\n')
          if re.search(r'\b%s\b' % re.escape(batch), l)]
    print('\nDIGEST lines naming %s (%d):' % (batch, len(dg)))
    for l in dg:
        print('  ' + (l if len(l) <= 600 else l[:600] + ' ...'))
    print('\n' + RULES)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
