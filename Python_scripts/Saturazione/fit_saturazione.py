import numpy as np
import os
import argparse
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import norm

laser, curr, dark = np.loadtxt('C:/Users/Marco/Desktop/Analisi_SiPM/Saturazione/photocurrent_200khz.txt', unpack=True)
photocurrent = - (curr - dark)

filepath = 'C:/Users/Marco/Desktop/Analisi_SiPM/Saturazione/aree_200khz.txt' #/
mu, sigma = np.loadtxt(filepath, unpack=True)
mu *= 1e-9
sigma *= 1e-9

plt.figure()
plt.plot(photocurrent, mu, 'o')

e = 1.6e-19
R = 50
G = 554046.5739371531 # foot
Vbd = 103.39807277259733
Eph = 4.9e-19
responsivity = 0.0732402716282601
nu = 2e5
f = 0.09
Vov = (120 - Vbd) / 2
dV = (mu / R) * nu * 2000

G = (G / Vov) *( Vov - (mu / R) * nu  * 2000)
#print(G)
#print(dV)
n_fired = mu / (e * R * G)
n_ph = f * photocurrent / (nu * Eph * responsivity)
dn =sigma / (e * R * G)

def fitfunc(x, a, b):
    return a *(1 - np.exp(-b*x))

p0 = [40000, 1e-7]

popt, pcov = curve_fit(fitfunc, n_ph, n_fired, p0, sigma=dn)
print(popt)
plt.figure()

plt.errorbar(n_ph, n_fired, dn, fmt='.')
_x = np.linspace(0, max(n_ph), 100000)
plt.plot(_x, fitfunc(_x, *popt))

plt.show()


