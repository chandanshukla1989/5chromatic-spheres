# Smaller 5-chromatic unit-distance graphs on two icosahedral spheres

Data, proofs and code for the paper by **Chandan Kumar Shukla** (Independent Researcher, India).

| Graph | Sphere | Vertices | Edges | Parent graph | Properties |
|---|---|---|---|---|---|
| **H231** | S²(r₁), r₁ = cos(π/10) | 231 | 938 | G372 (372 vertices) | χ = 5, vertex-critical, no Moser spindle |
| **H961** | S²(r₂), r₂ = cos(3π/10) | 961 | 4028 | G972 (972 vertices) | χ = 5, vertex-critical, no Moser spindle |

G372 and G972 are the graphs of V. Voronov, A. Neopryatnaya, E. Dergachev, *Discrete Mathematics* 345 (2022) 113106.
H231 is the smallest graph found by our search; it is **not** claimed to be a minimum.

## Verify everything (one command)

```sh
pip install -r requirements.txt          # python-sat, mpmath, numpy
# needs: PARI/GP >= 2.15, a C compiler, xz, drat-trim (https://github.com/marijnheule/drat-trim)
DRAT_TRIM=/path/to/drat-trim ./verify_all.sh
```
Every check prints its result and writes a log to `results/`. Expected output: see [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md).

## Where each claim of the paper is checked

| Claim in the paper | Data | Check (command) | Log |
|---|---|---|---|
| 231 vertices / 938 edges; 961 / 4028 | `H*/H*_vertices.txt`, `H*/H*_edges.txt` | `python verification/verify_graph.py H231` (and `H961`) | `results/verify_graph_*.json` |
| H231 ⊂ G372, H961 ⊂ G972 (parent indices) | `H*/H*_vertices.txt` col. 2, `construction/G*_vertices.txt` | `python construction/build_G372.py`, `build_G972.py`, then `verify_graph.py` | same |
| every vertex exactly on the sphere, every edge exactly of length 1 | `H*/H*_exact_coordinates.m` | `verification/verify_exact.sh` (PARI/GP + independent Python) | `results/exact_*.log` |
| no unit distance missing (non-edge margins 2.2·10⁻³, 4.1·10⁻⁴) | `H*/H*_vertices.txt` | `verify_graph.py` | `results/verify_graph_*.json` |
| not 4-colourable (DRAT) | `H*/H*_4col.cnf`, `H*/H*_4col.drat.xz` | `verification/verify_drat.sh` | `results/drat-trim_*.log`, `H*/H*_drat-trim.log` |
| not 4-colourable (CaDiCaL, Glucose, MiniSat; two encodings) | `H*/H*_edges.txt` | `python verification/crosscheck_solvers.py H231` (and `H961`) | `results/crosscheck_*.json` |
| not 4-colourable (no SAT solver, H231) | `H231/H231_edges.txt` | `verification/verify_dsatur.sh` | `results/dsatur_H231.log` |
| a proper 5-colouring exists | `H*/H*_5colouring.txt` | `verify_graph.py` | `results/verify_graph_*.json` |
| vertex-critical (a 4-colouring of G − v for every v) | `H*/H*_criticality_certificates.txt` | `verify_graph.py` | `results/verify_graph_*.json` |
| no Moser spindle | `H*/H*_edges.txt` | `verify_graph.py` | `results/verify_graph_*.json` |
| exact coordinates in radicals (human-readable) | `paper/Supplementary_Material.pdf`, App. A–B | `verification/check_exact_radicals.py` | `results/exact_radicals_*.log` |
| 16 greedy runs (235–337), local search 235 → 231, G972 triage 968 → 963 → 961 | `experiments/` | logs, see `experiments/README.md` | `experiments/*/` |

## Layout

```
paper/         manuscript (LaTeX, figures, PDF) and Supplementary_Material (LaTeX, PDF, generator)
H231/, H961/   final graphs: vertices, edges, exact coordinates (.m, .py), 5-colouring,
               criticality certificates, CNF + DRAT proof, drat-trim log
construction/  rebuild the parent graphs G372 and G972 from the published minimal polynomials
verification/  all verification code (PARI/GP, Python, C) and shell drivers
experiments/   original search scripts and the logs/outputs of the runs that produced the graphs
results/       output of the verification runs
```

## Citation, licence, AI use
See [`CITATION.cff`](CITATION.cff); code is MIT-licensed ([`LICENSE`](LICENSE)), data CC BY 4.0 ([`LICENSE-DATA.md`](LICENSE-DATA.md)).
Use of AI tools is described in [`AI_USE.md`](AI_USE.md); how the result was obtained in [`RESEARCH_PROGRESSION.md`](RESEARCH_PROGRESSION.md).
