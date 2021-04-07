import numpy as np
from matplotlib import pyplot as plt
import time

np.random.seed(0)

dt = np.dtype([
    ('x_coord',     int), 
    ('y_coord',     int), 
    ('time',        np.float32),
    ('type',        np.unicode_, 16)
     ])

dt_evt = np.dtype([
    ('id_event',    np.float32), 
    ('time',        np.float32), 
    ('x',           np.float32),
    ('y',           np.float32)
     ])

class Microcell:

    def __init__(self, gain=1, overvoltage=1, pde=0.2, t_df=1.21, t_ds=24.8, t_rise=0.98):
        self.gain = gain # expressed as unit of overvoltage
        self.overvoltage = overvoltage
        self.pde = pde
        self.t_df = t_df
        self.t_ds = t_ds
        self.t_rise = t_rise
        self.tau_af = 14.5
        self.last_trigger_time = np.nan

    def eval_overvoltage(self, ev):
        if np.isnan(self.last_trigger_time):
            return self.overvoltage
        else:
            return self.overvoltage * (1 - np.exp(-(ev['time'] - self.last_trigger_time) / self.t_ds))

    def eval_gain(self, ev):
        return self.gain * self.eval_overvoltage(ev)

    def eval_pde(self, ev):
        if ev['type'] != 'P':
            return True
        else:
             return np.random.uniform() < self.pde * self.eval_overvoltage(ev)

    def generate_signal(self, ev, t):
        t0 = ev['time']
        a1, a2 = -4.1, -4.13
        #signal = (a1*np.exp(-(t-t0)/self.t_ds) + a2*np.exp(-(t-t0)/self.t_df) - (a1+a2)*np.exp(-(t-t0)/self.t_rise))
        #signal = (1.6e-19 * 50 * 5.5e5 / 2e-8) * np.exp(-(t-t0)/20)
        signal = (a1*np.exp(-(t-t0)/self.t_rise) + a2*np.exp(-(t-t0)/self.t_ds) )
        signal *= np.heaviside(t-t0, 0) 
        #print(f'OH {self.eval_gain(ev)} {max(signal)}')
        return self.eval_gain(ev) * signal*4.4e-5

    
