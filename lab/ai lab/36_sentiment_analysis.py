pos={'good','great','love','happy','excellent'}
neg={'bad','worst','hate','sad','poor'}
def sentiment(t):
    w=t.lower().split()
    s=sum(x in pos for x in w)-sum(x in neg for x in w)
    return 'Positive' if s>0 else 'Negative' if s<0 else 'Neutral'
for t in ["I love this great phone","This is the worst movie","It is a phone"]:
    print(t,"->",sentiment(t))

# OUTPUT:
# I love this great phone -> Positive
# This is the worst movie -> Negative
# It is a phone -> Neutral
