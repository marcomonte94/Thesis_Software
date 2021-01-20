import numpy as np
import os
import argparse
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import norm

laser, curr, dark = np.loadtxt('C:/Users/Marco/Desktop/Analisi_SiPM/Saturazione/photocurrent.txt', unpack=True)
photocurrent = - (curr - dark)

filepath = 'C:/Users/Marco/Desktop/Analisi_SiPM/Saturazione/Aree' #/aree_8.txt'
datalist = list(os.listdir(filepath))
mu, sigma = np.array([]), np.array([])

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
plt.plot(photocurrent, mu, 'o')

e = 1.6e-19
R = 50
G = 554046.5739371531
Eph = 4.9e-19
responsivity = 0.067
nu = 1e6
f = 0.36
Vov = 8.5
dV = (mu / R) * nu * 2000

G = (G / Vov) *( Vov - (mu / R) * nu /2 * 2000) 
print(G)
print(dV)
n_fired = mu / (e * R * G)
n_ph = f * photocurrent / (nu * Eph * responsivity)

def fitfunc(x, a, b):
    return a *(1 - np.exp(-b*x)) 

p0 = [40000, 1e-5]

popt, pcov = curve_fit(fitfunc, n_ph, n_fired, p0)
print(popt)
plt.figure()

plt.plot(n_ph, n_fired, '.', color='black')
plt.plot(n_ph, fitfunc(n_ph, *popt))

plt.show()