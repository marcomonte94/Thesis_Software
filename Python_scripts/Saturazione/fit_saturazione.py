import numpy as np
import os
import argparse
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def light_calibration(photocurrent):

    i_ref = np.array([1.86, 2.55, 3.28, 4.67, 5.71]) * 1e-6
    i_cal = np.array([78, 106, 135, 191, 232]) * 1e-9

    def f(x, a):
        return a * x

    popt, _ = curve_fit(f, i_ref, i_cal)
    return photocurrent * popt



Eph = 4.9e-19 # Laser photon energy
responsivity = 0.0732402716282601 # Responsivity of calibrated PD
nu = 1e5 # Laser frequency
Vov = 8.27 # SiPM overvoltage
e = 1.6e-19 # Elementary charge
R = 50 # Oscilloscope resistance
G = 551357.040194198 # FOOT SiPM gain (V = 120)
f = 1.2

Q = np.array([67.9, 95.5, 109.3, 121.2, 129.4, 139.2, 146.8, 157.2, 169.6, 175.5, 180.3, 185.6, 189.5, 193.3, 197.2, 200.3, 203.2, 206.3, 207.8, 209.9, 211.6, 213.7, 215.3, 217.4, 217.7]) * 1e-9 / R # Measured charge

photocurrent = np.array([5.73, 9.6, 11.9, 14.4, 16.2, 18.7, 20.8, 24, 28.7, 31.6, 34.3, 37.4, 40.2, 43.2, 47.2, 51.5, 53.8, 57.3, 60.8, 64.3, 68.6, 72.9, 77.3, 82.9, 87]) *1e-9 # Measured photocurrent (reference PD)

dQ = np.loadtxt('C:/Users/Marco/Desktop/Analisi_SiPM/Saturazione/prova.txt', usecols=(0), unpack=True)* 1e-9 / R

dp = np.loadtxt('C:/Users/Marco/Desktop/Analisi_SiPM/Saturazione/prova.txt', usecols=(1), unpack=True)

photocurrent = light_calibration(photocurrent)

dV = Q * nu * 2000
G = (G / Vov) *( Vov - Q * nu  * 2000)

n_ph = f * photocurrent / (nu * Eph * responsivity)
dnph = f * dp / (nu * Eph * responsivity)
n_fired = Q / (e * G)
dncell = dQ / (e * G)

plt.figure(figsize=[7., 5.])
plt.rc('font', size=12)
plt.plot(dV, G/1e5, color='blue')
plt.plot(dV, G/1e5, '.', color='black')
plt.xlabel('$\Delta V$ [V]')
plt.ylabel('SiPM gain [$10^5$]')



def fitfunc(x, a, b):
    #return a *(1 - np.exp(-b*(x)))
    return a * (1 - np.exp(-x*b/a))

p0 = [5000, 1e-1]

popt, pcov = curve_fit(fitfunc, n_ph, n_fired, p0)#, sigma=dncell)
a, b = popt[0], popt[1]
da, db1 = np.sqrt(pcov.diagonal())[0], np.sqrt(pcov.diagonal())[1]
print(popt)

dy = (a*b * np.exp(-b*n_ph) * dnph) ** 2
dy += (da * (1 - np.exp(-b*n_ph))) ** 2
dy += (a*n_ph * np.exp(-b*n_ph) * db1) ** 2
#dy = np.sqrt(dy)

chi2 = sum(((n_fired - fitfunc(n_ph, *popt)) / np.sqrt(dy))**2.)
print(chi2 / (len(Q)-2))

plt.figure(figsize=[7., 5.])
plt.rc('font', size=12)
#plt.plot(n_ph, n_fired, '.', color='black')
plt.errorbar(n_ph, n_fired, dncell, dnph, fmt='.', capsize=2, elinewidth=0.5, color='black')
_x = np.linspace(0, max(n_ph), 100000)
plt.plot(_x, fitfunc(_x, *popt), color='red')
plt.xlabel('$N_{photon}$')
plt.ylabel('$N_{fired}$')

plt.show()

