import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import InterpolatedUnivariateSpline

r = np.loadtxt('C:/Users/Marco/Desktop/Analisi_SiPM/Saturazione/responsivity.txt')
l = np.arange(350, 1110, 10)
s3 = InterpolatedUnivariateSpline(l, r, k=3)
print(s3(405))
plt.figure(figsize=[8, 5])
plt.rc('font', size=12)
plt.plot(l, s3(l), color='blue')
plt.xlabel('Wavelength [nm]')
plt.ylabel('Responsivity [A/W]')
plt.show()