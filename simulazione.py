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
    parser.add_argument('-d', '--debug', help='Debug mode', default = '0')
    parser.add_argument('-w', '--graphs', help='Graph mode', default = '0')
    args = parser.parse_args()

    data = f'/Users/luigimasturzo/Documents/Dati_MC/{args.f}/detect{args.side}.raw'
    data = readSimBinary(data)
    data = toCells(data)
    data = deleteMissingEvents(data)


    if args.debug == '0':

        ncell, pde, dark_count_rate, p_ct, p_af = 57600, 0.2, 3e6, 0.04, 0.12

        for j in range(1, 101):
            print(f'Simulazione di evento {j}\n')
            sipm = SiPM(ncell, pde, dark_count_rate, p_ct, p_af)
            sipm.initialize_sipm()
            k = j+40
                        
            print(f'/Users/luigimasturzo/Documents/{args.f}/Segnali_{args.side}/wf_{k}.txt')

            a = run_simulation(sipm, data[data['id_event']==j])
            np.savetxt(f'/Users/luigimasturzo/Documents/{args.f}/Segnali_{args.side}/wf_{k}.txt', a)

    elif args.debug == '1':

        if args.graphs == '1':
            plt.figure()
            plt.hist(data['x'], bins=len(data))
            plt.figure()
            plt.hist(data['y'], bins=len(data))
            plt.figure()
            plt.hist(data['time'], bins=len(data))

        i = input('Event to debug: ')
        ncell, pde, dark_count_rate, p_ct, p_af = 57600, 0.2, 3e6, 0.04, 0.12
        print(len(data[data['id_event']==(int(i))]))

        data = deleteMissingEvents(data)        
        print(f'Simulazione di evento {i}\n')
        sipm = SiPM(ncell, pde, dark_count_rate, p_ct, p_af)
        sipm.initialize_sipm()
        print(len(data[data['id_event']==(int(i))]))
        a = run_simulation(sipm, data[data['id_event']==(int(i))])
        np.savetxt(f'/Users/luigimasturzo/Documents//{args.f}/Segnali_{args.side}/wf_{i}.txt', a)
        plt.figure()
        plt.plot(sipm.all_time, a)
        plt.show()
    