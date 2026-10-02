#!/usr/bin/env bash
# SAT-free exhaustive search for a proper 4-colouring of H231 (DSATUR order, colour-symmetry breaking).
# usage: verification/verify_dsatur.sh   (run from the repository root)
set -euo pipefail
cc -O2 -o verification/dsatur verification/dsatur.c
{ echo "231 938"; grep -v '^#' H231/H231_edges.txt; } | verification/dsatur | tee results/dsatur_H231.log
