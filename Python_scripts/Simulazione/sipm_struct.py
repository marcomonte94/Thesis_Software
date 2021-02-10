import numpy as np
from matplotlib import pyplot as plt
import time

dt = np.dtype([('x_coord', np.int), ('y_coord', np.int), ('time', np.float64), ('type', np.unicode_, 16)])
all_time = np.arange(0, 500, 0.001)


class Microcell:

    def __init__(self, gain=1, overvoltage=1, pde=0.2, t_df=20, t_ds=20, t_rise=3.5):
        self.gain = gain # expressed as unit of overvoltage
        self.overvoltage = overvoltage
        self.pde = pde
        self.t_df = t_df
        self.t_ds = t_ds
        self.t_rise = t_rise
        self.tau_af = 100
        self.last_trigger_time = np.nan

    def eval_overvoltage(self, ev):
        if np.isnan(self.last_trigger_time):
            return self.overvoltage
        else:
            return self.overvoltage * (1 - np.exp(-(ev[2] - self.last_trigger_time) / self.t_ds))

    def eval_gain(self, ev):
        return self.gain * self.eval_overvoltage(ev)

    def eval_pde(self, ev):
        if ev['type'] != 'P':
            return True
        else:
             return np.random.uniform() < self.pde * self.eval_overvoltage(ev)

    def generate_signal(self, t0, t):
        a1, a2 = 7e-2, 3.2e-2
        signal = (a1*np.exp(-(t-t0)/self.t_ds) + a2*np.exp(-(t-t0)/self.t_df) - (a1+a2)*np.exp(-(t-t0)/self.t_rise))
        signal *= np.heaviside(t-t0, 0) 
        return self.gain * signal

    
class SiPM: 
    ''' Class describing a SiPM'''
    def __init__(self, ncell, pde, dark_count_rate, p_ct, p_af):
        self.ncell = ncell
        self.dark_count_rate = dark_count_rate
        self.p_ct = p_ct
        self.p_af = p_af
        self.cellmap = np.full((int(np.sqrt(self.ncell)), int(np.sqrt(self.ncell))), Microcell())
        self.triggers_in = np.empty([0,3], dtype=dt)
        self.triggers_out = np.empty([0,2], float)
        self.signal_ampl = np.zeros(len(all_time))
        self.ct_counts = 0
        self.af_counts = 0
        self.det_counts = 0

    def initialize_sipm(self):
        
        for i in range(int(np.sqrt(self.ncell))):
            for j in range(int(np.sqrt(self.ncell))):
                self.cellmap[i,j] = Microcell()



    def map_photons(self, photonList):
        
        x = np.random.randint(0, int(np.sqrt(self.ncell)), size=len(photonList))
        y = np.random.randint(0, int(np.sqrt(self.ncell)), size=len(photonList))
        #x, y = np.zeros(len(photonList)) + 5, np.zeros(len(photonList)) + 5
        self.triggers_in = np.zeros(len(photonList), dtype=dt)
        self.triggers_in['x_coord'] = x
        self.triggers_in['y_coord'] = y
        self.triggers_in['time'] = photonList
        self.triggers_in[:]['type'] = 'P'

    def add_darkcount(self, t0, t1):
        ''' t1 - t0 = time range of the simulation '''      
        n_mean = self.dark_count_rate * ((t1 - t0) * 1e-9)
        n_events = np.random.poisson(n_mean)
        timestamps = np.random.uniform(t0, t1, size=n_events)
        print(n_events)
        x = np.random.uniform(0, int(np.sqrt(self.ncell)), size=len(timestamps))
        y = np.random.uniform(0, int(np.sqrt(self.ncell)), size=len(timestamps))
        dark_events = np.zeros(len(timestamps), dtype=dt)
        dark_events['x_coord'] = x
        dark_events['y_coord'] = y
        dark_events['time'] = timestamps
        dark_events[:]['type'] = 'dark'

        self.triggers_in = np.append(self.triggers_in, dark_events)
        #print(len(dark_events))


    def add_crosstalk(self, ev, nearest_cells=4):

        p = 1 - ((1-self.p_ct)**(1/nearest_cells))
        n_ct = np.random.binomial(nearest_cells, p)
        step = np.random.choice(nearest_cells, n_ct, replace=False)

        for i in step:
            
            if i == 0 and ev[0] > 0: 
                #print(f'Crosstalk sx: {np.array((ev[0]-1, ev[1], ev[2]), dt)}')
                self.triggers_in = np.append(self.triggers_in, np.array((ev[0]-1, ev[1], ev[2], 'ct'), dt))
                self.ct_counts += 1
            elif i == 1 and ev[0] < (int(np.sqrt(self.ncell)) - 1): 
                #print(f'Crosstalk dx: {np.array((ev[0]+1, ev[1], ev[2]), dt)}')
                self.triggers_in = np.append(self.triggers_in, np.array((ev[0]+1, ev[1], ev[2], 'ct'), dt))
                self.ct_counts += 1
            elif i == 2 and ev[1] > 0:
                #print(f'Crosstalk up: {np.array((ev[0], ev[1]-1, ev[2]), dt)}')
                self.triggers_in = np.append(self.triggers_in, np.array((ev[0], ev[1]-1, ev[2], 'ct'), dt))
                self.ct_counts += 1
            elif i == 3 and ev[1] < (int(np.sqrt(self.ncell)) - 1): 
                #print(f'Crosstalk down: {np.array((ev[0], ev[1]+1, ev[2]), dt)}')
                self.triggers_in = np.append(self.triggers_in, np.array((ev[0], ev[1]+1, ev[2], 'ct'), dt))
                self.ct_counts += 1


    def add_afterpulse(self, ev):

        if np.random.uniform() < self.p_af:
            self.af_counts +=1
            taf = np.random.exponential(self.cellmap[ev[0], ev[1]].tau_af)
            #print(f'Af: {np.array((ev[0], ev[1], ev[2]+taf), dt)}')
            self.triggers_in = np.append(self.triggers_in, np.array((ev[0], ev[1], ev[2]+taf, 'af'), dt))


    def process_photon(self, ev):

        self.triggers_in = self.triggers_in[self.triggers_in!=ev]
        if self.cellmap[ev[0], ev[1]].eval_pde(ev):
            self.det_counts += 1
            g = self.cellmap[ev[0], ev[1]].eval_gain(ev)
            self.add_crosstalk(ev)
            self.add_afterpulse(ev)
            self.triggers_out = np.vstack((self.triggers_out, np.array([g, ev[2]])))
            self.cellmap[ev[0], ev[1]].last_trigger_time = ev[2]
            self.signal_ampl += self.cellmap[ev[0], ev[1]].generate_signal(ev[2], all_time)
        sipm.triggers_in = np.sort(self.triggers_in, order='time' )
        


if __name__ == '__main__':

    ncell, pde, dark_count_rate, p_ct, p_af = 57600, 0.2, 3e6, 0.04, 0.12
    sipm = SiPM(ncell, pde, dark_count_rate, p_ct, p_af)
    sipm.initialize_sipm()
    photon_timestamps = np.arange(1, 20, 0.5)
    print(f'Starting photons: {len(photon_timestamps)}')    
    
    sipm.map_photons(photon_timestamps)
    sipm.add_darkcount(all_time[0], all_time[-1])
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
    
    



    


    