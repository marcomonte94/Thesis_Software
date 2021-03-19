import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.optimize import curve_fit
from scipy.stats import norm

datapath = 'C:/Users/Marco/Desktop/Analisi_SiPM/Simulazione/5V'
dataList = list(os.listdir(f'{datapath}'))
de = np.array([78.5, 42.6, 33.4, 3.4])
r = np.array([])

q, ph = np.array([]), np.array([])
l = list(os.listdir(f'{datapath}'))
for i in l:

    print(i)

    fp = f'C:/Users/Marco/Desktop/Analisi_SiPM/Simulazione/5V/{i}/photons.txt'
    fa = f'C:/Users/Marco/Desktop/Analisi_SiPM/Simulazione/5V/{i}/aree.txt'

    a = np.loadtxt(fa)
    p = np.loadtxt(fp)
    ph = np.append(ph, np.mean(p))

    q = np.append(q, np.mean(a))
    #print(a.mean())
    #print(a.std())
    '''
    plt.figure()
    plt.title(f'{i} -> aree')
    ydata, edges, _ = plt.hist(a, bins=100)
    xdata = 0.5 * (edges[1:] + edges[:-1])
    popt, pcov = fit_gauss(xdata, ydata)
    q = np.append(q, popt[1])
    plt.close()


    plt.figure()
    plt.title(f'{i} -> photons')
    ydata, edges, _ = plt.hist(p[p<1e5], bins=50)
    xdata = 0.5 * (edges[1:] + edges[:-1])
    popt, pcov = fit_gauss(xdata, ydata)
    ph = np.append(ph, popt[1])
    #plt.close()
    '''


plt.figure()
birks_param_q, _ = fit_birks(de, q)
birks_param_ph, _ = fit_birks(de, ph)

rph, drph, rq, drq = np.array([]), np.array([]), np.array([]), np.array([])

plt.figure()
for i in l:
    fa = f'C:/Users/Marco/Desktop/Analisi_SiPM/Simulazione/5V/{i}/aree.txt'
    fp = f'C:/Users/Marco/Desktop/Analisi_SiPM/Simulazione/5V/{i}/photons.txt'
    ph = np.loadtxt(fp)
    a = np.loadtxt(fa)
    #print(a.mean())
    bq = birks_inv(a, *birks_param_q)
    bph = birks_inv(ph, *birks_param_ph)

    bph = bph[np.logical_and(bph>0, bph<100)]
    ydata, edges, _ = plt.hist(bph, bins=200)
    xdata = 0.5 * (edges[1:] + edges[:-1])
    p0 = [max(ydata), max(xdata), 10]
    popt, pcov = curve_fit(gaus, xdata, ydata, p0=p0)
    plt.plot(xdata, gaus(xdata, *popt), color='red')
    popt, pcov = fit_gauss(xdata, ydata)
    plt.close()
    delta_q = np.sqrt(pcov.diagonal()[1]*(1/popt[1])**2 + pcov.diagonal()[2] * (popt[2]/popt[1]**2))
    print(f'Energy resolution for {i}: {popt[2]/popt[1]} +- {delta_e}')
    rph = np.append(rph, popt[2]/popt[1])
    drph = np.append(drph, delta_e)

    bq = bq[np.logical_and(bq>0, bq<100)]
    ydata, edges, _ = plt.hist(bq, bins=200)
    xdata = 0.5 * (edges[1:] + edges[:-1])
    p0 = [max(ydata), max(xdata), 10]
    popt, pcov = curve_fit(gaus, xdata, ydata, p0=p0)
    plt.plot(xdata, gaus(xdata, *popt), color='red')
    popt, pcov = fit_gauss(xdata, ydata)
    plt.close()
    delta_e = np.sqrt(pcov.diagonal()[1]*(1/popt[1])**2 + pcov.diagonal()[2] * (popt[2]/popt[1]**2))
    print(f'Energy resolution for {i}: {popt[2]/popt[1]} +- {delta_e}')
    rq = np.append(rq, popt[2]/popt[1])
    drq = np.append(drq, delta_e)

plt.figure(figsize=[7., 5.])
plt.rc('font', size=12)
plt.ylabel('Energy Resolution [%]')
plt.xlabel('Mean Released Energy [MeV]')
#plt.text(5,5, 'ciao')
plt.errorbar(de, rq*100, drq*100, fmt='.', capsize=2, elinewidth=0.5, color='black')
plt.plot(de, rq*100, color='red', label='Charge')
plt.errorbar(de, rph*100, drph*100, fmt='.', capsize=2, elinewidth=0.5, color='black')
plt.plot(de, rph*100, color='blue', label='Photons')
plt.legend(loc='best')

plt.show()





