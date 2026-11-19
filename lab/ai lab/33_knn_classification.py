from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
X,y=load_iris(return_X_y=True)
a,b,c,d=train_test_split(X,y,test_size=.2,random_state=1)
m=KNeighborsClassifier(3).fit(a,c)
print("Accuracy:",m.score(b,d))
print("Predicted class:",m.predict([[5.1,3.5,1.4,0.2]]))

# OUTPUT:
# Accuracy: 1.0
# Predicted class: [0]
