import pyvisa
import time
import numpy as np
import os
import argparse
from datetime import datetime
import matplotlib.pyplot as plt
from test_gpib import Keithley2750
from scipy.optimize import curve_fit

_description='Recostruction of a SiPM I-V curve.'


def makeIVcurve(data_out):

    t0 = time.time()

    rm = pyvisa.ResourceManager()
    print(rm.list_resources())

    RESOURCE_NAME = 'GPIB0::22::INSTR'
    k = Keithley2750(RESOURCE_NAME)
    print("My name is {} \n".format(k.send_gpib_command("*IDN?")))

    k.write_gpib_command("*RST")
    k.write_gpib_command("SYST:ZCH OFF")
    k.write_gpib_command('SOUR:VOLT:RANG 500')   
    k.write_gpib_command('RANG:AUTO ON')
    k.write_gpib_command('SOUR:VOLT 3')   
    k.write_gpib_command('SOUR:VOLT:ILIM 2.5e-3')
    k.write_gpib_command('SOUR:VOLT:STAT ON')


    '''
    ans = k.send_gpib_command('READ?').split("A")[0]
    ans = float(ans)
    print(ans)
    '''

    v1 = np.arange(80, 100, 1)
    v2 = np.arange(100, 120, 0.1)
    v = np.concatenate((v1,v2))
    curr = np.zeros(len(v))

    file = open(data_out, 'w')
    file.write('# Voltage (V)    Current (A) \n')
   
    for i in range(len(v)):
        
        k.write_gpib_command('SOUR:VOLT {}'.format(str(v[i])))
        k.write_gpib_command('RANG 2e-4')
        print(k.send_gpib_command('READ?'))
        i_set = np.zeros(10)
        
        for j in range(len(i_set)):
            i_set[j] = float(k.send_gpib_command('READ?').split("A")[0])

        time.sleep(0.3)             
        
        curr[i] = i_set.mean()
        file.write("{}  {} \n".format(v[i], curr[i]))
        print(curr[i])

    #t_str = datetime.strftime(datetime.now(),"%Y-%m-%d %H-%M-%S")
    k.write_gpib_command('SOUR:VOLT:STAT OFF')
    
    plt.plot(v, curr)
    plt.xlabel('Voltage [V]')
    plt.ylabel('I [A]')
    plt.yscale("log")
    #print(t_str)
    rm.close()
    file.close()
    print('Elapses time to build a IV curve: {:.3f}'.format(time.time()-t0))
    #plt.show()

def plotIVcurve(input_file):

    v, i = np.loadtxt(input_file, unpack=True)

    plt.figure()
    plt.plot(v, i, label='I-V curve')
    plt.xlabel('Voltage [V]')
    plt.ylabel('I [A]')
    plt.yscale("log")
    plt.legend(loc='best')

    plt.figure()
    plt.plot(v[1:], np.diff(i))
    #plt.yscale("log")
    #plt.show()

def fitBreakDown(input_file):

    v, i = np.loadtxt(input_file, unpack=True)
    maskV = np.logical_and((v > 105), (v < 110))
    v_fit, i_fit = v[maskV], i[maskV]
    #v_fit, i_fit = v, i


    def fitfunc(x, a, b):
        #y = np.sqrt((a*x + b)**2)
        #y += np.sqrt(c*x + d*x*y)
        #return (a*x**2 + b*x + c)
        #return (a*x + b)**2 
        return a*x + b
        

    p0 = [1e-7, -1]
    popt, pcov = curve_fit(fitfunc, v_fit, np.sqrt(i_fit), p0)

    Vbr = -popt[1] / popt[0]

    d = np.matrix([-Vbr/popt[0], -1/popt[0]])
    dT = np.transpose(d)    
    pcov = np.matrix(pcov)

    dVbr = np.sqrt(d*pcov*dT)

    plt.figure("{}".format(input_file))
    plt.rc('font', size=12)
    plt.plot(v, np.sqrt(i), color='blue', label='I-V curve')
    plt.xlabel('Voltage [V]')
    plt.ylabel('$\sqrt{I}$ [$\sqrt{A}$]')
    plt.yscale("log")

    plt.plot(v_fit, fitfunc(v_fit, *popt), color='red', label='Fit $V_{BR}$')
    plt.legend(loc='best')
    print('Vbr: {} +/- {}'.format(-popt[1]/popt[0], dVbr))
    



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=_description)
    parser.add_argument('infile', help='path to the input file')
    #parser.add_argument('-r', '--read', help='Read input file', action = 'store_true')
    parser.add_argument('-w', '--write', help='Build IV curve and write input file', default = '0')
    parser.add_argument('-b', '--bd', help='Fitting V breakdown', action = 'store_true')
    args = parser.parse_args()

    if args.write == '0':
        print("Read I-V curve")
        plotIVcurve(args.infile)
    elif args.write == '1':
        print("Build I-V curve")
        makeIVcurve(args.infile)
    #if args.bd:
    print('Fitting V breakdown')
    fitBreakDown(args.infile)

    plt.show()