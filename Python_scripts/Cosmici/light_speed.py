import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import norm


def light_speed(dt_AB, myBar):

    ev_Su_myBar = np.where(t[:,myBar] != 0)[0]

    if myBar < 20:
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
        #plt.show()
        plt.close()

        mu = np.append(mu, popt[1])
        sigma =  np.append(sigma, popt[2])

    def line(x, a, b):
        return a*x + b

    x = np.arange(1, 41, 2) - 19
    popt, pcov = curve_fit(line, x, mu)
    print(popt[0])

    plt.figure()
    _x = np.linspace(-19, 19, 100)
    plt.plot(_x, line(_x, *popt), color='red')
    plt.plot(x, mu, '.', color='black')
    plt.close()
    #plt.show()

    return popt[0]


if __name__ == '__main__':

    path = 'C:/Users/Marco/Desktop/cosmici/5V'
    data = np.fromfile(f'{path}/BAR_DeltaT_AB.bin')
    t = np.reshape(data, (600263, 40))
    m = np.array([])

    for myBar in range(40):
        print(f'Barra numero {myBar}')
        m = np.append(m, light_speed(t, myBar))


    plt.figure()
    plt.hist(m, bins=40)
    plt.show()

