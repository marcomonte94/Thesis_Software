import numpy as np
import os
from math import modf
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from scipy.signal import find_peaks
from scipy.stats import norm
from readTrc import Trc
from wf_analysis import DLED, wf_correction, compute_area


def wf_data(wf_path, n_wf):

    all_amplitude = np.array([])
    all_delay = np.array([])
    areas = np.array([])

    trc = Trc()

    #allMyData = list = os.listdir('C:/Users/39348/Desktop/Thesis_Software/test-gpib/A6_56V')
    allMyData = list(os.listdir(wf_path))

    for input_file in allMyData[:n_wf]:

        print("Sto facendo il file {}\n".format(input_file))

        my_wf = '{}/{}.'.format(wf_path, input_file)
        time, ampl, d = trc.open(my_wf)

        amplDLED = wf_correction(time, ampl)

        peaks, _ = find_peaks(-amplDLED, height=0.0085, prominence=0.02)

        peak_timestamp = time[peaks]
        peak_amplitude = amplDLED[peaks]
        time_distance = peak_timestamp[1:]-peak_timestamp[:-1]
        
        all_delay = np.concatenate((all_delay, time_distance)) 
        all_amplitude = np.concatenate((all_amplitude, -peak_amplitude[1:]))

        dt = np.abs(time[1:] - time[:-1])
        dt = dt.mean()
    
        for i in range(2, len(peaks)-2):

            if peak_timestamp[i] - peak_timestamp[i-1] > 500e-9:

                area = compute_area(ampl, peaks[i], dt)
                area = np.array([area])
                areas = np.concatenate((areas, area))

    return areas, all_amplitude, all_delay


def gain(areas):
      
    mask1 = areas > 3e-9
    mask2 = areas < 4.5e-9
    
    area_fit = areas[np.logical_and(areas > 3e-9, areas < 4.5e-9)]
        
    y_data, edges, _ = plt.hist(areas, bins=250)
    x_data = 0.5 * (edges[1:] + edges[:-1])

    peakHisto, _ = find_peaks(y_data, prominence=40)
    plt.plot(x_data[peakHisto], y_data[peakHisto], "x", color='black')

    def gaus(x, a, mu, sigma):
        return a * norm.pdf(x, mu, sigma)

    #x_fit1 = x_data[np.logical_and(x_data > 2e-9, x_data < 5e-9)]
    #y_fit1 = y_data[np.logical_and(x_data > 2e-9, x_data < 5e-9)]
    mask_fit1 = np.logical_and(x_data > x_data[peakHisto[0]]-3e-9, x_data < x_data[peakHisto[0]]+3e-9)    
    x_fit1 = x_data[mask_fit1]
    y_fit1 = y_data[mask_fit1]

    p0 = [100, 3e-9, 1e-9]
    popt1, pcov1 = curve_fit(gaus, x_fit1, y_fit1, p0)
    
    mask_fit2 = np.logical_and(x_data > x_data[peakHisto[1]]-1e-9, x_data < x_data[peakHisto[1]]+1e-9) 
    x_fit2 = x_data[mask_fit2]
    y_fit2 = y_data[mask_fit2]
    p0 = [100, 7e-9, 1e-9]
    popt2, pcov2 = curve_fit(gaus, x_fit2, y_fit2, p0)
    
    plt.figure()
    plt.plot(x_fit1, gaus(x_fit1, *popt1), color='red')
    plt.plot(x_fit2, gaus(x_fit2, *popt2), color='red')

    gain = (popt2[1] - popt1[1]) / (1.6e-19 * 1e4)

    return gain


def cross_talk(all_delay, all_amplitude, p):

    plt.figure()
    plt.xscale('log')
    plt.scatter(all_delay, all_amplitude, marker='.')

    plt.figure()
    ydata, edges, _ = plt.hist(all_amplitude, bins=150, orientation='horizontal')
    xdata = 0.5 * (edges[1:] + edges[:-1])

    xcdf = np.sort(all_amplitude)
    xcdf[::-1].sort()
    n = xcdf.size
    ycdf = np.arange(1, n+1) 
    
    plt.plot(ycdf, xcdf)

    peaksHisto, _ = find_peaks(ydata, height=10, prominence=p)
    plt.plot(ydata[peaksHisto], xdata[peaksHisto], "x", color='black')
    plt.xscale('log')

    edgeIndex = int(modf((peaksHisto[1] + peaksHisto[0])/2)[1])

    ct = len(all_amplitude[all_amplitude > xdata[edgeIndex]]) / len(all_amplitude)
    return ct
    

def after_pulse(all_delay):

    plt.figure()

    bins = 10**np.arange(-3, +2, 0.02)
    bins2 = np.linspace(1e-3, 1e+2, 200)

    all_delay *= 1e6
    y_data, edges, _ = plt.hist(all_delay, bins=bins2)
    
    def fitfunc(x, a, b):
        return (a*np.exp(-x/b))

    edges = edges[5:]

    y_data = y_data / (edges[1]-edges[0])
    x_data = 0.5 * (edges[1:] + edges[:-1]) 
    popt, pcov = curve_fit(fitfunc, x_data, y_data[5:])
    
    plt.figure()
    ydata, _, _ = plt.hist(all_delay, bins=bins)
    

    _x = 0.5 * (bins[1:] + bins[:-1])
    _y = -popt[1]*popt[0]*(np.exp(-bins[1:]/popt[1]) - np.exp(-bins[:-1]/popt[1]))
    #print(len(y_data[y_data > _y]))
    plt.plot(_x, _y, color='red')
    
    yaf = ydata[_x < 2e-1] - _y[_x < 2e-1]
    yaf = yaf[yaf > 0]
    n_event = sum(ydata)
    
    plt.xscale('log')
    plt.yscale('log')
    plt.ylim(0.1, 3e4)

    return yaf.sum()/ n_event


if __name__ == '__main__':
    
    path = 'C:/Users/39348/Desktop/Thesis_Software/test-gpib/SIPM test/A6_56e5V'
    areas, all_amplitude, all_delay = wf_data(path, 20)
    
    #g = gain(areas)
    ct = cross_talk(all_delay, all_amplitude, 100)
    #r = after_pulse(all_delay)

    #print('Gain: {}'.format(g))
    print("Cross talk probability: {}".format(ct))
    #print("After pulse probability: {}".format(r))

    plt.show()

