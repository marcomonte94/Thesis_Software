import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import InterpolatedUnivariateSpline

vov = np.array([2, 3, 4, 5, 6, 7, 8, 9])
pde = np.array([0.12, 0.17, 0.22, 0.25, 0.27, 0.283, 0.293, 0.3])*0.68
s3 = InterpolatedUnivariateSpline(vov, pde, k=3)

plt.figure(figsize=[8, 5])
plt.rc('font', size=12)
v = np.linspace(2, 9, 100)
plt.plot(v, s3(v), color='blue')
plt.xlabel('Wavelength [nm]')
plt.ylabel('Responsivity [A/W]')
plt.show()
