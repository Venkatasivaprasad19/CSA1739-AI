from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
X,y=load_digits(return_X_y=True)                  # 8x8 digit images
a,b,c,d=train_test_split(X/16,y,test_size=.2,random_state=0)
m=MLPClassifier((32,),max_iter=300,random_state=0).fit(a,c)
print("Test accuracy:",m.score(b,d))

# OUTPUT:
# Test accuracy: 0.9777777777777777
