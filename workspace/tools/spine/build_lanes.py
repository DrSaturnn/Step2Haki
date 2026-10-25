#!/usr/bin/env python3
"""build_lanes: prepare one builder lane per brief for S1 to S3 by builder agents (s152 close, 2026-10-25; BATCH_RUNBOOK
section 2). The deterministic S1 prep the lead used to do by hand, then the lane's INSTRUCTIONS.md and launch prompt.

  python3 tools/spine/build_lanes.py <spec.json> [--only id,id]

spec.json:
  {"batch": "s153", "plan_step": "s153", "budget": 90,
   "briefs": [{"id": "masld", "folder": "repair/migration/gi/masld/spine", "entry": "disease",
               "golden": "repair/migration/<...>/copd/spine", "model": "repair/migration/peds/kawasaki/spine"}]}

Per brief: makes the folder; dumps the live brief to local/<batch>/live/<id>.json and .txt (dump_lines.py); writes
board_index.txt (board_index.py show <id> --all), cards.md (card_dispositions.py make), amend_rows.md (the brief's rows
in BRIEF_AMEND_LIST.md from the private clone); fills tools/spine/BUILD_CONTRACT.md into <folder>/INSTRUCTIONS.md; and
writes the launch prompt to local/<batch>/build_prompts/<id>.txt. Prints one line per brief. Existing files the builder
wrote (author.py, BUILD_NOTES.md, boards.md) are never touched, so a relaunch keeps its work.
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, '..', '..'))
PRIV = os.environ.get('AX_PRIVATE', '/home/claude/step2haki-private')
AMEND = os.path.join(PRIV, 'claude', 'pending', 'BRIEF_AMEND_LIST.md')
SPINE_SPEC = os.path.join(PRIV, 'claude', 'SPINE_SPEC.md')


def sh(cmd, out=None):
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=WS)
    if out:
        open(out, 'w', encoding='utf-8').write(r.stdout)
    return r


def title_of(bid):
    sys.path.insert(0, os.path.join(WS, 'tools'))
    import pagelib as P
    pg = P.read_page(os.path.join(WS, 'index.html'))
    b = P.brief_by_id(pg, bid)
    if not b:
        return None
    m = re.search(r'<h4[^>]*>(.*?)</h4>', pg[b.start:b.end], re.S)
    return re.sub(r'<[^>]+>', '', m.group(1)).strip() if m else bid


def amend_rows(bid):
    if not os.path.exists(AMEND):
        return '(BRIEF_AMEND_LIST.md not found at %s)\n' % AMEND
    keep = [l for l in open(AMEND, encoding='utf-8') if re.search(r'(?<![\w-])%s(?![\w-])' % re.escape(bid), l)]
    return ''.join(keep) or '(no rows name %s)\n' % bid


def prompt(spec, b, folder):
    return ('Role: brief-build\nPlan step: %s\nLane: %s\nBudget: %d\n\nRead INSTRUCTIONS.md in your lane first.\n'
            % (spec['plan_step'], folder, spec.get('budget', 90)))


def lane(spec, b):
    batch, bid = spec['batch'], b['id']
    folder = os.path.join(WS, b['folder'])
    os.makedirs(folder, exist_ok=True)
    title = title_of(bid)
    if title is None:
        return '%s: not on the page (a new brief needs its own prep)' % bid
    live_dir = os.path.join(WS, 'local', batch, 'live')
    os.makedirs(live_dir, exist_ok=True)
    live = os.path.join(live_dir, bid + '.json')
    r = sh([sys.executable, os.path.join(HERE, 'dump_lines.py'), bid, live], out=live[:-5] + '.txt')
    if r.returncode:
        return '%s: dump_lines FAIL %s' % (bid, r.stderr.strip()[-200:])
    sh([sys.executable, os.path.join(HERE, 'board_index.py'), 'show', bid, '--all'],
       out=os.path.join(folder, 'board_index.txt'))
    r = sh([sys.executable, os.path.join(HERE, 'card_dispositions.py'), 'make', bid, folder])
    cards = (r.stdout.strip().splitlines() or ['?'])[-1]
    open(os.path.join(folder, 'amend_rows.md'), 'w', encoding='utf-8').write(amend_rows(bid))
    fill = {'batch': batch, 'bid': bid, 'title': title, 'entry': b.get('entry', 'disease'), 'folder': folder,
            'budget': spec.get('budget', 90), 'live': live, 'live_txt': live[:-5] + '.txt',
            'model': os.path.join(WS, b['model']), 'golden': os.path.join(WS, b['golden']), 'spine_spec': SPINE_SPEC}
    t = open(os.path.join(HERE, 'BUILD_CONTRACT.md'), encoding='utf-8').read()
    for k, v in fill.items():
        t = t.replace('{%s}' % k, str(v))
    left = sorted(set(re.findall(r'\{([a-z_]+)\}', t)))
    if left:
        return '%s: contract placeholders unfilled: %s' % (bid, ', '.join(left))
    open(os.path.join(folder, 'INSTRUCTIONS.md'), 'w', encoding='utf-8').write(t)
    pdir = os.path.join(WS, 'local', batch, 'build_prompts')
    os.makedirs(pdir, exist_ok=True)
    open(os.path.join(pdir, bid + '.txt'), 'w', encoding='utf-8').write(prompt(spec, b, folder))
    missing = [p for p in (fill['model'], fill['golden']) if not os.path.isdir(p)]
    return '%s: lane ready (%s; cards: %s)%s' % (bid, os.path.relpath(folder, WS), cards,
                                                 '; MISSING %s' % ', '.join(missing) if missing else '')


def main(argv):
    if not argv:
        sys.exit(__doc__.strip().splitlines()[3].strip())
    spec = json.load(open(argv[0], encoding='utf-8'))
    only = set(argv[argv.index('--only') + 1].split(',')) if '--only' in argv else None
    for b in spec['briefs']:
        if only and b['id'] not in only:
            continue
        print(lane(spec, b))
    print('prompts: local/%s/build_prompts/<id>.txt (launch each as agent type lean-builder, model opus)' % spec['batch'])
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
