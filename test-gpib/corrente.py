import pyvisa
import time
import numpy
import sys
from datetime import datetime

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

        k.write_gpib_command('SYST:ZCH ON')
        #k.write_gpib_command('RANG 2e-9')
        #print(k.write_gpib_command('RANG 2e-9'))
        k.write_gpib_command('SYST:ZCOR:ACQ')
        k.write_gpib_command('SYST:ZCOR ON')
        k.write_gpib_command('SYST:ZCH OFF')


    def median_voltage(self,n):
        ans = numpy.zeros(n)
        for i in range(n):
            time.sleep(.5)
            try:
                ans[i] = float((self.send_gpib_command("MEAS:VOLT?")).split("VDC")[0])
                print(i,ans[i])
            except:
                ans[i] = numpy.nan
        return numpy.median(ans[~numpy.isnan(ans)])

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

    #k.reset_strum()

    for i in range(10):
        k.write_gpib_command('SOUR:VOLT {}'.format(str(i)))
        k.write_gpib_command('RANG 2e-4')
        print(k.send_gpib_command('READ?').split("A")[0])
        time.sleep(0.5)







    #rm.close()
    #sys.exit(0)

    # to read back:
    # t_date = datetime.strptime(t_str,"%Y-%m-%d %H-%M-%S")
    t_str = datetime.strftime(datetime.now(),"%Y-%m-%d %H-%M-%S")

    print(t_str)
    rm.close()
