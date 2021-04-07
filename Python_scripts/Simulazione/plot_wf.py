import numpy as np
import matplotlib.pyplot as plt

path = f'C:/Users/Marco/Desktop/Analisi_SiPM/Simulazione/5V/results_C1380_Birks3e-3/Segnali_1/wf_1.txt'
a = np.loadtxt(path)
#a = A / max(a)
t = np.arange(0, 500, 0.1)
x, y = t[t<200], a[t<200]
print(f'Area curva: {sum(a*0.001)}')

_x = np.loadtxt('C:/Users/Marco/Desktop/Analisi_SiPM/Simulazione/x.txt')
_y = np.loadtxt('C:/Users/Marco/Desktop/Analisi_SiPM/Simulazione/y.txt')

_x = _x*1e9 -73
mask = _x>0

plt.figure()
plt.rc('font', size=12)
y = y/(min(y))
plt.plot(x, y, color='blue', label='Simulated wf')
plt.plot(_x[mask],_y[mask], color='orange', label='Experimental wf')

plt.xlabel('Time [ns]')
plt.ylabel('Normalized amplitude [a.u]')
plt.legend(loc='best')

plt.show()