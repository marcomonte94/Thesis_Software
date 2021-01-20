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
            ans = float((self.send_gpib_command("MEAS:CURR?")).split("A")[0])
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
    #m = k.median_voltage(10)
    a = k.meas_current()
    k.write_gpib_command('SYST:ZCH ON')
    #rm.close()
    #sys.exit(0)

    # to read back:
    # t_date = datetime.strptime(t_str,"%Y-%m-%d %H-%M-%S")
    t_str = datetime.strftime(datetime.now(),"%Y-%m-%d %H-%M-%S")

    print(t_str)
    print("current {:.6f}".format(a))
    rm.close()
