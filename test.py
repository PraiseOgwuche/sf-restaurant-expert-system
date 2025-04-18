from pyswip import Prolog
p = Prolog()
print(list(p.query("member(X, [1,2,3])")))