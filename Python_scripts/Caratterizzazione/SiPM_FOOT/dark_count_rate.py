import numpy as np
from matplotlib import pyplot as plt
from readTrc import Trc

trc = Trc()
time, _, _ = trc.open('C:/Users/Marco/Desktop/C1--trigger--00000.trc')
all_events = np.loadtxt('C:/Users/Marco/Desktop/Analisi_SiPM/Caratterizzazione/id31/123/all_ampl.txt')
dt = (time[-1] - time[0])*40
print(time[9]-time[8])
print(len(time)*(time[9]-time[8]))
print(dt)
print(f'Dark count rate: {len(all_events)/dt}')