import numpy as np
import os 
from matplotlib import pyplot as plt
from readTrc import Trc

trc = Trc()
time, _, _ = trc.open('C:/Users/Marco/Desktop/C1--trigger--00000.trc')
dt = (time[-1] - time[0])*40
print(time[-1]-time[0])