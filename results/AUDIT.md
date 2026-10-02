# Audit: manuscript numbers and claims vs. artifacts

| # | item | result | detail |
|---|---|---|---|
| 1 | H231: 231 vertices / 938 edges (files) and in paper | **PASS** | 231 / 938 |
| 2 | H231: parent-graph mapping | **PASS** | max diff 4.6e-31 |
| 3 | H231: all listed edges have length 1 (numerical, 30 digits) | **PASS** | 6.6e-31 |
| 4 | H231: no missing unit edges | **PASS** | min non-edge gap 2.296e-03 |
| 5 | H231: valid 5-colouring | **PASS** |  |
| 6 | H231: criticality certificates (231) valid | **PASS** |  |
| 7 | H231: no Moser spindle | **PASS** | 0 |
| 8 | H961: 961 vertices / 4028 edges (files) and in paper | **PASS** | 961 / 4028 |
| 9 | H961: parent-graph mapping | **PASS** | max diff 4.8e-31 |
| 10 | H961: all listed edges have length 1 (numerical, 30 digits) | **PASS** | 8.5e-31 |
| 11 | H961: no missing unit edges | **PASS** | min non-edge gap 4.186e-04 |
| 12 | H961: valid 5-colouring | **PASS** |  |
| 13 | H961: criticality certificates (961) valid | **PASS** |  |
| 14 | H961: no Moser spindle | **PASS** | 0 |
| 15 | paper non-edge margins 2.2e-3 / 4.1e-4 match | **PASS** |  |
| 16 | H231: exact sphere identities (PARI/GP) | **PASS** |  |
| 17 | H231: exact unit-edge identities (PARI/GP) | **PASS** |  |
| 18 | H231: exact identities from radical files (independent checker) | **PASS** |  |
| 19 | H231: DRAT proof verified by drat-trim | **PASS** |  |
| 20 | H231: CaDiCaL/Glucose/MiniSat + binary encoding all UNSAT | **PASS** |  |
| 21 | H961: exact sphere identities (PARI/GP) | **PASS** |  |
| 22 | H961: exact unit-edge identities (PARI/GP) | **PASS** |  |
| 23 | H961: exact identities from radical files (independent checker) | **PASS** |  |
| 24 | H961: DRAT proof verified by drat-trim | **PASS** |  |
| 25 | H961: CaDiCaL/Glucose/MiniSat + binary encoding all UNSAT | **PASS** |  |
| 26 | H231: SAT-free DSATUR search finds no 4-colouring (~7e6 nodes) | **PASS** | 6997499 |
| 27 | G372: 372 vertices / 1710 edges, as in paper | **PASS** |  |
| 28 | G372: min distance between vertices 0.049 (paper) | **PASS** | 0.0493 |
| 29 | G972: 972 vertices / 4110 edges, as in paper | **PASS** |  |
| 30 | G972: min distance between vertices 0.009 (paper) | **PASS** | 0.0090 |
| 31 | H231 colour-class sizes 55,51,49,46,30 | **PASS** | [55, 51, 49, 46, 30] |
| 32 | H231 composition 12+99+60+60 | **PASS** | [12, 99, 60, 60] |
| 33 | H961 = G972 minus 11 vertices; composition 12+8x120-11 | **PASS** |  |
| 34 | H231 degrees 4--25, average 8.12 | **PASS** |  |
| 35 | H961 degrees 5--65, average 8.38 | **PASS** |  |
| 36 | 38% fewer vertices than G372 | **PASS** |  |
| 37 | 16 greedy runs on G372, sizes 235..337 | **PASS** | [235, 249, 252, 253, 261, 264, 265, 268, 272, 272, 280, 318, 323, 324, 330, 337] |
| 38 | local search result ils_8.json is H231 | **PASS** |  |
| 39 | G972 triage: 968 vertices, 931 essential, 34 removable, 3 untested | **PASS** | 968, 931, 34, 3 |
| 40 | G972: greedy joint removal 963, local search 961 = H961 | **PASS** |  |
| 41 | Table 2: the 11 deleted vertices of G972 (labels, orbits) | **PASS** |  |
| 42 | Supplementary Appendix S1: 231 vertices in radicals, parent indices and colours match the data files | **PASS** |  |
| 43 | all file names referenced in the manuscript exist | **PASS** | H231_4col.cnf, H231_4col.drat.xz, H231_5colouring.txt, H231_criticality_certificates.txt, H231_exact_coordinates.m, H231_vertices.txt, H961_5colouring.txt, H961_criticality_certificates.txt, H961_exact_coordinates.m, H961_vertices.txt, construction/build_G972.py, verification/crosscheck_solvers.py, verify_all.sh |

43 of 43 checks passed.
