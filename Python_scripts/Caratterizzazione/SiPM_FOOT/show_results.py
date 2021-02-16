import numpy as np
import os
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import argparse
from analysis_workflow import gain, cross_talk, after_pulse


def compute_results(voltage, datapath):
    #g, ct, af = [], [], []
    voltage_dir = list(os.listdir(f'{datapath}'))

    with open(f'{datapath}/dcr.txt', 'w') as fileresults:

        fileresults.write('#Dark-count-rate  Gain   Cross-talk  After-pulse \n')

        for i in range(0, len(voltage_dir)):

            if os.path.isdir(f'{datapath}/{voltage_dir[i]}'):

                print('Sono a voltaggio {}\n'.format(voltage_dir[i]))
                areas =np.loadtxt(f'{datapath}/{voltage_dir[i]}/all_areas.txt', unpack=True)
                ampl = np.loadtxt(f'{datapath}/{voltage_dir[i]}/all_ampl.txt', unpack=True)
                delay = np.loadtxt(f'{datapath}/{voltage_dir[i]}/all_delay.txt', unpack=True)
                dcr = np.loadtxt(f'{datapath}/{voltage_dir[i]}/dark_count_rate.txt', unpack=True)

                fileresults.write(f'{dcr}   ')
                '''
                fileresults.write(f'{gain(areas)}   ')
                plt.close()
                fileresults.write(f'{cross_talk(ampl)}  ')
                plt.close()
                fileresults.write(f'{after_pulse(delay)}  ')
                plt.close()
                '''
                fileresults.write('\n')


def plot_results(voltage, dcr, g, ct, af):

    def fitfunc(x, a, b):
        return a + b * x

    popt, pcov = curve_fit(fitfunc, voltage, g)

    Vbr = -popt[0] / popt[1]
    d = np.matrix([-1/popt[1], -Vbr/popt[1]])
    dT = np.transpose(d)
    pcov = np.matrix(pcov)
    dVbr = np.sqrt(d*pcov*dT)
    print(f'V Breakdown: {Vbr} +/- {dVbr}')

    plt.figure(figsize=[8, 5])
    plt.rc('font', size=12)
    plt.plot((voltage), g/1e5, '.', color='black')
    plt.plot((voltage), fitfunc(voltage, *popt)/1e5, color='red')
    plt.xlabel('Voltage [V]')
    plt.ylabel('Gain $[10^5]$')

    plt.figure(figsize=[8, 5])
    plt.rc('font', size=12)
    plt.plot((voltage-Vbr)/2, ct*100, color='blue')
    plt.plot((voltage-Vbr)/2, ct*100, '.', color='black')   
    plt.ylabel('$P_{cross-pulse} [\%]$')
    plt.xlabel('Overvoltage [V]') 

    plt.figure(figsize=[8, 5])
    plt.rc('font', size=12)
    plt.plot((voltage-Vbr)/2, af*100, color='blue')
    plt.plot((voltage-Vbr)/2, af*100, '.', color='black')
    plt.ylabel('$P_{after-pulse} [\%]$')
    plt.xlabel('Overvoltage [V]')

    plt.figure(figsize=[8, 5])
    plt.rc('font', size=12)
    plt.plot((voltage-Vbr)/2, dcr/1e6, color='blue')
    plt.plot((voltage-Vbr)/2, dcr/1e6, '.', color='black')
    plt.ylabel('Dark count rate [MHz]')
    plt.xlabel('Overvoltage [V]')
    
    plt.show()
    

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='SiPM analysis results')
    parser.add_argument('id', help='SiPM ID')
    parser.add_argument('-w', '--write', help='Compute and process results', default = '0')
    args = parser.parse_args()

    datapath = f'C:/Users/Marco/Desktop/Analisi_SiPM/Caratterizzazione/{args.id}'
    
    if args.id == 'id1':
        voltage = np.array([120, 121, 122, 123, 124, 125, 126, 127, 128])
    else:
        voltage = np.array([116, 117, 118, 119, 120, 121, 122, 123, 124])


    if args.write == '0':
        dcr, g, ct, af = np.loadtxt(f'{datapath}/results.txt', unpack=True)
        dcr = dcr - af*dcr
        plot_results(voltage, dcr, g, ct, af)

    elif args.write == '1':
        compute_results(voltage, datapath)




