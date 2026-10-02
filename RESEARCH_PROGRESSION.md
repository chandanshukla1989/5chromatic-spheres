# Research progression

This document records how the graphs H231 and H961 were obtained. Times are taken from the
modification times of the retained files in `experiments/` (IST, UTC+05:30).

## Background

- Since December 2023 the author has worked on computational aspects of the Hadwiger–Nelson problem.
- In February 2024 the author corresponded with A. de Grey about a candidate construction. The main lesson
  of that exchange — vertices must be represented exactly (algebraically), and chromatic numbers must be
  checked rigorously rather than with floating-point distances or heuristic colouring — determined the
  verification standard adopted in this work (exact radical coordinates, certificate-based proofs).
- The author reports that the idea of revisiting small published constructions was developed from
  mid-September 2026.

## 2 October 2026 — computations

1. Several directions were explored first (plane constructions around the 509-vertex record, the
   heptagonal Moser-spindle-free construction of arXiv:2608.04542, other number fields). They did not
   produce a result and are not part of this repository.
2. Literature check of records for unit-distance graphs on spheres. The paper of Voronov, Neopryatnaya
   and Dergachev states that G372 stays 5-chromatic after deleting any single vertex and gives no
   minimal subgraphs; it was chosen as the target.
3. G372 and G972 were rebuilt from the published data and the authors' notebooks (counts 372/1710 and
   972/4110 reproduced).
4. **G372, greedy vertex deletion** (`experiments/G372_greedy/`, first runs finished at 19:54–19:55):
   16 completed runs with different random deletion orders gave non-4-colourable subgraphs of sizes
   235, 249, 252, 253, 261, 264, 265, 268, 272, 272, 280, 318, 323, 324, 330, 337 (seed 7: 235).
5. **G372, local search** (`experiments/G372_local_search/`, from the 235-vertex graph): seed 8 found
   234, 233, 232 and 231 (`ils_8.log`); `ils_8.json` (20:55) is identical to H231.
6. **G972, greedy deletion** (`experiments/G972_greedy/`): best 968 (`start_6.json`, 20:52).
7. **G972, triage** (`experiments/G972_triage/`, finished 21:13): of the 968 vertices, 931 were shown
   to be individually essential, 34 individually removable, and the 3 vertices of the triangle fixed for
   symmetry breaking were not tested; greedy joint removal gave 963
   (`red_8.json`, 21:19).
8. **G972, local search** (`experiments/G972_local_search/`): 961 (`ils_103.json`, 21:54) = H961.

## 2–3 October 2026 — verification and writing

- Exact verification in a degree-8 number field (PARI/GP), DRAT proofs (Kissat, checked with drat-trim),
  cross-checks with three further SAT solvers and an alternative encoding, a SAT-free DSATUR search for
  H231, exact radical coordinates with an independent checker, criticality certificates, Moser-spindle
  search.
- Manuscript and supplementary material.

A SAT-free search for H961, split into the 10 colourings of the 12 great-icosahedron vertices, was started
but had not finished at the time of writing; the paper makes no claim based on it.
