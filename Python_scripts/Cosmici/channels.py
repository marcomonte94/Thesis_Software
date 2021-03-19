import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import moyal
from scipy.optimize import curve_fit

def charge_map(q, myBar):

    ev_Su_myBar = np.where(q[:,myBar] != 0)[0]

    if myBar < 20:
        par_BAR = np.arange(20, 40)
    else:
        par_BAR = np.arange(0, 20)

    m, dm = np.array([]), np.array([])

    for otherBar in par_BAR:


        ev_Su_otherBar = np.where(q[:,otherBar] != 0)[0]
        ev_GOOD = np.intersect1d(ev_Su_otherBar, ev_Su_myBar)
        plt.figure(figsize=[7., 5.])
        plt.rc('font', size=12)
        plt.xlabel('Charge')
        plt.ylabel('Counts')
        ydata, edges, _ = plt.hist(q[ev_GOOD, myBar], bins=100, color='blue')
        xdata = 0.5 * (edges[1:] + edges[:-1])

        def fitfunc(x, a, mu, sigma):
            return a * moyal.pdf(x, mu, sigma)

        p0 = [40, 2, 0.3]
        popt, pcov = curve_fit(fitfunc, xdata, ydata, p0=p0, sigma=None)
        _x = np.linspace(0, max(xdata), 100)
        plt.plot(_x, fitfunc(_x, *popt), color='red')
        m = np.append(m, popt[1])
        #plt.show()
        plt.close()
    return m

if __name__ == '__main__':

    path = 'C:/Users/Marco/Desktop/cosmici/5V'
    data = np.fromfile(f'{path}/BAR_Charge.bin')
    q = np.reshape(data, (600263, 40))

    res = np.array([])

    for myBar in range(20):
        print(f'Barra numero {myBar}')
        res = np.append(res, charge_map(q, myBar))

    res = np.reshape(res, (20, 20))
    plt.imshow(res)

