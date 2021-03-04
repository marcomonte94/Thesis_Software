import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import moyal
from scipy.optimize import curve_fit

path = 'C:/Users/Marco/Desktop/cosmici'

data = np.fromfile(f'{path}/BAR_ChargeA.bin')
a = np.reshape(data, (110000, 40))

data = np.fromfile(f'{path}/BAR_ChargeB.bin')
b = np.reshape(data, (110000, 40))

myBar = 10


evA_Su_BARmyBar = np.where(a[:,myBar]>0)[0]
evB_Su_BARmyBar = np.where(b[:,myBar]>0)[0]

q, dq = [], []

for otherBar in range(20, 40):

    ev_GOOD_Su_BARmyBar = np.intersect1d(evA_Su_BARmyBar, evB_Su_BARmyBar)

    evA_Su_BARotherBar = np.where(a[:,otherBar]>0)[0]
    evB_Su_BARotherBar = np.where(b[:,otherBar]>0)[0]

    ev_GOOD_Su_BARotherBar = np.intersect1d(evA_Su_BARotherBar, evB_Su_BARotherBar)

    ev_GOOD = np.intersect1d(ev_GOOD_Su_BARotherBar, ev_GOOD_Su_BARmyBar)

    y, edges, _ = plt.hist(a[ev_GOOD, myBar], bins=50)
    plt.close()
    x = 0.5 * (edges[1:] + edges[:-1])
    #plt.hist(b[ev_GOOD, myBar], bins=50)

    def fitfunc(x, a, mu, sigma):
        return a * moyal.pdf(x, mu, sigma)

    p0 = [40, 2, 0.3]
    popt, pcov = curve_fit(fitfunc, x, y, p0=p0, sigma=None)
    q.append(popt[1])
    dq.append(np.sqrt(pcov.diagonal()[1]))

'''
print(f'Media A: {a[ev_GOOD, myBar].mean()}')
_x = np.linspace(0, max(x), 1000)
plt.plot(_x, fitfunc(_x, *popt))
print(f'Media B: {b[ev_GOOD, myBar].mean()}')
'''
q, dq = np.array(q), np.array(dq)
x = np.arange(0,len(q))
def fitfunc(x, a, l, c):
    return a * np.exp(-x/l) + c

p0 = [40, 20, 0.3]
popt, pcov = curve_fit(fitfunc, x, q, p0=p0, sigma=None)
print(popt)
plt.errorbar(x,q, dq, fmt='.')
plt.plot(x, fitfunc(x, *popt))

plt.show()














