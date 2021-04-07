import numpy as np
from matplotlib import pyplot as plt
import time
import argparse
from sipm_struct import Microcell, SiPM, run_simulation, dt_evt
import time


def readSimBinary(fileName):
    data = np.fromfile(fileName, dtype=dt_evt)
    return data

def toCells(data):
    data['y'] += 1.5
    data['x'] += 10
    data['x'] = np.floor(data['x'] / 25e-3).astype(int)-1
    data['y'] = np.floor(data['y'] / 25e-3).astype(int)-1
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
    parser.add_argument('f', help='Input data')
    parser.add_argument('-l', '--side', help='Bar side (1 -> A, 2 -> B)')
    parser.add_argument('-v', '--ov', help='SiPM overvoltage')
    parser.add_argument('-d', '--debug', help='Debug mode', default = '0')
    parser.add_argument('-w', '--graphs', help='Graph mode', default = '0')
    args = parser.parse_args()

    data = f'C:/Users/Marco/Desktop/Dati_MC/{args.f}/detect{args.side}.raw'
    data = readSimBinary(data)
    data = toCells(data)
    data = deleteMissingEvents(data)

    np.random.seed(0)


    if args.debug == '0':

        #ncell, pde, dark_count_rate, p_ct, p_af = 57600, 0.2, 3e6, 0.04, 0.12
        if args.ov == '2':
            ncell, pde, dark_count_rate, p_ct, p_af = 57600, 0.08, 1.17e6, 0.009, 0.017 # 6 OV
        elif args.ov == '3':
            ncell, pde, dark_count_rate, p_ct, p_af = 57600, 0.11, 1.64e6, 0.013, 0.027 # 6 OV
        elif args.ov == '4':
            ncell, pde, dark_count_rate, p_ct, p_af = 57600, 0.15, 2.1e6, 0.017, 0.034 # 6 OV
        elif args.ov == '5':
            ncell, pde, dark_count_rate, p_ct, p_af = 57600, 0.17, 2.6e6, 0.022, 0.044 # 6 OV
        elif args.ov == '6':
            ncell, pde, dark_count_rate, p_ct, p_af = 57600, 0.18, 3e6, 0.027, 0.053 # 6 OV
        elif args.ov == '7':
            ncell, pde, dark_count_rate, p_ct, p_af = 57600, 0.19, 3.5e6, 0.036, 0.083 # 6 OV
        elif args.ov == '8':
            ncell, pde, dark_count_rate, p_ct, p_af = 57600, 0.199, 4e6, 0.044, 0.12 # 6 OV
        elif args.ov == '9':
            ncell, pde, dark_count_rate, p_ct, p_af = 57600, 0.2, 4.5e6, 0.054, 0.15 # 6 OV

        for j in range(1, 101):
            print(f'Simulazione di evento {j}\n')
            sipm = SiPM(ncell, pde, dark_count_rate, p_ct, p_af)
            sipm.initialize_sipm()
            #k = j+140
                        
            #print(f'C:/Users/Marco/Desktop/Simulazione/{args.f}/Segnali_{args.side}/wf_{k}.txt')

            a = run_simulation(sipm, data[data['id_event']==j])
            np.savetxt(f'C:/Users/Marco/Desktop/Analisi_SiPM/Simulazione/{args.ov}V/{args.f}/Segnali_{args.side}/wf_{j}.txt', a)

    elif args.debug == '1':

        if args.graphs == '1':
            plt.figure(figsize=[7., 5.])
            plt.rc('font', size=12)
            plt.xlabel('Distance from left side [mm]')
            plt.ylabel('Occurrences')
            plt.hist(data['x']*25e-3, bins=np.linspace(0, 20, 800))
            plt.xlim(0, 20)
            plt.figure()
            plt.hist(data['time'], bins=len(data))

        i = input('Event to debug: ')
        ncell, pde, dark_count_rate, p_ct, p_af = 57600, 0.2, 3e6, 0.04, 0.12
        print(len(data[data['id_event']==(int(i))]))

        data = deleteMissingEvents(data)        
        print(f'Simulazione di evento {i}\n')
        sipm = SiPM(ncell, pde, dark_count_rate, p_ct, p_af)
        sipm.initialize_sipm()
        o = time.time()
        print(len(data[data['id_event']==(int(i))]))
        a = run_simulation(sipm, data[data['id_event']==(int(i))])
        np.savetxt(f'C:/Users/Marco/Desktop/Analisi_SiPM/Simulazione/{args.f}/Segnali_{args.side}/wf_{i}.txt', a)
        print(f'Elapses time: {(time.time()-o)/60}')
        plt.figure()
        plt.plot(sipm.all_time, a)
        plt.show()
    