# step2haki-tools

## Builder agent (0.3.0, s153)

The runbook's S1 to S3 builder pilot (2026-10-25) launches role brief-build as agent type `lean-builder` on Opus (tools/hooks/roles.json). This harness reads agent types only from the account plugin, not from /root/.claude/agents or /home/claude/.claude/agents copied in mid-session (checked s153, 2026-10-25), so 0.3.0 adds agents/lean-builder.md. Source of truth: tools/hooks/agents/lean-builder.md.

One agent, `lean-reviewer`, for the Step2Haki batch runbook's review rounds (s135 efficiency item 1). It has only Read, Write, Grep and Glob, a short system prompt and a 27-turn cap (item 8), so a reviewer no longer starts with every shell, web and connector tool definition (about 83k tokens of fixed context in s133 and s134). The launch gate (tools/hooks/agentgate.py, roles.json "agent") requires the review roles to launch as this type.

Source of truth: tools/hooks/agents/lean-reviewer.md in the Step2Haki repo; this plugin carries the same body.

## Hooks (0.2.0, s148 item 9)

Jonathan, 2026-10-18: "how can we make the hooks install automatically done btw ive been having to approve them each time". The three hooks that tools/hooks/install.sh writes into a session's settings now ship in this plugin (hooks/hooks.json), so they load with the plugin at session start:

- PreToolUse on Agent and Task: agentgate.py (H1, the launch gate);
- PreToolUse on every tool: callgate.py (H2 to H4: lanes, git and per-agent call budgets);
- UserPromptSubmit: the approval script's hook mode (G-APPROVE, records "ship").

Each command goes through hooks/run.sh, which runs the repo script from /home/claude/Step2Haki/workspace/tools/hooks or /home/user/Step2Haki/workspace/tools/hooks when one exists and exits 0 otherwise, so the plugin does nothing outside a Step2Haki checkout. The script's own exit code passes through (a refusal, exit 2, is never masked). When the session's settings already run the same script (the install.sh fallback), run.sh defers to them, so no hook runs twice.

Runbook session start: when these hooks are live (test_hooks passes and a probe Agent launch with no model is refused), skip install.sh; otherwise run it and ask. Unverified until the first chat after this version is uploaded: whether this harness loads hooks from a synced account plugin (it does load the plugin's agent).
