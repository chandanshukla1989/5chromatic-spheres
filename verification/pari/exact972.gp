default(realprecision, 80); default(parisizemax, 8*10^9);
read("base972.gp");
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
Xf = readvec("X972flat.txt"); NX = #Xf/3;
Xn = vector(NX, i, [Xf[3*i-2], Xf[3*i-1], Xf[3*i]]);
PN = vector(#P, j, nv(P[j]));
{
  idx = vector(NX);
  for(i=1,NX, my(bd = 1e9, bj = 0); for(j=1,#P, my(d = normlp(PN[j] - Xn[i])); if(d < bd, bd = d; bj = j));
    if(bd > 1e-9, error("unmatched ", i)); idx[i] = bj);
}
print("all ", NX, " numeric points matched to distinct exact points: ", #Set(idx) == NX);
read("E961.gp"); read("S961.gp");
{
  okN = 1; for(i=1,#SB, my(w = P[idx[SB[i]]]); if(w~*w != r2sq, okN = 0));
  print("all ", #SB, " points exactly on sphere r2 (r2^2=(5-sqrt5)/8): ", okN);
  nE = matsize(EB)[1]; bad = 0;
  for(e=1,nE, my(d = P[idx[EB[e,1]]] - P[idx[EB[e,2]]]); if(d~*d != 1, bad++));
  print("edges checked exactly: ", nE, "   failures: ", bad);
}
quit
