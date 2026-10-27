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
           AX_WAVE=os.path.join(T, 'WAVE.json'), AX_LEDGER=os.path.join(T, 'ledger.csv'),
           AX_LEDGER_LEAD=os.path.join(T, 'ledger_lead.csv'), AX_TEST_LOG='{"v": 0, "note": "test"}')
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


# H6 contextgate (2026-10-26; rebased 2026-10-27): marks relative to the session's first reading
def _ctx(n, sid, sub=False):
    d = os.path.join(T, 'ctxt', 'subagents' if sub else 'lead')
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, '%s.jsonl' % sid)
    with open(p, 'w') as f:
        f.write(json.dumps({'type': 'assistant', 'message': {'id': 'm1', 'usage': {'input_tokens': 5, 'cache_creation_input_tokens': 1000, 'cache_read_input_tokens': 9000}}}) + '\n')
        f.write(json.dumps({'type': 'assistant', 'message': {'id': 'm2', 'usage': {'input_tokens': 5, 'cache_creation_input_tokens': 1000, 'cache_read_input_tokens': n - 1005}}}) + '\n')
    return run('contextgate.py', {'session_id': sid, 'transcript_path': p, 'tool_name': 'Bash'})


# rebased 2026-10-27: the first reading is the base; warn at base + 150k, finish notice at base + 200k, then one
# reminder per further 50k, never a notice on every call
expect('context: first reading 130k sets the base, silent', _ctx(130000, 'c2'), 0)
expect('context 205k (base + 75k): silent', _ctx(205000, 'c2'), 0)
expect('context 285k (base + 155k): warns', _ctx(285000, 'c2'), 2)
expect('context 300k, already warned: silent', _ctx(300000, 'c2'), 0)
expect('context 332k (base + 202k): finish notice', _ctx(332000, 'c2'), 2)
expect('context 340k, notice shown: silent', _ctx(340000, 'c2'), 0)
expect('context 381k (finish + 51k): one reminder', _ctx(381000, 'c2'), 2)
expect('context 390k: silent', _ctx(390000, 'c2'), 0)
expect('context: a session starting at 150k is silent', _ctx(150000, 'c1'), 0)
expect('a subagent at 240k: silent', _ctx(240000, 'c3', sub=True), 0)
expect('no transcript: silent', run('contextgate.py', {'session_id': 'c4', 'tool_name': 'Bash'}), 0)


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
    # ---- s148 S7: parallel calls from one agent never race on its count file (one read it empty: hook error)
    PR = P + ' (race)'
    transcript('r1', PR)
    with open(os.path.join(ENV['AX_HOOK_STATE'], 'launches.jsonl'), 'a') as f:
        f.write(json.dumps({'wave': 'TEST', 'prompt_sha': hashlib.sha256(PR.encode()).hexdigest()}) + '\n')
    import concurrent.futures as _cf
    with _cf.ThreadPoolExecutor(12) as _ex:
        _res = list(_ex.map(lambda i: call('r1', 'Read', {'file_path': LANE + '/facts.json'}), range(12)))
    _rec = json.load(open(os.path.join(ENV['AX_HOOK_STATE'], 'agents', 'r1.json')))
    expect('race: no hook error in 12 parallel calls', (0 if not any('HOOK ERROR' in o for _, o in _res) else 1, ''), 0)
    expect('race: every call counted', (_rec['count'], ''), 12)
    expect('race: exactly the budget allowed', (sum(1 for c, _ in _res if c == 0), ''), 3)
    # ---- s148 fix 3: a wave's spend from an earlier container (committed ledger rows) still counts at the gate
    def ledger(rows):
        with open(ENV['AX_LEDGER'], 'w') as f:
            f.write('agent_id,wave,role,calls,tokens\n')
            for r in rows:
                f.write(','.join(str(x) for x in r) + '\n')
    PP = 'Role: probe\nPlan step: PAST\nLane: %s\n\nDo the probe.' % LANE
    json.dump({'id': 'PAST', 'open': True, 'plan_step': 'PAST', 'max_agents': 3, 'max_calls': 50, 'max_tokens': 10 ** 7},
              open(ENV['AX_WAVE'], 'w'))
    ledger([('old1', 'PAST', 'probe', 5, 1000), ('old2', 'PAST', 'probe', 5, 1000), ('old3', 'PAST', 'probe', 5, 1000)])
    expect('fix 3: past agents fill the agent cap', launch(PP + ' (p1)'), 2)
    ledger([('old1', 'PAST', 'probe', 30, 1000), ('old2', 'PAST', 'probe', 20, 1000)])
    expect('fix 3: past calls fill the call cap', launch(PP + ' (p2)'), 2)
    ledger([('old1', 'PAST', 'probe', 5, 6 * 10 ** 6), ('old2', 'PAST', 'probe', 5, 4 * 10 ** 6)])
    expect('fix 3: past tokens fill the token cap', launch(PP + ' (p3)'), 2)
    ledger([('a1', 'PAST', 'probe', 999, 10 ** 8), ('old9', 'OTHER', 'probe', 999, 10 ** 8),
            ('old1', 'PAST', 'probe', 5, 1000)])
    expect('fix 3: rows with a transcript here or of another wave are not counted', launch(PP + ' (p4)'), 0)
    os.remove(ENV['AX_LEDGER'])
    expect('fix 3: no ledger, no past spend', launch(PP + ' (p5)'), 0)
    # ---- s148 item 9: the plugin's guarded hook runner (tools/plugin/step2haki-tools/hooks/run.sh)
    RUN = os.path.join(WS, 'tools', 'plugin', 'step2haki-tools', 'hooks', 'run.sh')
    HM = os.path.join(T, 'home')
    os.makedirs(os.path.join(HM, '.claude'), exist_ok=True)

    def plug(script, d, dirs=H, settings=None):
        sp = os.path.join(HM, '.claude', 'settings.json')
        if settings is None:
            if os.path.exists(sp):
                os.remove(sp)
        else:
            open(sp, 'w').write(settings)
        r = subprocess.run(['sh', RUN, script], input=json.dumps(d), text=True, capture_output=True,
                           env=dict(ENV, HOME=HM, AX_HOOK_DIRS=dirs))
        return r.returncode, (r.stdout + r.stderr).strip()
    NOMODEL = {'hook_event_name': 'PreToolUse', 'tool_name': 'Agent', 'session_id': 'S',
               'tool_input': {'description': 'x', 'prompt': 'Role: probe\nPlan step: R2\nLane: %s\n' % LANE}}
    expect('item 9: plugin runs the gate, a launch with no model is refused (exit 2 passes through)', plug('agentgate.py', NOMODEL), 2)
    expect('item 9: plugin allows a non-Agent call through the launch gate', plug('agentgate.py', dict(NOMODEL, tool_name='Read')), 0)
    expect('item 9: no checkout here, the plugin does nothing', plug('agentgate.py', NOMODEL, dirs='/nonexistent/x'), 0)
    expect('item 9: the settings already run the gate, the plugin defers (no double count)',
           plug('agentgate.py', NOMODEL, settings='{"hooks": "python3 /x/tools/hooks/agentgate.py"}'), 0)
    expect('item 9: settings for another script do not make it defer',
           plug('agentgate.py', NOMODEL, settings='{"hooks": "python3 /x/tools/hooks/callgate.py"}'), 2)
    _hj = json.load(open(os.path.join(os.path.dirname(RUN), 'hooks.json')))['hooks']
    expect('item 9: hooks.json has the three hooks',
           (0 if [m['matcher'] for m in _hj['PreToolUse']] == ['Agent|Task', ''] and len(_hj['UserPromptSubmit']) == 1 else 1, ''), 0)
    # ---- s148 fix 7: the lead's row per session in ledger_lead.csv, updated in place on a re-record
    lp = os.path.join(T, 'projects', 'p', 'LEADSESS.jsonl')
    with open(lp, 'w') as f:
        for i, out in enumerate((100, 200)):
            f.write(json.dumps({'type': 'assistant', 'message': {'id': 'L%d' % i, 'model': 'm', 'usage': {
                'input_tokens': 5, 'cache_creation_input_tokens': 50, 'cache_read_input_tokens': 1000, 'output_tokens': out}}}) + '\n')
    json.dump({'id': 'LEADW', 'open': True, 'max_agents': 1, 'max_calls': 1, 'max_tokens': 10 ** 6, 'max_lead_tokens': 5000},
              open(ENV['AX_WAVE'], 'w'))
    for _ in range(2):
        rc_, out_ = run('usage_ledger.py', {}, '--lead', '--record', 'LEADW')
    import csv as _csv
    _rows = list(_csv.DictReader(open(ENV['AX_LEDGER_LEAD'])))
    expect('fix 7: one lead row per session, updated in place', (len(_rows), out_), 1)
    expect('fix 7: lead row tokens', (int(_rows[0]['tokens']) if _rows else -1, out_), 10 + 100 + 2000 + 300)
    expect('fix 7: batch total printed with the lead cap', (0 if 'lead cap 5000' in out_ and 'total' in out_ else 1, out_), 0)
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
    # ---- s135 efficiency item 1: review roles launch only as the lean agent type (file or plugin name)
    json.dump({'id': 'TEST2', 'open': True, 'plan_step': 'R2', 'max_agents': 9, 'max_calls': 99, 'max_tokens': 10 ** 9},
              open(ENV['AX_WAVE'], 'w'))
    RP = 'Role: read-review\nPlan step: R2\nLane: %s\n\nReview.' % LANE
    def rlaunch(kind, tag):
        d = {'hook_event_name': 'PreToolUse', 'tool_name': 'Agent', 'session_id': 'S',
             'tool_input': {'description': 'x', 'prompt': RP + tag, 'subagent_type': kind, 'model': 'sonnet'}}
        return run('agentgate.py', d)
    expect('H1 review role as general-purpose refused', rlaunch('general-purpose', ' 1'), 2)
    expect('H1 review role with no type refused', rlaunch('', ' 2'), 2)
    expect('H1 review role as a look-alike type refused', rlaunch('evil-lean-reviewer', ' 3'), 2)
    expect('H1 review role as lean-reviewer', rlaunch('lean-reviewer', ' 4'), 0)
    expect('H1 review role as the plugin lean-reviewer', rlaunch('step2haki-tools:lean-reviewer', ' 5'), 0)
    # ---- s152 close (2026-10-25): the brief-build role launches only as lean-builder on opus
    BP = 'Role: brief-build\nPlan step: R2\nLane: %s\n\nBuild.' % LANE
    def blaunch(kind, model, tag):
        d = {'hook_event_name': 'PreToolUse', 'tool_name': 'Agent', 'session_id': 'S',
             'tool_input': {'description': 'x', 'prompt': BP + tag, 'subagent_type': kind, 'model': model}}
        return run('agentgate.py', d)
    expect('H1 build role as general-purpose refused', blaunch('general-purpose', 'opus', ' 1'), 2)
    expect('H1 build role on sonnet refused', blaunch('lean-builder', 'sonnet', ' 2'), 2)
    expect('H1 build role as lean-builder on opus', blaunch('lean-builder', 'opus', ' 3'), 0)
    rj = json.load(open(os.path.join(H, 'roles.json')))['roles']
    nofile = [r for r, v in rj.items() if v.get('agent') and not os.path.exists(os.path.join(H, 'agents', v['agent'] + '.md'))]
    expect('roles: every agent type has its file in tools/hooks/agents', (1 if nofile else 0, str(nofile)), 0)
    # ---- s135 efficiency item 2: output estimated from what the agent wrote when the transcript keeps a stub count
    ep = os.path.join(T, 'usage_est.jsonl')
    with open(ep, 'w') as f:
        f.write(json.dumps({'type': 'assistant', 'message': {'id': 'mE', 'model': 'claude-sonnet-5-5', 'content': [
            {'type': 'text', 'text': 'x' * 380}], 'usage': {'input_tokens': 0, 'cache_creation_input_tokens': 0,
            'cache_read_input_tokens': 0, 'output_tokens': 1}}}) + '\n')
        f.write(json.dumps({'type': 'assistant', 'message': {'id': 'mE', 'model': 'claude-sonnet-5-5', 'content': [
            {'type': 'text', 'text': 'x' * 380}], 'usage': {'output_tokens': 1}}}) + '\n')
    _e = _C.usage(ep)
    expect('H5 output estimated from written text, block counted once', (0 if _e['output_est'] == 100 else 1, str(_e)), 0)
    expect('H5 tokens use the estimate', (0 if _e['tokens'] == 100 else 1, str(_e)), 0)
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
    # 2026-10-24 (Jonathan): no screenshots; present binds the batch, changelog and page alone
    r = subprocess.run([sys.executable, os.path.join(H, 'approval.py'), 'present', TB], env=ENV, capture_output=True, text=True)
    expect('present with no screenshots', (r.returncode, r.stdout + r.stderr), 0)
    expect('check after a new presentation, before ship', (chk().returncode, ''), 1)
    run('approval.py', {'prompt': 'ship', 'session_id': 'S'}, 'hook')
    expect('approval of a presentation with no screenshots', (chk().returncode, ''), 0)
    open(page, 'a').write('<!-- changed -->')
    expect('check after the page changed', (chk().returncode, ''), 1)
finally:
    shutil.rmtree(T, ignore_errors=True)
    shutil.rmtree(TBD, ignore_errors=True)
# lettered patch batches (s146b): the changelog row is matched exactly, never the parent batch's
sys.path.insert(0, os.path.join(WS, 'tools', 'hooks'))
import approval as _AP  # noqa: E402
_rows = [{'v': 146, 'note': 'a'}, {'v': '146b', 'note': 'b'}, {'v': 147, 'note': 'c'}]
expect('log row for s146', ((_AP.match_entry(_rows, 's146') or {}).get('note'), ''), 'a')
expect('log row for s146b is its own', ((_AP.match_entry(_rows, 's146b') or {}).get('note'), ''), 'b')
expect('no log row for s148', (_AP.match_entry(_rows, 's148'), ''), None)
expect('no log row for a malformed id', (_AP.match_entry(_rows, 's146bb'), ''), None)
print('test_hooks: %d passed, %d failed' % (ok, bad))
sys.exit(1 if bad else 0)
