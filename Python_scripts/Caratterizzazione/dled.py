import time
import numpy as np
import os
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from scipy.signal import find_peaks
from readTrc import Trc

def shift(xs, n):
    if n >= 0:
        return np.concatenate((np.full(n, 0), xs[:-n]))
    else:
        return np.concatenate((xs[-n:], np.full(-n, 0)))

def DLED(time, ampl, delay):

    right_time = np.linspace(time[len(time)-1]+1e-10, time[len(time)-1]+(1+delay)*1e-10, delay)

    time_delay = np.concatenate((time[delay:], right_time))
    ampl_delay = shift(ampl, delay)

    timeDLED = time_delay
    amplDLED = ampl_delay - ampl
    '''
    plt.figure()
    plt.plot(time, ampl, label='Wavefor')
    plt.plot(time_delay, ampl_delay, label='DLED Waveform')
    plt.legend(loc='best')

    plt.figure()
    plt.plot(time, -amplDLED)

    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude (V)')
    '''
    return timeDLED, amplDLED

allMyData = list = os.listdir('C:/Users/39348/Desktop/Thesis_Software/test-gpib/A6_56V')
#allMyData = list = os.listdir('A6_56V')
trc = Trc()

all_amplitude = np.array([])
all_delay = np.array([])

for input_file in allMyData[:20]:

    print("Sto facendo il file {}\n".format(input_file))

    wf_path = 'C:/Users/39348/Desktop/Thesis_Software/test-gpib/A6_56V/{}.'.format(input_file)
    time, ampl, d = trc.open(wf_path)

    timeDLED, amplDLED = DLED(time,ampl, 20)
    peaks, _ = find_peaks(-amplDLED, height=0.0085, prominence=0.02)
    peak_timestamp = time[peaks]
    peak_amplitude = amplDLED[peaks]
    time_distance = peak_timestamp[1:]-peak_timestamp[:-1]
    '''
    plt.figure()
    plt.plot(time, -amplDLED, label='Original wf')
    '''

    wfToNormalize = np.zeros(3000)
    
    for i in range(1, len(peaks)-2):
        
        if time_distance[i] > 500e-9 and time_distance[i+1] > 500e-9:
            wfGood = amplDLED[peaks[i]-1000 : peaks[i]+2000]
            wfGood = wfGood / peak_amplitude[i]
            wfToNormalize = np.vstack((wfToNormalize, wfGood))
            #plt.plot(time[peaks[i]-1000 : peaks[i]+2000], wfGood)
            #plt.show()
    wf_ok = np.mean(wfToNormalize, axis=0)
    #mask = wf_ok < 0
    undershoot = np.zeros(len(wf_ok))
    for i in range (len(wf_ok)):
        if wf_ok[i]<0:
            undershoot[i] = wf_ok[i]

    for i in range(1, len(peaks)-1):
        amplDLED[peaks[i]-1000 : peaks[i]+2000] -= undershoot*amplDLED[peaks[i]]

    plt.figure()
    plt.title('provA')
    plt.plot(wf_ok)
    plt.plot(undershoot)
    '''
    plt.plot(time, -amplDLED, label='Corrected wf')
    plt.plot(time[peaks], -amplDLED[peaks], "x")

    
    
    plt.xscale('log')
    plt.scatter(time_distance, -peak_amplitude[1:])
    '''
    peaks, _ = find_peaks(-amplDLED, height=0.0085, prominence=0.02)

    peak_timestamp = time[peaks]
    peak_amplitude = amplDLED[peaks]
    time_distance = peak_timestamp[1:]-peak_timestamp[:-1]
    
    all_delay = np.concatenate((all_delay, time_distance)) 
    all_amplitude = np.concatenate((all_amplitude, -peak_amplitude[1:]))

    

    print("fatto\n")

plt.figure()
plt.xscale('log')
plt.scatter(all_delay, all_amplitude, marker='.')

plt.figure()
plt.hist(all_amplitude, bins=200, orientation='horizontal')
plt.xscale('log')

plt.figure()

bins = 10**np.arange(-3, +2, 0.02)
bins2 = np.linspace(1e-3, 1e+2, 200)

all_delay *= 1e6
y_data, edges, _ = plt.hist(all_delay, bins=bins2)
#plt.xscale('log')
#plt.yscale('log')
def fitfunc(x, a, b):
    return (a*np.exp(-x/b))

plt.figure()
edges = edges[5:]

y_data = y_data / (edges[1]-edges[0])
x_data = 0.5 * (edges[1:] + edges[:-1]) 
popt, pcov = curve_fit(fitfunc, x_data, y_data[5:])
plt.plot(x_data, y_data[5:])
plt.plot(x_data, fitfunc(x_data, *popt), color='red')

#popt[1] *= 1e-6
#popt[1] = 1e-2

_x = 0.5 * (bins[1:] + bins[:-1])
_y = -popt[1]*popt[0]*(np.exp(-bins[1:]/popt[1]) - np.exp(-bins[:-1]/popt[1]))
#_y = popt[1]*popt[0]*np.exp(-_x/popt[1])
plt.figure()
plt.hist(all_delay, bins=bins)
plt.plot(_x, _y, color='red')
print(popt)
plt.xscale('log')
plt.yscale('log')
plt.ylim(0.1, 3e4)
plt.show()

