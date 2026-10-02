#!/usr/bin/env bash
# Check the DRAT proofs of non-4-colourability with drat-trim.
# usage: DRAT_TRIM=/path/to/drat-trim verification/verify_drat.sh   (run from the repository root)
set -euo pipefail
DRAT_TRIM=${DRAT_TRIM:-drat-trim}
for g in H231 H961; do
  xz -dkf "$g/${g}_4col.drat.xz"
  echo "== $g"
  "$DRAT_TRIM" "$g/${g}_4col.cnf" "$g/${g}_4col.drat" -t 20000 2>&1 | tr '\r' '\n' | tee "results/drat-trim_${g}.log" | grep -E '^s '
  rm -f "$g/${g}_4col.drat"
done
