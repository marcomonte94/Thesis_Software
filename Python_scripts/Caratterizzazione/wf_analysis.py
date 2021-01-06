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
    amplDLED = ampl_delay - ampl
    
    return timeDLED, amplDLED


def wf_correction(time, ampl):

    timeDLED, amplDLED = DLED(time,ampl, 20)
    peaks, _ = find_peaks(-amplDLED, height=0.0085, prominence=0.02)
    peak_timestamp = time[peaks]
    peak_amplitude = amplDLED[peaks]
    time_distance = peak_timestamp[1:]-peak_timestamp[:-1]

    wfToNormalize = np.zeros(3000)

    for i in range(1, len(peaks)-2):

        if time_distance[i] > 500e-9 and time_distance[i+1] > 500e-9:

            wfGood = amplDLED[peaks[i]-1000 : peaks[i]+2000]
            wfGood = wfGood / peak_amplitude[i]
            wfToNormalize = np.vstack((wfToNormalize, wfGood))

    wf_ok = np.mean(wfToNormalize, axis=0)
    undershoot = np.zeros(len(wf_ok))

    for i in range (3000):
        if wf_ok[i]<0:
            undershoot[i] = wf_ok[i]

    for i in range(1, len(peaks)-2):
        amplDLED[peaks[i]-1000 : peaks[i]+2000] -= undershoot*amplDLED[peaks[i]]
    #plt.plot(wf_ok)
    #plt.plot(undershoot)

    return amplDLED


def compute_area(ampl, picco, dt):

    baseline = ampl[picco-1000:picco-500].mean()
    ampl[picco-500:picco+3500] = ampl[picco-500:picco+3500]-baseline
    area = (ampl[picco-500:picco+3500]*dt).sum()
    return area


def recovery_time(time, ampl):

    timeDLED, amplDLED = DLED(time,ampl, 20)
    peaks, _ = find_peaks(-amplDLED, height=0.0085, prominence=0.02)
    peak_timestamp = time[peaks]
    peak_amplitude = amplDLED[peaks]
    time_distance = peak_timestamp[1:]-peak_timestamp[:-1]

    areas = np.array([])
    single_wf = np.zeros(3000)

    for i in range(1, len(peaks)-2):

        area = compute_area(ampl, peaks[i], time[1]-time[0])

        if area < 4e-9:

            if time_distance[i] > 500e-9 and time_distance[i+1] > 500e-9:
            
                wfGood = ampl[peaks[i]-500 : peaks[i]+2500]
                #wfGood = wfGood / peak_amplitude[i]
                single_wf = np.vstack((single_wf, wfGood))

    single_wf = np.mean(single_wf, axis=0)

    def f(x, a, b):
        #return a*np.exp(-b*x)
        return a - x*b

    yfit = np.log(single_wf[600:1150])
    #yfit = single_wf[600:1160]
    tfit = np.arange(600, 1150) * 1e-10

    popt, pcov = curve_fit(f, tfit, yfit)

    plt.figure()
    #plt.yscale('log')
    plt.plot(np.arange(0, 3000) * 1e-10, single_wf)
    #plt.plot(tfit, yfit)
    plt.plot(tfit, np.exp(f(tfit, *popt)))

    tau = 1 /popt[1]
    dtau = np.sqrt(pcov.diagonal()[1])/(popt[1]**2)

    return tau, dtau 


if __name__ == '__main__':

    allMyData = list = os.listdir('C:/Users/39348/Desktop/Thesis_Software/test-gpib/A6_56V')
    trc = Trc()
    

    for input_file in allMyData[:1]:

        print("Sto facendo il file {}\n".format(input_file))

        wf_path = 'C:/Users/39348/Desktop/Thesis_Software/test-gpib/A6_56V/{}.'.format(input_file)
        time, ampl, d = trc.open(wf_path)
        #ampl = -ampl
        timeDLED, amplDLED = DLED(time, ampl, 20)
        

    plt.figure()
    plt.title('Delayed Waveform')
    plt.plot(time, ampl, label='Waveform')
    plt.plot(timeDLED, amplDLED+ampl, label='Delayed Waveform')
    plt.legend(loc='best')
    plt.close()

    plt.figure()
    plt.title('DLED Waveform')
    plt.plot(time, -amplDLED)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude (V)')
    plt.close()
    #amplDLED = - amplDLED
    amplDLED = wf_correction(time, ampl)

    plt.figure()
    plt.title('Corrected waveform')
    plt.plot(time, -amplDLED, label='Corrected wf')
    plt.close()
    '''
    plt.figure()
    plt.title('Single-cell wf')
    plt.plot(oneCell_wf(time, ampl), label='Single-cell wf')
    #plt.yscale('log')
    '''
    tau, dtau = recovery_time(time, ampl)
    print('Recovey time: ({:.2f} +/- {:.2f}) ns'.format(tau*1e9, dtau*1e9))
    plt.show()









