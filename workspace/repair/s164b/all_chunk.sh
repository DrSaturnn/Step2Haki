#!/usr/bin/env bash
# all_chunk.sh: every-brief computed-style parity for a list of view:config pairs, one browser job at a time, so a chunk
# fits the 2 h cap on a background command (about 34 min per pair, 17 min when the before dump is cached).
#
#   repair/s164b/all_chunk.sh CAND TAG "desk:flat-dark-read phone:sculpted-dark-read ..."
#
# Appends one line per pair to local/s164b/<TAG>_all.txt (the sty_loop.sh result line).
set -u
cd "$(dirname "$0")/../.."
CAND="$1"; TAG="$2"; PAIRS="$3"
for p in $PAIRS; do
  v="${p%%:*}"; c="${p#*:}"
  repair/s164b/sty_loop.sh "$CAND" "$TAG" "$c" "$v" all | tee -a "local/s164b/${TAG}_all.txt"
done
