"""Cross-check every number and file name in the manuscript against the artifacts; write results/AUDIT.md.

Run after verify_all.sh (it reads the logs in results/).  usage: python verification/audit.py
"""
import glob
import itertools
import json
import os
import re

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, *a)
tex = open(P('paper', 'main.tex')).read()
rows = []


def check(item, ok, detail=''):
    rows.append((item, 'PASS' if ok else 'FAIL', detail))


def data(path):
    return [l.split() for l in open(P(path)) if l.strip() and not l.startswith('#')]


def in_tex(s):
    return s in tex


vg = {g: json.load(open(P('results', f'verify_graph_{g}.json'))) for g in ('H231', 'H961')}
for g, (n, m) in (('H231', (231, 938)), ('H961', (961, 4028))):
    r = vg[g]
    check(f'{g}: {n} vertices / {m} edges (files) and in paper', r['vertices'] == n and r['edges'] == m and in_tex(f'${n}$ vertices') and in_tex(f'${m}$ edges'), f"{r['vertices']} / {r['edges']}")
    check(f'{g}: parent-graph mapping', r['parent_ok'], f"max diff {r['parent_max_coordinate_difference']:.1e}")
    check(f'{g}: all listed edges have length 1 (numerical, 30 digits)', r['edge_length_max_deviation'] < 1e-25, f"{r['edge_length_max_deviation']:.1e}")
    check(f'{g}: no missing unit edges', r['missing_unit_edges'] == 0, f"min non-edge gap {r['nonedge_min_gap']:.3e}")
    check(f'{g}: valid 5-colouring', r['five_colouring_ok'])
    check(f'{g}: criticality certificates ({n}) valid', r['criticality_certificates_ok'])
    check(f'{g}: no Moser spindle', r['moser_spindles'] == 0, str(r['moser_spindles']))
check('paper non-edge margins 2.2e-3 / 4.1e-4 match', in_tex('2.2\\cdot10^{-3}') and in_tex('4.1\\cdot10^{-4}')
      and 2.2e-3 <= vg['H231']['nonedge_min_gap'] < 2.3e-3 and 4.1e-4 <= vg['H961']['nonedge_min_gap'] < 4.2e-4)

for g, log, m in (('H231', 'exact_pari_H231.log', 938), ('H961', 'exact_pari_H961.log', 4028)):
    t = open(P('results', log)).read()
    check(f'{g}: exact sphere identities (PARI/GP)', 'exactly on' in t and re.search(r'exactly on[^\n]*: 1', t) is not None)
    check(f'{g}: exact unit-edge identities (PARI/GP)', re.search(rf'checked exactly: {m}\s+failures: 0', t) is not None)
    t = open(P('results', f'exact_radicals_{g}.log')).read()
    check(f'{g}: exact identities from radical files (independent checker)', f'edges checked exactly: {m}; failures: 0' in t and 'all exactly on sphere: True' in t)
    t = open(P('results', f'drat-trim_{g}.log')).read()
    check(f'{g}: DRAT proof verified by drat-trim', re.search(r'^s VERIFIED', t, re.M) is not None)
    c = json.load(open(P('results', f'crosscheck_{g}.json')))
    check(f'{g}: CaDiCaL/Glucose/MiniSat + binary encoding all UNSAT', c['all_unsat'])
t = open(P('results', 'dsatur_H231.log')).read()
nodes = int(re.search(r'\+ (\d+)\)', t).group(1)) if 'NOT 4-COLOURABLE' in t else -1
check('H231: SAT-free DSATUR search finds no 4-colouring (~7e6 nodes)', 6.5e6 < nodes < 7.5e6 and in_tex('7\\cdot10^{6}'), str(nodes))

# parent graphs
for name, n, m, dmin in (('G372', 372, 1710, '0.049'), ('G972', 972, 4110, '0.009')):
    V = np.array([[float(x) for x in r[1:4]] for r in data(f'construction/{name}_vertices.txt')])
    E = data(f'construction/{name}_edges.txt')
    d = np.sqrt(((V[:, None] - V[None]) ** 2).sum(-1)) + np.eye(len(V)) * 9
    check(f'{name}: {n} vertices / {m} edges, as in paper', len(V) == n and len(E) == m and in_tex(f'${n}$') and in_tex(f'${m}$'))
    check(f'{name}: min distance between vertices {dmin} (paper)', abs(d.min() - float(dmin)) < 5e-4 and in_tex(f'${dmin}$'), f'{d.min():.4f}')

