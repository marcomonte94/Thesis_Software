import time
import numpy as np
import os
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from scipy.signal import find_peaks
from readTrc import Trc
from scipy.stats import norm

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
    
    return timeDLED, amplDLED

def gaus(x, a, mu, sigma):
    return a * norm.pdf(x, mu, sigma)

if __name__ == '__main__':

    

    allMyData = list = os.listdir('C:/Users/39348/Desktop/Thesis_Software/test-gpib/A6_56V')
    trc = Trc()
    areas = np.array([])
    for input_file in allMyData[:20]:

        print("Sto facendo il file {}\n".format(input_file))

        wf_path = 'C:/Users/39348/Desktop/Thesis_Software/test-gpib/A6_56V/{}.'.format(input_file)
        time, ampl, d = trc.open(wf_path)
        #print(d)

        timeDLED, amplDLED = DLED(time,ampl, 20)
        peaks, _ = find_peaks(-amplDLED, height=0.0085, prominence=0.02)

        peak_timestamp = time[peaks]
        peak_amplitude = amplDLED[peaks]
        time_distance = peak_timestamp[1:]-peak_timestamp[:-1]
        
        dt = np.abs(time[1:] - time[:-1])
        dt = dt.mean()
        #ampl = -ampl
        '''
        for i in peaks[2:-2]:

            print(i)
            print(i+1)
            print('\n')
            time_prima = time[i-1:i]
            baseline = ampl[i-1:i].mean()
            ampl[i-1:i+5]-baseline
            area.append((ampl[i-1:i+3]*dt).sum())
        '''
        for i in range(2, len(peaks)-2):

            #if time_distance[i] > 500e-9 and time_distance[i+1] > 500e-9:
            if peak_timestamp[i] - peak_timestamp[i-1] > 500e-9:

                baseline = ampl[peaks[i]-1000:peaks[i]-500].mean()
                #baseline =0
                ampl[peaks[i]-500:peaks[i]+3500] = ampl[peaks[i]-500:peaks[i]+3500]-baseline
                area = (ampl[peaks[i]-500:peaks[i]+3500]*dt).sum()
                area = np.array([area])
                areas = np.concatenate((areas, area))
                #plt.plot(ampl[peaks[i]-500:peaks[i]+2000])
    
    mask1 = areas > 3e-9
    mask2 = areas < 4.5e-9
    
    area_fit = areas[np.logical_and(areas > 3e-9, areas < 4.5e-9)]
        
    plt.figure()
    y_data, edges, _ = plt.hist(areas, bins=250)
    x_data = 0.5 * (edges[1:] + edges[:-1])

    peakHisto, _ = find_peaks(y_data, prominence=100)
    print(peakHisto)
    plt.plot(x_data[peakHisto], y_data[peakHisto], "x", color='black')

    x_fit1 = x_data[np.logical_and(x_data > 2e-9, x_data < 5e-9)]
    y_fit1 = y_data[np.logical_and(x_data > 2e-9, x_data < 5e-9)]
    p0 = [100, 3e-9, 1e-9]
    popt1, pcov1 = curve_fit(gaus, x_fit1, y_fit1, p0)
    
    x_fit2 = x_data[np.logical_and(x_data > 6.5e-9, x_data < 8.5e-9)]
    y_fit2 = y_data[np.logical_and(x_data > 6.5e-9, x_data < 8.5e-9)]
    p0 = [100, 7e-9, 1e-9]
    popt2, pcov2 = curve_fit(gaus, x_fit2, y_fit2, p0)
    

    plt.plot(x_fit1, gaus(x_fit1, *popt1), color='red')
    plt.plot(x_fit2, gaus(x_fit2, *popt2), color='red')
    #plt.figure()
    #plt.plot(x_fit, y_fit)
    #plt.plot(time[peaks], -amplDLED[peaks], "x")

    gain = (popt2[1] - popt1[1]) / (1.6e-19 * 1e4)

    print('Gain: {}'.format(gain))
    
    plt.show()

