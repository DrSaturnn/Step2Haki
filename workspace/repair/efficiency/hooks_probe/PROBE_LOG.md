# Hook probes, 2026-10-10 (Claude Code 2.1.296, Cowork cloud session)

Settings file: /home/claude/.claude/settings.json (written mid-session; removed after the probes).
Scripts: hooklog.sh (append raw hook input), agentgate.py (refuse an Agent launch with no model), lanegate.py (refuse a
subagent Write outside one lane, and Bash commands touching tools/, index.html, git commit/push, ship.sh, .config).

Observed hook input (trimmed):
- Lead Bash call: {"hook_event_name":"PreToolUse","tool_name":"Bash","tool_input":{"command":...},"permission_mode":"auto",...} (no agent_id)
- Lead Agent launch: tool_input keys description, prompt, subagent_type, model ("haiku")
- Subagent Bash call: adds "agent_id":"ab80d85b678e3266e","agent_type":"general-purpose"

Results:
- T1 hot reload: PASS (the next Bash call was logged).
- T2 Agent launch with no model: refused by agentgate.py ("PROBE GATE: launch refused: no model named"), no agent started.
- T3 lead vs subagent: PASS (agent_id present only for subagent calls).
- T4 lane: subagent Write into the lane allowed (file on disk); Write to tools/spine/PROBE.txt refused; Bash echo into
  tools/spine/PROBE2.txt refused; neither file exists on disk.
- T5 effective model: subagents/agent-<id>.meta.json {"model":"haiku"}; each API call in agent-<id>.jsonl: claude-haiku-5-5.
- T6 usage: lane probe agent, 6 API calls: cache write 103,858; cache read 277,806; output 22 (harness reported 68,186).
