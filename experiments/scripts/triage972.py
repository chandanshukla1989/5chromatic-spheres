"""Parallel single-vertex triage of a 5-chromatic subgraph S of G972.
For each v in S: is S - v still not 4-colourable?  SAT => v is essential in every subgraph of S (never re-check).
usage: triage972.py START.json NPROC   -> sphere/triage972.json (checkpointed), progress on stdout
"""
import json, os, pickle, sys, time
from multiprocessing import Pool
from pysat.solvers import Solver
K = 4
start, nproc = sys.argv[1], int(sys.argv[2])
g = pickle.load(open('sphere/G972.pkl', 'rb')); n = len(g['pts'])
S = sorted(json.load(open(start))['vertices'])
adj = [set() for _ in range(n)]
for u, v in g['E']: adj[u].add(v); adj[v].add(u)
Ss = set(S)
tri = next((u, v, min(adj[u] & adj[v] & Ss)) for u in S for v in adj[u] & Ss if adj[u] & adj[v] & Ss)
_solver = None


def init():
    global _solver
    var = lambda v, c: 1 + v * K + c; sel0 = n * K + 1
    s = Solver(name='cd15')
    for v in S: s.add_clause([-(sel0 + v)] + [var(v, c) for c in range(K)])
    for u, v in g['E']:
        if u in Ss and v in Ss:
            for c in range(K): s.add_clause([-var(u, c), -var(v, c)])
    _solver = (s, var, sel0)


def test(v):
    s, var, sel0 = _solver
    if v in tri: return v, 'ESSENTIAL(tri)', 0.0
    t = time.time(); s.conf_budget(20_000_000)
    r = s.solve_limited(assumptions=[var(x, i) for i, x in enumerate(tri)] + [sel0 + w for w in S if w != v])
    return v, {True: 'ESSENTIAL', False: 'REMOVABLE', None: 'UNKNOWN'}[r], time.time() - t


if __name__ == '__main__':
    ck = 'sphere/triage972.json'
    res = json.load(open(ck)) if os.path.exists(ck) else {}
    todo = [v for v in S if str(v) not in res]
    t0 = time.time()
    with Pool(nproc, initializer=init) as p:
        for k, (v, r, dt) in enumerate(p.imap_unordered(test, todo)):
            res[str(v)] = [r, round(dt, 1)]
            if k % 25 == 0 or k == len(todo) - 1:
                json.dump(res, open(ck, 'w'))
                c = {x: sum(1 for y in res.values() if y[0].startswith(x)) for x in ('ESSENTIAL', 'REMOVABLE', 'UNKNOWN')}
                print(f'scanned {len(res)}/{len(S)}  {c}  t={time.time()-t0:.0f}s', flush=True)
    json.dump(res, open(ck, 'w'))
    print('TRIAGE DONE', flush=True)
