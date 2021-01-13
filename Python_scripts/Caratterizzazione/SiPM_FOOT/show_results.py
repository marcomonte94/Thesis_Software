import numpy as np
import os
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import argparse
from analysis_workflow import gain, cross_talk, after_pulse

datapath = 'C:/Users/Marco/Desktop/Analisi_SiPM/Caratterizzazione/id11'
voltage_dir = list(os.listdir(f'{datapath}'))

def compute_results(voltage, datapath):
    #g, ct, af = [], [], []

    with open(f'{datapath}/results.txt', 'w') as fileresults:
        fileresults.write('# Gain   Cross-talk  After-pulse \n')

        for i in range(len(voltage_dir)):

            print('Sono a voltaggio {}\n'.format(voltage_dir[i]))
            areas =np.loadtxt(f'{datapath}/{voltage_dir[i]}/all_areas.txt', unpack=True)
            ampl = np.loadtxt(f'{datapath}/{voltage_dir[i]}/all_ampl.txt', unpack=True)
            delay = np.loadtxt(f'{datapath}/{voltage_dir[i]}/all_delay.txt', unpack=True)

            fileresults.write(f'{gain(areas)}   ')
            plt.close()
            fileresults.write(f'{cross_talk(ampl)}  ')
            plt.close()
            fileresults.write(f'{after_pulse(delay)}  ')
            plt.close()
            fileresults.write('\n')


def plot_results(voltage, g, ct, af):

    def fitfunc(x, a, b):
        return a + b * x

    popt, pcov = curve_fit(fitfunc, voltage, g)

    plt.figure()
    plt.plot(voltage, g, '.', color='black')
    plt.plot(voltage, fitfunc(voltage, *popt), color='red')

    Vbr = -popt[0] / popt[1]
    d = np.matrix([-1/popt[1], -Vbr/popt[1]])
    dT = np.transpose(d)    
    pcov = np.matrix(pcov)
    dVbr = np.sqrt(d*pcov*dT)
    print(f'V Breakdown: {Vbr} +/- {dVbr}')

    plt.figure()
    plt.plot(voltage, ct, 'o')
    plt.figure()
    plt.plot(voltage, af, 'o')
    plt.show()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='SiPM analysis results')
    parser.add_argument('id', help='SiPM ID')
    parser.add_argument('-w', '--write', help='Compute and process results', default = '0')
    args = parser.parse_args()

    datapath = f'C:/Users/Marco/Desktop/Analisi_SiPM/Caratterizzazione/{args.id}'
    voltage_dir = list(os.listdir(f'{datapath}'))
    voltage = np.array([116, 117, 118, 119, 120, 121, 122, 123, 124])


    if args.write == '0':       
        g, ct, af = np.loadtxt(f'{datapath}/results.txt', unpack=True)
        plot_results(voltage, g, ct, af)

    elif args.write == '1':
        compute_results(voltage, datapath)




