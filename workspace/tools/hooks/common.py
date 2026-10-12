"""Shared helpers for the Step2Haki hooks (SPINE_SCALE_PLAN.md section 4).

State lives outside the repo in /home/claude/.config/axbx/hooks (subagents may not touch /home/claude/.config):
  launches.jsonl   one line per allowed Agent launch (H1)
  agents/<id>.json role, lane and call count per subagent (T8, H4)
  present/<b>.json the screenshots manifest the lead registered for batch b (G-APPROVE)
  approvals/<b>.json written only by the UserPromptSubmit hook when Jonathan says "ship" (G-APPROVE)
  events.jsonl     every refusal, for the record
"""
import glob
import hashlib
import json
import os
import re
import time

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, '..', '..'))
REPO = os.path.dirname(WS)
STATE = os.environ.get('AX_HOOK_STATE', '/home/claude/.config/axbx/hooks')
WAVE = os.environ.get('AX_WAVE', os.path.join(WS, 'repair', 'efficiency', 'WAVE.json'))
PROJECTS = os.environ.get('AX_TRANSCRIPTS', '/root/.claude/projects')


def roles():
    return json.load(open(os.path.join(HERE, 'roles.json'), encoding='utf-8'))


def state(*parts):
    p = os.path.join(STATE, *parts)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    return p


def log_event(kind, **kw):
    kw.update(kind=kind, t=time.strftime('%Y-%m-%dT%H:%M:%S'))
    with open(state('events.jsonl'), 'a', encoding='utf-8') as f:
        f.write(json.dumps(kw) + '\n')


def refuse(msg, **kw):
    """exit 2: the tool call is blocked and msg goes back to the model"""
    import sys
    log_event('refuse', msg=msg, **kw)
    print(msg, file=sys.stderr)
    sys.exit(2)


def sha(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def header(prompt):
    """Role:, Plan step: and Lane: lines from the top of a launch prompt (the first 6 non-blank lines)"""
    out = {}
    lines = [l.strip() for l in (prompt or '').splitlines() if l.strip()][:6]
    for l in lines:
        m = re.match(r'(Role|Plan step|Lane)\s*:\s*(.+)$', l)
        if m:
            out[m.group(1).lower().replace(' ', '_')] = m.group(2).strip()
    return out


def norm(p, cwd=None):
    if not p:
        return ''
    p = os.path.expanduser(p)
    if not os.path.isabs(p):
        p = os.path.join(cwd or os.getcwd(), p)
    return os.path.realpath(p)


def inside(p, root):
    root = os.path.realpath(root.rstrip('/')) if root.endswith('/') else os.path.realpath(root)
    return p == root or p.startswith(root.rstrip('/') + '/')


def forbidden(p, cfg=None):
    """the forbidden entry that covers path p (folders end in /, files match exactly, forbidden_re are regexes)"""
    cfg = cfg or roles()
    for f in cfg['forbidden']:
        if (f.endswith('/') and inside(p, f)) or (not f.endswith('/') and p == os.path.realpath(f)):
            return f
    for r in cfg.get('forbidden_re', []):
        if re.search(r, p):
            return r
    return None


def lane_ok(lane, cfg=None):
    """a lane is an absolute folder under a lane root, not a root itself, and nothing in it is forbidden"""
    cfg = cfg or roles()
    if not lane or not os.path.isabs(lane):
        return 'Lane must be an absolute folder path'
    lp = os.path.realpath(lane)
    if not any(inside(lp, r) and lp != os.path.realpath(r.rstrip('/')) for r in cfg['lane_roots']):
        return 'Lane %s is not inside a lane root (%s)' % (lane, ', '.join(cfg['lane_roots']))
    if forbidden(lp + '/x', cfg):
        return 'Lane %s overlaps a forbidden path' % lane
    return None


# ---- transcripts (T5, T6, T8)
def first_user_text(path):
    try:
        for line in open(path, encoding='utf-8'):
            d = json.loads(line)
            if d.get('type') != 'user':
                continue
            c = (d.get('message') or {}).get('content')
            if isinstance(c, str):
                return c
            if isinstance(c, list):
                return '\n'.join(x.get('text', '') for x in c if isinstance(x, dict) and x.get('type') == 'text')
    except (OSError, ValueError):
        pass
    return ''


def agent_transcript(agent_id, hook=None):
    pats = []
    if hook and hook.get('transcript_path') and hook.get('session_id'):
        base = os.path.dirname(hook['transcript_path'])
        pats.append(os.path.join(base, hook['session_id'], 'subagents', 'agent-%s.jsonl' % agent_id))
    pats.append(os.path.join(PROJECTS, '*', '*', 'subagents', 'agent-%s.jsonl' % agent_id))
    for p in pats:
        hits = glob.glob(p)
        if hits:
            return hits[0]
    return None


def usage(path):
    """API calls and tokens of one agent transcript, de-duplicated by message id (streamed chunks share an id)"""
    seen, u = set(), {'calls': 0, 'input': 0, 'cache_write': 0, 'cache_read': 0, 'output': 0, 'models': set()}
    try:
        for line in open(path, encoding='utf-8'):
            d = json.loads(line)
            if d.get('type') != 'assistant':
                continue
            m = d.get('message') or {}
            mid = m.get('id') or d.get('uuid')
            if mid in seen or not m.get('usage'):
                continue
            seen.add(mid)
            us = m['usage']
            u['calls'] += 1
            u['input'] += us.get('input_tokens', 0) or 0
            u['cache_write'] += us.get('cache_creation_input_tokens', 0) or 0
            u['cache_read'] += us.get('cache_read_input_tokens', 0) or 0
            u['output'] += us.get('output_tokens', 0) or 0
            if m.get('model'):
                u['models'].add(m['model'])
    except (OSError, ValueError):
        pass
    u['tokens'] = u['input'] + u['cache_write'] + u['cache_read'] + u['output']
    u['models'] = sorted(u['models'])
    return u


def wave():
    try:
        return json.load(open(WAVE, encoding='utf-8'))
    except (OSError, ValueError):
        return None


def launches(wave_id=None):
    out = []
    p = state('launches.jsonl')
    if os.path.exists(p):
        for line in open(p, encoding='utf-8'):
            try:
                d = json.loads(line)
            except ValueError:
                continue
            if wave_id is None or d.get('wave') == wave_id:
                out.append(d)
    return out


def wave_spend(wave_id):
    """measured spend of a wave: every subagent transcript whose prompt matches a launch recorded for that wave"""
    want = {l['prompt_sha'] for l in launches(wave_id)}
    tot = {'agents': 0, 'calls': 0, 'tokens': 0}
    for p in glob.glob(os.path.join(PROJECTS, '*', '*', 'subagents', 'agent-*.jsonl')):
        if sha(first_user_text(p)) in want:
            u = usage(p)
            tot['agents'] += 1
            tot['calls'] += u['calls']
            tot['tokens'] += u['tokens']
    return tot