class SiPM: 
    ''' Class describing a SiPM'''
    def __init__(self, ncell, pde, dark_count_rate, p_ct, p_af):
        self.ncell = ncell
        self.pde=pde
        self.dark_count_rate = dark_count_rate
        self.p_ct = p_ct
        self.p_af = p_af
        self.cellmap = np.full((800, 500), Microcell())
        self.triggers_in = np.empty([0,3], dtype=dt)
        self.triggers_out = np.empty([0,2], float)
        self.all_time = np.arange(0, 500, 0.1)
        self.signal_ampl = np.zeros(len(self.all_time))
        self.ct_counts = 0
        self.af_counts = 0
        self.det_counts = 0

    def initialize_sipm(self):
        
        for i in range(0, 800):
            for j in range(0, 120):
                self.cellmap[i][j] = Microcell(pde=self.pde)



    def map_photons(self, x, y, t):
        
        #x = np.random.randint(0, int(np.sqrt(self.ncell)), size=len(photonList))
        #y = np.random.randint(0, int(np.sqrt(self.ncell)), size=len(photonList))
        #x, y = np.zeros(len(photonList)) + 5, np.zeros(len(photonList)) + 5
        #x = data[3]
        self.triggers_in = np.zeros(len(t), dtype=dt)
        self.triggers_in['x_coord'] = x
        self.triggers_in['y_coord'] = y
        self.triggers_in['time'] = t
        self.triggers_in[:]['type'] = 'P'

    def add_darkcount(self, t0, t1):
        ''' t1 - t0 = time range of the simulation '''      
        n_mean = self.dark_count_rate * ((t1 - t0) * 1e-9)
        n_events = np.random.poisson(n_mean)
        timestamps = np.random.uniform(t0, t1, size=n_events)
        #print(n_events)
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
                #self.triggers_in = np.insert(self.triggers_in, np.array((ev[0]-1, ev[1], ev[2], 'ct'), dt))
                self.triggers_in = np.insert(self.triggers_in, 0, np.array((ev[0]-1, ev[1], ev[2], 'ct'), dt))
                self.ct_counts += 1
            elif i == 1 and ev[0] < (int(np.sqrt(self.ncell)) - 1): 
                #print(f'Crosstalk dx: {np.array((ev[0]+1, ev[1], ev[2]), dt)}')
                #self.triggers_in = np.append(self.triggers_in, np.array((ev[0]+1, ev[1], ev[2], 'ct'), dt))
                self.triggers_in = np.insert(self.triggers_in, 0, np.array((ev[0]+1, ev[1], ev[2], 'ct'), dt))
                self.ct_counts += 1
            elif i == 2 and ev[1] > 0:
                #print(f'Crosstalk up: {np.array((ev[0], ev[1]-1, ev[2]), dt)}')
                #self.triggers_in = np.append(self.triggers_in, np.array((ev[0], ev[1]-1, ev[2], 'ct'), dt))
                self.triggers_in = np.insert(self.triggers_in, 0, np.array((ev[0], ev[1]-1, ev[2], 'ct'), dt))
                self.ct_counts += 1
            elif i == 3 and ev[1] < (int(np.sqrt(self.ncell)) - 1): 
                #print(f'Crosstalk down: {np.array((ev[0], ev[1]+1, ev[2]), dt)}')
                #self.triggers_in = np.append(self.triggers_in, np.array((ev[0], ev[1]+1, ev[2], 'ct'), dt))
                self.triggers_in = np.insert(self.triggers_in, 0, np.array((ev[0], ev[1]+1, ev[2], 'ct'), dt))
                self.ct_counts += 1


    def add_afterpulse(self, ev):

        if np.random.uniform() < self.p_af:
            self.af_counts +=1
            taf = np.random.exponential(self.cellmap[ev[0], ev[1]].tau_af)
            #print(f'Af: {np.array((ev[0], ev[1], ev[2]+taf), dt)}')
            self.triggers_in = np.append(self.triggers_in, np.array((ev[0], ev[1], ev[2]+taf, 'af'), dt))
            self.triggers_in = np.sort(self.triggers_in, order='time' )


    def process_photon(self, ev):

        self.triggers_in = self.triggers_in[self.triggers_in!=ev]
        #print(ev)
        #print(self.cellmap[ev[0], ev[1]].eval_pde(ev))
        if self.cellmap[ev[0], ev[1]].eval_pde(ev):
        #if np.random.random() < 0.2:
            self.det_counts += 1
            g = self.cellmap[ev[0], ev[1]].eval_gain(ev)
            self.signal_ampl += self.cellmap[ev[0], ev[1]].generate_signal(ev, self.all_time)
            self.add_crosstalk(ev)
            self.add_afterpulse(ev)
            self.triggers_out = np.vstack((self.triggers_out, np.array([g, ev[2]])))
            self.cellmap[ev[0], ev[1]].last_trigger_time = ev[2]
            
        #self.triggers_in = np.sort(self.triggers_in, order='time' )
        

def run_simulation(sipm, data):

    photon_timestamps = data['time']
    x, y = data['x'], data['y']
    #print(f'Starting photons: {len(photon_timestamps)}')       
    sipm.map_photons(x, y, photon_timestamps)
    sipm.add_darkcount(sipm.all_time[0], sipm.all_time[-1])
    sipm.triggers_in = np.sort(sipm.triggers_in, order='time' )

    while len(sipm.triggers_in) > 0:
        #print(sipm.triggers_in[0])  
        #print('Ciao')      
        sipm.process_photon(sipm.triggers_in[0])

    #print(f'***************** \n {sipm.triggers_in}')
    #print(sipm.triggers_out)
    #print(f'Number of total triggers: {len(sipm.triggers_out)}')
    ##print(f'Number of detected photons: {len(sipm.triggers_in[sipm.triggers_in['type']=='P'])}'')
    #print(f'Number of crosstalk: {sipm.ct_counts}')
    #print(f'Number of afterpulse: {sipm.af_counts}')
    print(sipm.det_counts)
    return sipm.signal_ampl


if __name__ == '__main__':

    ncell, pde, dark_count_rate, p_ct, p_af = 57600, 0.3, 3e6, 0.04, 0.12
    sipm = SiPM(ncell, pde, dark_count_rate, p_ct, p_af)
    sipm.initialize_sipm()
    print(sipm.cellmap[0][0].pde)

    
    
    



    


    