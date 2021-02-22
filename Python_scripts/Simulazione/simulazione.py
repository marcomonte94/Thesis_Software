import numpy as np
from matplotlib import pyplot as plt
import time
from sipm_struct import Microcell, SiPM

dt_evt = np.dtype([
    ('id_event',    np.float32), 
    ('time',        np.float32), 
    ('x',           np.float32),
    ('y',           np.float32)
     ])

def readSimBinary(fileName):
    data = np.fromfile(fileName, dtype=dt_evt)
    return data

def toCells(data):
    data['y'] += 1.5
    data['x'] += 10
    data['x'] = np.floor(data['x'] / 25e-3).astype(int)
    data['y'] = np.floor(data['y'] / 25e-3).astype(int)
    return data

def deleteMissingEvents(data):
    mask1 = np.logical_and(data['x'] > 100, data['x'] < 220)
    print(len(mask1))
    mask2 = np.logical_and(data['x'] > 260, data['x'] < 380)
    print(len(mask2))

    a = np.logical_or(mask1, mask2)
    mask3 = np.logical_and(data['x'] > 420, data['x'] < 540)
    mask4 = np.logical_and(data['x'] > 580, data['x'] < 700)
    b = np.logical_or(mask3, mask4)
    c = np.logical_or(a, b)
    print(len(a))
    print(len(b))
    print(len(data[c]))

    return data[c]
    


if __name__ == '__main__':

    data = 'C:/Users/Marco/Desktop/results_C115_100ev/detect2.raw'
    data = readSimBinary(data)
    data = toCells(data)
    data = deleteMissingEvents(data)
    print(len(data['x']))

    plt.hist(data['y'], bins=np.arange(0, 800))
    plt.show()

    '''
    photon_timestamps = data[:,1]

    all_time = np.arange(0, 500, 0.001)


    ncell, pde, dark_count_rate, p_ct, p_af = 57600, 0.2, 3e6, 0.04, 0.12
    sipm = SiPM(ncell, pde, dark_count_rate, p_ct, p_af)
    print(sipm.ncell)
    sipm.initialize_sipm()
    print(f'Starting photons: {len(photon_timestamps)}')    
    
    sipm.map_photons(photon_timestamps)
    sipm.add_darkcount(all_time[0], all_time[-1])
    sipm.triggers_in = np.sort(sipm.triggers_in, order='time' )
    i = 0

    while len(sipm.triggers_in) > 0:
        print(sipm.triggers_in[0])        
        sipm.process_photon(sipm.triggers_in[0])

    print(f'***************** \n {sipm.triggers_in}')
    print(sipm.triggers_out)
    print(f'Number of total triggers: {len(sipm.triggers_out)}')
    #print(f'Number of detected photons: {len(sipm.triggers_in[sipm.triggers_in['type']=='P'])}'')
    print(f'Number of crosstalk: {sipm.ct_counts}')
    print(f'Number of afterpulse: {sipm.af_counts}')

    plt.plot(all_time, sipm.signal_ampl)
    plt.show()
    '''
