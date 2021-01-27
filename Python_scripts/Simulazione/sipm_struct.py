import numpy as np
from matplotlib import pyplot as plt
import time

dt = np.dtype([('x_coord', np.int), ('y_coord', np.int), ('time', np.float64)])


class Microcell:

    def __init__(self, gain=1, overvoltage=1, t_recovery=30):
        self.gain = gain # expressed as unit of overvoltage
        self.overvoltage = overvoltage
        self.t_recovery = t_recovery
        self.tau_af = 100
        self.last_trigger_time = np.nan

    def eval_overvoltage(self, ev):
        if np.isnan(self.last_trigger_time):
            return self.overvoltage
        else:
            return self.overvoltage * (1 - np.exp(-(ev[2] - self.last_trigger_time) / self.t_recovery))
            #return self.overvoltage +1

    def eval_gain(self, ev):
        return self.gain * self.eval_overvoltage(ev)

    
class SiPM: 
    ''' Class describing a SiPM'''
    def __init__(self, ncell, pde, dark_count_rate, p_ct, p_af):
        self.ncell = ncell
        self.pde = pde
        self.dark_count_rate = dark_count_rate
        self.p_ct = p_ct
        self.p_af = p_af
        self.cellmap = np.full((int(np.sqrt(self.ncell)), int(np.sqrt(self.ncell))),Microcell())
        self.triggers_in = np.empty([0,3], dtype=dt)
        self.triggers_out = np.empty([0,2], float)
        self.ct_counts = 0
        self.af_counts = 0
        self.det_counts = 0

    def initialize_sipm(self):
        
        for i in range(int(np.sqrt(self.ncell))):
            for j in range(int(np.sqrt(self.ncell))):
                self.cellmap[i,j] = Microcell()
        


    def detected_photons(self, all_photon):
        mask = np.random.uniform(size=len(all_photon)) > self.pde
        return all_photon[mask]


    def map_photons(self, photonList):
        
        #x, y = np.random.randint(1, 9, size=len(photonList)), np.random.randint(1, 9, size=len(photonList))
        x, y = np.zeros(len(photonList)) + 5, np.zeros(len(photonList)) + 5
        self.triggers_in = np.zeros(len(photonList), dtype=dt)
        self.triggers_in['x_coord'] = x
        self.triggers_in['y_coord'] = y
        self.triggers_in['time'] = photonList

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
        self.triggers_in = np.append(self.triggers_in, dark_events)
        #print(len(dark_events))


    def add_crosstalk(self, ev, nearest_cells=4):

        p = 1 - ((1-self.p_ct)**(1/nearest_cells))
        n_ct = np.random.binomial(nearest_cells, p)
        step = np.random.choice(nearest_cells, n_ct, replace=False)

        for i in step:
            #print(i)
            if i == 0 and ev[0] > 0: 
                print(f'Nuovo: {np.array((ev[0]-1, ev[1], ev[2]), dt)}')
                self.triggers_in = np.append(self.triggers_in, np.array((ev[0]-1, ev[1], ev[2]), dt))
                self.ct_counts += 1
            if i == 1 and ev[0] < (int(np.sqrt(self.ncell)) - 1): 
                print(f'Nuovo: {np.array((ev[0]+1, ev[1], ev[2]), dt)}')
                self.triggers_in = np.append(self.triggers_in, np.array((ev[0]+1, ev[1], ev[2]), dt))
                self.ct_counts += 1
            if i == 2 and ev[1] > 0:
                print(f'Nuovo: {np.array((ev[0], ev[1]-1, ev[2]), dt)}')
                self.triggers_in = np.append(self.triggers_in, np.array((ev[0], ev[1]-1, ev[2]), dt))
                self.ct_counts += 1
            if i == 3 and ev[1] < (int(np.sqrt(self.ncell)) - 1): 
                print(f'Nuovo: {np.array((ev[0], ev[1]+1, ev[2]), dt)}')
                self.triggers_in = np.append(self.triggers_in, np.array((ev[0], ev[1]+1, ev[2]), dt))
                self.ct_counts += 1


    def add_afterpulse(self, ev):

        if np.random.uniform() < self.p_af:
            self.af_counts +=1
            print('Af')
            taf = np.random.exponential(self.cellmap[ev[0], ev[1]].tau_af)
            self.triggers_in = np.append(self.triggers_in, np.array((ev[0], ev[1], ev[2]+taf), dt))


    def process_photon(self, ev):
        
        self.det_counts += 1
        g = self.cellmap[ev[0], ev[1]].eval_gain(ev)
        #self.cellmap[ev[0], ev[1]].gain = g
        self.add_crosstalk(ev)
        self.add_afterpulse(ev)
        self.triggers_out = np.vstack((self.triggers_out, np.array([g, ev[2]])))
        self.cellmap[ev[0], ev[1]].last_trigger_time = ev[2]



if __name__ == '__main__':
    sipm = SiPM(57600, 0.2, 0.5, 0.05, 0.05)
    sipm.initialize_sipm()
    photon_timestamps = np.arange(1, 50, 0.5)
    sipm.map_photons(photon_timestamps)
    sipm.add_darkcount(photon_timestamps[0], photon_timestamps[-1])
    #print(sipm.triggers_in)
    #print(sipm.triggers_in)
    #ev = sipm.triggers_in[0]
    #print(ev)
    i = 0
    #for i in range(len(sipm.triggers_in)):
    while i < len(sipm.triggers_in):
        #print(sipm.triggers_in[i])
        sipm.triggers_in = np.sort(sipm.triggers_in, order='time' )
        sipm.process_photon(sipm.triggers_in[i])
        i += 1

    print(sipm.triggers_out)
    print(f'Number of total events: {len(sipm.triggers_out)}')
    print(f'Number of detected photons: {len(photon_timestamps)}')
    print(f'Number of crosstalk: {sipm.ct_counts}')
    print(f'Number of afterpulse: {sipm.af_counts}')
    #sipm.triggers_out = sipm.triggers_out.reshape(int(len(sipm.triggers_out)/2), 2)
    #print(len(photon_timestamps))
    #print(len(sipm.triggers_out))
    #print(sipm.ct_counts)
    
    



    


    