#!/usr/bin/env bash
# sty_loop.sh: computed-style parity of a candidate page against local/s164b/before.html, per view and config, one
# browser job at a time (the container has 2 cores; concurrent Chromium jobs crash each other).
#
#   repair/s164b/sty_loop.sh CAND TAG "cfg1 cfg2" "desk tablet phone" [SAMPLE|all]
#
# SAMPLE (default 20) is ui_styles --sample (about 21 briefs plus the chrome); "all" dumps every brief.
# Before dumps are cached in local/s164b/sty/before_<view>_<cfg>_<sample>.json (delete them when before.html changes).
# Prints one STYLES SAME / STYLES DIFFER line per view x config; full diffs go to local/s164b/sty/<tag>_<view>_<cfg>.diff.
# Tracked in the repo (was local/s164b/sty_loop.sh in chat 2, lost with the container).
set -u
cd "$(dirname "$0")/../.."
CAND="$1"; TAG="$2"; CFGS="$3"; VIEWS="$4"; S="${5:-20}"
D=local/s164b/sty; mkdir -p "$D"
if [ "$S" = all ]; then OPT=(--chrome); else OPT=(--sample "$S" --chrome); fi
# D-20261105-10: in dark and tinted the shapes follow light, so they are left out of the dark comparison (theme_gate.js
# checks that no box moves; the underline style is a shape too: dark .xref underlines go dotted as in light; the
# text-decoration shorthand is left out, its color and line longhands are compared; background-size follows light too:
# the phone dark .w5an rule reset the .fl annotation line to 100% and is now 12px as in light); light
# configs compare everything
SHAPE='^(border(-(top|right|bottom|left|block|inline)(-(start|end))?)?-(width|style)|border(-[a-z-]*)?-radius|outline-(width|style|offset)|text-decoration-style|text-decoration|background-size)$'
for v in $VIEWS; do for c in $CFGS; do
  # the --t-* color tokens (D-20261105-10) inherit to every element; their effect shows in the real properties
  K=(--skip '^--t-'); case "$c" in *dark*|*tinted*) K=(--skip "${SHAPE%\$}\$|^--t-");; esac
  B="$D/before_${v}_${c}_${S}.json"; C="$D/${TAG}_${v}_${c}_${S}.json"
  [ -s "$B" ] || node tools/ui_styles.js dump local/s164b/before.html "$B" --view "$v" --config "$c" "${OPT[@]}" "${K[@]}" > /dev/null 2>&1
  node tools/ui_styles.js dump "$CAND" "$C" --view "$v" --config "$c" "${OPT[@]}" "${K[@]}" > /dev/null 2>&1
  node tools/ui_styles.js diff "$B" "$C" > "$D/${TAG}_${v}_${c}.diff" 2>&1
  echo "$v $c: $(grep -E '^STYLES' "$D/${TAG}_${v}_${c}.diff")"
done; done
