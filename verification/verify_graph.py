"""Combinatorial and numerical checks of H231 / H961 that do not rely on any SAT solver.

Checks
  counts       number of vertices and edges
  parent       every vertex coincides with the vertex of the parent graph with the stated parent index
  sphere       every vertex lies on the sphere (numerically, 30 digits; exact check: check_exact_radicals.py)
  edges        every listed edge has length 1 and every pair at distance 1 is listed (no missing unit edge);
               reports the smallest gap | |p-q| - 1 | over non-adjacent pairs
  colouring    the 5-colouring is proper
  critical     each certificate line "v colours" is a proper 4-colouring of G - v, for every vertex v
  spindle      the graph contains no Moser spindle (two rhombi with a common apex and adjacent tips)

usage: python verify_graph.py H231|H961   (run from the repository root)
"""
import collections
import json
import sys

import mpmath as mp

mp.mp.dps = 40
SPEC = {
    'H231': dict(n=231, m=938, parent='construction/G372_vertices.txt', r2=(5 + mp.sqrt(5)) / 8),
    'H961': dict(n=961, m=4028, parent='construction/G972_vertices.txt', r2=(5 - mp.sqrt(5)) / 8),
}


def rows(path):
    return [line.split() for line in open(path) if line.strip() and not line.startswith('#')]


def moser_spindles(n, adj):
    count = 0
    for a in range(n):
        tips = collections.defaultdict(list)
        for b in adj[a]:
            for c in adj[b] & adj[a]:
                if c > b:
                    for t in (adj[b] & adj[c]) - {a}:
                        tips[t].append((b, c))
        ts = list(tips)
        for i in range(len(ts)):
            for j in range(i + 1, len(ts)):
                if ts[j] in adj[ts[i]]:
                    count += sum(1 for p in tips[ts[i]] for q in tips[ts[j]] if len({a, *p, ts[i], *q, ts[j]}) == 7)
    return count


def main():
    name = sys.argv[1]
    spec = SPEC[name]
    verts = rows(f'{name}/{name}_vertices.txt')
    pts = [[mp.mpf(t) for t in r[2:5]] for r in verts]
    parent_idx = [int(r[1]) for r in verts]
    edges = [tuple(map(int, r)) for r in rows(f'{name}/{name}_edges.txt')]
    n, m = len(pts), len(edges)
    adj = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    res = {'graph': name, 'vertices': n, 'edges': m, 'counts_ok': (n, m) == (spec['n'], spec['m'])}

    parent = {int(r[0]): [mp.mpf(t) for t in r[1:4]] for r in rows(spec['parent'])}
    res['parent_indices_distinct'] = len(set(parent_idx)) == n
    res['parent_max_coordinate_difference'] = float(max(abs(parent[i][k] - p[k]) for i, p in zip(parent_idx, pts) for k in range(3)))
    res['parent_ok'] = res['parent_indices_distinct'] and res['parent_max_coordinate_difference'] < 1e-28

    res['sphere_max_deviation'] = float(max(abs(sum(t * t for t in p) - spec['r2']) for p in pts))
    gap, max_edge_err, missing = mp.mpf(1), mp.mpf(0), 0
    for i in range(n):
        for j in range(i + 1, n):
            dev = abs(mp.sqrt(sum((pts[i][k] - pts[j][k]) ** 2 for k in range(3))) - 1)
            if j in adj[i]:
                max_edge_err = max(max_edge_err, dev)
            else:
                gap = min(gap, dev)
                missing += dev < mp.mpf(10) ** -20
    res['edge_length_max_deviation'] = float(max_edge_err)
    res['nonedge_min_gap'] = float(gap)
    res['missing_unit_edges'] = missing
    res['edges_ok'] = max_edge_err < 1e-25 and missing == 0

    col = {int(r[0]): int(r[1]) for r in rows(f'{name}/{name}_5colouring.txt')}
    res['five_colouring_ok'] = len(col) == n and set(col.values()) <= {1, 2, 3, 4, 5} and all(col[u] != col[v] for u, v in edges)

    cert = {int(r[0]): r[1] for r in rows(f'{name}/{name}_criticality_certificates.txt')}
    ok = len(cert) == n
    for v, s in cert.items():
        ok &= len(s) == n and s[v] == '-' and all(s[x] in '0123' for x in range(n) if x != v)
        ok &= all(s[a] != s[b] for a, b in edges if v not in (a, b))
    res['criticality_certificates_ok'] = bool(ok)

    res['moser_spindles'] = moser_spindles(n, adj)
    res['all_ok'] = all([res['counts_ok'], res['parent_ok'], res['sphere_max_deviation'] < 1e-25, res['edges_ok'],
                         res['five_colouring_ok'], res['criticality_certificates_ok'], res['moser_spindles'] == 0])
    print(json.dumps(res, indent=1))
    json.dump(res, open(f'results/verify_graph_{name}.json', 'w'), indent=1)
    sys.exit(0 if res['all_ok'] else 1)


if __name__ == '__main__':
    main()
