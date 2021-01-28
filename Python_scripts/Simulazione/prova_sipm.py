import numpy as np
from matplotlib import pyplot as plt
import time
from sipm_struct import SiPM

s = SiPM(10000, 0.2, 0.5, 0.05, 0.05)
s.cellmap[5,5].gain = 5
print(s.cellmap.dtype)
print(s.cellmap[5,5].gain)
print(s.cellmap[1,5].gain)
print(s.cellmap.shape)
print(len(s.signal_ampl))
