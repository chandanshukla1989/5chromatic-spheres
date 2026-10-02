#!/usr/bin/env bash
# Exact verification of all coordinates, sphere identities and unit edges.
#   1. PARI/GP: coordinates as elements of a degree-8 number field (independent of the radical files)
#   2. Python: the nested-radical coordinate files, with exact arithmetic in Q(sqrt5)(sqrt(beta))(sqrt(gamma))
# usage: verification/verify_exact.sh   (run from the repository root)
set -euo pipefail
PY=${PYTHON:-python3}
(cd verification/pari && gp -q exact372.gp < /dev/null 2>&1 | grep -v Warning) | tee results/exact_pari_H231.log
(cd verification/pari && gp -q exact972.gp < /dev/null 2>&1 | grep -v Warning) | tee results/exact_pari_H961.log
"$PY" verification/check_exact_radicals.py H231/H231_exact_coordinates.m H231/H231_edges.txt 5/8 1/8 H231/H231_vertices.txt | tee results/exact_radicals_H231.log
"$PY" verification/check_exact_radicals.py H961/H961_exact_coordinates.m H961/H961_edges.txt 5/8 -1/8 H961/H961_vertices.txt | tee results/exact_radicals_H961.log
