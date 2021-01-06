import numpy as np
from matplotlib import pyplot as plt

def shift(xs, n):
    # N.B. n = numero posizioni dentro l'array!
    if n >= 0:
        return np.concatenate((np.full(n, 0), xs[:-n]))
    else:
        return np.concatenate((xs[-n:], np.full(-n, 0)))

timestamps = np.arange(1., 50, 1)
t = np.arange(0, 2000, 5)

tau = 300

v = np.exp(-t/tau)
vtot = np.zeros(len(t))

for i in timestamps:
    v1 = shift(v, int(i))
    vtot += v1

plt.plot(t, vtot)
plt.show()