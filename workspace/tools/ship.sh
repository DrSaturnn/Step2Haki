#!/usr/bin/env bash
# ship.sh sNN "<message>" [--attr-only]
# One call per batch: build repair/sNN/*.json onto a scratch copy, gate (base HEAD; with
# --attr-only also assert attribute-only vs HEAD), render, then and only then write index.html,
# git commit, copy index.html to /mnt/user-data/outputs/index.html and write the git bundle
# /mnt/user-data/outputs/axbx-repo.bundle. Summary lines only. Any failure aborts before writing.
set -uo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT=/mnt/user-data/outputs
B="${1:-}"; MSG="${2:-}"; MODE="${3:-}"
if [[ ! "$B" =~ ^s[0-9A-Za-z_-]+$ || -z "$MSG" ]]; then echo 'usage: tools/ship.sh sNN "<message>" [--attr-only]'; exit 2; fi
cd "$REPO" || exit 2
TMP="$(mktemp -d /tmp/axbx-ship-XXXXXX)"; trap 'rm -rf "$TMP"' EXIT
fail(){ echo "ship $B: ABORT at $1 (nothing written)"; [[ -n "${2:-}" ]] && echo "$2"; exit 1; }

o=$(python3 repair/build.py "$B" --out "$TMP/index.html" 2>&1) || fail build "$o"; echo "$o"
GA=(--base HEAD); [[ "$MODE" == "--attr-only" ]] && GA=(--attr-only HEAD)
o=$(python3 tools/gate.py "$TMP/index.html" "${GA[@]}" 2>&1) || fail gate "$o"; echo "$o" | head -1
o=$(node tools/render.js "$TMP/index.html" 2>&1) || fail render "$o"; echo "$o" | head -1

cp index.html "$TMP/index.prev.html"
cp "$TMP/index.html" index.html
git add -A >/dev/null 2>&1
if git diff --cached --quiet; then
  echo "commit: nothing to commit (tree already matches HEAD)"
else
  git commit -q -m "$B: $MSG" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01AgUUwsL6Nx5TMh8uAEX8Ak" \
    || { cp "$TMP/index.prev.html" index.html; git reset -q; fail commit; }
  echo "commit: $(git log -1 --format='%h %s')"
fi
mkdir -p "$OUT"
cp index.html "$OUT/index.html.tmp" && mv "$OUT/index.html.tmp" "$OUT/index.html"
git bundle create "$TMP/axbx-repo.bundle" --all >/dev/null 2>&1 && mv "$TMP/axbx-repo.bundle" "$OUT/axbx-repo.bundle" \
  || { echo "ship $B: bundle failed (page committed and copied)"; exit 1; }
echo "outputs: index.html sha256 $(sha256sum "$OUT/index.html" | cut -c1-12), axbx-repo.bundle $(du -h "$OUT/axbx-repo.bundle" | cut -f1) ($(git rev-list --all --count) commits)"
