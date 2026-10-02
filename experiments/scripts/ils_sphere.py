"""Iterated local search below the best 5-chromatic subgraph of G372.
Each round: S -> S + R (R = random vertices of G372 \\ S with >= d neighbours in S) [- a few random kicks]
-> randomized vertex-MUS reduction (pysat, triangle symmetry breaking) -> accept if not larger.
usage: ils_sphere.py SEED START.json OUTDIR
"""
import json, os, pickle, random, sys, time
from pysat.solvers import Solver
K = 4
seed, start, outdir = int(sys.argv[1]), sys.argv[2], sys.argv[3]
rng = random.Random(seed)
g = pickle.load(open('sphere/G372.pkl', 'rb')); n = len(g['pts'])
adj = [set() for _ in range(n)]
for u, v in g['E']: adj[u].add(v); adj[v].add(u)
var = lambda v, c: 1 + v * K + c; sel0 = n * K + 1
s = Solver(name='cd15')
for v in range(n): s.add_clause([-(sel0 + v)] + [var(v, c) for c in range(K)])
for u, v in g['E']:
    for c in range(K): s.add_clause([-var(u, c), -var(v, c)])


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


def unsat(T, tri):
    s.conf_budget(2_000_000)
    r = s.solve_limited(assumptions=[sel0 + v for v in T] + [var(t, i) for i, t in enumerate(tri)])
    return (True, {l - sel0 for l in s.get_core() if l >= sel0}) if r is False else (False, None)


def reduce(T):
    T = core4(T)
    tris = [(u, v, w) for u in T for v in adj[u] & T if v > u for w in adj[u] & adj[v] & T if w > v]
    tri = rng.choice(tris); fixed = set(tri)
    ok, core = unsat(T, tri)
    if not ok: return None
    T = core4(core | fixed); crit = set(fixed)
    while True:
        c = [v for v in T if v not in crit]
        if not c: return T
        v = rng.choice(c); U = core4(T - {v})
        if not fixed <= U: crit.add(v); continue
        ok, core = unsat(U, tri)
        if ok: T = core4(core | fixed); crit &= T
        else: crit.add(v)


S = set(json.load(open(start))['vertices']); best = len(S); t0 = time.time(); it = 0
out = os.path.join(outdir, f'ils_{seed}.json')
while True:
    it += 1
    cnt = {}
    for v in S:
        for w in adj[v]:
            if w not in S: cnt[w] = cnt.get(w, 0) + 1
    d = rng.choice([2, 3, 4])
    fr = [w for w, c in cnt.items() if c >= d]
    R = set(rng.sample(fr, min(rng.choice([5, 10, 20, 40]), len(fr))))
    kick = set(rng.sample(sorted(S), rng.choice([0, 0, 3, 8])))
    T = reduce((S - kick) | R) or reduce(S | R)
    if T is None: continue
    if len(T) <= len(S):
        S = T
        if len(S) < best:
            best = len(S)
            json.dump({'size': best, 'vertices': sorted(S)}, open(out, 'w'))
            print(f'[{seed}] *** NEW BEST {best} *** it={it} t={time.time()-t0:.0f}s', flush=True)
    if it % 10 == 0:
        print(f'[{seed}] it={it} cur={len(S)} best={best} t={time.time()-t0:.0f}s', flush=True)
