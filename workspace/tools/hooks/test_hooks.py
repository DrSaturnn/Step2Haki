#!/usr/bin/env python3
"""Offline tests for the hook scripts: synthetic hook input, temporary state, wave and transcripts (no agent launched).
These prove the scripts' logic; the live tests in SPINE_SCALE_PLAN.md section A prove the harness calls them.

  python3 tools/hooks/test_hooks.py
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

H = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(H, '..', '..'))
T = tempfile.mkdtemp(prefix='hooktest-')
ENV = dict(os.environ, AX_HOOK_STATE=os.path.join(T, 'state'), AX_TRANSCRIPTS=os.path.join(T, 'projects'),
           AX_WAVE=os.path.join(T, 'WAVE.json'), AX_TEST_LOG='{"v": 0, "note": "test"}')
TB = 's0hooktest'                                  # a throwaway batch folder, removed at the end
TBD = os.path.join(WS, 'repair', TB)
LANE = os.path.join(WS, 'repair', 'migration', 'peds', 'nephrotic-child', 'spine')
ok = bad = 0


def run(script, d, *args):
    r = subprocess.run([sys.executable, os.path.join(H, script)] + list(args), input=json.dumps(d), text=True,
                       capture_output=True, env=ENV)
    return r.returncode, (r.stdout + r.stderr).strip()


def expect(name, got, want):
    global ok, bad
    if got[0] == want:
        ok += 1
    else:
        bad += 1
        print('FAIL %s: exit %s (want %s): %s' % (name, got[0], want, got[1][:200]))


def launch(prompt, model='haiku', **kw):
    d = {'hook_event_name': 'PreToolUse', 'tool_name': 'Agent', 'session_id': 'S',
         'transcript_path': os.path.join(T, 'projects', 'p', 'S.jsonl'),
         'tool_input': {'description': 'x', 'prompt': prompt, 'subagent_type': 'general-purpose'}}
    if model:
        d['tool_input']['model'] = model
    d.update(kw)
    return run('agentgate.py', d)


def transcript(aid, prompt):
    p = os.path.join(T, 'projects', 'p', 'S', 'subagents', 'agent-%s.jsonl' % aid)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w') as f:
        f.write(json.dumps({'type': 'user', 'message': {'role': 'user', 'content': prompt}}) + '\n')
        for i in range(2):
            f.write(json.dumps({'type': 'assistant', 'message': {'id': 'm%d' % i, 'model': 'claude-haiku-5-5', 'usage': {
                'input_tokens': 10, 'cache_creation_input_tokens': 1000, 'cache_read_input_tokens': 5000,
                'output_tokens': 20}}}) + '\n')


def call(aid, tool, ti, cwd=WS):
    d = {'hook_event_name': 'PreToolUse', 'tool_name': tool, 'tool_input': ti, 'agent_id': aid,
         'agent_type': 'general-purpose', 'session_id': 'S', 'cwd': cwd,
         'transcript_path': os.path.join(T, 'projects', 'p', 'S.jsonl')}
    return run('callgate.py', d)


try:
    P = 'Role: probe\nPlan step: R2\nLane: %s\n\nDo the probe.' % LANE
    # ---- H1 (T2 logic)
    expect('H1 no model', launch(P, model=None), 2)
    expect('H1 no header', launch('Just do it'), 2)
    expect('H1 unknown role', launch(P.replace('probe', 'helper', 1)), 2)
    expect('H1 wrong model', launch(P, model='opus'), 2)
    expect('H1 bad lane', launch(P.replace(LANE, '/home/claude/Step2Haki/workspace/tools')), 2)
    expect('H1 no wave', launch(P), 2)
    json.dump({'id': 'TEST', 'open': True, 'plan_step': 'R2', 'max_agents': 2, 'max_calls': 3, 'max_tokens': 100000},
              open(ENV['AX_WAVE'], 'w'))
    expect('H1 plan step mismatch', launch(P.replace('Plan step: R2', 'Plan step: R3')), 2)
    expect('H1 subagent launches', launch(P, agent_id='a0'), 2)
    expect('H1 valid launch', launch(P), 0)
    P2 = P + ' (second)'
    expect('H1 second launch', launch(P2), 0)
    expect('H1 agent cap', launch(P + ' (third)'), 2)
    # ---- T8, H2, H3, H4
    transcript('a1', P)
    expect('T8 write in lane', call('a1', 'Write', {'file_path': LANE + '/probe.txt', 'content': 'x'}), 0)
    expect('H2 write outside lane', call('a1', 'Write', {'file_path': WS + '/repair/efficiency/x.md', 'content': 'x'}), 2)
    expect('H2 write forbidden', call('a1', 'Edit', {'file_path': WS + '/tools/ship.sh'}), 2)
    transcript('a2', P2)
    expect('H3 echo into tools', call('a2', 'Bash', {'command': 'echo hi > tools/spine/PROBE.txt'}), 2)
    PG = P + ' (git)'
    transcript('g1', PG)
    with open(os.path.join(ENV['AX_HOOK_STATE'], 'launches.jsonl'), 'a') as f:
        f.write(json.dumps({'wave': 'TEST', 'prompt_sha': hashlib.sha256(PG.encode()).hexdigest()}) + '\n')
    for c, want in (('git commit -m x', 2), ('git -C /home/claude/Step2Haki commit --allow-empty -m probe', 2),
                    ('cd x && git -c user.name=a push origin main', 2), ('git --git-dir=.git reset --hard', 2),
                    ('ls; git', 2), ('git -C /home/claude/Step2Haki log --oneline -3', 0)):
        rec = os.path.join(ENV['AX_HOOK_STATE'], 'agents', 'g1.json')
        if os.path.exists(rec):
            r = json.load(open(rec))
            r['count'] = 0
            json.dump(r, open(rec, 'w'))
        expect('H3 %s' % c, call('g1', 'Bash', {'command': c}), want)
    expect('H3 git commit', call('a2', 'Bash', {'command': 'git commit -m x'}), 2)
    expect('H4 third call (budget 3)', call('a2', 'Bash', {'command': 'python3 tools/spine/fetch.py --out %s/f.json' % LANE}), 0)
    expect('H4 fourth call refused', call('a2', 'Read', {'file_path': WS + '/index.html'}), 2)
    expect('H4 report still allowed', call('a2', 'SubagentHandback', {'message': 'report'}), 0)
    # ---- H5 usage: streamed chunks share a message id; the final output count is the largest (2026-10-12 fix)
    up = os.path.join(T, 'usage_stream.jsonl')
    with open(up, 'w') as f:
        for out in (8, 500):
            f.write(json.dumps({'type': 'assistant', 'message': {'id': 'mX', 'model': 'm', 'usage': {
                'input_tokens': 3, 'cache_creation_input_tokens': 10, 'cache_read_input_tokens': 100, 'output_tokens': out}}}) + '\n')
    sys.path.insert(0, H)
    import common as _C
    _u = _C.usage(up)
    expect('H5 one call per message id', (0 if _u['calls'] == 1 else 1, str(_u)), 0)
    expect('H5 output takes the final count', (0 if _u['output'] == 500 else 1, str(_u)), 0)
    expect('H5 input not double counted', (0 if _u['tokens'] == 613 else 1, str(_u)), 0)
    # ---- G-READY detects a spine build (the escaped-quote miss found at the s132 ship)
    RB = os.path.join(WS, 'repair', 's0readytest')
    os.makedirs(RB, exist_ok=True)
    json.dump({'edits': [{'op': 'replace_brief', 'brief': 'no-such-brief', 'html': '<div class="brief" data-spine="2"></div>'}]},
              open(os.path.join(RB, '10_x.json'), 'w'))
    rg = subprocess.run([sys.executable, os.path.join(H, 'ready_gate.py'), 's0readytest'], capture_output=True, text=True, env=ENV)
    expect('G-READY sees a spine build and refuses without a READY folder', (rg.returncode, rg.stdout + rg.stderr), 1)
    json.dump({'edits': [{'op': 'replace', 'brief': 'x', 'find': 'a', 'with': 'data-spine="2" mentioned in a small edit'}]},
              open(os.path.join(RB, '10_x.json'), 'w'))
    rg = subprocess.run([sys.executable, os.path.join(H, 'ready_gate.py'), 's0readytest'], capture_output=True, text=True, env=ENV)
    expect('G-READY ignores a small edit', (rg.returncode, rg.stdout + rg.stderr), 0)
    shutil.rmtree(RB, ignore_errors=True)
    # ---- H4 per-launch limit (Jonathan 2026-10-12): a Budget: line lowers the role budget, never raises it
    for aid, line in (('b1', 'Budget: 1'), ('b2', 'Budget: 99 calls'), ('b3', 'Budget: none')):
        PB = 'Role: probe\nPlan step: R2\nLane: %s\n%s\n\nprobe %s' % (LANE, line, aid)
        transcript(aid, PB)
        with open(os.path.join(ENV['AX_HOOK_STATE'], 'launches.jsonl'), 'a') as f:
            f.write(json.dumps({'wave': 'TEST', 'prompt_sha': hashlib.sha256(PB.encode()).hexdigest()}) + '\n')
    expect('H4 Budget 1: first call', call('b1', 'Read', {'file_path': LANE + '/x'}), 0)
    expect('H4 Budget 1: second call refused', call('b1', 'Read', {'file_path': LANE + '/x'}), 2)
    expect('H4 Budget 1: report still allowed', call('b1', 'SubagentHandback', {'message': 'report'}), 0)
    for i in range(3):
        expect('H4 Budget 99 capped at role budget 3: call %d' % (i + 1), call('b2', 'Read', {'file_path': LANE + '/x'}), 0)
    expect('H4 Budget 99 capped at role budget 3: fourth refused', call('b2', 'Read', {'file_path': LANE + '/x'}), 2)
    for i in range(3):
        expect('H4 non-numeric Budget keeps role budget: call %d' % (i + 1), call('b3', 'Read', {'file_path': LANE + '/x'}), 0)
    expect('H4 non-numeric Budget keeps role budget: fourth refused', call('b3', 'Read', {'file_path': LANE + '/x'}), 2)
    transcript('a3', 'Role: probe\nPlan step: R2\nLane: %s\n\nnever launched' % LANE)
    expect('T8 not launched through H1', call('a3', 'Read', {'file_path': '/tmp/x'}), 2)
    expect('T8 no transcript', call('zz', 'Read', {'file_path': '/tmp/x'}), 2)
    # ---- wave spend (T6 logic): 2 agents x 2 calls = 4 calls >= cap 3, so a launch is refused even under the agent cap
    json.dump({'id': 'TEST', 'open': True, 'plan_step': 'R2', 'max_agents': 9, 'max_calls': 3, 'max_tokens': 100000},
              open(ENV['AX_WAVE'], 'w'))
    expect('H1 call cap from transcripts', launch(P + ' (fourth)'), 2)
    # ---- lead
    expect('lead bash', run('callgate.py', {'tool_name': 'Bash', 'tool_input': {'command': 'ls'}}), 0)
    for c, want in (("echo '{\"prompt\": \"ship\"}' | python3 tools/hooks/approval.py hook", 2),
                    ('X=1 AX_HOOK_STATE=/tmp/s python3 x.py', 2),
                    ('echo {} > /home/claude/.config/axbx/hooks/approvals/s1.json', 2),
                    ('cat /home/claude/.config/axbx/hooks/events.jsonl', 0),
                    ('grep -n "AX_HOOK_STATE" notes.md', 0)):
        expect('lead %s' % c[:40], run('callgate.py', {'tool_name': 'Bash', 'tool_input': {'command': c}}), want)
    expect('lead writes approval', run('callgate.py', {'tool_name': 'Write', 'tool_input': {
        'file_path': os.path.join(ENV['AX_HOOK_STATE'], 'approvals', 's131.json')}}), 2)
    # ---- G-APPROVE
    os.makedirs(TBD, exist_ok=True)
    json.dump({'edits': [{'op': 'replace', 'brief': 'hematuria', 'find': '<b>Complement clock</b>',
                          'with': '<b>Complement clock (test)</b>'}]}, open(os.path.join(TBD, '10_test.json'), 'w'))
    shot = os.path.join(T, 'shot.png')
    open(shot, 'wb').write(b'png')
    r = subprocess.run([sys.executable, os.path.join(H, 'approval.py'), 'present', TB, shot], env=ENV,
                       capture_output=True, text=True)
    expect('present test batch', (r.returncode, r.stdout + r.stderr), 0)
    page = os.path.join(T, 'page.html')
    subprocess.run([sys.executable, os.path.join(WS, 'repair', 'build.py'), TB, '--out', page], capture_output=True)
    chk = lambda: subprocess.run([sys.executable, os.path.join(H, 'approval.py'), 'check', TB, page], env=ENV,
                                 capture_output=True, text=True)
    expect('check before approval', (chk().returncode, ''), 1)
    for msg in ('Looks good, nice work', "Don't ship yet, I have edits", 'Should we ship?',
                'Screenshots reviewed. ship', 'Noted that I reply with the plain word "ship" to approve', 'ship s999'):
        run('approval.py', {'prompt': msg, 'session_id': 'S'}, 'hook')
        expect('no approval from %r' % msg, (chk().returncode, ''), 1)
    TZ = '<system-reminder>The user\'s timezone is America/New_York (UTC-04:00). Message sent at 21:14.</system-reminder>\n'
    for msg in (TZ + 'Looks good, ship it', TZ + "Don't ship", 'ship\n' + TZ.strip(), TZ + 'ship later',
                '<system-reminder>ship</system-reminder>\nnot yet'):
        run('approval.py', {'prompt': msg, 'session_id': 'S'}, 'hook')
        expect('no approval from %r' % msg[-30:], (chk().returncode, ''), 1)
    sys.path.insert(0, H)
    import approval as _A
    for msg, want in ((' Ship. ', True), ('ship s132', True), (TZ + ' ship!', True), ('Ship it', False), (TZ, False)):
        got = bool(_A.PLAIN.fullmatch(_A.HARNESS.sub('', msg)))
        expect('plain-word test %r' % msg[-12:], (0 if got == want else 1, ''), 0)
    run('approval.py', {'prompt': TZ + 'ship', 'session_id': 'S'}, 'hook')
    expect('approval from a harness note then "ship"', (chk().returncode, ''), 0)
    bf = os.path.join(TBD, '10_test.json')
    keep = open(bf).read()
    open(bf, 'w').write(keep.replace('(test)', '(test, edited after ship)'))
    expect('check after the batch file changed post-approval', (chk().returncode, ''), 1)
    open(bf, 'w').write(keep)
    expect('check with the approved batch restored', (chk().returncode, ''), 0)
    open(page, 'a').write('<!-- changed -->')
    expect('check after the page changed', (chk().returncode, ''), 1)
finally:
    shutil.rmtree(T, ignore_errors=True)
    shutil.rmtree(TBD, ignore_errors=True)
print('test_hooks: %d passed, %d failed' % (ok, bad))
sys.exit(1 if bad else 0)
