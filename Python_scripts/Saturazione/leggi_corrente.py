import pyvisa
import time
import numpy as np
import os
import argparse
from datetime import datetime
import matplotlib.pyplot as plt
from test_gpib import Keithley2750
from scipy.optimize import curve_fit

rm = pyvisa.ResourceManager()
print(rm.list_resources())

RESOURCE_NAME = 'GPIB0::22::INSTR'
k = Keithley2750(RESOURCE_NAME)
print("My name is {} \n".format(k.send_gpib_command("*IDN?")))

k.write_gpib_command("*RST")
k.write_gpib_command("SYST:ZCH OFF")
k.write_gpib_command('SOUR:VOLT:RANG 500')
k.write_gpib_command('RANG:AUTO ON')
k.write_gpib_command('CURR:RANG 2e-7')
#k.write_gpib_command('SOUR:VOLT 0')
k.write_gpib_command('SOUR:VOLT:ILIM 2.5e-3')
k.write_gpib_command('SOUR:VOLT:STAT OFF')

i = np.zeros(20)

for j in range(len(i)):
    print(float(k.send_gpib_command('READ?').split("A")[0]))
    i[j] = float(k.send_gpib_command('READ?').split("A")[0])
print('*********************\n')
print(i.mean())
print(i.std())
