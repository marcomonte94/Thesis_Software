import pyvisa
import time
import numpy as np
import os
import argparse
from curveIV import plotIVcurve, fitBreakDown
import matplotlib.pyplot as plt
from test_gpib import Keithley2750
from scipy.optimize import curve_fit

for i in range(1, 15):

    fileName = 'id_{}.txt'.format(str(i))
    if (os.path.isfile(fileName) == False):
        pass

    else:
        print('V breakdown of {} \n'.format(fileName))
        fitBreakDown(fileName)
        print('\n')
plt.show()

