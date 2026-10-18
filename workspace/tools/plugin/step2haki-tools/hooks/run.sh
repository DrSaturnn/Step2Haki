#!/bin/sh
# run.sh <hook script> [args]: run a Step2Haki repo hook (tools/hooks/<script>) when a checkout is present in this
# container; otherwise allow the call (exit 0). The repo script's own exit code passes through unchanged (exec), so a
# refusal (exit 2) is never masked. When the session's own settings already run the same script (install.sh, the
# fallback), this defers to them, so a hook never runs twice (a doubled launch record would halve the agent cap).
s="$1"; shift
if grep -qs "tools/hooks/$s" "$HOME/.claude/settings.json"; then exit 0; fi
for d in ${AX_HOOK_DIRS:-/home/claude/Step2Haki/workspace/tools/hooks /home/user/Step2Haki/workspace/tools/hooks}; do
  if [ -f "$d/$s" ]; then exec python3 "$d/$s" "$@"; fi
done
exit 0
