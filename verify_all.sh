#!/usr/bin/env bash
# Run every verification step of the paper. Logs go to results/.
# Requirements: Python 3 with requirements.txt, PARI/GP, a C compiler, xz, drat-trim (set DRAT_TRIM).
set -euo pipefail
cd "$(dirname "$0")"
PY=${PYTHON:-python3}
export PYTHON=$PY
mkdir -p results

echo "== 1. rebuild parent graphs G372, G972"
"$PY" construction/build_G372.py
"$PY" construction/build_G972.py

echo "== 2. counts, parent indices, edges, 5-colourings, criticality certificates, Moser spindles"
"$PY" verification/verify_graph.py H231 | grep -E "\"(vertices|edges|missing_unit_edges|nonedge_min_gap|moser_spindles|all_ok)\""
"$PY" verification/verify_graph.py H961 | grep -E "\"(vertices|edges|missing_unit_edges|nonedge_min_gap|moser_spindles|all_ok)\""

echo "== 3. exact arithmetic (sphere and unit-edge identities)"
verification/verify_exact.sh | grep -E "failures|matched"

echo "== 4. DRAT proofs of non-4-colourability"
verification/verify_drat.sh

echo "== 5. cross-check: three SAT solvers, two encodings"
"$PY" verification/crosscheck_solvers.py H231 | grep all_unsat
"$PY" verification/crosscheck_solvers.py H961 | grep all_unsat

echo "== 6. SAT-free exhaustive search (H231)"
verification/verify_dsatur.sh | head -1
rm -f verification/dsatur

echo "== 7. audit: every number and file name in the manuscript vs. the artifacts"
"$PY" verification/audit.py | tail -1

echo "== all checks finished; see results/"
