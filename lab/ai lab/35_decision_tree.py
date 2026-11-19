from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
X,y=load_iris(return_X_y=True)
a,b,c,d=train_test_split(X,y,test_size=.2,random_state=1)
m=DecisionTreeClassifier().fit(a,c)
print("Accuracy:",m.score(b,d))
print("Predicted class:",m.predict([[6.0,3.0,4.8,1.8]]))

# OUTPUT:
# Accuracy: 0.9666666666666667
# Predicted class: [2]
