import numpy as np
import os
import argparse
from curveIV import plotIVcurve, fitBreakDown
import matplotlib.pyplot as plt
from test_gpib import Keithley2750
from scipy.optimize import curve_fit

file_path = 'montefiori\montefiori_116v\C1--prova--00000.txt'

v = np.loadtxt(file_path, skiprows=3, unpack=True)
t = np.arange(0, len(v), 1)

plt.plot(t, v)
plt.show()