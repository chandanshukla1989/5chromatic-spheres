"""Exact check of the nested-radical coordinate files (Mathematica syntax) of H231 / H961.

Uses only the strings in the .m file and its own arithmetic in the tower Q(s5)(sb)(sg) with
s5^2 = 5, sb^2 = beta = b0 + b1*s5, sg^2 = gamma = g0 + g1*s5 + (g2 + g3*s5)*sb  (rationals read from the header).
Checks: every vertex lies on the sphere (|p|^2 = R2 exactly), every listed edge has |p-q|^2 = 1 exactly,
and the expressions agree numerically (50 digits) with an independent coordinate list.
usage: check_exact_m.py FILE.m EDGES.txt R2_rational_part R2_sqrt5_part [numeric_vertices.txt]
"""
import re, sys
from fractions import Fraction as Fr
import mpmath as mp
mp.mp.dps = 60

path, edges_path = sys.argv[1], sys.argv[2]
R2 = {(0, 0, 0): Fr(sys.argv[3]), (1, 0, 0): Fr(sys.argv[4])}
txt = open(path).read()
hdr = txt.split('*)')[0]
SB = re.search(r'sqrt\(beta\) = (Sqrt\[.*?\]\]?)\s*,', hdr).group(1)
SG = re.search(r'sqrt\(gamma\) = (Sqrt\[.*\])\s*$', hdr.strip()).group(1)
q = lambda s: Fr(s.strip('()'))
b0, b1 = [q(v) for v in re.match(r'Sqrt\[(.*?)\+(.*?)\*Sqrt\[5\]\]$', SB).groups()]
inner = SG[len('Sqrt['):-1].replace(SB, 'B')
g0, g1, g2, g3 = [q(v) for v in re.match(r'(.*?)\+(.*?)\*Sqrt\[5\]\+\((.*?)\+(.*?)\*Sqrt\[5\]\)\*B$', inner).groups()]
BETA = {(0, 0, 0): b0, (1, 0, 0): b1}
GAMMA = {(0, 0, 0): g0, (1, 0, 0): g1, (0, 1, 0): g2, (1, 1, 0): g3}


def add(a, b, s=1):
    r = dict(a)
    for k, v in b.items(): r[k] = r.get(k, 0) + s * v
    return {k: v for k, v in r.items() if v}


def mul(a, b):
    r = {}
    for (i, j, k), u in a.items():
        for (l, m, n), v in b.items():
            term = {(0, 0, 0): u * v}
            e5, eb, eg = i + l, j + m, k + n
            if e5 == 2: term = {(0, 0, 0): u * v * 5}; e5 = 0
            if eg == 2: term = mul(term, GAMMA); eg = 0
            if eb == 2: term = mul(term, BETA); eb = 0
            # shift remaining single factors
            shifted = {}
            for (x, y, z), c in term.items():
                key, coef = [x + e5, y + eb, z + eg], c
                if key[0] == 2: key[0] = 0; coef *= 5
                if key[1] == 2:
                    sub = mul({(key[0], 0, key[2]): coef}, BETA)
                    for kk, vv in sub.items(): shifted[kk] = shifted.get(kk, 0) + vv
                    continue
                shifted[tuple(key)] = shifted.get(tuple(key), 0) + coef
            r = add(r, shifted)
    return r


def parse(expr):
    e = expr.replace(SG, 'G').replace(SB, 'B').replace(' ', '')
    if e == '0': return {}
    out = {}
    for term in re.split(r'\+(?=\()|\+(?=\d)', e):
        m = re.match(r'^\(?(-?\d+(?:/\d+)?)\)?((?:\*(?:Sqrt\[5\]|B|G))*)$', term)
        if not m: raise ValueError('cannot parse term: ' + term)
        c = Fr(m.group(1)); fac = m.group(2)
        key = (int('Sqrt[5]' in fac), int('*B' in fac), int('*G' in fac))
        out[key] = out.get(key, 0) + c
    return out


vals = {'s5': mp.sqrt(5)}
vals['sb'] = mp.sqrt(b0 + b1 * vals['s5'])
vals['sg'] = mp.sqrt(g0 + g1 * vals['s5'] + (g2 + g3 * vals['s5']) * vals['sb'])
num = lambda a: sum(mp.mpf(c.numerator) / c.denominator * vals['s5'] ** i * vals['sb'] ** j * vals['sg'] ** k for (i, j, k), c in a.items())

body = txt.split('= {', 1)[1].rsplit('};', 1)[0]
rows = [r.strip().rstrip(',') for r in body.strip().split('\n') if r.strip()]
pts = []
for r in rows:
    r = r[1:-1]
    parts, depth, cur = [], 0, ''
    for ch in r:
        if ch == '[': depth += 1
        if ch == ']': depth -= 1
        if ch == ',' and depth == 0: parts.append(cur); cur = ''
        else: cur += ch
    parts.append(cur)
    pts.append([parse(p) for p in parts])
E = [tuple(map(int, l.split())) for l in open(edges_path) if l.strip() and not l.startswith('#')]
on_sphere = all(add(add(mul(p[0], p[0]), mul(p[1], p[1])), mul(p[2], p[2])) == R2 for p in pts)
bad = 0
for u, v in E:
    d = [add(pts[u][i], pts[v][i], -1) for i in range(3)]
    if add(add(mul(d[0], d[0]), mul(d[1], d[1])), mul(d[2], d[2])) != {(0, 0, 0): Fr(1)}: bad += 1
print(f'{path}: {len(pts)} vertices; all exactly on sphere: {on_sphere}; edges checked exactly: {len(E)}; failures: {bad}')
if len(sys.argv) > 5:
    ref = [list(map(mp.mpf, l.split()[2:5])) for l in open(sys.argv[5]) if l.strip() and not l.startswith('#')]
    err = max(abs(num(pts[i][k]) - ref[i][k]) for i in range(len(pts)) for k in range(3))
    print(f'  max |exact expression - reference coordinate| = {mp.nstr(err, 3)}')
