# Reproducibility

## Software used for the reported results

| Tool | Version | Used for |
|---|---|---|
| Python | 3.14.7 | all Python scripts |
| python-sat (PySAT) | 1.9.dev15 (CaDiCaL 1.5.3, Glucose 4, MiniSat 2.2) | vertex search, cross-checks, certificates |
| mpmath / numpy / sympy | 1.3.0 / 2.5.3 / 1.14.0 | 60-digit construction, numerics, Python-format check |
| PARI/GP | 2.19.0 (with galdata) | exact number-field verification, radical coordinates |
| Kissat | 4.0.4 | DRAT proofs (`kissat --no-binary`) |
| drat-trim | commit 2e3b2dc (2024-11-25) | DRAT proof checking |
| Apple clang | 21.0.0 | `verification/dsatur.c` |
| XZ Utils | 5.8.4 | proof compression |
| macOS | Darwin arm64 | platform |

## One command

```sh
pip install -r requirements.txt
DRAT_TRIM=/path/to/drat-trim ./verify_all.sh      # about 6 minutes on a laptop
```

## Step by step (from the repository root)

| Step | Command | Expected result |
|---|---|---|
| 1 | `python construction/build_G372.py` | `G372: 372 vertices, 1710 edges` |
| 2 | `python construction/build_G972.py` | `G972: 972 vertices, 4110 edges` |
| 3 | `python verification/verify_graph.py H231` | `"all_ok": true`, 231 vertices, 938 edges, `missing_unit_edges: 0`, `nonedge_min_gap ≈ 0.0023`, `moser_spindles: 0` |
| 4 | `python verification/verify_graph.py H961` | `"all_ok": true`, 961 vertices, 4028 edges, `missing_unit_edges: 0`, `nonedge_min_gap ≈ 0.00042`, `moser_spindles: 0` (takes ~2 min) |
| 5 | `verification/verify_exact.sh` | PARI: `failures: 0` for 938 and 4028 edges, all points on the sphere; Python: `failures: 0` for both |
| 6 | `DRAT_TRIM=... verification/verify_drat.sh` | `s VERIFIED` for H231 and H961 |
| 7 | `verification/verify_dsatur.sh` | `NOT 4-COLOURABLE (search nodes: 0 e9 + 6997499)` |

`verify_graph.py` checks: vertex/edge counts; that each vertex equals the parent-graph vertex with the
stated index; that all listed edges have length 1 and no other pair has length 1; the 5-colouring; one
4-colouring of G − v for every vertex v (vertex-criticality); absence of Moser spindles.

## Regenerating derived data (optional)

- Criticality certificates: `python verification/make_criticality_certificates.py H231/H231_edges.txt H231/H231_criticality_certificates.txt`
- CNF and DRAT proof: the CNF files list, for every vertex, an at-least-one and at-most-one colour
  constraint, for every edge and colour a conflict clause, and fix the colours of the two endpoints of one
  edge. `kissat --no-binary H231/H231_4col.cnf proof.drat` regenerates a proof (the proof file may differ
  between runs; any proof accepted by drat-trim certifies unsatisfiability).
- Radical coordinates: `cd construction/radicals && gp -q radicals_H231.gp < /dev/null` (likewise `radicals_H961.gp`)
  writes `H231_exact_coordinates.m` from the quadratic tower of the paper; `python m_to_py.py H231` writes the Python
  version. Both outputs are byte-identical to the files in `H231/` and `H961/`. They are checked by
  `verification/check_exact_radicals.py` without PARI/GP.
