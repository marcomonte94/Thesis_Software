import numpy as np
import os
import argparse
from math import modf
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from scipy.signal import find_peaks
from scipy.stats import norm
from readTrc import Trc
from wf_analysis import DLED, wf_correction, compute_area
import matplotlib.colors as mcolors


def wf_data(wf_path, res_path, n_wf, threshold):

    all_amplitude = np.array([])
    all_delay = np.array([])
    areas = np.array([])

    trc = Trc()
    allMyData = list(os.listdir(wf_path))

    for input_file in allMyData[:n_wf]:

        print("Sto facendo il file {}\n".format(input_file))

        my_wf = '{}/{}.'.format(wf_path, input_file)
        time, ampl, _ = trc.open(my_wf)
        ampl = -ampl
        _, amplDLED = DLED(time, ampl, 50)

        amplDLED = wf_correction(time, amplDLED, threshold)

        peaks, _ = find_peaks(amplDLED, height=threshold, prominence=0.01)

        peak_timestamp = time[peaks]
        peak_amplitude = amplDLED[peaks]
        time_distance = peak_timestamp[1:]-peak_timestamp[:-1]
        
        all_delay = np.concatenate((all_delay, time_distance)) 
        all_amplitude = np.concatenate((all_amplitude, peak_amplitude[1:]))

        dt = np.abs(time[1:] - time[:-1])
        dt = dt.mean()
    
        for i in range(2, len(peaks)-2):

            if peak_timestamp[i] - peak_timestamp[i-1] > 100e-9 and peak_timestamp[i+1] - peak_timestamp[i] > 100e-9:
            #if time_distance[i] > 100e-9 and time_distance[i-1] > 100e-9:

                area = compute_area(ampl, peaks[i], dt)
                area = np.array([area])
                areas = np.concatenate((areas, area))

        
                
    fampl = open(f'{res_path}/all_ampl.txt', 'w')
    fareas = open(f'{res_path}/all_areas.txt', 'w')
    fdelay = open(f'{res_path}/all_delay.txt', 'w')
    #fdcr = open(f'{res_path}/dark_count_rate.txt', 'w')
    
    for i in areas:
        fareas.write(f'{i} \n')
    fareas.close()
        
    for i in range(len(all_amplitude)):
        fampl.write(f'{all_amplitude[i]} \n')
        fdelay.write(f'{all_delay[i]} \n')
        
    
    fdelay.close()
    fampl.close()

    dt = n_wf*0.002
    fdcr = open(f'{res_path}/dark_count_rate.txt', 'w')
    fdcr.write(f'{len(all_amplitude)/dt}')
    fdcr.close()


    #fdcr.write(f'{dark_count_rate(all_amplitude, time, n_wf)}')

    return areas, all_amplitude, all_delay


def gain(areas):
        
    plt.figure()
    y_data, edges, _ = plt.hist(areas, bins=250)
    x_data = 0.5 * (edges[1:] + edges[:-1])

    peakHisto, _ = find_peaks(y_data, height=180, prominence=100)
    plt.plot(x_data[peakHisto], y_data[peakHisto], "x", color='black')
    
    def gaus(x, a, mu, sigma):
        return a * norm.pdf(x, mu, sigma)

    #x_fit1 = x_data[np.logical_and(x_data > 2e-9, x_data < 5e-9)]
    #y_fit1 = y_data[np.logical_and(x_data > 2e-9, x_data < 5e-9)]
    mask_fit1 = np.logical_and(x_data > x_data[peakHisto[0]]-2e-10, x_data < x_data[peakHisto[0]]+2e-10)    
    x_fit1 = x_data[mask_fit1]
    y_fit1 = y_data[mask_fit1]

    p0 = [y_data[peakHisto[0]], x_data[peakHisto[0]], 1e-10]
    popt1, pcov1 = curve_fit(gaus, x_fit1, y_fit1, p0)
    
    mask_fit2 = np.logical_and(x_data > x_data[peakHisto[1]]-1e-10, x_data < x_data[peakHisto[1]]+1e-10) 
    x_fit2 = x_data[mask_fit2]
    y_fit2 = y_data[mask_fit2]
    p0 = [y_data[peakHisto[1]], x_data[peakHisto[1]], 1e-10]
    popt2, pcov2 = curve_fit(gaus, x_fit2, y_fit2, p0)
    
    plt.plot(x_fit1, gaus(x_fit1, *popt1), color='red')
    plt.plot(x_fit2, gaus(x_fit2, *popt2), color='red')

    gain = (popt2[1] - popt1[1]) / (1.6e-19 * 1e4)
    
    return gain
    
    #return 0

