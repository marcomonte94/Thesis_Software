import numpy as np
import os
import matplotlib.pyplot as plt


def compute_area(dt, ampl):
    return (ampl*dt).sum()


wf_path = 'C:/Users/Marco/Desktop/Analisi_SiPM/Simulazione/Segnali_2'
allMyData = list(os.listdir(wf_path))
a = []

for i in allMyData:
    print(i)
    wf = np.loadtxt(f'{wf_path}/{i}')
    a.append(compute_area(0.001, wf))

plt.hist(a, bins=8)
plt.show()
