#!/usr/bin/env python3
"""PreToolUse on every tool. Lead calls: only the approval records are protected (G-APPROVE: they are written by the
UserPromptSubmit hook alone). Subagent calls:
  T8  role and lane come from the Role: and Lane: lines of the agent's own launch prompt, read from its transcript, and
      the launch must be one H1 recorded; otherwise every call is refused (fail closed);
  H4  calls are counted per agent and refused past the role's budget (tools/hooks/roles.json);
  H2  Write, Edit and NotebookEdit only inside the lane, never a forbidden path;
  H3  Bash: no git history changes or pushes, ship.sh, mac_sync, ~/.config, .claude or the token; a command that writes
      may not name a forbidden path except as the script it runs, and its redirect or tee targets must be in the lane
      or /tmp. (A pattern gate: it stops plain writes, not a determined evasion; the lead's diff review backs it.)
"""
import json
import os
import re
import shlex
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C  # noqa: E402

ALWAYS = [r'ship\.sh', r'mac_sync', r'\.config(/|\b)', r'\.claude(/|\b)', r'gh_token', r'axbx/hooks']
WRITE_OPS = (r'(?<![0-9&<])>>?(?!&)|\btee\b|\bcp\b|\bmv\b|\brm\b|\bsed\s+(-[a-zA-Z]*i|--in-place)|\btouch\b|\bmkdir\b|'
             r'\binstall\b|\bln\b|\btruncate\b|\brsync\b|\bdd\b|\bunzip\b|\btar\b|open\([^)]*[\'"][wax]|write_text|\.write\(')
RUNNERS = {'python', 'python3', 'node', 'bash', 'sh', 'npx'}
# git for agents is read-only: every git invocation must name one of these subcommands. Options before the
# subcommand (-C dir, -c key=value, --git-dir=...) are skipped: R2 probe 2 showed "git -C <dir> commit" passing the
# earlier "git commit" pattern, and it made a commit (removed by the lead; never pushed).
GIT_READ = {'log', 'show', 'diff', 'status', 'ls-files', 'rev-parse', 'blame', 'grep', 'cat-file', 'ls-tree',
            'describe', 'shortlog', 'rev-list', 'merge-base', 'name-rev', 'version', 'help'}
GIT_OPT_ARG = {'-C', '-c', '--git-dir', '--work-tree', '--namespace', '--exec-path', '--config-env'}


def git_writes(cmd):
    """the first git subcommand in cmd that is not read-only, or None (a bare git counts as not read-only)"""
    for m in re.finditer(r'(?:^|[\s;&|(`$])git(?=\s|$)', cmd):
        rest = cmd[m.end():]
        try:
            toks = shlex.split(rest, posix=True)
        except ValueError:
            toks = rest.split()
        i = 0
        while i < len(toks) and toks[i].startswith('-'):
            i += 2 if toks[i] in GIT_OPT_ARG else 1
        sub = toks[i] if i < len(toks) else ''
        if sub not in GIT_READ:
            return sub or '(none)'
    return None


def lead(d):
    ti = d.get('tool_input') or {}
    appr = os.path.join(C.STATE, 'approvals')
    if d.get('tool_name') in ('Write', 'Edit', 'NotebookEdit'):
        p = C.norm(ti.get('file_path') or ti.get('notebook_path'), d.get('cwd'))
        if C.inside(p, appr):
            C.refuse('APPROVAL GATE: approval records are written only by the hook, when Jonathan says "ship" in reply '
                     'to the screenshots.')
    if d.get('tool_name') == 'Bash' and re.search(r'axbx/hooks/approvals|hooks/approvals|AX_HOOK_STATE', ti.get('command', '')):
        C.refuse('APPROVAL GATE: the lead may not touch approval records or the hook state path by command.')
    return 0


def agent_record(d):
    aid = d['agent_id']
    p = C.state('agents', '%s.json' % aid)
    if os.path.exists(p):
        return p, json.load(open(p, encoding='utf-8'))
    tr = C.agent_transcript(aid, d)
    if not tr:
        C.refuse('CALL GATE: no transcript found for agent %s, so its role and lane are unknown; every call is refused.'
                 % aid, agent=aid)
    text = C.first_user_text(tr)
    h = C.header(text)
    if 'role' not in h or 'lane' not in h:
        C.refuse('CALL GATE: agent %s has no Role: and Lane: lines in its launch prompt; every call is refused.' % aid,
                 agent=aid)
    launched = [l for l in C.launches() if l['prompt_sha'] == C.sha(text)]
    if not launched:
        C.refuse('CALL GATE: agent %s was not launched through the launch gate; every call is refused.' % aid, agent=aid)
    cfg = C.roles()
    rec = {'agent_id': aid, 'role': h['role'], 'lane': os.path.realpath(h['lane']), 'wave': launched[-1]['wave'],
           'budget': cfg['roles'].get(h['role'], {}).get('budget', 0), 'count': 0, 'transcript': tr}
    json.dump(rec, open(p, 'w', encoding='utf-8'))
    return p, rec


