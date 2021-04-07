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
    print(f'{popt[1]} +- {np.sqrt(pcov.diagonal()[1])}')
    return popt, pcov

def birks_inv(x, s, k):
    return x / (s - k*x)

def gaus(x, a, mu, sigma):
    return a * norm.pdf(x, mu, sigma)

def fit_gauss(x, y):
    p0 = [max(y), max(x), 100]
    popt, pcov = curve_fit(gaus, x, y, p0=p0)
    x = np.linspace(min(x), max(x), 200)
    plt.plot(x, gaus(x, *popt), color='red')
    return popt, pcov

datapath = 'C:/Users/Marco/Desktop/Analisi_SiPM/Simulazione/5V'
dataList = list(os.listdir(f'{datapath}'))
de = np.array([78.5, 42.6, 33.4, 3.4])
r = np.array([])

q, ph = np.array([]), np.array([])
l = list(os.listdir(f'{datapath}'))

for i in l:

    print(i)

    fp = f'C:/Users/Marco/Desktop/Analisi_SiPM/Simulazione/5V/{i}/photons_tot.txt'
    fa = f'C:/Users/Marco/Desktop/Analisi_SiPM/Simulazione/5V/{i}/aree.txt'

    a = np.loadtxt(fa)
    p = np.loadtxt(fp)
    ph = np.append(ph, np.mean(p))

    q = np.append(q, np.mean(a))
    #print(a.mean())
    #print(a.std())

    if i == 'results_C1380_Birks3e-3':

        plt.figure()
        plt.rc('font', size=12)
        plt.ylabel('Occurrences')
        plt.xlabel('Charge [a.u.]')
        #plt.xlim(2, 4)
        #plt.title(f'{i} -> aree')

        ydata, edges, _ = plt.hist(a, bins=100, color='blue', label='Entries')
        xdata = 0.5 * (edges[1:] + edges[:-1])
        p0 = [max(ydata), max(xdata), 100]
        popt, pcov = curve_fit(gaus, xdata, ydata, p0=p0)
        x = np.linspace(popt[1]-3*popt[2], popt[1]+3*popt[2], 200)
        plt.plot(x, gaus(x, *popt), color='red', label='Gaussian fit')
        plt.legend(loc='best')
        #q = np.append(q, popt[1])
        #plt.close()

        plt.show()
        plt.figure()
        plt.rc('font', size=12)
        plt.ylabel('Occurrences')
        plt.xlabel('Number of photons')
        #plt.xlim(6000, 8500)
        #plt.title(f'{i} -> photons')
        ydata, edges, _ = plt.hist(p[p<1e5], bins=90, color='blue', label='Entries')
        xdata = 0.5 * (edges[1:] + edges[:-1])
        p0 = [max(ydata), 9e4, 100]
        popt, pcov = curve_fit(gaus, xdata, ydata, p0=p0)
        x = np.linspace(popt[1]-3*popt[2], popt[1]+3*popt[2], 200)
        plt.plot(x, gaus(x, *popt), color='red', label='Gaussian fit')
         #ph = np.append(ph, popt[1])
        plt.legend(loc='best')
        plt.show()
    #plt.close()


plt.figure()
plt.rc('font', size=12)
plt.xlabel('Mean Released Energy [MeV]')
plt.ylabel('Charge [a.u.]')
birks_param_q, _ = fit_birks(de, q)
plt.text(5, 3, 'p 60 MeV')
plt.text(16, 25, 'C 400 MeV/u')
plt.text(44, 27, 'C 260 MeV/u')
plt.text(60, 39, 'C 115 MeV/u')
plt.xlim(0, 80)
plt.ylim(0, 50)
plt.close()


plt.figure()
plt.rc('font', size=12)
plt.xlabel('Mean Released Energy [MeV]')
plt.ylabel('Number of photons')
birks_param_ph, _ = fit_birks(de, ph)
plt.text(5, 4e3, 'p 60 MeV')
plt.text(17, 5.4e4, 'C 400 MeV/u')
plt.text(44, 6e4, 'C 260 MeV/u')
plt.text(60, 9.13e4, 'C 115 MeV/u')
plt.xlim(0, 80)

plt.ylim(0, 120000)
#plt.show()

plt.close()

rph, drph, rq, drq = np.array([]), np.array([]), np.array([]), np.array([])

plt.figure()
plt.rc('font', size=12)
plt.xlabel('Released Energy [MeV]')
plt.ylabel('Occurrences [a.u.]')

