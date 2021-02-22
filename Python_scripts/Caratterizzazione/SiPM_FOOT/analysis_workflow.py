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
        
    plt.figure(figsize=[7., 5.])
    plt.rc('font', size=12)
    y_data, edges, _ = plt.hist(areas, bins=250, color='blue', label='Occurrences')
    x_data = 0.5 * (edges[1:] + edges[:-1])
    plt.xlim(0, 3e-9)
    plt.xlabel('Waveforms area [$V\cdot s$]')
    plt.ylabel('Counts')

    peakHisto, _ = find_peaks(y_data, height=180, prominence=50)
    plt.plot(x_data[peakHisto], y_data[peakHisto], "x", color='black')
    
    def gaus(x, a, mu, sigma):
        return a * norm.pdf(x, mu, sigma)

    #x_fit1 = x_data[np.logical_and(x_data > 2e-9, x_data < 5e-9)]
    #y_fit1 = y_data[np.logical_and(x_data > 2e-9, x_data < 5e-9)]
    mask_fit1 = np.logical_and(x_data > x_data[peakHisto[0]]-2e-10, x_data < x_data[peakHisto[0]]+1.7e-10)    
    x_fit1 = x_data[mask_fit1]
    y_fit1 = y_data[mask_fit1]

    p0 = [y_data[peakHisto[0]], x_data[peakHisto[0]], 1e-10]
    popt1, pcov1 = curve_fit(gaus, x_fit1, y_fit1, p0, sigma=np.sqrt(y_fit1))
    
    mask_fit2 = np.logical_and(x_data > x_data[peakHisto[1]]-2e-10, x_data < x_data[peakHisto[1]]+2e-10) 
    x_fit2 = x_data[mask_fit2]
    y_fit2 = y_data[mask_fit2]
    p0 = [y_data[peakHisto[1]], x_data[peakHisto[1]], 1e-10]
    popt2, pcov2 = curve_fit(gaus, x_fit2, y_fit2, p0, sigma=np.sqrt(y_fit2))
    
    plt.plot(x_fit1, gaus(x_fit1, *popt1), color='red', label='Gaussian fit')
    plt.plot(x_fit2, gaus(x_fit2, *popt2), color='red')
    plt.legend(loc='best')

    gain = (popt2[1] - popt1[1]) / (1.6e-19 * 1e4)
    d_gain = np.sqrt((pcov1.diagonal()[1] + pcov2.diagonal()[1])) / (1.6e-19 * 1e4)
    #d_gain = np.sqrt((popt1[2]**2 + popt2[2]**2)) / (1.6e-19 * 1e4)
    return gain, d_gain
    
    #return 0, 0

def make_scatterplot(all_delay, all_amplitude):

    plt.figure(figsize=[7., 5.])
    plt.rc('font', size=12)
    bins_x = 10 ** np.linspace(-8.5, -5.5, 200)
    plt.hist2d(all_delay, all_amplitude, bins=[bins_x, 200], norm=mcolors.LogNorm(), cmap='jet')
    plt.xscale('log')
    plt.xlim(5e-9, 5e-6)
    plt.xlabel('Time distance [$s$]')
    plt.ylabel('Amplitude [$V$]')
    plt.colorbar()
#plt.ylim(0, 0.12)


def cross_talk(all_amplitude, p=100):

    plt.figure(figsize=[7., 5.])
    plt.rc('font', size=12)
    plt.yscale('log')
    #plt.legend(loc='best')
    #plt.title('Amplitudes')
    y_data, edges, _ = plt.hist(all_amplitude, bins=120, color='blue', label='Occurrences')
    x_data = 0.5 * (edges[1:] + edges[:-1])
    plt.ylabel('Amplitude [$V$]')
    plt.xlabel('Counts')

    peakHisto, _ = find_peaks(y_data, height=100, prominence=p)
    #peakHisto = []
    #peakHisto.append(max(y_data[x_data > 0.025]))
    #peakHisto.append(max(y_data[x_data > 0.045]))
    #plt.plot(y_data[peakHisto], x_data[peakHisto], "x", color='black')
    plt.plot(x_data[peakHisto], y_data[peakHisto], "x", color='black')

    
    def gaus(x, a, mu, sigma):
        return a * norm.pdf(x, mu, sigma)

    mask_fit1 = np.logical_and(x_data > x_data[peakHisto[0]]-5e-3, x_data < x_data[peakHisto[0]]+8e-3)    
    x_fit1 = x_data[mask_fit1]
    y_fit1 = y_data[mask_fit1]

    p0 = [y_data[peakHisto[0]], x_data[peakHisto[0]], 1e-3]
    popt1, pcov1 = curve_fit(gaus, x_fit1, y_fit1, p0, sigma=np.sqrt(y_fit1))
    
    mask_fit2 = np.logical_and(x_data > x_data[peakHisto[1]]-5e-3, x_data < x_data[peakHisto[1]]+8e-3) 
    x_fit2 = x_data[mask_fit2]
    y_fit2 = y_data[mask_fit2]
    p0 = [y_data[peakHisto[1]], x_data[peakHisto[1]], 1e-3]
    popt2, pcov2 = curve_fit(gaus, x_fit2, y_fit2, p0, sigma=np.sqrt(y_fit2))
    
    plt.plot(x_fit1, gaus(x_fit1, *popt1), color='red', label='Gaussian fit')
    plt.plot(x_fit2, gaus(x_fit2, *popt2), color='red')
    plt.legend(loc='best')
    
    xcdf = np.sort(all_amplitude)
    _x = xcdf[::-1].sort()
    n = xcdf.size
    ycdf = np.arange(1, n+1) 
    
    #_y, _x = np.linspace(0, max(ycdf), 1000), np.linspace(0, max(_x), 1000)
    #plt.plot(ycdf, xcdf, color='green', label='Cumulative function')


    a = (popt1[1] + popt2[1]) / 2
    da = np.sqrt(pcov1.diagonal()[1] + pcov2.diagonal()[1]) / 2
    ct1 = len(all_amplitude[all_amplitude > a+da]) / len(all_amplitude) 
    ct2 = len(all_amplitude[all_amplitude > a-da]) / len(all_amplitude) 
    ct = np.mean([ct1, ct2])
    print(da)
    print(f'{ct1}, {ct2}')
    d_ct = np.std([ct1, ct2])
    
    edgeIndex = int(modf((peakHisto[1] + peakHisto[0])/2)[1])
    print(x_data[edgeIndex])
    ct = len(all_amplitude[all_amplitude > x_data[edgeIndex]]) / len(all_amplitude)
    
    return ct, d_ct
    
    #return 0, 0
    
