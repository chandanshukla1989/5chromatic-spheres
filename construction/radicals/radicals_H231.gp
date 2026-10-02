\ Generate exact nested-radical coordinates of H231 (quadratic tower over Q(sqrt5)); writes H231_exact_coordinates.m
\ usage: cd construction/radicals && gp -q radicals_H231.gp < /dev/null
\\ All coordinates live in a number field K = Q[y]/(F(y)); points are vectors of t_POLMOD.
default(realprecision, 80);
Px1 = x^4-2*x^3+2*x^2-x-1;  Py1 = x^4+x^3-2*x^2+2*x-1;  Pz1 = x^8-5*x^6+2*x^4+20*x^2-19;
Px2 = x^8-x^7-4*x^6+6*x^5+28*x^4-7*x^3+9*x^2+8*x+1;
Py2 = x^8-2*x^7+x^6-5*x^5+9*x^4-4*x^3+5*x^2-5*x-1;
Pz2 = x^8-3*x^7+10*x^5+4*x^4-24*x^3-13*x^2+7*x-1;
Pz3 = x^8+3*x^7-10*x^5+4*x^4+24*x^3-13*x^2-7*x-1;
num = [0.71584,0.34924,0.51972; -0.07961,-0.08345,0.94404; -0.17646,0.79929,0.48426];
PP  = [Px1,Py1,Pz1; Px2,Py2,Pz2; Px2,Py2,Pz3];
need = [Px1,Py1,Pz1,Px2,Py2,Pz2,Pz3,x^2-5];
{
  F = subst(polredbest(Pz2), x, y);
  for(i=1,#need,
    if(#nfroots(nfinit(F), need[i]) == 0,
      F = subst(polredbest(polcompositum(subst(F,y,x), need[i])[1]), x, y)));
}
K = nfinit(F);
print("field degree: ", poldegree(F));
ev(a, t) = subst(lift(a), y, t);
{
  pick(P, target, t) =
    my(R = nfroots(K, P), best = 0, bd = 1e9);
    for(j=1, #R, my(v = ev(R[j], t)/2); if(abs(v - target) < bd, bd = abs(v - target); best = R[j]));
    [best, bd];
}
{
  found = 0; rr = polroots(F);
  for(k=1, #rr,
    if(abs(imag(rr[k])) > 1e-30, next);
    t = real(rr[k]); err = 0; c = vector(9);
    for(i=1,3, for(j=1,3, my(z = pick(PP[i,j], num[i,j], t)); c[3*(i-1)+j] = z[1]/2; err = max(err, z[2])));
    s5 = pick(x^2-5, sqrt(5)/2, t);
    if(err < 1e-4 && s5[2] < 1e-9, found = 1; break));
  if(!found, error("no consistent embedding"));
}
print("embedding: y -> ", t);
S5 = s5[1];
if(abs(ev(S5,t) - sqrt(5)) > 1e-9, error("sqrt5 embedding mismatch"));
f = (1+S5)/2; r1sq = (5+S5)/8;
v1 = [c[1],c[2],c[3]]~; v2 = [c[4],c[5],c[6]]~; v3 = [c[7],c[8],c[9]]~;
for(i=1,3, my(v=[v1,v2,v3][i]); print("|v",i,"|^2 == r1^2 exactly: ", v~*v == r1sq));
gens = [[-1,0,0;0,-1,0;0,0,1], [0,0,1;1,0,0;0,1,0], [1,-f,1/f; f,1/f,-1; 1/f,1,f]/2, [1,0,0;0,-1,0;0,0,1]];
{
  Grp = List([matid(3)*Mod(1,F)]); keys = Set([lift(Grp[1])]); fr = Vec(Grp);
  while(#fr,
    nf = List();
    for(a=1,#fr, for(b=1,#gens,
      my(N = gens[b]*fr[a], kk = lift(N));
      if(!setsearch(keys, kk), keys = setunion(keys, Set([kk])); listput(Grp, N); listput(nf, N))));
    fr = Vec(nf));
  Grp = Vec(Grp);
}
print("group order: ", #Grp, "   all orthogonal: ", vecprod(vector(#Grp, a, Grp[a]~*Grp[a] == matid(3))));
{
  orb(v) = my(L = List(), ks = Set());
    for(a=1,#Grp, my(w = Grp[a]*v, kk = lift(w)); if(!setsearch(ks, kk), ks = setunion(ks, Set([kk])); listput(L, w)));
    Vec(L);
}
ico = [(1+S5)/4, 1/2, 0]~ * Mod(1,F);
P = concat([orb(ico), orb(v1), orb(v2), orb(v3)]);
print("exact points: ", #P);
nv(w) = vector(3, i, ev(w[i], t));
Xf = readvec("../../verification/pari/X372flat.txt");
Xn = vector(372, i, [Xf[3*i-2], Xf[3*i-1], Xf[3*i]]);
{
  idx = vector(372);
  for(i=1,372,
    my(bd = 1e9, bj = 0);
    for(j=1,#P, my(d = normlp(nv(P[j]) - Xn[i])); if(d < bd, bd = d; bj = j));
    if(bd > 1e-9, error("unmatched point ", i)); idx[i] = bj);
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
SB = Str("Sqrt[", fmtq(BETA[1]), "+", fmtq(BETA[2]), "*Sqrt[5]]");
SG = Str("Sqrt[", fmtq(GAM[1]), "+", fmtq(GAM[2]), "*Sqrt[5]+(", fmtq(GAM[3]), "+", fmtq(GAM[4]), "*Sqrt[5])*", SB, "]");
BS = ["1", "Sqrt[5]", SB, Str("Sqrt[5]*",SB), SG, Str("Sqrt[5]*",SG), Str(SB,"*",SG), Str("Sqrt[5]*",SB,"*",SG)];
mstr(z) = my(c = rep(z), s = ""); for(j=1,8, if(c[j] != 0, s = Str(s, if(#s, "+", ""), fmtq(c[j]), if(j>1, Str("*", BS[j]), "")))); if(#s, s, "0");
read("../../verification/pari/S231.gp"); S235 = S231;
{
  out = "H231_exact_coordinates.m";
  write1(out, "(* H231: exact coordinates of the 231 vertices, Mathematica syntax. sqrt(beta) = ", SB, ", sqrt(gamma) = ", SG, " *)\n");
  write1(out, "H231 = {\n");
  for(i=1,#S235, my(w = P[idx[S235[i]]]);
    write1(out, Str("{", mstr(w[1]), ", ", mstr(w[2]), ", ", mstr(w[3]), "}", if(i<#S235, ",", ""), "\n")));
  write1(out, "};\n");
}
print("written H231_exact_coordinates.m");
quit
