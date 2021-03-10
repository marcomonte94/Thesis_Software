all_amplitude = np.loadtxt('C:/Users/Marco/Desktop/Analisi_SiPM/Caratterizzazione/id11/124/all_ampl.txt', unpack=True)
all_delay = np.loadtxt('C:/Users/Marco/Desktop/Analisi_SiPM/Caratterizzazione/id11/120/all_delay.txt', unpack=True)

bins_log = 10**np.arange(-3, +2, 0.02)
bins_norm = np.linspace(1e-3, 1e+2, 2000)

all_delay *= 1e6
plt.figure(figsize=[7., 5.])
plt.rc('font', size=12)
y_data, edges, _ = plt.hist(all_delay, bins=bins_norm)
#plt.close()

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
plt.plot(xfit, fitfunc(xfit, *popt))
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

plt.figure()
bb = np.linspace(0, 1, 200)
y, e, _ =  plt.hist(all_delay, bins=bb)
yf = -popt[1]*popt[0]*(np.exp(-bb[1:]/popt[1]) - np.exp(-bb[:-1]/popt[1]))
xf = 0.5 * (bb[1:] + bb[:-1])
plt.plot(xf, yf)
plt.figure()
plt.plot(xf, y-yf, '.', color='black')
yy = y-yf
m = np.logical_and(xf>0.02, xf<0.1)
p0 = [1e5, 0.1]
popt, pcov = curve_fit(fitfunc, xf[m], yy[m], p0)
plt.plot(xf, fitfunc(xf, *popt))
plt.show()





