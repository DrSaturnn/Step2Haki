#!/usr/bin/env bash
# s169 candidate checks (the ship.sh check list, run on a candidate). Usage from workspace/:
#   C=c2 bash repair/s169/run_checks.sh        -> local/s169/checks_$C/*.txt, rc.txt
# (the ship.sh check list on a candidate)
set -u
C=${C:-c1}; P=local/s169/$C/index.html; O=local/s169/checks_$C; mkdir -p "$O"; : > "$O/rc.txt"
SITE=../discriminator-briefs-site/index.html
run() { local n=$1; shift; "$@" > "$O/$n.txt" 2>&1; echo "$n rc $?" >> "$O/rc.txt"; }
UA=(); [ -f repair/s169/ui_allow.json ] && UA=(--allow repair/s169/ui_allow.json)
run migrate_check python3 tools/test_migrate_check.py
run gate_rules env AXBX_PAGE="$P" python3 tools/test_gate_rules.py
run gate python3 tools/gate.py "$P" --base HEAD
run render node tools/render.js "$P"
run ui_lint bash -c "python3 tools/spine/ui_lint.py --site && python3 tools/spine/ui_lint.py $P --baseline tools/spine/ui_baseline.json"
run vendor python3 tools/vendor_scan.py
run vendor_page python3 tools/vendor_scan.py --page "$P"
run preflight python3 tools/preflight.py "$P" --base HEAD
run ui_gate python3 tools/ui_gate.py "$P" "$SITE" "${UA[@]}"
echo done >> "$O/rc.txt"
