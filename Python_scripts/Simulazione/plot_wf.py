import numpy as np
import matplotlib.pyplot as plt

path = f'C:/Users/Marco/Desktop/Analisi_SiPM/Simulazione/results_C1380_Birks3e-3/Segnali_1/wf_1.txt'
a = np.loadtxt(path)
t = np.arange(0, 500, 0.001)
x, y = t[t<200], a[t<200]

print(f'Area curva: {sum(a*0.001)}')



plt.figure(figsize=[7., 5.])
plt.rc('font', size=12)
plt.plot(x, y, color='blue')
plt.xlabel('Time [ns]')
plt.ylabel('Amplitude [V]')
plt.show()