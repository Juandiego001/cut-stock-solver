set O := {0,1};	#orientación
set JJ;	#items
param Platos;
set J:= {0..Platos};	#subespacios
set Q{J,O};	#	#posición donde se puede hacer el corte en j, de forma o

param a{o in O, k in J, Q[k,o], J diff {0}} default 0;	
	#cortar k en pos q en o -> j
param Dem{JJ};	#demanda items j [und]
param Area{J};	#área de j [cm^2]
#param Desp{o in O, k in J, Q[k,o]} default 0;	#desper al cortar j en o en q [cm^2]
param platosOri = 1;

var X{o in O, j in J, q in Q[j,o]: card(Q[j,o]) <> 0} >= 0 integer;	
#veces que se corta j en q y o
var Y{j in JJ} >= 0 integer;
#items j obtenidos
var Inv{JJ} >= 0 integer;
#iniventario de j
var InvNoIt{J diff JJ diff {0}} >= 0 integer;

#minimize z : # Desp[o,j,q] 
#	sum{o in O, j in J, q in Q[j,o]: card(Q[j,o]) <> 0} 
#	X[o,j,q]*1 + sum{j in JJ} Inv[j]*Area[j];
minimize z : 
	sum{j in JJ} Inv[j]*Area[j] + 
	sum{j in J diff JJ diff {0}} InvNoIt[j]*Area[j];
s.t.
r1{j in JJ}:
	sum{o in O, k in J, q in Q[k,o]: card(Q[k,o]) <> 0} a[o,k,q,j]*X[o,k,q] =
	sum{o in O, q in Q[j,o]: card(Q[j,o]) <> 0} X[o,j,q] + Y[j];
r2{j in J diff JJ diff {0}}:
	sum{o in O, k in J, q in Q[k,o]: card(Q[k,o]) <> 0} a[o,k,q,j]*X[o,k,q] =
	sum{o in O, q in Q[j,o]: card(Q[j,o]) <> 0} X[o,j,q] + InvNoIt[j];
r3{j in JJ}:
	Y[j] = Dem[j] + Inv[j];
r4:
	sum{o in O, q in Q[0,o]: card(Q[0,o]) <> 0} X[o,0,q] <= platosOri;
