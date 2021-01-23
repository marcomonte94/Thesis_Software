import numpy as np
import os
import argparse
import matplotlib.pyplot as plt
from readTrc import Trc


def compute_area(inputfile):
    trc = Trc()
    time, ampl, _ = trc.open(inputfile)
    ampl = -ampl
    baseline = ampl[:150].mean()
    dt = (np.abs(time[1:] - time[:-1])).mean()
    area = ((ampl - baseline) * dt).sum()
    return area


filepath = 'C:/Users/Marco/Desktop/Saturazione/50mu'
laser_directories = list(os.listdir(filepath))

for i in range(len(laser_directories)):
    print(laser_directories[i])
    waveforms = list(os.listdir(f'{filepath}/{laser_directories[i]}'))
    f = open(f'C:/Users/Marco/Desktop/Analisi_SiPM/Saturazione/Aree_50/{laser_directories[i]}.txt', 'w')
    for wf_j in waveforms:
        a = compute_area(f'{filepath}/{laser_directories[i]}/{wf_j}')
        f.write(f'{a}\n')
    f.close()