def make_scatterplot(all_delay, all_amplitude):

    plt.figure()
    bins_x = 10 ** np.linspace(-8.5, -5.5, 200)
    plt.hist2d(all_delay, all_amplitude, bins=[bins_x, 200], norm=mcolors.LogNorm(), cmap='jet')
    plt.xscale('log')
    plt.xlim(5e-9, 5e-6)
#plt.ylim(0, 0.12)


def cross_talk(all_amplitude, p=80):

    plt.figure()
    plt.title('Amplitudes')
    ydata, edges, _ = plt.hist(all_amplitude, bins=120, orientation='horizontal', label='All amplitudes')
    xdata = 0.5 * (edges[1:] + edges[:-1])
    
    xcdf = np.sort(all_amplitude)
    xcdf[::-1].sort()
    n = xcdf.size
    ycdf = np.arange(1, n+1) 
    
    plt.plot(ycdf, xcdf)

    peaksHisto, _ = find_peaks(ydata, height=300, prominence=p)
    plt.plot(ydata[peaksHisto], xdata[peaksHisto], "x", color='black')
    plt.xscale('log')

    edgeIndex = int(modf((peaksHisto[1] + peaksHisto[0])/2)[1])

    ct = len(all_amplitude[all_amplitude > xdata[edgeIndex]]) / len(all_amplitude)
    return ct
    
def after_pulse(all_delay):

    bins_log = 10**np.arange(-3, +2, 0.02)
    bins_norm = np.linspace(1e-3, 1e+2, 2000)

    all_delay *= 1e6
    plt.figure()
    
    y_data, edges, _ = plt.hist(all_delay, bins=bins_norm)
    plt.close()
    
    def fitfunc(x, a, b):
        return (a*np.exp(-x/b))

    edges = edges[5:]

    y_data = y_data / (edges[1]-edges[0])
    y_data = y_data[5:]
    x_data = 0.5 * (edges[1:] + edges[:-1]) 
    xfit = x_data[x_data>-1]
    yfit = y_data[x_data>-1]
    popt, pcov = curve_fit(fitfunc, xfit, yfit)
    #plt.plot(xfit, fitfunc(xfit, *popt))
    
    plt.figure()
    ydata, _, _ = plt.hist(all_delay, bins=bins_log)
    

    _x = 0.5 * (bins_log[1:] + bins_log[:-1])
    _y = -popt[1]*popt[0]*(np.exp(-bins_log[1:]/popt[1]) - np.exp(-bins_log[:-1]/popt[1]))
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

    parser = argparse.ArgumentParser(description='SiPM analysis results')
    parser.add_argument('id', help='SiPM ID and Voltage')
    parser.add_argument('-w', '--write', help='Compute and process results', default = '0')
    args = parser.parse_args()

    if args.write == '0':
        areas = np.loadtxt(f'C:/Users/Marco/Desktop/Analisi_SiPM/Caratterizzazione/{args.id}/all_areas.txt', unpack=True)
        all_amplitude = np.loadtxt(f'C:/Users/Marco/Desktop/Analisi_SiPM/Caratterizzazione/{args.id}/all_ampl.txt', unpack=True)
        all_delay = np.loadtxt(f'C:/Users/Marco/Desktop/Analisi_SiPM/Caratterizzazione/{args.id}/all_delay.txt', unpack=True)
    

    elif args.write == '1':
        path = f'C:/Users/Marco/Desktop/{args.id}'
        res_path = f'C:/Users/Marco/Desktop/Analisi_SiPM/Caratterizzazione/{args.id}' 
        areas, all_amplitude, all_delay = wf_data(path, res_path, 40, 0.016)
    
    make_scatterplot(all_delay, all_amplitude)
    g = gain(areas)
    ct = cross_talk(all_amplitude, 150)
    r = after_pulse(all_delay)

    print('Gain: {}'.format(g))
    print("Cross talk probability: {}".format(ct))
    print("After pulse probability: {}".format(r))

    plt.show()

