import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import moyal
from scipy.optimize import curve_fit

def attenuation(charge_A, charge_B, myBar):

    evA_Su_myBar = np.where(charge_A[:,myBar]>0)[0]
    evB_Su_myBar = np.where(charge_B[:,myBar]>0)[0]
    q, dq = np.array([]), np.array([])

    if myBar < 20:
        par_BAR = np.arange(20, 40)
    else:
        par_BAR = np.arange(0, 20)

    for otherBar in par_BAR:

        ev_GOOD_Su_myBar = np.intersect1d(evA_Su_myBar, evB_Su_myBar)
        evA_Su_otherBar = np.where(charge_A[:,otherBar]>0)[0]
        evB_Su_otherBar = np.where(charge_B[:,otherBar]>0)[0]
        ev_GOOD_Su_otherBar = np.intersect1d(evA_Su_otherBar, evB_Su_otherBar)
        ev_GOOD = np.intersect1d(ev_GOOD_Su_otherBar, ev_GOOD_Su_myBar)
        plt.figure(figsize=[7., 5.])
        plt.rc('font', size=12)
        plt.xlabel('Charge')
        plt.ylabel('Counts')
        y, edges, _ = plt.hist(charge_A[ev_GOOD, myBar], bins=50, color='blue', label='Entries')

        x = 0.5 * (edges[1:] + edges[:-1])
        #plt.show()
        def fitfunc(x, a, mu, sigma):
            return a * moyal.pdf(x, mu, sigma)

        p0 = [40, 2, 0.3]
        popt, pcov = curve_fit(fitfunc, x, y, p0=p0, sigma=None)
        _x = np.linspace(0, max(x), 1000)
        plt.plot(_x, fitfunc(_x, *popt), color='red', label='Landau fit')
        q = np.append(q, popt[1])
        dq = np.append(dq, np.sqrt(pcov.diagonal()[1]))
        plt.legend(loc='best')
        #plt.show()
        plt.close()
    xfit, yfit, dy = np.arange(1, 41, 2), q, dq

    def f(x, a, l, c):
        return a * np.exp(-x/l) + c

    p0 = [4, 20, 0.3]
    popt, pcov = curve_fit(f, xfit, yfit, p0=p0, sigma=None)
    print(f'{popt[1]} +- {np.sqrt(pcov.diagonal()[1])}')
    plt.figure(figsize=[7., 5.])
    plt.rc('font', size=12)
    plt.errorbar(xfit, yfit, dy, fmt='.', capsize=2, elinewidth=0.5, color='black')
    plt.plot(xfit, f(xfit, *popt), color='red')
    plt.xlabel('Distance from SiPM [cm]')
    plt.ylabel('Charge')
    plt.close()

    return popt[1]


if __name__ == '__main__':
    path = 'C:/Users/Marco/Desktop/cosmici/5V'
    data = np.fromfile(f'{path}/BAR_ChargeA.bin')
    a = np.reshape(data, (600263, 40))
    data = np.fromfile(f'{path}/BAR_ChargeB.bin')
    b = np.reshape(data, (600263, 40))
    l = np.array([])
    for myBar in range(40):
    #myBar = 3
        l = np.append(l, attenuation(a, b, myBar))

    plt.figure(figsize=[7., 5.])
    h, bins = np.histogram(l, bins=10)
    width = 1* (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2
    plt.bar(center, h, align='center', width=width, color='blue', edgecolor="k")
    plt.xlabel('Attenuation length [cm]')
    plt.ylabel('Occurrences')
    plt.xlim(6, 20)
    plt.show()







