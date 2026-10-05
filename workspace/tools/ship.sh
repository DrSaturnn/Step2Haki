#!/usr/bin/env bash
# ship.sh sNN "<message>" [--attr-only]
# One call per batch, from anywhere. Workspace = this script's parent; repo root = Step2Haki.
#  1. build repair/sNN/*.json onto a scratch copy; rules self-tests (test_migrate_check, test_gate_rules);
#     gate (every brief type, incl. source-and-scope G1-G3, K3; base HEAD; --attr-only also asserts
#     attribute-only); render; vendor scan (no source text in tracked files, page under limit);
#     refuse if any local-only path is tracked; vendor scan against the NEW page (orphaned source runs);
#     preflight.py content warnings (advisory, never abort).   -> any failure aborts before writing anything
#  2. write workspace/index.html and ../discriminator-briefs-site/index.html (the deployed copy)
#  3. commit body from the page diff (tools/changelog.py), prepended to workspace/CHANGELOG.md
#  4. commit "<sNN>: <message>" + body + trailers
#  5. push origin main only if /home/claude/.config/axbx/gh_token exists (one-shot extraheader via
#     GIT_CONFIG_* env: never in .git/config, argv or output); else "push skipped: no token"
#  6. /mnt/user-data/outputs: index.html, axbx-repo.bundle, axbx-local-only.tar.gz
# Summary lines only.
set -uo pipefail
WS="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROOT="$(git -C "$WS" rev-parse --show-toplevel)"
git -C "$ROOT" config user.email 297481111+DrSaturnn@users.noreply.github.com; git -C "$ROOT" config user.name DrSaturnn  # GitHub blocks pushes exposing a private email
SITE="$ROOT/discriminator-briefs-site/index.html"
OUT=/mnt/user-data/outputs
TOKF=/home/claude/.config/axbx/gh_token
B="${1:-}"; MSG="${2:-}"; MODE="${3:-}"
if [[ ! "$B" =~ ^s[0-9A-Za-z_-]+$ || -z "$MSG" ]]; then echo 'usage: tools/ship.sh sNN "<message>" [--attr-only]'; exit 2; fi
cd "$WS" || exit 2
TMP="$(mktemp -d /tmp/axbx-ship-XXXXXX)"; trap 'rm -rf "$TMP"' EXIT
fail(){ echo "ship $B: ABORT at $1 (nothing written)"; [[ -n "${2:-}" ]] && echo "$2"; exit 1; }

# ---- 1. checks on a scratch copy
o=$(python3 repair/build.py "$B" --out "$TMP/index.html" 2>&1) || fail build "$o"; echo "$o"
# stamp the build for the page's version label and update check (s43): <meta name="ax-build"> now, version.json in step 2
STAMP_DAY=$(TZ=America/New_York date +%Y-%m-%d)
python3 - "$TMP/index.html" "$B" "$STAMP_DAY" <<'PY' || fail stamp
import re, sys
p, b, d = sys.argv[1:]
s = open(p, encoding='utf-8').read()
s = re.sub(r'<meta name="ax-build" content="[^"]*">', '<meta name="ax-build" content="%s|%s">' % (b, d), s, count=1)
open(p, 'w', encoding='utf-8').write(s)
PY
# change log (s74): fill <script id="axlog"> from repair/changelog/axlog.py; every shipped build needs an entry there
LOGJSON=$(python3 repair/changelog/axlog.py 2>&1) || fail changelog "$LOGJSON"
AXLOG="$LOGJSON" python3 - "$TMP/index.html" "$B" <<'PY' || fail changelog "add an entry for $B to repair/changelog/axlog.py (reader-facing note; merges as [new title, [old titles]])"
import json, os, re, sys
p, b = sys.argv[1], sys.argv[2]
data = os.environ['AXLOG']; log = json.loads(data)
n = re.sub(r'^s0*', '', b)
if not n.isdigit() or int(n) not in [e['v'] for e in log]:
    sys.exit(1)
s = open(p, encoding='utf-8').read()
safe = data.strip().replace('</', '<\\/')
s, k = re.subn(r'(<script type="application/json" id="axlog">)(.*?)(</script>)', lambda m: m.group(1) + safe + m.group(3), s, count=1, flags=re.S)
if k != 1:
    sys.exit(1)
