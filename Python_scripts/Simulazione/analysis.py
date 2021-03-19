import numpy as np
import matplotlib.pyplot as plt
import os
import argparse
from scipy.optimize import curve_fit
from simulazione import readSimBinary, toCells, deleteMissingEvents

def compute_area(wf):
    dt = 500 / len(wf)
    return sum(wf*dt)


def process_data(v, fileName):

    aa, ab = np.array([]), np.array([])
    wf_path = f'C:/Users/Marco/Desktop/Analisi_SiPM/Simulazione/{v}V/{fileName}'

    wfList = list(os.listdir(f'{wf_path}/Segnali_1'))
    for i in wfList:
        #print(i)
        wf = np.loadtxt(f'{wf_path}/Segnali_1/{i}')
        aa = np.append(aa, compute_area(wf))
    wfList = list(os.listdir(f'{wf_path}/Segnali_2'))
    for i in wfList:
        #print(i)
        wf = np.loadtxt(f'{wf_path}/Segnali_2/{i}')
        ab = np.append(ab, compute_area(wf))
    np.savetxt(f'{wf_path}/aree.txt', np.sqrt(aa*ab))





if __name__ == '__main__':

    for v in range(2, 3):
        print(v)
        wf_path = f'C:/Users/Marco/Desktop/Analisi_SiPM/Simulazione/{v}V'
        wf_list = list(os.listdir(f'{wf_path}'))

        for i in wf_list:
            if i == 'results_C3120_Birks3e-3':
                print(i)
                process_data(v, i)











