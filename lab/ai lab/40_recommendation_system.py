import numpy as np
R=np.array([[5,4,0,1],      # rows = users, columns = items, 0 = not rated
            [4,5,1,0],
            [1,0,5,4],
            [0,1,4,5]])
sim=lambda a,b:a@b/(np.linalg.norm(a)*np.linalg.norm(b))
u=0                                           # recommend for user 0
s=np.array([sim(R[u],R[v]) if v!=u else 0 for v in range(4)])
for i in range(4):
    if R[u,i]==0:
        r=R[:,i]>0
        print("Item",i,"predicted rating:",round(s[r]@R[r,i]/s[r].sum(),2))

# OUTPUT:
# Item 2 predicted rating: 2.09
