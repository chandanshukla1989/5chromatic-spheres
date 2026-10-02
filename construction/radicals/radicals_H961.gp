\ Generate exact nested-radical coordinates of H961 (quadratic tower over Q(sqrt5)); writes H961_exact_coordinates.m
\ usage: cd construction/radicals && gp -q radicals_H961.gp < /dev/null
default(realprecision, 80); default(parisizemax, 8*10^9);
read("../../verification/pari/base972.gp");
u = (1-2*x)^2 - 6;  P82 = (u^2+119)^2 - 5*(34-6*u)^2;   \\ 2*v82 is a root
for(i=1,8, if(POL[i,2]==0, POL[i,2] = P82));
\\ grow a field containing all 24 doubled coordinates and sqrt5
{
  F = subst(polredbest(POL[1,1]), x, y); K = nfinit(F);
  for(i=1,8, for(j=1,3,
    if(#nfroots(K, POL[i,j]) == 0,
      F = subst(polredbest(polcompositum(subst(F,y,x), POL[i,j])[1]), x, y); K = nfinit(F);
      print("  field degree now ", poldegree(F)))));
  if(#nfroots(K, x^2-5) == 0, F = subst(polredbest(polcompositum(subst(F,y,x), x^2-5)[1]), x, y); K = nfinit(F));
}
print("final field degree: ", poldegree(F));
ev(a, t) = subst(lift(a), y, t);
{
  rr = polroots(F); found = 0;
  for(k=1,#rr, if(abs(imag(rr[k])) > 1e-40, next); t = real(rr[k]); err = 0; C = matrix(8,3);
    for(i=1,8, for(j=1,3, my(R = concat(nfroots(K, POL[i,j]), -nfroots(K, POL[i,j])), bd = 1e9, best);
      for(m=1,#R, my(d = abs(ev(R[m],t)/2 - NUM[i,j])); if(d < bd, bd = d; best = R[m]));
      C[i,j] = best/2; err = max(err, bd)));
    my(R5 = nfroots(K, x^2-5)); S5 = if(abs(ev(R5[1],t) - sqrt(5)) < 1e-20, R5[1], R5[2]);
    if(err < 1e-30, found = 1; break));
  if(!found, error("no consistent real embedding"));
}
print("embedding found; max coordinate error < 1e-30");
f = (1+S5)/2; r2sq = (5-S5)/8;
okS = 1; for(i=1,8, my(v = C[i,]~);  if(v~*v != r2sq, okS = 0)); print("all 8 base points exactly on sphere r2: ", okS);
mirr = [1,0,0;0,0,1;0,1,0];
gens = [[-1,0,0;0,-1,0;0,0,1], [0,0,1;1,0,0;0,1,0], mirr*([1,-f,1/f; f,1/f,-1; 1/f,1,f]/2)*mirr, [1,0,0;0,-1,0;0,0,1]];
{
  Grp = List([matid(3)*Mod(1,F)]); keys = Set([lift(Grp[1])]); fr = Vec(Grp);
  while(#fr, nf = List();
    for(a=1,#fr, for(b=1,#gens, my(N = gens[b]*fr[a], kk = lift(N));
      if(!setsearch(keys, kk), keys = setunion(keys, Set([kk])); listput(Grp, N); listput(nf, N))));
    fr = Vec(nf));
  Grp = Vec(Grp);
}
print("group order ", #Grp);
{
  orb(v) = my(L = List(), ks = Set());
    for(a=1,#Grp, my(w = Grp[a]*v, kk = lift(w)); if(!setsearch(ks, kk), ks = setunion(ks, Set([kk])); listput(L, w)));
    Vec(L);
}
ico = [1/2, (1+S5)/4, 0]~ / f * Mod(1,F);
P = orb(ico); for(i=1,8, P = concat(P, orb(C[i,]~)));
print("exact points ", #P);
nv(w) = vector(3, i, ev(w[i], t));
Xf = readvec("../../verification/pari/X972flat.txt"); NX = #Xf/3;
Xn = vector(NX, i, [Xf[3*i-2], Xf[3*i-1], Xf[3*i]]);
PN = vector(#P, j, nv(P[j]));
{
  idx = vector(NX);
  for(i=1,NX, my(bd = 1e9, bj = 0); for(j=1,#P, my(d = normlp(PN[j] - Xn[i])); if(d < bd, bd = d; bj = j));
    if(bd > 1e-9, error("unmatched ", i)); idx[i] = bj);
}
\\ ---- quadratic tower  Q < Q(s5) < L=Q(s5,sb) < K=L(sg)
coords(z) = my(p = lift(z)); vector(poldegree(F), i, polcoef(p, i-1, y));
solveQ(vs, z) = my(M = matrix(poldegree(F), #vs, i, j, coords(vs[j])[i])); matsolve(M, coords(z)~);
\\ quartic subfields containing sqrt5
subs4 = nfsubfields(K, 4);
{
  ok = 0;
  for(i=1,#subs4, my(g = subs4[i][1], h = Mod(subst(subs4[i][2], x, y), F));
    \\ relative minimal polynomial of h over Q(s5): h^2 = a + b*s5 + (c + d*s5)*h
    my(sol = iferr(solveQ([1, S5, h, S5*h], h^2), E, 0));
    if(sol != 0, th = h; Pc = -(sol[3] + sol[4]*S5); Qc = -(sol[1] + sol[2]*S5); ok = 1; break));
  if(!ok, error("no quartic subfield containing sqrt5"));
}
beta = Pc^2 - 4*Qc;  sb = 2*th + Pc;                 \\ sb^2 == beta
if(sb^2 != beta, error("sb^2 != beta"));
if(ev(sb, t) < 0, sb = -sb);
\\ K over L: use phi = y ; phi^2 = l0 + l1*phi with l0,l1 in L
Lb = [1, S5, sb, S5*sb]; phi = Mod(y, F);
sol = solveQ(concat(Lb, vector(4, j, Lb[j]*phi)), phi^2);
Pp = -sum(j=1,4, sol[4+j]*Lb[j]); Qq = -sum(j=1,4, sol[j]*Lb[j]);
gam = Pp^2 - 4*Qq; sg = 2*phi + Pp;
if(sg^2 != gam, error("sg^2 != gamma"));
if(ev(sg, t) < 0, sg = -sg);
B8 = [1, S5, sb, S5*sb, sg, S5*sg, sb*sg, S5*sb*sg];
BETA = solveQ([1, S5], beta);              \\ beta = b0 + b1 s5   (rational b0,b1)
GAM  = solveQ(Lb, gam);                    \\ gamma = g0 + g1 s5 + g2 sb + g3 s5 sb
print("beta  = ", BETA, "   numeric ", ev(beta,t));
print("gamma = ", GAM, "   numeric ", ev(gam,t));
print("sqrt(beta) > 0: ", ev(sb,t) > 0, "   sqrt(gamma) > 0: ", ev(sg,t) > 0, "   beta>0: ", ev(beta,t)>0, " gamma>0: ", ev(gam,t)>0);
\\ coordinates of every point in basis B8
rep(z) = solveQ(B8, z);
\\ Mathematica / python string of an element
fmtq(q) = if(denominator(q)==1, Str(q), Str("(", numerator(q), "/", denominator(q), ")"));
STRB = Str("Sqrt[", fmtq(BETA[1]), "+", fmtq(BETA[2]), "*Sqrt[5]]");
STRG = Str("Sqrt[", fmtq(GAM[1]), "+", fmtq(GAM[2]), "*Sqrt[5]+(", fmtq(GAM[3]), "+", fmtq(GAM[4]), "*Sqrt[5])*", STRB, "]");
BS = ["1", "Sqrt[5]", STRB, Str("Sqrt[5]*",STRB), STRG, Str("Sqrt[5]*",STRG), Str(STRB,"*",STRG), Str("Sqrt[5]*",STRB,"*",STRG)];
mstr(z) = my(c = rep(z), s = ""); for(j=1,8, if(c[j] != 0, s = Str(s, if(#s, "+", ""), fmtq(c[j]), if(j>1, Str("*", BS[j]), "")))); if(#s, s, "0");
read("../../verification/pari/S961.gp");
{
  out = "H961_exact_coordinates.m";
  write1(out, "(* H961: exact coordinates of the 961 vertices, Mathematica syntax. sqrt(beta) = ", STRB, ", sqrt(gamma) = ", STRG, " *)\n");
  write1(out, "H961 = {\n");
  for(i=1,#SB, my(w = P[idx[SB[i]]]);
    write1(out, Str("{", mstr(w[1]), ", ", mstr(w[2]), ", ", mstr(w[3]), "}", if(i<#SB, ",", ""), "\n")));
  write1(out, "};\n");
}
print("written H961_exact_coordinates.m");
quit
