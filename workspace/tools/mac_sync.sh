#!/usr/bin/env bash
# mac_sync.sh: after a ship, prepare everything the Mac folder Documents/Step2Haki needs, in
# pieces small enough for device_commit_files (30 MB per file).
#
#   bash tools/mac_sync.sh [--handoff PATH]    # pack and print the plan
#   bash tools/mac_sync.sh --done              # after the Mac side succeeded: advance the marker
#
# It packs local-only files (tools/local_only.txt) changed since /home/claude/restore_marker
# (written by tools/bootstrap.sh) into /mnt/user-data/outputs/mac-sync/, split into 25 MB parts
# when needed; refreshes index.html and axbx-repo.bundle there when they lag HEAD; and writes
# plan.json listing each output file and its Mac destination, plus the one device_bash command
# that unpacks the delta into local-only/. Nothing on the Mac is touched by this script.
set -uo pipefail
WS="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROOT="$(git -C "$WS" rev-parse --show-toplevel)"
MARK=/home/claude/restore_marker
OUT=/mnt/user-data/outputs/mac-sync
MAC="~/Documents/Step2Haki"
PART=25M
HANDOFF=""
case "${1:-}" in
  --done) touch "$MARK"; echo "marker advanced: next sync packs only files changed after now"; exit 0;;
  --handoff) HANDOFF="$2";;
  "") ;;
  *) echo "usage: tools/mac_sync.sh [--handoff PATH] | --done"; exit 2;;
esac
cd "$WS" || exit 2
[[ -e "$MARK" ]] || { echo "no restore marker: run tools/bootstrap.sh first (or touch $MARK at restore time)"; exit 1; }
rm -rf "$OUT"; mkdir -p "$OUT"
LAST=$(git -C "$ROOT" log --format=%s | grep -m1 -oE '^s[0-9]+' || true); LAST=${LAST:-sNN}
STAMP=$(TZ=America/New_York date +%Y%m%d-%H%M)

# ---- changed local-only files (ignored by git, newer than the marker)
LIST="$OUT/.files"
python3 - "$WS" "$MARK" > "$LIST" <<'PY'
import glob, os, subprocess, sys
ws, mark = sys.argv[1], sys.argv[2]
sys.path.insert(0, os.path.join(ws, 'tools'))
import vendor_scan as v
t0 = os.path.getmtime(mark)
cand = []
for pat in v.local_only(ws):
    for p in glob.glob(os.path.join(ws, pat.rstrip('/'))):
        if os.path.isdir(p):
            for d, _, fs in os.walk(p):
                cand += [os.path.join(d, f) for f in fs]
        elif os.path.isfile(p):
            cand.append(p)
new = sorted({os.path.relpath(p, ws) for p in cand if os.path.getmtime(p) > t0 and '__pycache__' not in p})
if new:  # keep only paths git ignores: a tracked file never belongs in local-only/
    r = subprocess.run(['git', '-C', ws, 'check-ignore', '--stdin'], input='\n'.join(new), capture_output=True, text=True)
    ign = set(r.stdout.split('\n'))
    new = [p for p in new if p in ign]
print('\n'.join(new))
PY
N=$(grep -c . "$LIST" || true)
PARTS=()
if [[ "$N" -gt 0 ]]; then
  BASE="local-delta-$LAST-$STAMP.tar.gz"
  tar -czf "$OUT/$BASE" -C "$WS" -T "$LIST"
  SZ=$(stat -c %s "$OUT/$BASE")
  if (( SZ > 28*1024*1024 )); then
    split -b $PART -d -a 2 "$OUT/$BASE" "$OUT/$BASE.part"; rm "$OUT/$BASE"
    for f in "$OUT/$BASE".part*; do PARTS+=("$(basename "$f")"); done
  else PARTS=("$BASE"); fi
  echo "local-only delta: $N files, $(du -h --apparent-size -c "${PARTS[@]/#/$OUT/}" | tail -1 | cut -f1) in ${#PARTS[@]} file(s)"
  sed 's/^/  /' "$LIST" | head -15; [[ "$N" -gt 15 ]] && echo "  ... and $((N-15)) more"
else
  echo "local-only delta: nothing changed since the marker"
fi

# ---- page and bundle (ship.sh writes them to outputs; refresh if missing or behind HEAD)
cp index.html "$OUT/index.html"
git -C "$ROOT" bundle create "$OUT/axbx-repo.bundle" --all >/dev/null 2>&1 || { echo "bundle FAILED"; exit 1; }
BS=$(stat -c %s "$OUT/axbx-repo.bundle")
(( BS > 30*1024*1024 )) && echo "  ! axbx-repo.bundle is $((BS/1048576)) MB, over the 30 MB commit limit: leave it out this time"
echo "index.html and axbx-repo.bundle at $(git -C "$ROOT" rev-parse --short HEAD) ($((BS/1048576)) MB bundle)"
[[ -n "$HANDOFF" && -s "$HANDOFF" ]] && cp "$HANDOFF" "$OUT/STEP2HAKI_HANDOFF.md" && echo "handoff copy included"

# ---- plan
python3 - "$OUT" "$MAC" "${PARTS[@]}" <<'PY'
import json, os, sys
out, mac, parts = sys.argv[1], sys.argv[2], sys.argv[3:]
files = []
for f in sorted(os.listdir(out)):
    if f.startswith('.') or f == 'plan.json':
        continue
    files.append({'stagedPath': os.path.join(out, f), 'devicePath': '%s/%s' % (mac, f)})
cmd = None
if parts:
    src = ' '.join(parts)
    cmd = ('cd ~/mnt/Step2Haki && cat %s | tar --overwrite -xzf - -C local-only && echo extracted '
           '&& (rm -f %s 2>/dev/null || { mkdir -p _to_delete && mv -f %s _to_delete/; echo moved to _to_delete; }) '
           '&& df -h . | tail -1') % (src, src, src)
plan = {'commit': files, 'then_device_bash': cmd,
        'then_cloud': 'bash tools/mac_sync.sh --done'}
json.dump(plan, open(os.path.join(out, 'plan.json'), 'w'), indent=1)
print('plan: %s (%d files to commit)' % (os.path.join(out, 'plan.json'), len(files)))
for f in files:
    print('  %s -> %s' % (os.path.basename(f['stagedPath']), f['devicePath']))
if cmd:
    print('then device_bash:\n  ' + cmd)
print('then: bash tools/mac_sync.sh --done')
PY
rm -f "$LIST"
