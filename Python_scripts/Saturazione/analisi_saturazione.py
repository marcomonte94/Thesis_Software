import numpy as np
import os
import argparse
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import norm
'''
laser, curr, dark = np.loadtxt('C:/Users/Marco/Desktop/Analisi_SiPM/Saturazione/photocurrent_200khz.txt', unpack=True)
photocurrent = - (curr - dark)

filepath = 'C:/Users/Marco/Desktop/Analisi_SiPM/Saturazione/aree_200khz.txt' #/aree_8.txt'
#datalist = list(os.listdir(filepath))
#mu, sigma = np.array([]), np.array([])
mu, sigma = np.loadtxt(filepath, unpack=True)

for ifile in datalist:
    print(ifile)
    a = np.loadtxt(f'{filepath}/{ifile}', unpack=True)
    a = a[2500:]
    #plt.plot(a)
    plt.figure()
    plt.title(f'Laser {ifile}')
    ydata, edges, _ = plt.hist(a, bins=80)
    xdata = 0.5 * (edges[1:] + edges[:-1])

    def gaus(x, a, mu, sigma):
        return a * norm.pdf(x, mu, sigma)

    p0 = [max(ydata), np.mean(xdata), np.std(xdata)]
    popt, pcov = curve_fit(gaus, xdata, ydata, p0)#, sigma=np.sqrt(ydata))
    mu = np.concatenate((mu, np.array([popt[1]])))
    sigma = np.concatenate((sigma, np.array([popt[2]])))

    plt.plot(xdata, gaus(xdata, *popt), color='red')

plt.figure()
#photocurrent = photocurrent / 0.37
plt.plot(photocurrent, mu, 'o')
'''
#mu = np.array([55, 100, 118, 130.4, 145.5, 161, 172, 180, 188, 194.6, 200, 202.1, 204.5, 206.8, 208.9])
#photocurrent = np.array([3.2, 7.9, 10.3, 12.4, 15.5, 19.6, 23.6, 27.2, 31.6, 36.8, 41.9, 44.9, 48.6, 52, 56.3])

mu = np.array([67.9, 95.5, 109.3, 121.2, 129.4, 139.2, 146.8, 157.2, 169.6, 175.5, 180.3, 185.6, 189.5, 193.3, 197.2, 200.3, 203.2, 206.3, 207.8, 209.9, 211.6, 213.7, 215.3, 217.4, 217.7])
photocurrent = np.array([5.73, 9.6, 11.9, 14.4, 16.2, 18.7, 20.8, 24, 28.7, 31.6, 34.3, 37.4, 40.2, 43.2, 47.2, 51.5, 53.8, 57.3, 60.8, 64.3, 68.6, 72.9, 77.3, 82.9, 87])
e = 1.6e-19
R = 50
G = 554046.5739371531 # foot
#G = # 50mu
#G = 876702.7516737487 #25mu
#G = 7e5
#G = 1.7e6
Eph = 4.9e-19
responsivity = 0.0732402716282601
nu = 1e5
f = 0.09
Vov = 8.27
dV = (mu / R) * nu * 2000
mu *= 1e-9

G = (G / Vov) *( Vov - (mu / R) * nu  * 2000)
#print(G)
#print(dV)
#sigma *= 1e-9
n_fired = mu / (e * R * G)
n_ph = f * photocurrent / (nu * Eph * responsivity)
#dn =sigma / (e * R * G)

def fitfunc(x, a, b, x0):
    return a *(1 - np.exp(-b*(x-x0)))

p0 = [5000, 1e-15, 1]

popt, pcov = curve_fit(fitfunc, n_ph, n_fired, p0)#, sigma=dn)
print(popt)
plt.figure()
plt.plot(n_ph, n_fired, 'o')
#plt.errorbar(n_ph, n_fired, dn, fmt='.')
_x = np.linspace(0, max(n_ph), 100000)
plt.plot(_x, fitfunc(_x, *popt))

plt.show()