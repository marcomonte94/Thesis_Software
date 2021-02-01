import numpy as np
import os
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from scipy.signal import find_peaks
from readTrc import Trc
from wf_analysis import DLED, wf_correction, compute_area
from analysis_workflow import wf_data, gain, cross_talk, after_pulse

#threshold = np.array([0.014, 0.015, 0.015, 0.016, 0.016, 0.017, 0.017, 0.017, 0.018])
threshold = np.array([0.016, 0.017, 0.017, 0.017, 0.018, 0.018, 0.019, 0.019, 0.02])
allGain, allCT, allAF = [], [], []

ov_directories = 'C:/Users/Marco/Desktop/id1'
listaFile = list(os.listdir(ov_directories))

for i in range(len(listaFile)):

    if os.path.isdir(f'{ov_directories}/{listaFile[i]}'):

        print('Sono a {} V \n'.format(listaFile[i]))

        waveforms = f'{ov_directories}/{listaFile[i]}'
        res_path = f'C:/Users/Marco/Desktop/Analisi_SiPM/Caratterizzazione/id1/{listaFile[i]}'
        areas, all_amplitude, all_delay = wf_data(waveforms, res_path, 40, threshold[i])    
