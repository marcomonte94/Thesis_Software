import pylab as plt
import numpy as np

i_ref = np.array([1.86, 2.55, 3.28, 4.67, 5.71]) * 1e-6
i_cal = np.array([78, 106, 135, 191, 232]) * 1e-9

def f(x, a):
    return a * x

popt, pcov = curve_fit(f, i_ref, i_cal)

plt.plot(i_ref, i_cal, '.', color='black')
x = np.linspace(0, max(i_ref), 100)
plt.plot(x, f(x, *popt), color='red')
plt.show()