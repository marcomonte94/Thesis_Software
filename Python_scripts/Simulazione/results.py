import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.optimize import curve_fit
from scipy.stats import norm

def birks(x, s, k):
    return s*x / (1 + k*x)

def fit_birks(de, yfit):
    popt, pcov = curve_fit(birks, de, yfit)
    x = np.linspace(0, max(de), 100)
    plt.plot(x, birks(x, *popt), color='red')
    plt.plot(de, yfit, '.', color='black')
    return popt, pcov

def birks_inv(x, s, k):
    return x / (s - k*x)

def gaus(x, a, mu, sigma):
    return a * norm.pdf(x, mu, sigma)

def fit_gauss(x, y):
    p0 = [max(y), max(x), 100]
    popt, pcov = curve_fit(gaus, x, y, p0=p0)
    #x = np.linspace(min(x), max(x), 100)
    #plt.plot(x, gaus(x, *popt), color='red')
    return popt, pcov

datapath = 'C:/Users/Marco/Desktop/Analisi_SiPM/Simulazione/'
dataList = list(os.listdir(f'{datapath}'))
v = np.array([2, 4, 6, 8])
de = np.array([78.5, 42.6, 33.4, 3.4])
r, dr = np.array([]), np.array([])

for i in v:

    print(i)

    wfpath = f'{datapath}/{i}V'
    wfList = list(os.listdir(f'{wfpath}'))
    q = np.array([])

    for j in wfList:

        fa = f'{datapath}/{i}V/{j}/aree.txt'
        a = np.loadtxt(fa)
        q = np.append(q, np.mean(a))


    birks_param_q, _ = fit_birks(de, q)
    plt.close()
    bq = birks_inv(a, *birks_param_q)
    ydata, edges, _ = plt.hist(bq, bins=100, color='blue', label='Entries')
    xdata = 0.5 * (edges[1:] + edges[:-1])
    p0 = [max(ydata), max(xdata), 10]
    popt, pcov = curve_fit(gaus, xdata, ydata, p0=p0)
    _x = np.linspace(popt[1]-3*popt[2], popt[1]+3*popt[2], 200)
    plt.plot(_x, gaus(_x, *popt), color='red', label='Gaussian fit')
    plt.close()
    print(f'{popt[1]} +- {popt[2]}')
    r = np.append(r, popt[2]/popt[1])
    delta_q = np.sqrt(pcov.diagonal()[1]*(1/popt[1])**2 + pcov.diagonal()[2] * (popt[2]/popt[1]**2))
    dr = np.append(dr, delta_q)

plt.figure()
rr = np.array([0.0671818,  0.06097297, 0.0600961 , 0.059819811])*100
drr = np.array([0.00098564, 0.0011049, 0.00053591 , 0.00083335])*100
plt.errorbar(v, rr, drr, fmt='.', capsize=2, elinewidth=0.5, color='black')
plt.plot(v, rr, color='red')
plt.ylim(5, 7.5)
plt.ylabel('Energy Resolution [%]')
plt.xlabel('Overvoltage [V]')




plt.show()




