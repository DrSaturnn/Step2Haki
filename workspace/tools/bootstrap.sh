#!/usr/bin/env bash
# bootstrap.sh: start-of-session setup for a fresh cloud chat. One call after the clone.
#
#   git clone https://github.com/DrSaturnn/Step2Haki /home/claude/Step2Haki
#   bash /home/claude/Step2Haki/workspace/tools/bootstrap.sh [--tarball PATH] [--token PATH] [--no-gate]
#
# Before running it, from the Mac folder Documents/Step2Haki (device tools):
#   1. device_bash:  cd ~/mnt/Step2Haki && tar -czf axbx-local-only.tar.gz -C local-only .
#   2. device_stage_files: ~/Documents/Step2Haki/axbx-local-only.tar.gz and ~/Documents/Step2Haki/gh_token
#   3. after this script: delete (or move to _to_delete/) the Mac tarball; it is rebuilt every session
#      and the Mac disk runs near full.
# Staged files land in /mnt/user-data/uploads/Step2Haki/, which is where --tarball and --token
# default to. Either can be missing: the script reports what that costs and carries on.
#
# Steps: git identity; npm i (jsdom 24) when missing or wrong; extract the local-only tarball into
# workspace/; install the token at /home/claude/.config/axbx/gh_token (mode 600, never printed);
# write the restore marker (/home/claude/restore_marker, outside the repo) that tools/mac_sync.sh
# diffs against; then a status report and a gate run on the current page.
set -uo pipefail
WS="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROOT="$(git -C "$WS" rev-parse --show-toplevel)"
UP=/mnt/user-data/uploads/Step2Haki
TAR="$UP/axbx-local-only.tar.gz"; TOKSRC="$UP/gh_token"; GATE=1
TOKF=/home/claude/.config/axbx/gh_token
MARK=/home/claude/restore_marker
while [[ $# -gt 0 ]]; do
  case "$1" in
    --tarball) TAR="$2"; shift 2;;
    --token) TOKSRC="$2"; shift 2;;
    --no-gate) GATE=0; shift;;
    *) echo "usage: tools/bootstrap.sh [--tarball PATH] [--token PATH] [--no-gate]"; exit 2;;
  esac
done
cd "$WS" || exit 2
WARN=0; warn(){ echo "  ! $*"; WARN=$((WARN+1)); }

echo "== bootstrap $(TZ=America/New_York date '+%Y-%m-%d %H:%M %Z')"
git -C "$ROOT" config user.email 297481111+DrSaturnn@users.noreply.github.com
git -C "$ROOT" config user.name DrSaturnn

# ---- npm (render.js needs jsdom 24; v30 breaks it)
JV=$(node -p "require('jsdom/package.json').version" 2>/dev/null || true)
if [[ "$JV" != 24.* ]]; then
  npm i --silent --no-audit --no-fund >/dev/null 2>&1 || warn "npm i failed"
  JV=$(node -p "require('jsdom/package.json').version" 2>/dev/null || echo none)
fi
echo "jsdom: $JV"; [[ "$JV" == 24.* ]] || warn "jsdom is not 24.x: render.js will fail"

# ---- local-only restore
if [[ -s "$TAR" ]]; then
  if tar -tzf "$TAR" >/dev/null 2>&1; then
    tar -xzf "$TAR" -C "$WS" && touch "$MARK"
    echo "local-only: restored $(tar -tzf "$TAR" | grep -vc '/$') files from $(basename "$TAR"); marker set"
  else
    warn "local-only: $TAR is not a readable gzip tar (partial stage? re-stage it)"
  fi
elif [[ -d repair/sources ]]; then
  echo "local-only: already on disk (no tarball given)"; [[ -e "$MARK" ]] || touch "$MARK"
else
  warn "local-only: missing. ship will print 'vendor: NOT CHECKED' and merge tools are absent"
fi
for d in repair/sources repair/migration local; do
  [[ -d "$d" ]] && echo "  $d: $(find "$d" -type f | wc -l) files" || echo "  $d: absent"
done

# ---- token (never printed, never in git config)
if [[ -s "$TOKSRC" ]]; then
  mkdir -p "$(dirname "$TOKF")" && install -m 600 "$TOKSRC" "$TOKF" && echo "token: installed (mode 600)"
elif [[ -s "$TOKF" ]]; then
  echo "token: already installed"
else
  warn "token: none. ship commits but prints 'push skipped: no token'"
fi
if [[ -s "$TOKF" ]]; then
  [[ "$(stat -c %a "$TOKF")" == 600 ]] || { chmod 600 "$TOKF"; echo "token: mode fixed to 600"; }
  AUTH="$(printf 'x-access-token:%s' "$(tr -d ' \r\n' < "$TOKF")" | base64 -w0)"
  if GIT_TERMINAL_PROMPT=0 GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0="http.https://github.com/.extraheader" \
     GIT_CONFIG_VALUE_0="AUTHORIZATION: basic $AUTH" git -C "$ROOT" ls-remote -q origin HEAD >/dev/null 2>&1; then
    echo "token: accepted by GitHub"
  else
    warn "token: GitHub refused it (expired? it has a 90-day life). Pushes will fail"
  fi
  unset AUTH
fi

# ---- status
LAST=$(git -C "$ROOT" log --format=%s | grep -m1 -oE '^s[0-9]+' || true)
echo "repo: $(git -C "$ROOT" rev-parse --short HEAD) '$(git -C "$ROOT" log -1 --format=%s)'; last ship $LAST"
NEXT=$(python3 -c "import re,sys; print('s%d' % (int(sys.argv[1][1:])+1))" "${LAST:-s0}")
echo "next build id: $NEXT (check the handoff agrees; another chat may have shipped since it was written)"
if cmp -s index.html "$ROOT/discriminator-briefs-site/index.html"; then echo "site copy: matches workspace/index.html"
else warn "site copy differs from workspace/index.html"; fi
M=$(python3 - <<'PY'
b = open('tools/retired_items.csv', 'rb').read()
crlf, lf = b.count(b'\r\n'), b.count(b'\n')
if 0 < crlf < lf:
    print("retired_items.csv: mixed line endings (%d CRLF of %d lines); normalize to CRLF before the next commit" % (crlf, lf))
PY
)
[[ -n "$M" ]] && warn "$M"
if [[ -n "$(git -C "$ROOT" status --porcelain)" ]]; then warn "git tree not clean:"; git -C "$ROOT" status --short | head -10; fi

# ---- gate on the current page (about 1 s)
if [[ $GATE == 1 ]]; then
  G=$(python3 tools/gate.py index.html --base HEAD 2>&1); RC=$?
  echo "gate: $(echo "$G" | head -1)"; [[ $RC == 0 ]] || { warn "gate fails on HEAD's own page"; echo "$G" | sed -n '2,8p'; }
fi
echo "== bootstrap done, $WARN warning(s)"
[[ -s "$TAR" ]] && echo "next: remove the Mac copy of axbx-local-only.tar.gz (rebuilt each session)"
exit 0
