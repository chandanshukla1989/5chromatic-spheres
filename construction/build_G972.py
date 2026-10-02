"""Rebuild G972 (Voronov, Neopryatnaya, Dergachev 2022) on the sphere of radius r2 = cos(3*pi/10).

Vertices: the 12 vertices of the unit-edge great icosahedron and the orbits of eight points w1..w8 under
the group G' of order 120 generated, as in the authors' notebook (github.com/vsvor/dist-graphs,
checkGraph972.nb), by g1, g2, M g3 M, g4, where g1..g4 are the generators used for G372 and M swaps the
y and z axes. Each coordinate of w_i is
sign * Root(p, k) / 2 in Mathematica's convention (k-th smallest real root of p). The second coordinate of
w8 is (1 - sqrt(6 - 3 sqrt5 + 2 sqrt((17 sqrt5 - 37)/2))) / 4; for indexing we use its mirror image
(x8, -y8, z8), which lies in the same G'-orbit because the reflection y -> -y belongs to G'.

Output: G972_vertices.txt (index, x, y, z; 60 digits) and G972_edges.txt.
Vertex order ("parent index"): orbits of w1..w8 (0-959, 120 each), great icosahedron (960-971).
"""
import os

import mpmath as mp
import numpy as np

mp.mp.dps = 60
HERE = os.path.dirname(os.path.abspath(__file__))
TAU = (1 + mp.sqrt(5)) / 2
SQRT5 = mp.sqrt(5)

# (coefficients low -> high, root index k, sign); None = given in closed form (w8, y)
REPRESENTATIVES = [
    [([-49, -147, -71, 67, 129, 97, 42, 10, 1], 2, 1), ([-19, 57, 206, 117, -11, -23, 1, 2, 1], 1, 1), ([25, 150, 315, 370, 284, 145, 49, 10, 1], 2, 1)],
    [([-49, -147, -71, 67, 129, 97, 42, 10, 1], 1, 1), ([-19, 57, 206, 117, -11, -23, 1, 2, 1], 2, 1), ([25, 150, 315, 370, 284, 145, 49, 10, 1], 1, -1)],
    [([1, 1, -16, -21, 34, 156, 234, 159, 41], 1, 1), ([-1, -15, -55, -121, 269, 690, 616, 257, 41], 1, 1), ([-41, -211, -231, -148, -13, 75, 223, 174, 41], 1, 1)],
    [([1, 1, -16, -21, 34, 156, 234, 159, 41], 2, 1), ([-1, -15, -55, -121, 269, 690, 616, 257, 41], 2, -1), ([-41, -211, -231, -148, -13, 75, 223, 174, 41], 2, -1)],
    [([-1, 5, 10, 8, 69, 205, 269, 169, 41], 2, 1), ([1, -13, 61, -138, 164, -118, 96, -93, 41], 2, 1), ([269, -232, -669, 471, 642, -335, -258, 72, 41], 2, 1)],
    [([-1, 5, 10, 8, 69, 205, 269, 169, 41], 1, 1), ([1, -13, 61, -138, 164, -118, 96, -93, 41], 1, 1), ([269, 232, -669, -471, 642, 335, -258, -72, 41], 2, 1)],
    [([-1, 4, -2, -12, -1, 15, 15, 6, 1], 1, 1), ([-1, 10, -5, 18, 19, -15, -1, -1, 1], 2, 1), ([1, -14, 36, 29, 13, 17, 19, 7, 1], 1, 1)],
    [([-1, -1, -2, 4, 14, 15, 13, 6, 1], 1, 1), None, ([-41, -37, 108, 45, -42, -11, 4, 2, 1], 2, 1)],
]
MIRROR = [[1, 0, 0], [0, 0, 1], [0, 1, 0]]
G_GENERATORS = [
    [[-1, 0, 0], [0, -1, 0], [0, 0, 1]],
    [[0, 0, 1], [1, 0, 0], [0, 1, 0]],
    [[1 / 2, -TAU / 2, 1 / (2 * TAU)], [TAU / 2, 1 / (2 * TAU), -1 / 2], [1 / (2 * TAU), 1 / 2, TAU / 2]],
    [[1, 0, 0], [0, -1, 0], [0, 0, 1]],
]


def mathematica_root(coeffs, k):
    roots = mp.polyroots(list(reversed(coeffs)), maxsteps=500, extraprec=300)
    real = sorted(mp.re(r) for r in roots if abs(mp.im(r)) < mp.mpf(10) ** -40)
    return real[k - 1]


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
    m = mp.matrix(MIRROR)
    gens = [mp.matrix(g) for g in G_GENERATORS]
    gens[2] = m * gens[2] * m
    elements = group(gens)
    assert len(elements) == 120
    y8 = (1 - mp.sqrt(6 - 3 * SQRT5 + 2 * mp.sqrt((17 * SQRT5 - 37) / 2))) / 4
    reps = []
    for row in REPRESENTATIVES:
        reps.append([-y8 if item is None else item[2] * mathematica_root(item[0], item[1]) / 2 for item in row])
    r2 = mp.cos(3 * mp.pi / 10)
    assert all(abs(mp.sqrt(sum(t * t for t in r)) - r2) < mp.mpf(10) ** -50 for r in reps)
    points = []
    for r in reps:
        points += orbit(r, elements)
    points += orbit([1 / (2 * TAU), (1 + SQRT5) / (4 * TAU), 0], elements)
    assert len(points) == 972 and len({key(p) for p in points}) == 972
    edges = unit_edges(points)
    with open(os.path.join(HERE, 'G972_vertices.txt'), 'w') as f:
        f.write('# G972: index x y z (60 significant digits); radius cos(3*pi/10)\n')
        for i, p in enumerate(points):
            f.write(f'{i} ' + ' '.join(mp.nstr(t, 60) for t in p) + '\n')
    with open(os.path.join(HERE, 'G972_edges.txt'), 'w') as f:
        f.write(f'# G972: {len(edges)} unit-distance edges\n')
        f.writelines(f'{u} {v}\n' for u, v in edges)
    print(f'G972: {len(points)} vertices, {len(edges)} edges')


if __name__ == '__main__':
    main()
