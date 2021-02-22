import numpy as np
import os
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import argparse
from analysis_workflow import gain, cross_talk, after_pulse


def compute_results(voltage, datapath):
    #g, ct, af = [], [], []
    voltage_dir = list(os.listdir(f'{datapath}'))
    #p = [80, 80, 80, 80, 80, 80, 80, 280, 280] # id 31
    #p = [80, 80, 80, 80, 80, 80, 80, 80, 80] # id 11, id 2
    p = [80, 80, 80, 280, 280, 280, 280, 280, 280] # id 31

    with open(f'{datapath}/risultati.txt', 'w') as fileresults:

        fileresults.write('#Dark-count-rate  Gain   Cross-talk  After-pulse \n')

        for i in range(0, len(voltage_dir)):

            if os.path.isdir(f'{datapath}/{voltage_dir[i]}'):

                print('Sono a voltaggio {}\n'.format(voltage_dir[i]))
                areas =np.loadtxt(f'{datapath}/{voltage_dir[i]}/all_areas.txt', unpack=True)
                ampl = np.loadtxt(f'{datapath}/{voltage_dir[i]}/all_ampl.txt', unpack=True)
                delay = np.loadtxt(f'{datapath}/{voltage_dir[i]}/all_delay.txt', unpack=True)

                #fileresults.write(f'{dcr}   ')
                x, dx = gain(areas)
                fileresults.write(f'{x}   {dx}  ')
                plt.close()
                x, dx = cross_talk(ampl, p[i])
                fileresults.write(f'{x}   {dx}   ')
                plt.close()
                x, dx, y, dy = after_pulse(delay)
                fileresults.write(f'{x}     {dx}    {y}     {dy}  ')
                plt.close()
                
                fileresults.write('\n')


def plot_results(voltage, g, dg, ct, d_ct, dcr, d_dcr, af, d_af):

    def fitfunc(x, a, b):
        return a + b * x

    popt, pcov = curve_fit(fitfunc, voltage, g, sigma=dg)

    Vbr = -popt[0] / popt[1]
    d = np.matrix([-1/popt[1], -Vbr/popt[1]])
    dT = np.transpose(d)
    pcov = np.matrix(pcov)
    dVbr = np.sqrt(d*pcov*dT)
    print(f'V Breakdown: {Vbr} +/- {dVbr}')

    plt.figure(figsize=[8, 5])
    plt.rc('font', size=12)
    plt.errorbar((voltage), g, dg, fmt='.', color='black')
    plt.plot((voltage), fitfunc(voltage, *popt), color='red')
    plt.xlabel('Voltage [V]')
    plt.ylabel('Gain $[10^5]$')

    plt.figure(figsize=[8, 5])
    plt.rc('font', size=12)
    plt.plot((voltage-Vbr)/2, ct*100, color='blue')
    plt.errorbar((voltage-Vbr)/2,ct*100, d_ct*100, fmt='.', color='black')   
    plt.ylabel('$P_{cross-pulse} [\%]$')
    plt.xlabel('Overvoltage [V]') 

    plt.figure(figsize=[8, 5])
    plt.rc('font', size=12)
    plt.plot((voltage-Vbr)/2, af*100, color='blue')
    plt.errorbar((voltage-Vbr)/2, af*100, d_af*100, fmt= '.', color='black')
    plt.ylabel('$P_{after-pulse} [\%]$')
    plt.xlabel('Overvoltage [V]')

    plt.figure(figsize=[8, 5])
    plt.rc('font', size=12)
    plt.plot((voltage-Vbr)/2, dcr, color='blue')
    plt.errorbar((voltage-Vbr)/2, dcr, d_dcr , fmt='.', color='black')
    plt.ylabel('Dark count rate [MHz]')
    plt.xlabel('Overvoltage [V]')
    #plt.yscale('log')
    
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
        g, dg, ct, d_ct, dcr, d_dcr, af, d_af = np.loadtxt(f'{datapath}/risultati.txt', unpack=True)
        #dcr = dcr - af*dcr
        plot_results(voltage, g, dg, ct, d_ct, dcr, d_dcr, af, d_af)

    elif args.write == '1':
        compute_results(voltage, datapath)




