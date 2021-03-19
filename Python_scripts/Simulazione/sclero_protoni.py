import numpy as np
from matplotlib import pyplot as plt
import time
import argparse
from sipm_struct import Microcell, SiPM, run_simulation, dt_evt
import time
from simulazione import readSimBinary, toCells, deleteMissingEvents


inputFile = 'results_p060_Birks3e-3'

for i in range(2, 10):
    if i == 2:
        ncell, pde, dark_count_rate, p_ct, p_af = 57600, 0.08, 1.17e6, 0.009, 0.017 
    elif i == 3:
        ncell, pde, dark_count_rate, p_ct, p_af = 57600, 0.11, 1.64e6, 0.013, 0.027 
    elif i == 4:
        ncell, pde, dark_count_rate, p_ct, p_af = 57600, 0.15, 2.1e6, 0.017, 0.034 
    elif i == 5:
        ncell, pde, dark_count_rate, p_ct, p_af = 57600, 0.17, 2.6e6, 0.022, 0.044 
    elif i == 6:
        ncell, pde, dark_count_rate, p_ct, p_af = 57600, 0.18, 3e6, 0.027, 0.053 
    elif i == 7:
        ncell, pde, dark_count_rate, p_ct, p_af = 57600, 0.19, 3.5e6, 0.036, 0.083 
    elif i == 8:
        ncell, pde, dark_count_rate, p_ct, p_af = 57600, 0.199, 4e6, 0.044, 0.12 
    elif i == 9:
        ncell, pde, dark_count_rate, p_ct, p_af = 57600, 0.2, 4.5e6, 0.054, 0.15 

    print(f'OV = {i}')

    inputFile = 'results_p060_250ev_birks3e-3_1'
    data = f'C:/Users/Marco/Desktop/Dati_MC/protoni/{inputFile}/detect2.raw'
    data = readSimBinary(data)
    data = toCells(data)
    data = deleteMissingEvents(data)

    for j in range(1, 251):
        print(f'Simulazione di evento {j}\n')
        sipm = SiPM(ncell, pde, dark_count_rate, p_ct, p_af)
        sipm.initialize_sipm()
        k = j
                    
        #print(f'C:/Users/Marco/Desktop/Simulazione/{args.f}/Segnali_{args.side}/wf_{k}.txt')

        a = run_simulation(sipm, data[data['id_event']==j])
        np.savetxt(f'C:/Users/Marco/Desktop/Analisi_SiPM/Simulazione/{i}V/results_p060_Birks3e-3/Segnali_2/wf_{k}.txt', a)

    inputFile = 'results_p060_250ev_birks3e-3_2'
    data = f'C:/Users/Marco/Desktop/Dati_MC/protoni/{inputFile}/detect2.raw'
    data = readSimBinary(data)
    data = toCells(data)
    data = deleteMissingEvents(data)

    for j in range(1, 251):
        print(f'Simulazione di evento {j}\n')
        sipm = SiPM(ncell, pde, dark_count_rate, p_ct, p_af)
        sipm.initialize_sipm()
        k = j+250
                    
        #print(f'C:/Users/Marco/Desktop/Simulazione/{args.f}/Segnali_{args.side}/wf_{k}.txt')

        a = run_simulation(sipm, data[data['id_event']==j])
        np.savetxt(f'C:/Users/Marco/Desktop/Analisi_SiPM/Simulazione/{i}V/results_p060_Birks3e-3/Segnali_2/wf_{k}.txt', a)

    inputFile = 'results_p060_250ev_birks3e-3_3'
    data = f'C:/Users/Marco/Desktop/Dati_MC/protoni/{inputFile}/detect2.raw'
    data = readSimBinary(data)
    data = toCells(data)
    data = deleteMissingEvents(data)

    for j in range(1, 251):
        print(f'Simulazione di evento {j}\n')
        sipm = SiPM(ncell, pde, dark_count_rate, p_ct, p_af)
        sipm.initialize_sipm()
        k = j+500
                    
        #print(f'C:/Users/Marco/Desktop/Simulazione/{args.f}/Segnali_{args.side}/wf_{k}.txt')

        a = run_simulation(sipm, data[data['id_event']==j])
        np.savetxt(f'C:/Users/Marco/Desktop/Analisi_SiPM/Simulazione/{i}V/results_p060_Birks3e-3/Segnali_2/wf_{k}.txt', a)

    inputFile = 'results_p060_250ev_birks3e-3_4'
    data = f'C:/Users/Marco/Desktop/Dati_MC/protoni/{inputFile}/detect2.raw'
    data = readSimBinary(data)
    data = toCells(data)
    data = deleteMissingEvents(data)

    for j in range(1, 251):
        print(f'Simulazione di evento {j}\n')
        sipm = SiPM(ncell, pde, dark_count_rate, p_ct, p_af)
        sipm.initialize_sipm()
        k = j+750
                    
        #print(f'C:/Users/Marco/Desktop/Simulazione/{args.f}/Segnali_{args.side}/wf_{k}.txt')

        a = run_simulation(sipm, data[data['id_event']==j])
        np.savetxt(f'C:/Users/Marco/Desktop/Analisi_SiPM/Simulazione/{i}V/results_p060_Birks3e-3/Segnali_2/wf_{k}.txt', a)