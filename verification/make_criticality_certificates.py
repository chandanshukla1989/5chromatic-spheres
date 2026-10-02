"""Write vertex-criticality certificates for a graph.

For every vertex v, a proper 4-colouring of G - v is computed with a SAT solver and stored as one line
    v <colours>
where <colours> is a string over {0,1,2,3,-} giving the colour of each vertex ('-' for v itself).
The certificates are checked independently by verify_graph.py.

usage: python make_criticality_certificates.py EDGES.txt OUT.txt [processes]
"""
import sys
from multiprocessing import Pool

from pysat.solvers import Solver

K = 4


def read_edges(path):
    edges = [tuple(map(int, line.split())) for line in open(path) if line.strip() and not line.startswith('#')]
    return edges, 1 + max(max(e) for e in edges)


def colouring_without(args):
    v, edges, n = args
    var = lambda x, c: 1 + x * K + c
    with Solver(name='cd15') as s:
        for x in range(n):
            if x != v:
                s.add_clause([var(x, c) for c in range(K)])
        for a, b in edges:
            if v not in (a, b):
                for c in range(K):
                    s.add_clause([-var(a, c), -var(b, c)])
        if not s.solve():
            return v, None
        model = set(l for l in s.get_model() if l > 0)
    return v, ''.join('-' if x == v else str(next(c for c in range(K) if var(x, c) in model)) for x in range(n))


def main():
    edges_path, out_path = sys.argv[1], sys.argv[2]
    procs = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    edges, n = read_edges(edges_path)
    with Pool(procs) as pool:
        results = dict(pool.imap_unordered(colouring_without, [(v, edges, n) for v in range(n)], chunksize=4))
    missing = [v for v in range(n) if results[v] is None]
    if missing:
        sys.exit(f'not vertex-critical: G - v is not 4-colourable for v in {missing}')
    with open(out_path, 'w') as f:
        f.write(f'# vertex-criticality certificates: for each vertex v, a proper 4-colouring of G - v ({n} lines)\n')
        for v in range(n):
            f.write(f'{v} {results[v]}\n')
    print(f'{out_path}: {n} certificates written')


if __name__ == '__main__':
    main()