# derived numbers in the paper
col = [int(r[1]) for r in data('H231/H231_5colouring.txt')]
sizes = sorted((col.count(c) for c in range(1, 6)), reverse=True)
check('H231 colour-class sizes 55,51,49,46,30', sizes == [55, 51, 49, 46, 30] and in_tex('$55,51,49,46,30$'), str(sizes))
par = [int(r[1]) for r in data('H231/H231_vertices.txt')]
comp = [sum(v < 12 for v in par), sum(12 <= v < 132 for v in par), sum(132 <= v < 252 for v in par), sum(v >= 252 for v in par)]
check('H231 composition 12+99+60+60', comp == [12, 99, 60, 60] and in_tex('$12+99+60+60$'), str(comp))
par9 = [int(r[1]) for r in data('H961/H961_vertices.txt')]
check('H961 = G972 minus 11 vertices; composition 12+8x120-11', len(par9) == 961 and sum(v >= 960 for v in par9) == 12 and in_tex('$12+8\\times120-11$'))
for g, rng, avg in (('H231', '4--25', '8.12'), ('H961', '5--65', '8.38')):
    E = data(f'{g}/{g}_edges.txt')
    deg = {}
    for u, v in E:
        deg[u] = deg.get(u, 0) + 1
        deg[v] = deg.get(v, 0) + 1
    ok = f'{min(deg.values())}--{max(deg.values())}' == rng and f'{2 * len(E) / len(deg):.2f}' == avg and in_tex(f'{rng} (avg.\\ {avg})')
    check(f'{g} degrees {rng}, average {avg}', ok)
check('38% fewer vertices than G372', round(100 * (1 - 231 / 372)) == 38 and in_tex('$38\\%$'))

# experiments
finals = sorted(int(re.search(r'FINAL (\d+)', open(f).read()).group(1)) for f in glob.glob(P('experiments', 'G372_greedy', '*.log')))
check('16 greedy runs on G372, sizes 235..337', len(finals) == 16 and finals[0] == 235 and finals[-1] == 337 and in_tex('Sixteen runs') and in_tex('$235$ and $337$'), str(finals))
ils8 = json.load(open(P('experiments', 'G372_local_search', 'ils_8.json')))
check('local search result ils_8.json is H231', sorted(ils8['vertices']) == sorted(par))
tri = json.load(open(P('experiments', 'G972_triage', 'triage972.json')))
ess = sum(1 for v in tri.values() if v[0] == 'ESSENTIAL')
rem = sum(1 for v in tri.values() if v[0] == 'REMOVABLE')
untested = sum(1 for v in tri.values() if v[0] == 'ESSENTIAL(tri)')
check('G972 triage: 968 vertices, 931 essential, 34 removable, 3 untested', (len(tri), ess, rem, untested) == (968, 931, 34, 3) and in_tex('$931$ were shown') and in_tex('at least $931$ of the $968$') and in_tex('Only $34$ of the $968$'), f'{len(tri)}, {ess}, {rem}, {untested}')
red = json.load(open(P('experiments', 'G972_triage', 'red_8.json')))
fin = json.load(open(P('experiments', 'G972_local_search', 'ils_103.json')))
check('G972: greedy joint removal 963, local search 961 = H961', red['size'] == 963 and sorted(fin['vertices']) == sorted(par9))

# Table 2 and Appendix A labels
G9 = {int(r[0]): [float(x) for x in r[1:4]] for r in data('construction/G972_vertices.txt')}
removed = sorted(set(G9) - set(par9))
labels = re.findall(r'\$w_(\d)\$-orbit & \$([^$]+)\$ & \$([^$]+)\$ & \$([^$]+)\$', tex)
num = lambda s: float(s.replace('\\phantom{-}', ''))
ok = len(labels) == 11 and all(abs(num(lab[1 + k]) - round(G9[v][k], 4)) < 1e-9 and int(lab[0]) == v // 120 + 1 for lab, v in zip(labels, removed) for k in range(3))
check('Table 2: the 11 deleted vertices of G972 (labels, orbits)', ok)
sup = open(P('paper', 'Supplementary_Material.tex')).read()
app = re.findall(r'\\textbf\{(\d+)\} \(parent (\d+), [^,]+, colour (\d)\)', sup)
ok = len(app) == 231 and all(int(p) == par[int(i) - 1] and int(c) == col[int(i) - 1] for i, p, c in app) \
    and in_tex('Appendix~S1 of the Supplementary Material')
check('Supplementary Appendix S1: 231 vertices in radicals, parent indices and colours match the data files', ok)

# file names referenced in the manuscript
names = set(re.findall(r'\\texttt\{([^}]*)\}', tex))
files = {n.replace('\\_', '_') for n in names if '.' in n and ' ' not in n and '@' not in n}
existing = {os.path.relpath(p, ROOT) for p in glob.glob(P('**', '*'), recursive=True)}
missing = [f for f in sorted(files) if not any(e == f or e.endswith('/' + f) for e in existing)]
check('all file names referenced in the manuscript exist', not missing, ', '.join(sorted(files)) if not missing else 'missing: ' + ', '.join(missing))

with open(P('results', 'AUDIT.md'), 'w') as f:
    f.write('# Audit: manuscript numbers and claims vs. artifacts\n\n| # | item | result | detail |\n|---|---|---|---|\n')
    for i, (item, res, det) in enumerate(rows, 1):
        f.write(f'| {i} | {item} | **{res}** | {det} |\n')
    f.write(f"\n{sum(r[1] == 'PASS' for r in rows)} of {len(rows)} checks passed.\n")
print(open(P('results', 'AUDIT.md')).read())
