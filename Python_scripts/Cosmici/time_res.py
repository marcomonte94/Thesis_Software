import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import norm


def time_resolution(dt_AB, myBar):

    ev_Su_myBar = np.where(t[:,myBar] != 0)[0]

    if myBar < 19:
        par_BAR = np.arange(20, 40)
    else:
        par_BAR = np.arange(0, 20)

    mu, sigma = np.array([]), np.array([])

    for otherBar in par_BAR:
        ev_Su_otherBar = np.where(t[:,otherBar] != 0)[0]

        ev_GOOD = np.intersect1d(ev_Su_otherBar, ev_Su_myBar)
        plt.figure(figsize=[7., 5.])
        plt.rc('font', size=12)
        plt.xlabel('$\Delta t_{AB}$ [ns]')
        plt.ylabel('Counts')
        plt.xlim(-5,5)
        ydata, edges, _ = plt.hist(t[ev_GOOD, myBar], bins=200)
        xdata = 0.5 * (edges[1:] + edges[:-1])

        def gaus(x, a, mu, sigma):
            return a * norm.pdf(x, mu, sigma)

        p0 = [max(ydata), 0, 2]
        popt, pcov = curve_fit(gaus, xdata, ydata, p0)
        _x = np.linspace(-10, 10, 1000)
        plt.plot(_x, gaus(_x, *popt), color='red')
        plt.show()
        #plt.close()

        mu = np.append(mu, popt[1])
        sigma =  np.append(sigma, popt[2])

    return mu, sigma


if __name__ == '__main__':

    path = 'C:/Users/Marco/Desktop/cosmici'
    '''
    data = np.fromfile(f'{path}/BAR_TimeA.bin')
    a = np.reshape(data, (110000, 40))

    data = np.fromfile(f'{path}/BAR_TimeB.bin')
    b = np.reshape(data, (110000, 40))
    '''
    data = np.fromfile(f'{path}/BAR_DeltaT_AB.bin')
    t = np.reshape(data, (110000, 40))

    m, s = time_resolution(t, 9)
    plt.figure()
    plt.plot(m ,'o')
    plt.figure()
    plt.plot(s ,'o')
    plt.show()
