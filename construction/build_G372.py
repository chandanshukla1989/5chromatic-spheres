"""Rebuild G372 (Voronov, Neopryatnaya, Dergachev 2022) on the sphere of radius r1 = cos(pi/10).

Vertices: the 12 vertices of the unit-edge icosahedron and the orbits of three points v1, v2, v3 under the
full icosahedral group (order 120). Twice each coordinate of v_i is the root, closest to the published
value, of the minimal polynomial listed below. Output: G372_vertices.txt (index, x, y, z; 60 digits) and
G372_edges.txt (all pairs at distance 1, decided numerically with a 1e-9 tolerance; exact checks are in
verification/).

Vertex order (used as "parent index" throughout): icosahedron (0-11), orbit of v1 (12-131),
orbit of v2 (132-251), orbit of v3 (252-371).
"""
import os

import mpmath as mp
import numpy as np

mp.mp.dps = 60
HERE = os.path.dirname(os.path.abspath(__file__))
TAU = (1 + mp.sqrt(5)) / 2

# (coefficients low -> high of the minimal polynomial of 2*coordinate, published value)
REPRESENTATIVES = [
    [([-1, -1, 2, -2, 1], 0.71584), ([-1, 2, -2, 1, 1], 0.34924), ([-19, 0, 20, 0, 2, 0, -5, 0, 1], 0.51972)],
    [([1, 8, 9, -7, 28, 6, -4, -1, 1], -0.07961), ([-1, -5, 5, -4, 9, -5, 1, -2, 1], -0.08345),
     ([-1, 7, -13, -24, 4, 10, 0, -3, 1], 0.94404)],
    [([1, 8, 9, -7, 28, 6, -4, -1, 1], -0.17646), ([-1, -5, 5, -4, 9, -5, 1, -2, 1], 0.79929),
     ([-1, -7, -13, 24, 4, -10, 0, 3, 1], 0.48426)],
]
GENERATORS = [
    [[-1, 0, 0], [0, -1, 0], [0, 0, 1]],
    [[0, 0, 1], [1, 0, 0], [0, 1, 0]],
    [[1 / 2, -TAU / 2, 1 / (2 * TAU)], [TAU / 2, 1 / (2 * TAU), -1 / 2], [1 / (2 * TAU), 1 / 2, TAU / 2]],
    [[1, 0, 0], [0, -1, 0], [0, 0, 1]],
]


def real_root(coeffs, approx):
    roots = mp.polyroots(list(reversed(coeffs)), maxsteps=200, extraprec=200)
    real = [mp.re(r) for r in roots if abs(mp.im(r)) < mp.mpf(10) ** -40]
    return min(real, key=lambda r: abs(r - 2 * approx)) / 2


def key(v):
    return tuple(int(round(float(t) * 1e9)) for t in v)


def group(generators):
    gens = [mp.matrix(g) for g in generators]
    elements = {key(mp.eye(3)): mp.eye(3)}
    frontier = [mp.eye(3)]
    while frontier:
        new = []
        for m in frontier:
            for g in gens:
                p = g * m
                if key(p) not in elements:
                    elements[key(p)] = p
                    new.append(p)
        frontier = new
    return list(elements.values())


def orbit(point, elements):
    seen = {}
    for m in elements:
        w = m * mp.matrix(point)
        seen.setdefault(key(w), [w[0], w[1], w[2]])
    return list(seen.values())


def unit_edges(points):
    x = np.array([[float(t) for t in p] for p in points])
    d = np.sqrt(((x[:, None] - x[None]) ** 2).sum(-1))
    i, j = np.where(np.triu(np.abs(d - 1) < 1e-9, 1))
    return list(zip(i.tolist(), j.tolist()))


def main():
    elements = group(GENERATORS)
    assert len(elements) == 120
    reps = [[real_root(c, a) for c, a in rep] for rep in REPRESENTATIVES]
    points = orbit([TAU / 2, mp.mpf(1) / 2, 0], elements)
    for r in reps:
        points += orbit(r, elements)
    assert len(points) == 372 and len({key(p) for p in points}) == 372
    edges = unit_edges(points)
    with open(os.path.join(HERE, 'G372_vertices.txt'), 'w') as f:
        f.write('# G372: index x y z (60 significant digits); radius cos(pi/10)\n')
        for i, p in enumerate(points):
            f.write(f'{i} ' + ' '.join(mp.nstr(t, 60) for t in p) + '\n')
    with open(os.path.join(HERE, 'G372_edges.txt'), 'w') as f:
        f.write(f'# G372: {len(edges)} unit-distance edges\n')
        f.writelines(f'{u} {v}\n' for u, v in edges)
    print(f'G372: {len(points)} vertices, {len(edges)} edges')


if __name__ == '__main__':
    main()
