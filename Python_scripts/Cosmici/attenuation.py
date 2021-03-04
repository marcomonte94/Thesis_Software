import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import moyal
from scipy.optimize import curve_fit

def attenuation(charge_A, charge_B, myBar):

    evA_Su_myBar = np.where(a[:,myBar]>0)[0]
    evB_Su_myBar = np.where(b[:,myBar]>0)[0]
    q, dq = np.array([]), np.array([])

    if myBar < 19:
        par_BAR = np.arange(20, 40)
    else:
        par_BAR = np.arange(0, 20)

    for otherBar in par_BAR:

        ev_GOOD_Su_myBar = np.intersect1d(evA_Su_myBar, evB_Su_myBar)
        evA_Su_otherBar = np.where(a[:,otherBar]>0)[0]
        evB_Su_otherBar = np.where(b[:,otherBar]>0)[0]
        ev_GOOD_Su_otherBar = np.intersect1d(evA_Su_otherBar, evB_Su_otherBar)
        ev_GOOD = np.intersect1d(ev_GOOD_Su_otherBar, ev_GOOD_Su_myBar)
        plt.figure(figsize=[7., 5.])
        plt.rc('font', size=12)
        plt.xlabel('Charge')
        plt.ylabel('Counts')
        y, edges, _ = plt.hist(a[ev_GOOD, myBar], bins=50, color='blue')

        x = 0.5 * (edges[1:] + edges[:-1])
        #plt.show()
        def fitfunc(x, a, mu, sigma):
            return a * moyal.pdf(x, mu, sigma)

        p0 = [40, 2, 0.3]
        popt, pcov = curve_fit(fitfunc, x, y, p0=p0, sigma=None)
        _x = np.linspace(0, max(x), 1000)
        plt.plot(_x, fitfunc(_x, *popt), color='red')
        q = np.append(q, popt[1])
        dq = np.append(dq, np.sqrt(pcov.diagonal()[1]))
        #plt.show()
        plt.close()
    xfit, yfit, dy = np.arange(1, 41, 2), q, dq

    def f(x, a, l, c):
        return a * np.exp(-x/l) + c

    p0 = [4, 20, 0.3]
    popt, pcov = curve_fit(f, xfit, yfit, p0=p0, sigma=None)
    print(popt)
    plt.figure(figsize=[7., 5.])
    plt.rc('font', size=12)
    plt.errorbar(xfit, yfit, dy, fmt='.', capsize=2, elinewidth=0.5, color='black')
    plt.plot(xfit, f(xfit, *popt), color='red')
    plt.xlabel('Distance from SiPM [cm]')
    plt.ylabel('Charge')
    plt.show()


if __name__ == '__main__':
    path = 'C:/Users/Marco/Desktop/cosmici'
    data = np.fromfile(f'{path}/BAR_ChargeA.bin')
    a = np.reshape(data, (110000, 40))
    data = np.fromfile(f'{path}/BAR_ChargeB.bin')
    b = np.reshape(data, (110000, 40))
    myBar = 3
    attenuation(a, b, myBar)
