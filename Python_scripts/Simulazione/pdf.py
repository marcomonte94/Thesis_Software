import numpy as np
import matplotlib.pyplot as plt

dcr = 3e4
n = np.random.poisson(dcr, size=100)
plt.figure()
plt.hist(n, bins=100)

p_ct = 0.05
nearest_cells = 4
p = 1 - ((1-p_ct)**(1/nearest_cells))
n_ct = np.random.binomial(nearest_cells, p, size=100000)
plt.figure()
plt.hist(n_ct, bins=100)

tau_af = 100
taf = np.random.exponential(tau_af, size=100000)
plt.figure()
plt.hist(taf, bins=int(taf.std()))
plt.show()