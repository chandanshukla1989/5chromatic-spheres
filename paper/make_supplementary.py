"""Generate Supplementary_Material.tex (file manifest with SHA-256 hashes is computed at build time).

usage: python paper/make_supplementary.py   (from the repository root), then pdflatex twice in paper/
"""
import hashlib
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RADICALS = os.path.join(ROOT, 'paper', 'radicals')

FILES = [
    ('H231/H231_vertices.txt', 'vertex index, parent index in $G_{372}$, coordinates (30 digits)'),
    ('H231/H231_edges.txt', 'edge list (0-based)'),
    ('H231/H231_exact_coordinates.m', 'exact coordinates, nested radicals, Mathematica syntax'),
    ('H231/H231_exact_coordinates.py', 'exact coordinates, Python syntax'),
    ('H231/H231_5colouring.txt', 'proper 5-colouring'),
    ('H231/H231_criticality_certificates.txt', '231 certificates: 4-colouring of $H_{231}-v$'),
    ('H231/H231_4col.cnf', 'CNF: $H_{231}$ is 4-colourable'),
    ('H231/H231_4col.drat.xz', 'DRAT proof (xz)'),
    ('H231/H231_drat-trim.log', 'drat-trim output'),
    ('H961/H961_vertices.txt', 'vertex index, parent index in $G_{972}$, coordinates (30 digits)'),
    ('H961/H961_edges.txt', 'edge list (0-based)'),
    ('H961/H961_exact_coordinates.m', 'exact coordinates, Mathematica syntax'),
    ('H961/H961_exact_coordinates.py', 'exact coordinates, Python syntax'),
    ('H961/H961_5colouring.txt', 'proper 5-colouring'),
    ('H961/H961_criticality_certificates.txt', '961 certificates: 4-colouring of $H_{961}-v$'),
    ('H961/H961_4col.cnf', 'CNF: $H_{961}$ is 4-colourable'),
    ('H961/H961_4col.drat.xz', 'DRAT proof (xz)'),
    ('H961/H961_drat-trim.log', 'drat-trim output'),
    ('construction/build_G372.py', 'rebuilds $G_{372}$ (60 digits)'),
    ('construction/build_G972.py', 'rebuilds $G_{972}$ (60 digits)'),
    ('verification/verify_graph.py', 'counts, parent indices, edges, colourings, certificates, spindles'),
    ('verification/check_exact_radicals.py', 'exact check of the radical coordinates (no PARI/GP)'),
    ('verification/crosscheck_solvers.py', 'three SAT solvers, two encodings'),
    ('verification/dsatur.c', 'SAT-free exhaustive 4-colouring search'),
    ('verification/make_criticality_certificates.py', 'generates the criticality certificates'),
    ('verification/pari/exact372.gp', 'exact verification of $H_{231}$ in a degree-8 field'),
    ('verification/pari/exact972.gp', 'exact verification of $H_{961}$ in a degree-8 field'),
    ('verify_all.sh', 'runs every check'),
]


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def tt(s):
    return '\\texttt{' + s.replace('_', '\\_') + '}'


def radical_rows(name):
    return [line.rstrip('\n').split('|') for line in open(os.path.join(RADICALS, name))]


def main():
    vg = {g: json.load(open(os.path.join(ROOT, 'results', f'verify_graph_{g}.json'))) for g in ('H231', 'H961')}
    manifest = '\n'.join(
        f'{tt(p)} & {d} \\\\ \\multicolumn{{2}}{{l}}{{\\scriptsize\\texttt{{{sha256(os.path.join(ROOT, p))}}}}} \\\\'
        for p, d in FILES)
    colours = {int(l.split()[0]): int(l.split()[1]) for l in open(os.path.join(ROOT, 'H231', 'H231_5colouring.txt')) if not l.startswith('#')}
    parents = [int(l.split()[1]) for l in open(os.path.join(ROOT, 'H231', 'H231_vertices.txt')) if not l.startswith('#')]
    orbit = lambda v: 'icosahedron' if v < 12 else f'$v_{1 + (v - 12) // 120}$-orbit'
    h231 = ''.join(
        f"\\noindent\\textbf{{{r[0]}}} (parent {parents[int(r[0]) - 1]}, {orbit(parents[int(r[0]) - 1])}, colour {colours[int(r[0]) - 1]}):\\quad "
        f"$x={r[1]}$,\\quad $y={r[2]}$,\\quad $z={r[3]}$\\par\\smallskip\n" for r in radical_rows('H231_radicals_tex.txt'))
    removed = ''.join(f"\\noindent\\textbf{{{r[0]}}}:\\quad $x={r[1]}$,\\quad $y={r[2]}$,\\quad $z={r[3]}$\\par\\smallskip\n"
                      for r in radical_rows('H961_removed_radicals_tex.txt'))
    tex = open(os.path.join(ROOT, 'paper', 'Supplementary_Material_template.tex')).read()
    tex = tex.replace('%MANIFEST%', manifest).replace('%H231RADICALS%', h231).replace('%REMOVED%', removed)
    tex = tex.replace('%GAP231%', f"{vg['H231']['nonedge_min_gap']:.4f}").replace('%GAP961%', f"{vg['H961']['nonedge_min_gap']:.5f}")
    open(os.path.join(ROOT, 'paper', 'Supplementary_Material.tex'), 'w').write(tex)
    print('Supplementary_Material.tex written')


if __name__ == '__main__':
    main()
