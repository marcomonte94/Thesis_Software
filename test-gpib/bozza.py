import pyvisa
import time
import numpy as np
import sys
from datetime import datetime
from matplotlib import pyplot as plt

class Keithley2750:
    def __init__(self,resource_name):
        self.__rm = pyvisa.ResourceManager()
        self.K = self.__rm.open_resource(resource_name)
        print("Initialized instrument",self.send_gpib_command("*IDN?"))

    def send_gpib_command(self,command):
        return self.K.query(command)

    def write_gpib_command(self,command):
        return self.K.write(command)

    def reset_strum(self):
        '''Reset strument ONLY if there's no voltage (OL), or (better) if V=0 (CL) '''
        k.write_gpib_command("*RST")
        k.write_gpib_command('SOUR:VOLT 0')
        k.write_gpib_command('SYST:ZCH ON')
        k.write_gpib_command('SYST:ZCOR:ACQ')
        k.write_gpib_command('SYST:ZCOR ON')
        k.write_gpib_command('SYST:ZCH OFF')


    def meas_current(self):
        try:
            ans = float((self.send_gpib_command("READ?")).split("A")[0])
            #print(ans)
        except:
            ans = 0
        return ans


if __name__ == "__main__":
    rm = pyvisa.ResourceManager()
    print(rm.list_resources())
    print('aaa')

    RESOURCE_NAME = 'GPIB0::22::INSTR'
    k = Keithley2750(RESOURCE_NAME)
    print(k.send_gpib_command("*IDN?"))

    k.write_gpib_command('SOUR:VOLT:STAT ON')
    k.reset_strum()

    '''Define ranges for I and V'''

    k.write_gpib_command('SOUR:VOLT:RANG 10')
    k.write_gpib_command('SOUR:VOLT:ILIM 2.5e-3')

    '''Define an array of V-values with steps from a value to an other'''
    v = np.linspace(1,3,10)

    for i in v:

        curr = []
        k.write_gpib_command('SOUR:VOLT {}'.format(i))

        I = []
        for j in range(5):
            I.append(k.meas_current())
        print('{}, {} [V]'.format(I.mean(), i))
        curr.append(I.mean())
        time.sleep(2)



    k.write_gpib_command('SOUR:VOLT:STAT OFF')

    t_str = datetime.strftime(datetime.now(),"%Y-%m-%d %H-%M-%S")

    print(t_str)
    rm.close()

    plt.plot(v,curr)
    plot.show()
