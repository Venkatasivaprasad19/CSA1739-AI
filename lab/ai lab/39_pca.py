from sklearn.datasets import load_iris
from sklearn.decomposition import PCA
X=load_iris().data
p=PCA(n_components=2)
Z=p.fit_transform(X)
print("Before:",X.shape,"After:",Z.shape)
print("Variance kept:",p.explained_variance_ratio_)

# OUTPUT:
# Before: (150, 4) After: (150, 2)
# Variance kept: [0.92461872 0.05306648]
