\\ Exact verification of H231 (a 231-vertex subgraph of G372, Voronov et al.) in a degree-8 number field.
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
Xf = readvec("X372flat.txt");
Xn = vector(372, i, [Xf[3*i-2], Xf[3*i-1], Xf[3*i]]);
{
  idx = vector(372);
  for(i=1,372,
    my(bd = 1e9, bj = 0);
    for(j=1,#P, my(d = normlp(nv(P[j]) - Xn[i])); if(d < bd, bd = d; bj = j));
    if(bd > 1e-9, error("unmatched point ", i)); idx[i] = bj);
}
print("all 372 numeric points matched to distinct exact points: ", #Set(idx) == 372);
read("E231.gp"); read("S231.gp");
{
  okN = 1; for(i=1,#S231, my(w = P[idx[S231[i]]]); if(w~*w != r1sq, okN = 0));
  print("all points of H231 exactly on the sphere r1 (r1^2=(5+sqrt5)/8): ", okN);
  bad = 0; nE = matsize(E231)[1]; for(e=1,nE, my(d = P[idx[E231[e,1]]] - P[idx[E231[e,2]]]); if(d~*d != 1, bad++));
  print("edges of H231 checked exactly: ", nE, "   failures: ", bad);
}
quit
