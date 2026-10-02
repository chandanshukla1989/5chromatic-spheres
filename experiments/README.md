# Experiments

Original search scripts (`scripts/`) and the outputs of the runs that produced H231 and H961, with their
original file times. These are research records and are kept unchanged; the cleaned code used for
verification is in `../construction/` and `../verification/`.

| Folder | Script | What it contains |
|---|---|---|
| `G372_greedy/` | `scripts/hmus.py` | 16 completed runs of random-order vertex deletion on G372 (`<seed>.log`, `<seed>.json`; line `FINAL <size>`). Seed 7 gave 235. |
| `G372_local_search/` | `scripts/ils_sphere.py` | Local search from the 235-vertex graph; `ils_8.log` shows 234 → 233 → 232 → 231, `ils_8.json` = H231. |
| `G972_greedy/` | `scripts/hmus.py`, `scripts/hmus2.py` | Vertex deletion on G972; `start_6.json` (968 vertices) is the starting point of the triage. |
| `G972_triage/` | `scripts/triage972.py`, `scripts/reduce972.py` | Single-vertex triage of the 968-vertex graph (`triage972.json`: 931 essential, 34 removable, 3 untested triangle vertices) and greedy joint removal (`red_8.json`: 963). |
| `G972_local_search/` | `scripts/ils_any.py` | Local search from 963; `ils_103.json` (961) = H961. |

Note: the scripts were run from the original working directory; their relative input paths refer to that
layout.
