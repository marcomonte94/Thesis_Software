import pylab as plt
import numpy as np
from scipy.optimize import curve_fit

datapath = f'C:/Users/Marco/Desktop/Analisi_SiPM/Caratterizzazione/id31/risultati.txt'
g, dg, ct, d_ct, dcr, d_dcr, af, d_af = np.loadtxt(datapath, unpack=True)
v = np.arange(116, 125)
#v = np.arange(120, 129)

def line(x, a, b):
    return a + b*x

''''

def f(x, a, b, c):
    return a* (x**2)+b*x+c
'''

##GAIN

popt, pcov = curve_fit(line, v, g, sigma=dg)
chi2 = sum(((g - line(v, *popt)) / dg)**2.) / (len(g)-2)

Vbr = -popt[0] / popt[1]
d = np.matrix([-1/popt[1], -Vbr/popt[1]])
dT = np.transpose(d)
pcov = np.matrix(pcov)
dVbr = np.sqrt(d*pcov*dT)
print(f'V Breakdown: {Vbr} +/- {dVbr}')

plt.figure(figsize=[8, 6])
plt.rc('font', size=12)
plt.errorbar((v), g, dg, fmt='.', color='black')
plt.plot((v), line(v, *popt), color='red')
plt.xlabel('v [V]')
plt.ylabel('Gain $[10^5]$')

## CROSSTALK

'''
def f(x, a):
    return a* (x**2)
'''
def f(x, a, b):
    return a *(x) * (1- np.exp(-b*(x)))

xfit, yfit, dy = (v-Vbr)/2, ct, d_ct
p0 = [1,1]

popt, pcov = curve_fit(f, xfit, yfit, p0=p0, sigma=dy)
print(popt)
chi2 = sum(((yfit - f(xfit, *popt)) / dy)**2.) / (len(g)-2)

_x = np.linspace(min(xfit)-0.3, max(xfit)+0.3, 100)
plt.figure(figsize=[8, 6])
plt.rc('font', size=12)
plt.plot(_x, f(_x, *popt), color='blue')
#plt.plot(xfit, yfit, '.', color='black')
plt.errorbar(xfit, yfit, dy, fmt='.', color='black')
plt.ylabel('$P_{cross-pulse} [\%]$')
plt.xlabel('Overvoltage [V]')

## DARK COUNT RATE

def line(x, a,b):
    return a*x+b

xfit, yfit, dy = (v-Vbr)/2, dcr+0.8, d_dcr
p0 = [3, 0.3]
popt, pcov = curve_fit(line, xfit, yfit, p0=p0, sigma=dy)
print(popt)
chi2 = sum(((yfit - line(xfit, *popt)) / dy)**2.) / (len(g)-2)

_x = np.linspace(min(xfit)-0.3, max(xfit)+0.3, 100)
plt.figure(figsize=[8, 6])
plt.rc('font', size=12)
plt.plot(_x, line(_x, *popt), color='blue')
#plt.plot(xfit, yfit, '.', color='black')
plt.errorbar(xfit, yfit, dy, fmt='.', color='black')
plt.ylabel('Dark count rate [MHz]')
plt.xlabel('Overvoltage [V]')

## AFTERPULSE

'''
def f(x, a, b):
    return a *(x**2)

'''

def f(x, a, b):
    return a *(x**2) * (1- np.exp(-b*(x)))

xfit, yfit, dy = (v-Vbr)/2, af, d_af
p0 = [0.03, 0.01]
popt, pcov = curve_fit(f, xfit, yfit, p0=p0, sigma=dy)
print(popt)
chi2 = sum(((yfit - f(xfit, *popt)) / dy)**2.) / (len(g)-2)

_x = np.linspace(min(xfit)-0.3, max(xfit)+0.3, 100)
plt.figure(figsize=[8, 6])
plt.rc('font', size=12)
plt.plot(_x, f(_x, *popt), color='blue')
plt.plot(xfit, yfit, '.', color='black')
#plt.errorbar(xfit, yfit, dy, fmt='.', color='black')
plt.ylabel('$P_{after-pulse} [\%]$')
plt.xlabel('Overvoltage [V]')




plt.show()