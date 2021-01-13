import numpy as np
import os
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from scipy.signal import find_peaks
from readTrc import Trc
from wf_analysis import DLED, wf_correction, compute_area
from analysis_workflow import wf_data, gain, cross_talk, after_pulse

overVoltage = np.array([54.5, 55.5, 55., 56.5, 56., 57.])
allGain, allCT, allAF = [], [], []

ov_directories = 'C:/Users/39348/Desktop/Thesis_Software/test-gpib/SIPM test'
listaFile = list(os.listdir(ov_directories))

for i in range(len(listaFile)):

    print('Sono a overvoltage {}\n'.format(listaFile[i]))

    waveforms = 'C:/Users/39348/Desktop/Thesis_Software/test-gpib/SIPM test/{}'.format(listaFile[i])
    areas, all_amplitude, all_delay = wf_data(waveforms, 20)
    amplProminence = np.array([20, 40, 20, 100, 50, 200])
    

    allGain.append(gain(areas))
    plt.close()
    plt.close()
    
    allCT.append(cross_talk(all_delay, all_amplitude, amplProminence[i]))
    plt.close()
    plt.close()

    allAF.append(after_pulse(all_delay))
    plt.close()
    plt.close()

plt.figure()
plt.plot(overVoltage, allGain, 'o')

plt.figure()
plt.plot(overVoltage, allCT, 'o')

plt.figure()
plt.plot(overVoltage, allAF, 'o')

plt.show()