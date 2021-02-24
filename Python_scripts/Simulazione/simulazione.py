import numpy as np
from matplotlib import pyplot as plt
import time
import argparse
from sipm_struct import Microcell, SiPM, run_simulation, dt_evt


def readSimBinary(fileName):
    data = np.fromfile(fileName, dtype=dt_evt)
    return data

def toCells(data):
    data['y'] += 1.5
    data['x'] += 10
    data['x'] = np.floor(data['x'] / 25e-3).astype(int)
    data['y'] = np.floor(data['y'] / 25e-3).astype(int)
    return data

def deleteMissingEvents(data):
    mask1 = np.logical_and(data['x'] > 100, data['x'] < 220)
    mask2 = np.logical_and(data['x'] > 260, data['x'] < 380)
    a = np.logical_or(mask1, mask2)
    mask3 = np.logical_and(data['x'] > 420, data['x'] < 540)
    mask4 = np.logical_and(data['x'] > 580, data['x'] < 700)
    b = np.logical_or(mask3, mask4)
    c = np.logical_or(a, b)
    return data[c]
    


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='SiPM simulation')
    parser.add_argument('-d', '--debug', help='Debug mode', default = '0')
    args = parser.parse_args()

    data = 'C:/Users/Marco/Desktop/results_C115_100ev/detect1.raw'


    if args.debug == '0':

        ncell, pde, dark_count_rate, p_ct, p_af = 57600, 0.2, 3e6, 0.04, 0.12
        data = readSimBinary(data)
        data = toCells(data)
        data = deleteMissingEvents(data)

        for j in range(1, 101):
            print(f'Simulazione di evento {j}\n')
            sipm = SiPM(ncell, pde, dark_count_rate, p_ct, p_af)
            sipm.initialize_sipm()
            a = run_simulation(sipm, data[data['id_event']==j])
            np.savetxt(f'C:/Users/Marco/Desktop/Analisi_SiPM/Simulazione/Segnali_1/wf_{j}.txt', a)

    elif args.debug == '1':
        i = input('Event to debug: ')
        ncell, pde, dark_count_rate, p_ct, p_af = 57600, 0.2, 3e6, 0.04, 0.12
        data = readSimBinary(data)
        data = toCells(data)
        data = deleteMissingEvents(data)        
        print(f'Simulazione di evento {i}\n')
        sipm = SiPM(ncell, pde, dark_count_rate, p_ct, p_af)
        sipm.initialize_sipm()
        a = run_simulation(sipm, data[data['id_event']==(int(i))])
        np.savetxt(f'C:/Users/Marco/Desktop/Analisi_SiPM/Simulazione/Segnali_2/wf_{i}.txt', a)
        plt.figure()
        plt.plot(sipm.all_time, a)
        plt.show()
    