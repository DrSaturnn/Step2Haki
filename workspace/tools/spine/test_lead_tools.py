#!/usr/bin/env python3
"""Offline tests for the lead tools moved into the repo (s148 efficiency fix 5): lanes.py, reps.py, review_packet.py
--since (changed_steps), sheets.py --steps and verify_all.py's verdict reading.

  python3 tools/spine/test_lead_tools.py
"""
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'hooks'))
import common as HC  # noqa: E402
import lanes as LN  # noqa: E402
import reps as RP  # noqa: E402

ok = bad = 0


def expect(name, cond):
    global ok, bad
    if cond:
        ok += 1
    else:
        bad += 1
        print('FAIL', name)


T = tempfile.mkdtemp(prefix='leadtools-')
try:
    # ---- lanes: budgets from the runbook call plan, the cap, the header the launch gate reads, follow-up context
    expect('round 1 acc: 7 per brief plus 4', LN.budget('acc', 1, 3) == 25)
    expect('round 1 read: 5 per brief plus 4', LN.budget('read', 1, 3) == 19)
    expect('follow-up acc: 5 per brief plus 4', LN.budget('acc', 2, 2) == 14)
    expect('follow-up display: 7 per brief plus 4', LN.budget('display', 3, 2) == 18)
    pk = os.path.join(T, 'pk')
    for b in ('x', 'y'):
        for part in ('acc', 'read', 'display', 'flags'):
            d = os.path.join(pk, b, part)
            os.makedirs(d)
            open(os.path.join(d, 'deps.txt'), 'w').write('deps: brief=%s1 live=%s2\nbrief-sha: %s3\n' % (b, b, b))
            open(os.path.join(d, 'brief_text.txt'), 'w').write('text of %s' % b)
            open(os.path.join(d, 'changes.md'), 'w').write('# Changes since your last review\n+ new line of %s\n' % b)
    os.makedirs(os.path.join(T, 'r1'))
    for b in ('x', 'y'):
        open(os.path.join(T, 'r1', 'acc_%s.md' % b), 'w').write('part: acc\nVerdict: FAIL\n1. MED %s\n' % b)
        open(os.path.join(T, 'r1', 'adj_%s.md' % b), 'w').write('## Lead adjudication %s\n- MED 1 ACCEPT\n' % b)
    spec = {'batch': 'sT', 'plan_step': 'sT', 'round': 2, 'context': 'batch sT converts test briefs',
            'out': os.path.join(T, 'lanes'), 'packets': pk,
            'lanes': [{'part': 'acc', 'group': 'A', 'briefs': ['x', 'y']}],
            'types': {'x': 'presentation hub'},
            'prior': {'acc': {b: os.path.join(T, 'r1', 'acc_%s.md' % b) for b in ('x', 'y')}},
            'adjudication': {b: os.path.join(T, 'r1', 'adj_%s.md' % b) for b in ('x', 'y')},
            'notes': {'acc': ['the treatment ladders inside the hubs stay (Jonathan)']},
            'extra_judge': {'acc': ['Timelines: each Decides-it cell leads with its timeline.']}}
    rows = LN.build(spec)
    lane = rows[0][0]
    ins = open(os.path.join(lane, 'INSTRUCTIONS.md')).read()
    h = HC.header(ins)
    expect('INSTRUCTIONS header parses for the launch gate',
           h.get('role') == 'acc-review' and h.get('plan_step') == 'sT' and h.get('lane') == lane and h.get('budget') == '14')
    expect('call plan names 2 spare calls', '9 of your 14, 5 spare' in ins)
    expect('follow-up text and earlier findings', 'follow-up round 2' in ins and '`Earlier findings`' in ins)
    expect('deps lines per brief', 'line 2: deps: brief=x1 live=x2; line 3: brief-sha: x3' in ins)
    expect('notes and extra judge lines', 'Not a finding (decided): the treatment ladders' in ins and '- Timelines:' in ins)
    rv = open(os.path.join(lane, 'y', 'review.md')).read()
    expect('review.md = last receipt, adjudication, changes',
           rv.index('1. MED y') < rv.index('Lead adjudication y') < rv.index('new line of y'))
    expect('packet files copied', os.path.exists(os.path.join(lane, 'x', 'brief_text.txt')))
    spec1 = dict(spec, round=1, lanes=[{'part': 'acc', 'group': 'B', 'briefs': ['x', 'y', 'x', 'y']}])
    try:
        LN.build(spec1, dry=True)
        expect('a lane over 25 calls is refused', False)
    except SystemExit as ex:
        expect('a lane over 25 calls is refused', 'split the lane' in str(ex))
    spec1 = dict(spec, round=1, lanes=[{'part': 'read', 'group': 'B', 'briefs': ['x']}])
    ins1 = LN.lane_text(spec1, spec1['lanes'][0], 9)[1]
    expect('round 1 text has no follow-up block', 'follow-up' not in ins1 and 'Earlier findings' not in ins1)

    # ---- reps: exactly once across build.py, tail_fix.json, head_fix.json
    d = os.path.join(T, 'brief')
    os.makedirs(d)
    open(os.path.join(d, 'build.py'), 'w').write("A = T('the lateral hip is tender', 'b01')\nB = T('it\\'s weak', 'b02')\n"
                                                 "C = T('twice here', 'x')\nD = T('twice here', 'y')\n")
    json.dump({'fixes': [['old', 'Image first, <b>drain</b> the bladder']]}, open(os.path.join(d, 'tail_fix.json'), 'w'))
    res, all_ok = RP.apply(d, [('1', 'the lateral hip is tender', 'the lateral hip is tender to touch'),
                               ('2', "it's weak", "it's weak on abduction"),
                               ('3', 'twice here', 'once here'),
                               ('4', 'Image first, drain the bladder', 'Image and drain'),
                               ('5', 'nowhere at all', 'x')])
    st = {r[0]: r[1] for r in res}
    expect('reps: plain text applied', st['1'] == 'ok')
    expect('reps: python-escaped form applied', st['2'] == 'ok')
    expect('reps: two hits is ambiguous, not applied', st['3'] == 'ambiguous')
    expect('reps: tail text across markup is reported, not forced', st['4'] == 'crosses markup')
    expect('reps: absent text is not found', st['5'] == 'not found' and not all_ok)
    src = open(os.path.join(d, 'build.py')).read()
    expect('reps: the file holds the applied edits only',
           'tender to touch' in src and "weak on abduction" in src and src.count('twice here') == 2)
    rc = os.path.join(T, 'receipt.md')
    open(rc, 'w').write('Verdict: PASS-IF\nReplacements:\n1. old: {{a}}\n   new: {{b}}\n2. old: {{c}}\n   new: {{d}}\n')
    expect('reps: --only picks receipt replacements', [p[0] for p in RP.load(rc, {2})] == ['2'])

    # ---- review_packet --since: changed step numbers
    import review_packet as RV
    old = ['Title', '1Presentation', 'a', '2Urgent risks', 'b', '4Workup', 'c', 'Practice', 'q']
    new = ['Title!', '1Presentation', 'a', '2Urgent risks', 'b', '4Workup', 'c2', 'Practice', 'q', 'q2']
    expect('changed steps: header, 4, practice', RV.changed_steps(old, new) == ['header', '4', 'practice'])
    expect('changed steps: none', RV.changed_steps(old, old) == [])
    expect('since diff counts lines', '2 changed line(s)' in RV.since_diff(['a'], ['b']))

    # ---- sheets --steps
    import sheets as SH
    fs = ['b_phone_step%d%s.png' % (k, s) for k, s in ((0, ''), (1, ''), (3, 'a'), (3, 'b'), (4, ''), (9, ''))]
    expect('sheets: --steps 3,practice', SH.pick(fs, ['3', 'practice']) == ['b_phone_step3a.png', 'b_phone_step3b.png', 'b_phone_step9.png'])
    expect('sheets: header is step 0', SH.pick(fs, ['header']) == ['b_phone_step0.png'])
    expect('sheets: no --steps keeps all', SH.pick(fs, None) == fs)

    # ---- verify_all verdicts (verify exits 1 FAIL, 2 not READY, 0 READY or mechanical pass)
    import verify_all as VA
    expect('verify_all: READY', VA.state(0, 'verify pmr: READY (mechanical checks pass ...)', False) == 'READY')
    expect('verify_all: MECH', VA.state(2, 'verify pmr: MECHANICAL PASS, NOT READY: stale', False) == 'MECH')
    expect('verify_all: FAIL', VA.state(1, 'verify pmr: FAIL (2 fix(es))', False) == 'FAIL')
    expect('verify_all: --mech pass', VA.state(0, 'verify pmr: MECHANICAL PASS (G-MECH)', True) == 'PASS')
finally:
    shutil.rmtree(T, ignore_errors=True)

print('test_lead_tools: %d passed, %d failed' % (ok, bad))
sys.exit(1 if bad else 0)
