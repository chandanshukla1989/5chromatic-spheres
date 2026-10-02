"""Convert an exact-coordinate file from Mathematica syntax (Sqrt[...]) to Python syntax ((x)**(1/2)).

usage: python m_to_py.py H231   (reads H231_exact_coordinates.m, writes H231_exact_coordinates.py)
"""
import re
import sys


def to_python(expr):
    while 'Sqrt[' in expr:
        expr = re.sub(r'Sqrt\[([^\[\]]*)\]', r'(\1)**(1/2)', expr)
    return expr


def main():
    tag = sys.argv[1]
    text = open(f'{tag}_exact_coordinates.m').read()
    body = text.split('= {', 1)[1].rsplit('};', 1)[0]
    rows = [r.strip().rstrip(',') for r in body.strip().split('\n') if r.strip()]
    out = ['(' + to_python(r[1:-1]) + ')' for r in rows]
    assert not re.search(r'\d\.\d', ''.join(out)), 'decimal number found'
    with open(f'{tag}_exact_coordinates.py', 'w') as f:
        f.write(f'# {tag}: exact coordinates of all {len(rows)} vertices; only integers, fractions and square roots written as (x)**(1/2).\n')
        f.write('# Load with sympy: from sympy import Rational, sqrt; then sympify each tuple (or eval with Rational arithmetic).\n')
        f.write(f'{tag} = [\n' + ',\n'.join(out) + '\n]\n')


if __name__ == '__main__':
    main()
