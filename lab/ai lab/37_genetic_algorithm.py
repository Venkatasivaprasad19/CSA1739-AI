import random
random.seed(1)
f=lambda x:x*x                       # maximise f(x)=x^2, x in 0..31
pop=[random.randint(0,31) for _ in range(6)]
print("Start:",pop)
for g in range(20):
    pop.sort(key=f,reverse=True)
    a,b=pop[0],pop[1]                # selection: best two parents
    for i in range(2,6):
        mask=(1<<random.randint(1,4))-1
        c=(a&~mask)|(b&mask)         # crossover
        if random.random()<.3:c^=1<<random.randint(0,4)   # mutation
        pop[i]=c
best=max(pop,key=f)
print("Final:",pop)
print("Best x =",best,", f(x) =",f(best))

# OUTPUT:
# Start: [8, 4, 16, 7, 31, 28]
# Final: [31, 31, 31, 31, 30, 31]
# Best x = 31 , f(x) = 961
