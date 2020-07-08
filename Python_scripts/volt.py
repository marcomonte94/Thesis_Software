import pyvisa
import time
import numpy as np
import sys
import argparse
from datetime import datetime
import matplotlib.pyplot as plt

_description='Recostruction of a SiPM I-V curve.'

class Keithley2750:
    def __init__(self,resource_name):
        self.__rm = pyvisa.ResourceManager()
        self.K = self.__rm.open_resource(resource_name)
        print("Initialized instrument",self.send_gpib_command("*IDN?"))

    def send_gpib_command(self,command):
        return self.K.query(command)

    def write_gpib_command(self,command):
        return self.K.write(command)

    def median_voltage(self,n):
        ans = np.zeros(n)
        for i in range(n):
            time.sleep(.5)
            try:
                ans[i] = float((self.send_gpib_command("MEAS:VOLT?")).split("VDC")[0])
                print(i,ans[i])
            except:
                ans[i] = np.nan
        return np.median(ans[~np.isnan(ans)])

    def meas_current(self):
        try:
            ans = float((self.write_gpib_command("READ?")).split("A")[0])
            #print(ans)
        except:
            ans = 0
        return ans


if __name__ == "__main__":

    '''
    parser = argparse.ArgumentParser(description=_description)
    parser.add_argument('infile', help='path to the input file')
    args = parser.parse_args()
    '''
    rm = pyvisa.ResourceManager()

    print(rm.list_resources())
    print('aaa')

    RESOURCE_NAME = 'GPIB0::22::INSTR'
    k = Keithley2750(RESOURCE_NAME)
    print("My name is {} \n".format(k.send_gpib_command("*IDN?")))

    k.write_gpib_command("*RST")
    k.write_gpib_command("SYST:ZCH OFF")

    k.write_gpib_command('SOUR:VOLT:RANG 500')
    
    k.write_gpib_command('SOUR:VOLT 3')
    
    k.write_gpib_command('SOUR:VOLT:ILIM 2.5e-3')

    k.write_gpib_command('SOUR:VOLT:STAT ON')


    '''
    ans = k.send_gpib_command('READ?').split("A")[0]
    ans = float(ans)
    print(ans)
    '''

    v1 = np.linspace(30, 50, 21)
    v2 = np.linspace(50, 60, 100)
    v = np.concatenate((v1,v2))
    #v = np.zeros(10) + 2
    curr = np.zeros(len(v))

    file = open('prova.txt', 'w')
    file.write('# Voltage (V)    Current (A) \n')

    
    for i in range(len(v)):
        #v +=1
        k.write_gpib_command('SOUR:VOLT {}'.format(str(v[i])))
        print(k.send_gpib_command('READ?'))
        #curr[i] = k.send_gpib_command('READ?')[0]
        i_set = np.zeros(10)
        
        for j in range(len(i_set)):
            i_set[j] = float(k.send_gpib_command('READ?').split("A")[0])
        '''
            if v[i] < 50:
                time.sleep(0.3)
            else:
        '''
        time.sleep(0.3)
                
        
        curr[i] = i_set.mean()
        #curr[i] = float(k.send_gpib_command('READ?').split("A")[0])
        file.write("{}  {} \n".format(v[i], curr[i]))
        print(curr[i])
        #curr[i] = float(curr[i])
        #time.sleep(.5)

    

    t_str = datetime.strftime(datetime.now(),"%Y-%m-%d %H-%M-%S")
    k.write_gpib_command('SOUR:VOLT:STAT OFF')
    
    plt.plot(v, curr)
    plt.xlabel('V [V]')
    plt.ylabel('I [A]')
    plt.yscale("log")
    #print(t_str)
    rm.close()
    file.close()
    plt.show()
