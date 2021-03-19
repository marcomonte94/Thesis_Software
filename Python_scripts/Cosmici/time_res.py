import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import norm

def time_resolution(t, myBar):

    ev_Su_myBar = np.where(t[:,myBar] != 0)[0]

    if myBar < 20:
        par_BAR = np.arange(20, 40)
    else:
        par_BAR = np.arange(0, 20)

    mu, sigma = np.array([]), np.array([])

    for otherBar in par_BAR:

        ev_Su_otherBar = np.where(t[:,otherBar] != 0)[0]
        ev_GOOD = np.intersect1d(ev_Su_otherBar, ev_Su_myBar)

        dt = t[ev_GOOD, myBar] - t[ev_GOOD, otherBar]

        plt.figure(figsize=[7., 5.])
        plt.rc('font', size=12)
        plt.xlabel('Charge')
        plt.ylabel('Counts')
        ydata, edges, _ = plt.hist(dt, bins=1000, color='blue')
        xdata = 0.5 * (edges[1:] + edges[:-1])

        def gaus(x, a, mu, sigma):
            return a * norm.pdf(x, mu, sigma)

        p0 = [max(ydata), 0, 2]
        popt, pcov = curve_fit(gaus, xdata, ydata, p0)
        print(popt[2])
        sigma = np.append(sigma, popt[2])
        _x = np.linspace(-10, 10, 1000)
        plt.plot(_x, gaus(_x, *popt), color='red')
        plt.xlim(-4, 4)
        #plt.show()
        plt.close()

    return sigma


if __name__ == '__main__':

    path = 'C:/Users/Marco/Desktop/cosmici/5V'
    data = np.fromfile(f'{path}/BAR_Timestamp.bin')
    t = np.reshape(data, (600263, 40))

    res = np.array([])

    for myBar in range(20):
        print(f'Barra numero {myBar}')
        res = np.append(res, time_resolution(t, myBar))

    res = np.reshape(res, (20, 20))
    plt.imshow(res)