open(p, 'w', encoding='utf-8').write(s)
PY
echo "changelog: $(echo "$LOGJSON" | python3 -c 'import json,sys; print(len(json.load(sys.stdin)))') entries"
# rules self-tests: the checks themselves must still catch every known defect, on every brief type
o=$(python3 tools/test_migrate_check.py 2>&1) || fail rules-selftest "$(echo "$o" | grep -E '^BAD|passed')"
o2=$(AXBX_PAGE="$TMP/index.html" python3 tools/test_gate_rules.py 2>&1) || fail rules-selftest "$(echo "$o2" | grep -E '^BAD|passed')"
echo "rules: self-test $(echo "$o" | tail -1), all brief types $(echo "$o2" | tail -1)"
GA=(--base HEAD); [[ "$MODE" == "--attr-only" ]] && GA=(--attr-only HEAD)
GATE=$(python3 tools/gate.py "$TMP/index.html" "${GA[@]}" 2>&1) || fail gate "$GATE"; GATE=$(echo "$GATE" | head -1); echo "$GATE"
RENDER=$(node tools/render.js "$TMP/index.html" 2>&1) || fail render "$RENDER"; RENDER=$(echo "$RENDER" | head -1); echo "$RENDER"
TRACKED_LO=$(python3 - "$WS" <<'PY'
import os, subprocess, sys
sys.path.insert(0, os.path.join(sys.argv[1], 'tools'))
import vendor_scan as v
ws = sys.argv[1]
top = subprocess.run(['git', '-C', ws, 'rev-parse', '--show-toplevel'], capture_output=True, text=True).stdout.strip()
pre = os.path.relpath(ws, top)
lo = [x if pre == '.' else pre + '/' + x for x in v.local_only(ws)]
files = subprocess.run(['git', '-C', top, 'ls-files'], capture_output=True, text=True).stdout.split('\n')
print('\n'.join(f for f in files if f and v.is_local(f, lo)))
PY
)
[[ -z "$TRACKED_LO" ]] || fail local-only "tracked local-only paths (git rm --cached them): $TRACKED_LO"
o=$(python3 tools/vendor_scan.py 2>&1) || fail vendor-scan "$o"
VEND="vendor: clean ($(echo "$o" | head -1 | grep -o '[0-9]* source shingles'); page $(echo "$o" | grep '(workspace/index.html)' | grep -o '[0-9.]*%'))"
if [[ ! -d repair/sources ]]; then VEND="vendor: NOT CHECKED (repair/sources missing: restore axbx-local-only.tar.gz)"; fi
echo "$VEND"
# P7 (s105): judge tracked edit files against the page about to ship, so a wording change that
# orphans a source run in an old sNN json fails this ship instead of the next one (s103)
if [[ -d repair/sources ]]; then
  o=$(python3 tools/vendor_scan.py --page "$TMP/index.html" 2>&1) || fail vendor-orphan "$o
fix: reword or reorder the flagged file's run (git add it), as in s103"
fi
# advisory content checks (P1-P6): never abort; settle each line or pass it to the auditor
python3 tools/preflight.py "$TMP/index.html" --base HEAD 2>&1 | head -40

# ---- 2. write the page and the deployed copy
git -C "$ROOT" show HEAD:./workspace/index.html > "$TMP/prev.html" 2>/dev/null || cp index.html "$TMP/prev.html"
cp index.html "$TMP/index.keep.html"; [[ -f "$SITE" ]] && cp "$SITE" "$TMP/site.keep.html"
cp CHANGELOG.md "$TMP/changelog.keep.md" 2>/dev/null || true
restore(){ cp "$TMP/index.keep.html" index.html; [[ -f "$TMP/site.keep.html" ]] && cp "$TMP/site.keep.html" "$SITE"
  [[ -f "$TMP/changelog.keep.md" ]] && cp "$TMP/changelog.keep.md" CHANGELOG.md
  [[ -f "$TMP/version.keep.json" ]] && cp "$TMP/version.keep.json" "$(dirname "$SITE")/version.json"; git -C "$ROOT" reset -q; }
if cmp -s "$TMP/index.html" "$SITE"; then SITELINE="Site: discriminator-briefs-site/index.html unchanged (no deploy)"
else SITELINE="Site: discriminator-briefs-site/index.html updated (Vercel deploys on push)"; fi
cp "$TMP/index.html" index.html
mkdir -p "$(dirname "$SITE")" && cp "$TMP/index.html" "$SITE"
VERF="$(dirname "$SITE")/version.json"; [[ -f "$VERF" ]] && cp "$VERF" "$TMP/version.keep.json"
grep -q 'name="ax-build"' "$SITE" && printf '{"build":"%s","date":"%s"}\n' "$B" "$STAMP_DAY" > "$VERF"
echo "$SITELINE"

