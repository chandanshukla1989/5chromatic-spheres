"""Cross-check non-4-colourability with three SAT solvers and two encodings (in addition to the DRAT proof).

Encodings
  direct  : x_{v,c} for 4 colours, at-least-one colour per vertex, conflict clause per edge and colour
  binary  : two Boolean variables per vertex (colour = 2-bit number), one 4-literal clause per edge and colour
In both, the colours of one triangle are fixed (colour symmetry); this preserves satisfiability.

usage: python verification/crosscheck_solvers.py H231|H961   (writes results/crosscheck_<graph>.json)
"""
import json
import sys
import time

from pysat.solvers import Solver


def main():
    name = sys.argv[1]
    edges = [tuple(map(int, l.split())) for l in open(f'{name}/{name}_edges.txt') if l.strip() and not l.startswith('#')]
    n = 1 + max(max(e) for e in edges)
    adj = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    tri = next((u, v, min(adj[u] & adj[v])) for u in range(n) for v in sorted(adj[u]) if v > u and adj[u] & adj[v])
    result = {'graph': name, 'triangle_fixed': tri}

    for solver in ('cd15', 'g4', 'm22'):           # CaDiCaL 1.5.3, Glucose 4, MiniSat 2.2
        t = time.time()
        with Solver(name=solver) as s:
            for v in range(n):
                s.add_clause([4 * v + c + 1 for c in range(4)])
            for u, v in edges:
                for c in range(4):
                    s.add_clause([-(4 * u + c + 1), -(4 * v + c + 1)])
            for c, v in enumerate(tri):
                s.add_clause([4 * v + c + 1])
            result[f'direct/{solver}'] = 'SAT' if s.solve() else 'UNSAT'
        result[f'direct/{solver}/seconds'] = round(time.time() - t, 1)

    t = time.time()
    with Solver(name='cd15') as s:
        for u, v in edges:
            a, b = 2 * u + 1, 2 * v + 1
            for hi in (0, 1):
                for lo in (0, 1):
                    s.add_clause([a if not hi else -a, (a + 1) if not lo else -(a + 1),
                                  b if not hi else -b, (b + 1) if not lo else -(b + 1)])
        for (hi, lo), v in zip(((0, 0), (0, 1), (1, 0)), tri):
            s.add_clause([2 * v + 1 if hi else -(2 * v + 1)])
            s.add_clause([2 * v + 2 if lo else -(2 * v + 2)])
        result['binary/cd15'] = 'SAT' if s.solve() else 'UNSAT'
    result['binary/cd15/seconds'] = round(time.time() - t, 1)
    result['all_unsat'] = all(v == 'UNSAT' for k, v in result.items() if k.count('/') == 1)
    print(json.dumps(result, indent=1))
    json.dump(result, open(f'results/crosscheck_{name}.json', 'w'), indent=1)


if __name__ == '__main__':
    main()
