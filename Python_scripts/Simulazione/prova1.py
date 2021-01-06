import numpy as np
from matplotlib import pyplot as plt

def fattoriale(v):
    if len(v) == 1:
        return v[0]
    return v[1]*fattoriale(v[1:])

v = [1, 2, 3, 4]
print(fattoriale(v))


n, epsilon = 4, 0.5
p = 1 - ((1-epsilon)**(1/n))
s = np.random.binomial(n, p, 10000)
bins = np.arange(min(s), max(s), 1)

ydata, edges, _ = plt.hist(s, bins=100)
x = []
a = np.where(ydata>0)

trig = ydata[a] / len(s)

for i in range(1, len(trig)):
    #x.append(fattoriale(trig[:i]))
    x.append(trig[i]*trig[i-1])

print(ydata[a]/len(s))
plt.figure()
plt.plot(x)
plt.yscale('log')
plt.show()
