"""Randomized vertex-MUS for a graph pickle {'pts','E'} (complex points ok). Checkpoints OUT/<seed>.json."""
import json, os, pickle, random, sys, time
from pysat.solvers import Solver
K = 4
gpath, seed, outdir = sys.argv[1], int(sys.argv[2]), sys.argv[3]
start = sys.argv[4] if len(sys.argv) > 4 else None
rng = random.Random(seed)
g = pickle.load(open(gpath, 'rb')); n = len(g['pts']); E = g['E']
adj = [set() for _ in range(n)]
for u, v in E: adj[u].add(v); adj[v].add(u)
S = set(json.load(open(start))['vertices']) if start else set(range(n))
def core4(S):
    S = set(S); deg = {v: len(adj[v] & S) for v in S}; st = [v for v in S if deg[v] < 4]
    while st:
        v = st.pop()
        if v not in S: continue
        S.discard(v)
        for w in adj[v]:
            if w in S:
                deg[w] -= 1
                if deg[w] == 3: st.append(w)
    return S
var = lambda v, c: 1 + v * K + c; sel0 = n * K + 1
s = Solver(name='m22')
for v in range(n): s.add_clause([-(sel0 + v)] + [var(v, c) for c in range(K)])
for u, v in E:
    for c in range(K): s.add_clause([-var(u, c), -var(v, c)])
S = core4(S)
tris = [(u, v, min(adj[u] & adj[v] & S)) for u in S for v in adj[u] & S if v > u and adj[u] & adj[v] & S]
tri = rng.choice(tris); fixed = set(tri)
def unsat(T):
    s.conf_budget(int(os.environ.get('BUDGET', '3000000')))
    r = s.solve_limited(assumptions=[sel0 + v for v in T | fixed] + [var(t, i) for i, t in enumerate(tri)])
    if r is False: return True, {l - sel0 for l in s.get_core() if l >= sel0}
    return False, None
def save(S, done):
    f = os.path.join(outdir, f'{seed}.json')
    json.dump({'seed': seed, 'size': len(S), 'done': done, 'vertices': sorted(S), 'graph': gpath}, open(f + '.tmp', 'w')); os.replace(f + '.tmp', f)
t0 = time.time()
ok, core = unsat(S); assert ok, 'colourable?'
S = core4(core | fixed); crit = set(fixed); save(S, False)
print(f'[{seed}] start {len(S)} {time.time()-t0:.0f}s', flush=True)
mode = ['rand', 'lowdeg', 'highdeg'][seed % 3]
while True:
    c = [v for v in S if v not in crit]
    if not c: break
    if mode == 'rand': v = rng.choice(c)
    elif mode == 'lowdeg': v = min(c, key=lambda v: len(adj[v] & S) + rng.random() * 3)
    else: v = max(c, key=lambda v: len(adj[v] & S) + rng.random() * 3)
    T = core4(S - {v})
    if not fixed <= T: crit.add(v); continue
    ok, core = unsat(T)
    if ok:
        S = core4(core | fixed); crit &= S; save(S, False)
        print(f'[{seed}] -> {len(S)} crit={len(crit)} {time.time()-t0:.0f}s', flush=True)
    else: crit.add(v)
save(S, True); print(f'[{seed}] FINAL {len(S)} {time.time()-t0:.0f}s', flush=True)
