# step2haki-tools

One agent, `lean-reviewer`, for the Step2Haki batch runbook's review rounds (s135 efficiency item 1). It has only Read, Write, Grep and Glob, a short system prompt and a 27-turn cap (item 8), so a reviewer no longer starts with every shell, web and connector tool definition (about 83k tokens of fixed context in s133 and s134). The launch gate (tools/hooks/agentgate.py, roles.json "agent") requires the review roles to launch as this type.

Source of truth: tools/hooks/agents/lean-reviewer.md in the Step2Haki repo; this plugin carries the same body.
