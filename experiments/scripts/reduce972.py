"""Greedy joint removal over the triage's individually-removable vertices (random order per seed)."""
import json, pickle, random, sys, time
from pysat.solvers import Solver
K = 4; seed = int(sys.argv[1]); rng = random.Random(seed)
g = pickle.load(open('sphere/G972.pkl', 'rb')); n = len(g['pts'])
S = set(json.load(open('sphere/runs972/start_6.json'))['vertices'])
tri_res = json.load(open('sphere/triage972.json'))
cand = [int(v) for v, r in tri_res.items() if r[0] == 'REMOVABLE']
adj = [set() for _ in range(n)]
for u, v in g['E']: adj[u].add(v); adj[v].add(u)
tri = next((u, v, min(adj[u] & adj[v] & S)) for u in sorted(S) for v in adj[u] & S if adj[u] & adj[v] & S)
var = lambda v, c: 1 + v * K + c; sel0 = n * K + 1
s = Solver(name='cd15')
for v in S: s.add_clause([-(sel0 + v)] + [var(v, c) for c in range(K)])
for u, v in g['E']:
    if u in S and v in S:
        for c in range(K): s.add_clause([-var(u, c), -var(v, c)])
rng.shuffle(cand); t0 = time.time()
for v in cand:
    if v in tri or v not in S: continue
    s.conf_budget(20_000_000)
    r = s.solve_limited(assumptions=[var(x, i) for i, x in enumerate(tri)] + [sel0 + w for w in S if w != v])
    if r is False: S.discard(v)
print(f'[{seed}] candidates {len(cand)} -> size {len(S)} ({time.time()-t0:.0f}s)', flush=True)
json.dump({'size': len(S), 'vertices': sorted(S)}, open(f'sphere/runs972/red_{seed}.json', 'w'))