# ---- 3. commit body + CHANGELOG entry
python3 tools/changelog.py "$TMP/prev.html" index.html --site "$SITELINE" --check "$GATE" --check "$RENDER" --check "$VEND" \
  --entry "$B: $MSG" --changelog CHANGELOG.md > "$TMP/body.txt" || { restore; fail changelog; }

# ---- 4. commit
git -C "$ROOT" add -A -- workspace "discriminator-briefs-site/index.html" >/dev/null 2>&1
[[ -f "$ROOT/discriminator-briefs-site/version.json" ]] && git -C "$ROOT" add -- "discriminator-briefs-site/version.json" >/dev/null 2>&1
if git -C "$ROOT" diff --cached --quiet; then
  echo "commit: nothing to commit"
else
  { echo "$B: $MSG"; echo; cat "$TMP/body.txt"; echo; echo "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>";
    echo "Claude-Session: https://claude.ai/code/session_01AgUUwsL6Nx5TMh8uAEX8Ak"; } > "$TMP/msg.txt"
  git -C "$ROOT" commit -q -F "$TMP/msg.txt" || { restore; fail commit; }
  echo "commit: $(git -C "$ROOT" log -1 --format='%h %s') ($(git -C "$ROOT" rev-list --count HEAD) commits)"
fi

# ---- 5. push (token never on disk in .git/config, never in argv, never printed)
PUSHRC=0
if [[ -s "$TOKF" ]]; then
  URL="$(git -C "$ROOT" remote get-url origin 2>/dev/null)"
  if [[ "$URL" =~ ^https://github\.com/DrSaturnn/Step2Haki(\.git)?$ ]]; then
    AUTH="$(printf 'x-access-token:%s' "$(tr -d ' \r\n' < "$TOKF")" | base64 -w0)"
    PO=$(GIT_TERMINAL_PROMPT=0 GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0="http.https://github.com/.extraheader" \
         GIT_CONFIG_VALUE_0="AUTHORIZATION: basic $AUTH" git -C "$ROOT" push -q origin HEAD:main 2>&1); PUSHRC=$?
    unset AUTH
    PO="$(echo "$PO" | sed -E 's/(basic|bearer|token)[ :][^ ]+/\1 ***/Ig; s/gh[pousr]_[A-Za-z0-9_]+/***/g' | head -2)"
    if [[ $PUSHRC -eq 0 ]]; then echo "push: ok origin/main -> $(git -C "$ROOT" rev-parse --short HEAD)"; else echo "push: FAILED ($PO)"; fi
  else
    PUSHRC=1; echo "push: FAILED (origin is not the plain https Step2Haki URL)"
  fi
else
  echo "push skipped: no token"
fi

# ---- 6. outputs
mkdir -p "$OUT"
cp index.html "$OUT/index.html.tmp" && mv "$OUT/index.html.tmp" "$OUT/index.html"
git -C "$ROOT" bundle create "$TMP/repo.bundle" --all >/dev/null 2>&1 && mv "$TMP/repo.bundle" "$OUT/axbx-repo.bundle" || echo "outputs: bundle FAILED"
LOCAL=$(python3 - "$WS" <<'PY'
import glob, os, sys
sys.path.insert(0, os.path.join(sys.argv[1], 'tools'))
import vendor_scan as v
ws = sys.argv[1]
out = []
for x in v.local_only(ws):
    for p in sorted(glob.glob(os.path.join(ws, x.rstrip('/')))):
        out.append(os.path.relpath(p, ws))
print('\n'.join(out))
PY
)
if [[ -n "$LOCAL" ]]; then
  echo "$LOCAL" | tar -czf "$TMP/local.tgz" -C "$WS" -T - && mv "$TMP/local.tgz" "$OUT/axbx-local-only.tar.gz"
  LT="axbx-local-only.tar.gz $(tar -tzf "$OUT/axbx-local-only.tar.gz" | grep -vc '/$') files"
else LT="axbx-local-only.tar.gz skipped (no local-only files on disk)"; fi
echo "outputs: index.html sha256 $(sha256sum "$OUT/index.html" | cut -c1-12), axbx-repo.bundle $(du -h "$OUT/axbx-repo.bundle" | cut -f1), $LT"
exit $PUSHRC