def paths_in(cmd):
    try:
        toks = shlex.split(cmd, posix=True)
    except ValueError:
        toks = cmd.split()
    run = set()
    for i, t in enumerate(toks):
        if os.path.basename(t) in RUNNERS:
            j = i + 1
            while j < len(toks) and toks[j].startswith('-'):
                j += 1
            if j < len(toks):
                run.add(toks[j])
    pathish = [t for t in toks if ('/' in t or t.startswith('.')) and not t.startswith('-') and '://' not in t]
    return pathish, run


REPORT_TOOLS = {'SubagentHandback'}      # an agent must always be able to report, above all when its budget is spent


def subagent(d):
    p, rec = agent_record(d)
    if d.get('tool_name') in REPORT_TOOLS:
        return 0
    rec['count'] += 1
    json.dump(rec, open(p, 'w', encoding='utf-8'))
    who = '%s agent %s' % (rec['role'], d['agent_id'])
    if rec['count'] > rec['budget']:
        C.refuse('CALL BUDGET: %s has used its %d calls. Stop now and report what your packet lacked.'
                 % (who, rec['budget']), agent=d['agent_id'])
    tool, ti, cwd = d.get('tool_name'), d.get('tool_input') or {}, d.get('cwd')
    lane = rec['lane']
    if tool in ('Agent', 'Task'):
        C.refuse('CALL GATE: %s may not launch agents.' % who, agent=d['agent_id'])
    if tool in ('Write', 'Edit', 'NotebookEdit', 'MultiEdit'):
        f = C.norm(ti.get('file_path') or ti.get('notebook_path'), cwd)
        bad = C.forbidden(f)
        if bad or not C.inside(f, lane):
            C.refuse('LANE GATE: %s may write only inside %s; %s is refused%s.'
                     % (who, lane, f, ' (forbidden: %s)' % bad if bad else ''), agent=d['agent_id'])
    if tool == 'Bash':
        cmd = ti.get('command', '')
        for r in ALWAYS:
            if re.search(r, cmd):
                C.refuse('COMMAND GATE: %s: command refused (%s).' % (who, r), agent=d['agent_id'])
        g = git_writes(cmd)
        if g:
            C.refuse('COMMAND GATE: %s: git %s refused; agents may only read git (%s).'
                     % (who, g, ', '.join(sorted(GIT_READ))), agent=d['agent_id'])
        if re.search(WRITE_OPS, cmd):
            pathish, run = paths_in(cmd)
            for t in pathish:
                if t in run or t == '/dev/null':
                    continue
                bad = C.forbidden(C.norm(t, cwd))
                if bad:
                    C.refuse('COMMAND GATE: %s: a writing command may not name %s (forbidden: %s).' % (who, t, bad),
                             agent=d['agent_id'])
            for t in re.findall(r'(?<![0-9&<])>>?\s*([^\s;|&<>]+)', cmd) + re.findall(r'\btee\s+(?:-a\s+)?([^\s;|&<>]+)', cmd):
                q = C.norm(t, cwd)
                if t != '/dev/null' and not (C.inside(q, lane) or C.inside(q, '/tmp')):
                    C.refuse('LANE GATE: %s: output goes only to %s or /tmp, not %s.' % (who, lane, t),
                             agent=d['agent_id'])
    return 0


RAW = {}


def main():
    d = json.load(sys.stdin)
    RAW.update(d)
    return subagent(d) if d.get('agent_id') else lead(d)


if __name__ == '__main__':
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except Exception as ex:  # noqa: BLE001  fail closed for agents and launches, open for the lead's own tools
        C.log_event('hook-error', hook='callgate', error=repr(ex)[:300], agent=RAW.get('agent_id'))
        if RAW.get('agent_id'):                     # an agent's call is refused
            print('HOOK ERROR in callgate: %r; the call is refused' % ex, file=sys.stderr)
            sys.exit(2)
        sys.exit(0)                                 # never lock the lead out of its own tools over a hook bug
