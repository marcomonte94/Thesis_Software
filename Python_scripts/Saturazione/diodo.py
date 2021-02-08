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
#k.write_gpib_command('RANG:AUTO ON')
k.write_gpib_command('CURR:RANG 2e-6')
k.write_gpib_command('SOUR:VOLT 0')
k.write_gpib_command('SOUR:VOLT:ILIM 2.5e-3')
k.write_gpib_command('SOUR:VOLT:STAT OFF')

laser = np.arange(1.2, 9., 0.2)
photocurrent, dark_current = np.zeros(len(laser)), np.zeros(len(laser))

with open('C:/Users/Marco/Desktop/Analisi_SiPM/Saturazione/prova.txt', 'w') as f:

    f.write('# Laser      Photocurrent    Dark Current \n')

    for i in range(len(laser)):
        print('Accendi il laser a {:.1f}'.format(laser[i]))
        input()
        i_set, i_dark = np.zeros(20), np.zeros(20)
        for j in range(len(i_set)):
            print(float(k.send_gpib_command('READ?').split("A")[0]))
            i_set[j] = float(k.send_gpib_command('READ?').split("A")[0])
            time.sleep(0.3)
        print(f'Media:{i_set.mean()}')
        print('\n Spegni il laser!')
        input()
        for j in range(len(i_dark)):
            print(float(k.send_gpib_command('READ?').split("A")[0]))
            i_dark[j] = float(k.send_gpib_command('READ?').split("A")[0])
            time.sleep(0.3)
        print(f'Media: {i_dark.mean()}')
        photocurrent[i] = i_set.mean()
        dark_current[i] = i_dark.mean()
        f.write(f'{laser[i]}    {photocurrent[i]}   {dark_current[i]} \n')

k.write_gpib_command('SOUR:VOLT:STAT OFF')
plt.figure()
plt.plot(laser, -(photocurrent-dark_current))
plt.show()