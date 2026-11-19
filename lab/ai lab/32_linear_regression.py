import numpy as np
x=np.array([1,2,3,4,5]);y=np.array([2,4,5,4,5])
m=((x-x.mean())*(y-y.mean())).sum()/((x-x.mean())**2).sum()
c=y.mean()-m*x.mean()
print("y = %.1fx + %.1f"%(m,c))
print("Prediction for x=6:",m*6+c)

# OUTPUT:
# y = 0.6x + 2.2
# Prediction for x=6: 5.8
