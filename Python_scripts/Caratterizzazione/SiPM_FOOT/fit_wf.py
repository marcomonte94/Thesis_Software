import numpy as np
import os
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from scipy.signal import find_peaks
from readTrc import Trc
from wf_analysis import DLED, wf_correction

#plt.style.use('thesis')

def compute_area(ampl, picco, dt):

    baseline = ampl[picco-200:picco-100].mean()
    ampl[picco-200:picco+900] = ampl[picco-200:picco+900]-baseline
    area = (ampl[picco-200:picco+900]*dt).sum()
    #plt.figure()
    #plt.plot(ampl[picco-200:picco+900])
    #plt.plot(ampl[picco-200:picco-100])
    #plt.show()
    return area

time, a, _ = Trc().open('C:/Users/Marco/Desktop/Saturazione/9.5/C1--trigger--00000.trc')
a = -a
'''
timeDLED, amplDLED = DLED(time, ampl, 50)

#plt.figure()
#plt.plot(ampl)
#plt.figure()
#plt.plot(amplDLED)

peaks, _ = find_peaks(amplDLED, height=0.016, prominence=0.005)
amplDLED = wf_correction(timeDLED, amplDLED, 0.016)
peaks, _ = find_peaks(amplDLED, height=0.016, prominence=0.005)
peak_timestamp = time[peaks]
time_distance = peak_timestamp[1:]-peak_timestamp[:-1]

a = np.empty([0,1100], float)

for i in range(5, len(peaks)-5):

    if time_distance[i] > 500e-9 and time_distance[i-1] > 500e-9:

        if compute_area(ampl, peaks[i], time[1]-time[0]) < 2e-9:
            a = np.vstack((a, ampl[peaks[i]-200 : peaks[i]+900]))

a = np.mean(a, axis=0) /1e4
'''
def f(t, t0, a1, a2, tf, ts):
    #return np.heaviside(t-t0, 0) * np.exp(-(t-t0)/t_recovery)
    return np.heaviside(t-t0, 0) * (a1*np.exp(-(t-t0)/tf) + a2*np.exp(-(t-t0)/ts))

def fitfunc(t, t0, a1, a2, t_ds, t_df, t_r):
    return np.heaviside(t-t0, 0) * (a1*np.exp(-(t-t0)/t_ds) + a2*np.exp(-(t-t0)/t_df) - (a1+a2)*np.exp(-(t-t0)/t_r))


#tfit = np.arange(300, 800)*1e-10
#tfit = np.arange(len(a))*1e-10
tfit = time - min(time)

p0 = [3e-8, -5, 5, 5e-10, 30e-9]
#p0 = [1e-8, 10, 100, 2e-8, 1e-9, 1e-10]
popt, pcov = curve_fit(f, tfit, a, p0=p0)
print(popt)
print(f't0: {popt[0]} +- {np.sqrt(pcov.diagonal()[0])}')
print(f'a1: {popt[1]} +- {np.sqrt(pcov.diagonal()[1])}')
print(f'a2: {popt[2]} +- {np.sqrt(pcov.diagonal()[2])}')
print(f't rise: {popt[3]} +- {np.sqrt(pcov.diagonal()[3])}')
print(f't rec: {popt[4]} +- {np.sqrt(pcov.diagonal()[4])}')
#print(f'tr: {popt[5]}')

print('\n')
print(f'Area curva: {sum(a*(tfit[1]-tfit[0]))}')

plt.figure(figsize=[7., 5.5])
plt.rc('font', size=12)
plt.xlabel('Time [s]')
plt.ylabel('Amplitude [V]')
plt.plot(tfit, a, '.', color='black', label='Experimental points')
plt.plot(tfit, f(tfit, *popt), color='red', label='Fitted waveform')
plt.legend(loc='best')
#print('Single cell area:    {}.'format())

plt.show()