for i in l:
    fa = f'C:/Users/Marco/Desktop/Analisi_SiPM/Simulazione/5V/{i}/aree.txt'
    fp = f'C:/Users/Marco/Desktop/Analisi_SiPM/Simulazione/5V/{i}/photons_tot.txt'
    ph = np.loadtxt(fp)
    a = np.loadtxt(fa)
    #print(a.mean())
    bq = birks_inv(a, *birks_param_q)
    bph = birks_inv(ph, *birks_param_ph)

    bph = bph[np.logical_and(bph>0, bph<100)]
    bq = bq[np.logical_and(bq>0, bq<100)]

    if i == 'results_p060_Birks3e-3':

        ydata, edges, _ = plt.hist(bph, bins=200, color='blue', label='Entries')
        xdata = 0.5 * (edges[1:] + edges[:-1])
        p0 = [max(ydata), max(xdata), 10]
        popt, pcov = curve_fit(gaus, xdata, ydata, p0=p0)
        _x = np.linspace(popt[1]-3*popt[2], popt[1]+3*popt[2], 200)
        plt.plot(_x, gaus(_x, *popt), color='red', label='Gaussian fit')
        #popt, pcov = fit_gauss(xdata, ydata)
    else:
        ydata, edges, _ = plt.hist(bph, bins=200, color='blue')
        xdata = 0.5 * (edges[1:] + edges[:-1])
        p0 = [max(ydata), max(xdata), 10]
        popt, pcov = curve_fit(gaus, xdata, ydata, p0=p0)
        _x = np.linspace(popt[1]-3*popt[2], popt[1]+3*popt[2], 200)
        plt.plot(_x, gaus(_x, *popt), color='red')
        #popt, pcov = fit_gauss(xdata, ydata)

    #plt.close()

    delta_ph = np.sqrt(pcov.diagonal()[1]*(1/popt[1])**2 + pcov.diagonal()[2] * (popt[2]/popt[1]**2))
    print(f'PH: Mean: {popt[1]} +- {popt[2]}')
    print(f'PH: Energy resolution for {i}: {100*popt[2]/popt[1]} +- {100*delta_ph}')
    rph = np.append(rph, popt[2]/popt[1])
    drph = np.append(drph, delta_ph)
    plt.legend(loc='best')

    if i == 'results_p060_Birks3e-3':

        ydata, edges, _ = plt.hist(bq, bins=100, color='blue', label='Entries')
        xdata = 0.5 * (edges[1:] + edges[:-1])
        p0 = [max(ydata), max(xdata), 10]
        popt, pcov = curve_fit(gaus, xdata, ydata, p0=p0)
        _x = np.linspace(popt[1]-3*popt[2], popt[1]+3*popt[2], 200)
        plt.plot(_x, gaus(_x, *popt), color='red', label='Gaussian fit')
        #popt, pcov = fit_gauss(xdata, ydata)
    else:
        ydata, edges, _ = plt.hist(bq, bins=100, color='blue')
        xdata = 0.5 * (edges[1:] + edges[:-1])
        p0 = [max(ydata), max(xdata), 10]
        popt, pcov = curve_fit(gaus, xdata, ydata, p0=p0)
        _x = np.linspace(popt[1]-3*popt[2], popt[1]+3*popt[2], 100)
        plt.plot(_x, gaus(_x, *popt), color='red')

    plt.legend(loc='best')
    #plt.close()

    delta_q = np.sqrt(pcov.diagonal()[1]*(1/popt[1])**2 + pcov.diagonal()[2] * (popt[2]/popt[1]**2))
    print(i)
    print(f'Q: Mean: {popt[1]} +- {popt[2]}')


    print(f'Q: Energy resolution for {i}: {100*popt[2]/popt[1]} +- {100*delta_q}')
    rq = np.append(rq, popt[2]/popt[1])
    drq = np.append(drq, delta_q)

#plt.show()


plt.figure()
r_exp = np.array([5.32, 6.16, 6.42, 6.91])
plt.rc('font', size=12)
plt.ylabel('Energy Resolution [%]')
plt.xlabel('Mean Released Energy [MeV]')
#plt.text(5,5, 'ciao')
plt.errorbar(de, rq*100, drq*100, fmt='.', capsize=2, elinewidth=0.5, color='black')
plt.plot(de, rq*100, color='red', label='SiPM model')
drph[-1] = 0.001
plt.errorbar(de, rph*100, drph*100, fmt='.', capsize=2, elinewidth=0.5, color='black')
plt.plot(de, rph*100, color='blue', label='Ideal detector')
plt.ylim(0, 9)
plt.xlim(0, 90)
plt.text(3.5, 4.5, 'p 60 MeV')
plt.text(24, 6.1, 'C 400 MeV/u')
plt.text(43.1, 4.6, 'C 260 MeV/u')
plt.text(70, 1.2, 'C 115 MeV/u')
plt.legend(loc='best')

plt.figure()
r_exp = np.array([5.32, 6.16, 6.42, 6.91])
plt.rc('font', size=12)
plt.ylabel('Energy Resolution [%]')
plt.xlabel('Mean Released Energy [MeV]')
plt.plot(de, r_exp, color='lime', label='Exp. data')
plt.plot(de, r_exp, '.', color='black')
plt.plot(de, rq*100, color='red', label='SiPM model')
plt.errorbar(de, rq*100, drq*100, fmt='.', capsize=2, elinewidth=0.5, color='black')
plt.text(3.5, 5.3, 'p 60 MeV')
plt.text(24, 6.8, 'C 400 MeV/u')
plt.text(43.1, 5.2, 'C 260 MeV/u')
plt.text(70, 2., 'C 115 MeV/u')
plt.ylim(0, 9)
plt.xlim(0, 90)
plt.legend(loc='best')

plt.show()





