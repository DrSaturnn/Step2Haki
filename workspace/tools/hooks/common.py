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
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, '..', '..'))
REPO = os.path.dirname(WS)
MAC = sys.platform == 'darwin' and not os.path.isdir('/home/claude')  # Mac desktop session (s141)
STATE = os.environ.get('AX_HOOK_STATE', os.path.expanduser('~/.config/axbx/hooks') if MAC
                       else '/home/claude/.config/axbx/hooks')
WAVE = os.environ.get('AX_WAVE', os.path.join(WS, 'repair', 'efficiency', 'WAVE.json'))
PROJECTS = os.environ.get('AX_TRANSCRIPTS', os.path.expanduser('~/.claude/projects') if MAC
                          else '/root/.claude/projects')


ROLES_REPO = '/home/claude/Step2Haki'  # the repo path roles.json is written against (project chat container)


def roles():
    """roles.json, with its repo paths moved to where this checkout lives (a cloud session clones elsewhere, s138)"""
    cfg = json.load(open(os.path.join(HERE, 'roles.json'), encoding='utf-8'))
    if os.path.realpath(REPO) != ROLES_REPO:
        def mv(p):
            return REPO + p[len(ROLES_REPO):] if p == ROLES_REPO or p.startswith(ROLES_REPO + '/') else p
        cfg['lane_roots'] = [mv(p) for p in cfg['lane_roots']]
        cfg['forbidden'] = [mv(p) for p in cfg['forbidden']]
        cfg['forbidden_re'] = [r.replace('^' + re.escape(ROLES_REPO), '^' + re.escape(REPO))
                               .replace('^' + ROLES_REPO, '^' + re.escape(REPO)) for r in cfg.get('forbidden_re', [])]
    return cfg


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
    """Role:, Plan step:, Lane: and optional Budget: lines from the top of a launch prompt (the first 6 non-blank
    lines). Budget: may only lower the role's call budget (Jonathan 2026-10-12: a per-launch call limit, enforced)."""
    out = {}
    lines = [l.strip() for l in (prompt or '').splitlines() if l.strip()][:6]
    for l in lines:
        m = re.match(r'(Role|Plan step|Lane|Budget)\s*:\s*(.+)$', l)
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


CHARS_PER_TOKEN = 3.8   # English prose and JSON, Claude tokenizer; used only for the written-output estimate


def usage(path):
    """API calls and tokens of one agent transcript, de-duplicated by message id. Streamed chunks of one message share an
    id, and only the later chunks carry the final output count (the first records 1 to 8 tokens), so each field takes
    its largest value per message (Jonathan 2026-10-12: fix the output undercount).

    Sonnet transcripts keep only the starting output figure (s134 cost review), so output_est counts what the agent
    actually wrote (text, thinking and tool-call inputs, each block once) at CHARS_PER_TOKEN, and tokens uses the larger
    of the measured and estimated output per message (s135 efficiency item 2)."""
    per, models, wrote = {}, set(), {}
    try:
        for line in open(path, encoding='utf-8'):
            d = json.loads(line)
            if d.get('type') != 'assistant':
                continue
            m = d.get('message') or {}
            if not m.get('usage'):
                continue
            mid = m.get('id') or d.get('uuid')
            us, cur = m['usage'], per.setdefault(mid, {'input': 0, 'cache_write': 0, 'cache_read': 0, 'output': 0})
            for k, f in (('input', 'input_tokens'), ('cache_write', 'cache_creation_input_tokens'),
                         ('cache_read', 'cache_read_input_tokens'), ('output', 'output_tokens')):
                cur[k] = max(cur[k], us.get(f, 0) or 0)
            if m.get('model'):
                models.add(m['model'])
            seen = wrote.setdefault(mid, {})
            for b in m.get('content') or []:
                if not isinstance(b, dict):
                    continue
                t = b.get('text') or b.get('thinking') or ''
                if b.get('type') == 'tool_use':
                    t = b.get('name', '') + json.dumps(b.get('input') or {}, ensure_ascii=False)
                if t:
                    seen[hashlib.sha256(t.encode('utf-8')).hexdigest()] = len(t)
    except (OSError, ValueError):
        pass
    u = {k: sum(v[k] for v in per.values()) for k in ('input', 'cache_write', 'cache_read', 'output')}
    est = {mid: int(round(sum(wrote.get(mid, {}).values()) / CHARS_PER_TOKEN)) for mid in per}
    u['output_est'] = sum(max(per[mid]['output'], est[mid]) for mid in per)
    u['calls'] = len(per)
    u['tokens'] = u['input'] + u['cache_write'] + u['cache_read'] + u['output_est']
    u['models'] = sorted(models)
    return u


def first_context(path):
    """the fixed start-up context of a transcript: input + cache write + cache read of its first API call (system prompt,
    tool definitions and the first prompt), s135 efficiency item 9"""
    try:
        for line in open(path, encoding='utf-8'):
            d = json.loads(line)
            u = (d.get('message') or {}).get('usage') if d.get('type') == 'assistant' else None
            if u:
                return {'input': u.get('input_tokens', 0) or 0, 'cache_write': u.get('cache_creation_input_tokens', 0) or 0,
                        'cache_read': u.get('cache_read_input_tokens', 0) or 0}
    except (OSError, ValueError):
        pass
    return None


def lead_transcripts():
    return sorted(glob.glob(os.path.join(PROJECTS, '*', '*.jsonl')), key=os.path.getmtime)


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


LEDGER = os.environ.get('AX_LEDGER', os.path.join(WS, 'repair', 'efficiency', 'ledger_spine.csv'))


def past_spend(wave_id):
    """spend of a wave's agents that ran in an earlier container (s148 efficiency fix 3): the committed ledger rows of
    the wave whose agent ids have no transcript here. launches.jsonl and the transcripts live in the container, so
    without this a new chat would start every wave at zero and the caps would not hold across chats."""
    import csv
    tot = {'agents': 0, 'calls': 0, 'tokens': 0}
    if not os.path.exists(LEDGER):
        return tot
    here = {os.path.basename(p)[len('agent-'):-len('.jsonl')]
            for p in glob.glob(os.path.join(PROJECTS, '*', '*', 'subagents', 'agent-*.jsonl'))}
    try:
        for r in csv.DictReader(open(LEDGER, encoding='utf-8')):
            if r.get('wave') != wave_id or not r.get('agent_id') or r['agent_id'] in here:
                continue
            tot['agents'] += 1
            tot['calls'] += int(r.get('calls') or 0)
            tot['tokens'] += int(r.get('tokens') or 0)
    except (OSError, ValueError):
        pass
    return tot


def wave_spend(wave_id):
    """measured spend of a wave: every subagent transcript whose prompt matches a launch recorded for that wave, plus
    the ledger rows of the wave's agents from earlier containers (past_spend)"""
    want = {l['prompt_sha'] for l in launches(wave_id)}
    tot = past_spend(wave_id)
    for p in glob.glob(os.path.join(PROJECTS, '*', '*', 'subagents', 'agent-*.jsonl')):
        if sha(first_user_text(p)) in want:
            u = usage(p)
            tot['agents'] += 1
            tot['calls'] += u['calls']
            tot['tokens'] += u['tokens']
    return tot
