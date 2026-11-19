import torch,torch.nn as nn
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
X,y=load_digits(return_X_y=True)                  # 8x8 digit images
a,b,c,d=train_test_split(X/16,y,test_size=.2,random_state=0)
a,b=torch.FloatTensor(a),torch.FloatTensor(b)
c,d=torch.LongTensor(c),torch.LongTensor(d)
torch.manual_seed(0)
net=nn.Sequential(nn.Linear(64,32),nn.ReLU(),nn.Linear(32,10))
opt=torch.optim.Adam(net.parameters(),0.01);loss=nn.CrossEntropyLoss()
for e in range(100):
    opt.zero_grad();l=loss(net(a),c);l.backward();opt.step()
print("Final loss:",round(l.item(),4))
print("Test accuracy:",(net(b).argmax(1)==d).float().mean().item())

# OUTPUT:
# (Not run here: PyTorch could not be installed in my sandbox. Run it and note your output.
# Expected: test accuracy around 0.95 to 0.98.)
