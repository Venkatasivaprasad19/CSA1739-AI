from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.svm import SVC
X,y=load_breast_cancer(return_X_y=True)
a,b,c,d=train_test_split(X,y,test_size=.2,random_state=1)
m=make_pipeline(StandardScaler(),SVC(kernel='linear')).fit(a,c)
print("Accuracy:",m.score(b,d))

# OUTPUT:
# Accuracy: 0.9649122807017544
