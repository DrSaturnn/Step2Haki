#!/usr/bin/env python3
"""H1, launch gate (PreToolUse on Agent and Task). Refuses, before any token is spent, a launch that:
  - comes from a subagent (subagents never launch agents);
  - names no model, or a model other than its role's (tools/hooks/roles.json), or an agent type other than its role's
    'agent' (the lean reviewer type, s135);
  - lacks the Role:, Plan step: or Lane: line at the top of the prompt, or names an unknown role;
  - has a lane outside the lane roots or overlapping a forbidden path;
  - does not match the open wave (repair/efficiency/WAVE.json: plan step, roles), or would pass the wave's agent, call
    or token cap (spend measured from the agent transcripts, T6).
An allowed launch is recorded in launches.jsonl (role, model, lane, wave, prompt sha) so H2 to H5 can find it.
"""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C  # noqa: E402


def main():
    d = json.load(sys.stdin)
    if d.get('tool_name') not in ('Agent', 'Task'):
        return 0
    ti = d.get('tool_input') or {}
    if d.get('agent_id'):
        C.refuse('LAUNCH GATE: a subagent may not launch agents.', agent=d.get('agent_id'))
    cfg = C.roles()
    model = (ti.get('model') or '').strip().lower()
    if not model:
        C.refuse('LAUNCH GATE: refused: no model named. Every launch names its model (plan rule).')
    h = C.header(ti.get('prompt', ''))
    miss = [k for k in ('role', 'plan_step', 'lane') if k not in h]
    if miss:
        C.refuse('LAUNCH GATE: refused: the prompt must start with Role:, Plan step: and Lane: lines (missing: %s).'
                 % ', '.join(miss))
    role = h['role']
    if role not in cfg['roles']:
        C.refuse('LAUNCH GATE: refused: unknown role %r (tools/hooks/roles.json).' % role)
    want = cfg['roles'][role]['model']
    if model != want:
        C.refuse('LAUNCH GATE: refused: role %s runs on %s, not %s.' % (role, want, model))
    kind = cfg['roles'][role].get('agent')                    # s135 efficiency item 1: the lean agent type
    st = ti.get('subagent_type') or ''
    if kind and st != kind and not st.endswith(':' + kind):  # a plugin agent is named <plugin>:<agent>
        C.refuse('LAUNCH GATE: refused: role %s runs as agent type %s (tools/hooks/agents/%s.md), not %r.'
                 % (role, kind, kind, ti.get('subagent_type') or 'general-purpose'))
    bad = C.lane_ok(h['lane'], cfg)
    if bad:
        C.refuse('LAUNCH GATE: refused: %s.' % bad)
    w = C.wave()
    if not w or not w.get('open'):
        C.refuse('LAUNCH GATE: refused: no open wave (repair/efficiency/WAVE.json). Jonathan sets each wave budget.')
    if w.get('plan_step') and h['plan_step'] != w['plan_step']:
        C.refuse('LAUNCH GATE: refused: plan step %r is not the open wave\'s (%r).' % (h['plan_step'], w['plan_step']))
    if w.get('roles') and role not in w['roles']:
        C.refuse('LAUNCH GATE: refused: role %s is not in wave %s.' % (role, w['id']))
    n = len(C.launches(w['id']))
    if n >= int(w['max_agents']):
        C.refuse('LAUNCH GATE: refused: wave %s has used its %d agent(s). Stop and report.' % (w['id'], n))
    spent = C.wave_spend(w['id'])
    if spent['calls'] >= int(w['max_calls']) or spent['tokens'] >= int(w['max_tokens']):
        C.refuse('LAUNCH GATE: refused: wave %s is at its cap (measured %d calls, %d tokens; caps %s, %s). Stop and report.'
                 % (w['id'], spent['calls'], spent['tokens'], w['max_calls'], w['max_tokens']))
    rec = {'t': time.strftime('%Y-%m-%dT%H:%M:%S'), 'wave': w['id'], 'role': role, 'model': model, 'lane': h['lane'],
           'agent_type': ti.get('subagent_type') or '', 'plan_step': h['plan_step'], 'prompt_sha': C.sha(ti.get('prompt', '')), 'tool_use_id': d.get('tool_use_id')}
    with open(C.state('launches.jsonl'), 'a', encoding='utf-8') as f:
        f.write(json.dumps(rec) + '\n')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except Exception as ex:  # noqa: BLE001  fail closed for agents and launches, open for the lead's own tools
        C.log_event('hook-error', hook=os.path.basename(__file__), error=repr(ex)[:300])
        print('HOOK ERROR in %s: %r; the call is refused' % (os.path.basename(__file__), ex), file=sys.stderr)
        sys.exit(2)                                 # a launch is never allowed through a hook bug
