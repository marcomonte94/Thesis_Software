import numpy as np
import matplotlib.pyplot as plt
import os
import argparse
from scipy.optimize import curve_fit
from simulazione import readSimBinary, toCells, deleteMissingEvents

def compute_area(wf):
    return sum(wf*0.001)

def birks(x, s, k):
    return s*x / (1 + k*x)

def fit_birks(de, yfit):
    popt, pcov = curve_fit(birks, de, yfit)
    x = np.linspace(0, max(de), 100)
    plt.plot(x, birks(x, *popt), color='red')
    plt.plot(de, yfit, '.', color='black')
    return popt, pcov

def process_data(fileName):

    aa, ab = np.array([]), np.array([])
    wf_path = f'C:/Users/Marco/Desktop/Analisi_SiPM/Simulazione/{fileName}'
    wfList = list(os.listdir(f'{wf_path}/Segnali_1'))
    for i in wfList:
        wf = np.loadtxt(f'{wf_path}/Segnali_1/{i}')
        aa = np.append(aa, compute_area(wf))
    wfList = list(os.listdir(f'{wf_path}/Segnali_2'))
    for i in wfList:
        wf = np.loadtxt(f'{wf_path}/Segnali_2/{i}')
        aa = np.append(ab, compute_area(wf))
    np.savetxt(f'{fileName}/aree.txt', np.sqrt(aa*ab))

    from sipm_struct import dt_evt
    data = readSimBinary(f'C:/Users/Marco/Desktop/Dati_MC/{fileName}_detect1')
    photons_1 = np.array([])
    for i in range(min(data['id_event']), min(data['id_event'])):
        photons = np.append(photons, len(data[data['id_event']==i]))
    data = readSimBinary(f'C:/Users/Marco/Desktop/Dati_MC/{fileName}_detect2')
    photons_2 = np.array([])
    for i in range(min(data['id_event']), min(data['id_event'])):
        photons = np.append(photons, len(data[data['id_event']==i]))
    np.savetxt(f'{fileName}/photons.txt', np.sqrt(photons_1*photons_2))



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Process simulation output')
    parser.add_argument('f', help='Input data')
    args = parser.parse_args()

    process_data(args.f)
    

'''

a = np.array([4.4, 29.7, 35.5, 48])
e = np.array([3.4, 33.4, 42.6, 78.5])



popt, pcov = curve_fit(f, e, a)
x = np.linspace(0, 80, 100)
plt.plot(x, f(x, *popt))
plt.plot(e, a, '.', color='black')
plt.show()
'''