def after_pulse(all_delay):

    bins_log = 10**np.arange(-3, +2, 0.02)
    bins_norm = np.linspace(1e-3, 1e+2, 2000)

    all_delay *= 1e6
    plt.figure(figsize=[7., 5.])
    plt.rc('font', size=12)
    y_data, edges, _ = plt.hist(all_delay, bins=bins_norm)
    plt.close()
    
    def fitfunc(x, a, b):
        return (a*np.exp(-x/b))
        #return a * np.exp(-b*x)

    edges = edges[5:]
    dy_data = np.sqrt(y_data) / (edges[1]-edges[0])
    y_data = y_data / (edges[1]-edges[0])
    y_data = y_data[5:]
    dy_data = dy_data[5:]
    x_data = 0.5 * (edges[1:] + edges[:-1]) 
    mask = np.logical_and(x_data>1e-1, x_data<2)
    xfit = x_data[mask]
    yfit = y_data[mask]
    dyfit = dy_data[mask]
    p0 = [1e6, 0.5]
    popt, pcov = curve_fit(fitfunc, xfit, yfit, p0=p0, sigma=dyfit)
    #print(f'Fit params: {popt[0]}+- {np.sqrt(pcov.diagonal()[0])}, {popt[1]} +- {np.sqrt(pcov.diagonal()[1])}')
    #plt.plot(xfit, yfit)
    #plt.plot(xfit, fitfunc(xfit, *popt))
    #plt.xlim(0, 50)
    dcr, d_dcr = 1/popt[1], np.sqrt(pcov.diagonal()[1])/(popt[1]**2)
    
    plt.figure(figsize=[7., 5.])
    plt.rc('font', size=12)
    ydata, _, _ = plt.hist(all_delay, bins=bins_log, color='blue', label='Occurrences')
    plt.ylabel('Counts')
    plt.xlabel('Time distance [$\mu s$]')

    _x = 0.5 * (bins_log[1:] + bins_log[:-1])
    _y = -popt[1]*popt[0]*(np.exp(-bins_log[1:]/popt[1]) - np.exp(-bins_log[:-1]/popt[1]))
    #print(len(y_data[y_data > _y]))
    plt.plot(_x, _y, color='red', label='Exponential fit')
    
    yaf = ydata[_x < 1e-1] - _y[_x < 1e-1]
    yaf = yaf[yaf > 0]
    n_event = sum(ydata)
    #n_event = len(ydata)
    
    plt.xscale('log')
    plt.yscale('log')
    plt.ylim(0.1, 3e4)
    plt.legend(loc='best')
    #print(f'Error: {np.sqrt(yaf).sum()/ n_event}')
    af, d_af = yaf.sum()/ n_event, np.sqrt((yaf**2).sum())/ n_event
    return dcr, d_dcr, af, d_af


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
    g, dg = gain(areas)
    ct, d_ct = cross_talk(all_amplitude, 280)
    dcr, d_dcr, af, d_af = after_pulse(all_delay)
    print("Dcr: {} +- {}".format(dcr, d_dcr))
    print('Gain: {} +- {}'.format(g, dg))
    print("Cross talk probability: {} +- {}".format(ct, d_ct))
    print("After pulse probability: {} +- {}".format(af, d_af))

    plt.show()

