"""Write main_geombinatorics.tex: main.tex in the Geombinatorics submission format.

Format (journal web page "Submission Formatting"): 5.5in x 8.5in pages; top, left and right margins
0.35in, bottom margin 0.5in; Times 11 pt, single spacing; title in capital bold 14 pt, author name in bold
11 pt, then address and e-mail; no page numbers.

usage: python paper/make_geombinatorics.py   (from the repository root), then pdflatex twice in paper/
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
tex = open(os.path.join(HERE, 'main.tex')).read()


def sub(old, new, count=1):
    global tex
    assert tex.count(old) == count, (old, tex.count(old))
    tex = tex.replace(old, new)


sub(r'\usepackage[margin=1in]{geometry}',
    r'\usepackage[paperwidth=5.5in,paperheight=8.5in,top=0.35in,left=0.35in,right=0.35in,bottom=0.5in,'
    r'includehead=false,includefoot=false]{geometry}' '\n'
    r'\renewcommand{\rmdefault}{ptm}' '\n'
    r'\sloppy' '\n'
    r'\pagestyle{empty}' '\n'
    r'\setlength{\emergencystretch}{3em}')

# title block: capital bold 14 pt; author bold 11 pt; address and e-mail non-bold 11 pt
title = re.search(r'\\title\{.*?\}\n\\author\{.*?\}\n\\date\{\}\n', tex, re.S).group(0)
tex = tex.replace(title, '')
sub(r'\maketitle',
    r'\begin{center}' '\n'
    r'{\fontsize{14}{17}\selectfont\bfseries SMALLER 5-CHROMATIC UNIT-DISTANCE GRAPHS\\ ON TWO ICOSAHEDRAL SPHERES\par}' '\n'
    r'\vspace{6pt}' '\n'
    r'{\bfseries Chandan Kumar Shukla\par}' '\n'
    r'Independent Researcher, India\\ shukla.chandan12@gmail.com' '\n'
    r'\end{center}' '\n'
    r'\thispagestyle{empty}')

# narrow page: smaller type for wide tables and formulas
# file names: allow line breaks after underscores
sub(r'\pagestyle{empty}', r'\pagestyle{empty}' '\n' r'\renewcommand{\_}{\textunderscore\allowbreak}')
# group generators: two rows
sub('\\begin{pmatrix}0&0&1\\\\1&0&0\\\\0&1&0\\end{pmatrix},\\quad\n', '\\begin{pmatrix}0&0&1\\\\1&0&0\\\\0&1&0\\end{pmatrix},\\\\\n')
tex = tex.replace('generated as in~\\cite{VNDrepo} by\n\\[\n', 'generated as in~\\cite{VNDrepo} by\n\\begin{gather*}\n', 1)
sub('\\qquad \\tau=\\tfrac{1+\\sqrt5}{2}.\n\\]', '\\qquad \\tau=\\tfrac{1+\\sqrt5}{2}.\n\\end{gather*}')
sub('\\begin{table}[ht]\n\\centering\\small\n\\begin{tabular}{ccl}', '\\begin{table}[ht]\n\\centering\\scriptsize\\setlength{\\tabcolsep}{2.5pt}\n\\begin{tabular}{ccl}', count=tex.count('\\begin{table}[ht]\n\\centering\\small\n\\begin{tabular}{ccl}'))
sub('\\begin{table}[ht]\n\\centering\\small\n\\begin{tabular}{lcccccc}',
    '\\begin{table}[ht]\n\\centering\\scriptsize\\setlength{\\tabcolsep}{2.5pt}\n\\begin{tabular}{lcccccc}')
tex = re.sub(r'(\\section\{Exact orbit representatives\}.*?)\{\\small\n', r'\1{\\scriptsize\n', tex, count=1, flags=re.S)

open(os.path.join(HERE, 'main_geombinatorics.tex'), 'w').write(tex)
print('main_geombinatorics.tex written')
