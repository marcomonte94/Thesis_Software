import numpy as np
from matplotlib import pyplot as plt
from scipy.special import binom


p1 = (1-p)**n
p2 = n*p*(1-p)**(2*n-1)
p3 = 0.5*n*(3*n-1)*(p**2)*(1-p)**(3*n-2)
p4 = 0.33*n*(8*n**2 -6*n +1)*(p**3)*(1-p)**(4*n-3)

def f(n, c):

    if c == 0:
        return 1

    ris = 0

    for s in range(1, c+1):
        ris += binom(n, s)
        for i in range(c-s-1):

            ris *= f(n, c-s-i)

    return ris



x = [1,2,3,4]
y=[p1, p2, p3, p4]

plt.plot(x,y,'o')
plt.yscale('log')
plt.show()