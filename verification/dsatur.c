/* Exhaustive search (no SAT solver) for a proper 4-colouring of a graph, optionally with some vertices pre-coloured.
   DSATUR-ordered backtracking with colour-symmetry breaking (a vertex may only use a colour <= max_used+1).
   Input (stdin): n m, then m lines "u v" (0-based), then optionally k and k lines "v c" (pre-colouring).  Output: COLOURABLE + colouring, or NOT 4-COLOURABLE + node count. */
#include <stdio.h>
#include <stdlib.h>
#define K 4
static int n, m, *deg, **adj, *col, nodes_lo = 0, nodes_hi = 0;
static int sat_deg(int v, int *mask) {   /* number of distinct colours among coloured neighbours */
    int s = 0; *mask = 0;
    for (int i = 0; i < deg[v]; i++) { int c = col[adj[v][i]]; if (c >= 0) *mask |= 1 << c; }
    for (int c = 0; c < K; c++) if (*mask >> c & 1) s++;
    return s;
}
static int solve(int coloured, int maxused) {
    if (++nodes_lo == 1000000000) { nodes_lo = 0; nodes_hi++; }
    if (coloured == n) return 1;
    int best = -1, bs = -1, bd = -1, bmask = 0;
    for (int v = 0; v < n; v++) if (col[v] < 0) {
        int mask, s = sat_deg(v, &mask);
        if (s > bs || (s == bs && deg[v] > bd)) { best = v; bs = s; bd = deg[v]; bmask = mask; }
    }
    if (bs == K) return 0;
    for (int c = 0; c < K && c <= maxused + 1; c++) if (!(bmask >> c & 1)) {
        col[best] = c;
        if (solve(coloured + 1, c > maxused ? c : maxused)) return 1;
        col[best] = -1;
    }
    return 0;
}
int main(void) {
    int npre = 0, pv[64], pc[64];
    if (scanf("%d %d", &n, &m) != 2) return 2;
    int *eu = malloc(m * sizeof(int)), *ev = malloc(m * sizeof(int));
    deg = calloc(n, sizeof(int)); col = malloc(n * sizeof(int)); adj = malloc(n * sizeof(int *));
    for (int i = 0; i < m; i++) { if (scanf("%d %d", &eu[i], &ev[i]) != 2) return 2; deg[eu[i]]++; deg[ev[i]]++; }
    int *fill = calloc(n, sizeof(int));
    for (int v = 0; v < n; v++) adj[v] = malloc((deg[v] + 1) * sizeof(int));
    for (int i = 0; i < m; i++) { adj[eu[i]][fill[eu[i]]++] = ev[i]; adj[ev[i]][fill[ev[i]]++] = eu[i]; }
    for (int v = 0; v < n; v++) col[v] = -1;
    /* optional pre-colouring: k, then k lines "v c" (a case of an exhaustive case split) */
    if (scanf("%d", &npre) == 1) for (int i = 0; i < npre; i++) { if (scanf("%d %d", &pv[i], &pc[i]) != 2) return 2; col[pv[i]] = pc[i]; }
    for (int i = 0; i < m; i++) if (col[eu[i]] >= 0 && col[eu[i]] == col[ev[i]]) { printf("PRECOLOURING NOT PROPER\n"); return 3; }
    int r = solve(npre, npre ? K - 1 : -1);
    if (r) { printf("COLOURABLE\n"); for (int v = 0; v < n; v++) printf("%d ", col[v]); printf("\n"); }
    else printf("NOT 4-COLOURABLE  (search nodes: %d e9 + %d)\n", nodes_hi, nodes_lo);
    return 0;
}
