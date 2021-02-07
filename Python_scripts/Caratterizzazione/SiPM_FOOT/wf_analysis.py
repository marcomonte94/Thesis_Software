import numpy as np
import os
from matplotlib import pyplot as plt
from scipy.signal import find_peaks
from scipy.optimize import curve_fit
from readTrc import Trc


def DLED(time, ampl, delay):

    def shift(xs, n):
        if n >= 0:
            return np.concatenate((np.full(n, 0), xs[:-n]))
        else:
            return np.concatenate((xs[-n:], np.full(-n, 0)))

    right_time = np.linspace(time[len(time)-1]+1e-10, time[len(time)-1]+(1+delay)*1e-10, delay)

    time_delay = np.concatenate((time[delay:], right_time))
    ampl_delay = shift(ampl, delay)

    timeDLED = time_delay
    amplDLED = ampl - ampl_delay

    return timeDLED, amplDLED


def wf_correction(time, amplDLED, threshold):

    peaks, _ = find_peaks(amplDLED, height=threshold, prominence=threshold/2)
    peak_timestamp = time[peaks]
    peak_amplitude = amplDLED[peaks]
    time_distance = peak_timestamp[1:]-peak_timestamp[:-1]

    wfToNormalize = np.zeros(3000)

    for i in range(5, len(peaks)-5):

        if time_distance[i] > 500e-9 and time_distance[i-1] > 500e-9:
        #if time[peaks[i]] - time[peaks[i-1]] > 500e-9 and time[peaks[i+1]] - time[peaks[i]]> 500e-9:

            wfGood = amplDLED[peaks[i]-1000 : peaks[i]+2000]
            wfGood = wfGood / peak_amplitude[i]
            wfToNormalize = np.vstack((wfToNormalize, wfGood))

    wf_ok = np.mean(wfToNormalize[1:], axis=0)
    undershoot = np.zeros(len(wf_ok))

    for i in range (3000):
        if wf_ok[i]<0:
            undershoot[i] = wf_ok[i]

    for i in range(10, len(peaks)-10):
        amplDLED[peaks[i]-1000 : peaks[i]+2000] -= undershoot*amplDLED[peaks[i]]
    #plt.figure()
    #plt.plot(wf_ok)
    #plt.plot(undershoot)

    return amplDLED


def compute_area(ampl, picco, dt):

    baseline = ampl[picco-200:picco-100].mean()
    ampl[picco-200:picco+900] = ampl[picco-200:picco+900]-baseline
    area = (ampl[picco-200:picco+900]*dt).sum()
    #plt.figure()
    #plt.plot(ampl[picco-200:picco+900])
    #plt.plot(ampl[picco-200:picco-100])
    #plt.show()
    return area



if __name__ == '__main__':

    allMyData = list = os.listdir('C:/Users/Marco/Desktop/id31/124')
    trc = Trc()

    for input_file in allMyData[:1]:

        print("Sto facendo il file {}/n".format(input_file))

        wf_path = 'C:/Users/Marco/Desktop/id31/124/{}.'.format(input_file)
        time, ampl, d = trc.open(wf_path)
        print(d)
        ampl = -ampl
        timeDLED, amplDLED = DLED(time, ampl, 50)

    plt.figure()
    plt.title('Delayed Waveform')
    plt.plot(time, ampl, label='Waveform')
    #plt.plot(timeDLED, amplDLED+ampl, label='Delayed Waveform')
    plt.legend(loc='best')
    plt.close()

    plt.figure()
    plt.title('DLED Waveform')
    plt.plot(time, ampl, label='Waveform', color='blue')
    plt.plot(time, amplDLED, label='DLED Waveform', color='red')
    peaks, _ = find_peaks(amplDLED, height=0.016, prominence=0.008)
    plt.plot(time[peaks], amplDLED[peaks], 'x', color='black')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude (V)')
    plt.close()
    #amplDLED = - amplDLED
    amplDLED = wf_correction(timeDLED, amplDLED, 0.016)

    plt.figure()
    plt.title('Corrected waveform')
    plt.plot(time, amplDLED, label='Corrected wf')
    peaks, _ = find_peaks(amplDLED, height=0.016, prominence=0.008)
    plt.plot(time[peaks], amplDLED[peaks], 'x', color='black')
    plt.close()

    plt.figure()
    plt.title('Picchi onda vera')
    time *= 1e9
    plt.plot(time, ampl, label='Waveform', color='blue')
    peaks, _ = find_peaks(amplDLED, height=0.016, prominence=0.008)
    plt.plot(time[peaks], ampl[peaks], 'x', color='black')
    plt.xlabel('Time (ns)')
    plt.ylabel('Amplitude (V)')
    plt.close()
    
    plt.show()









