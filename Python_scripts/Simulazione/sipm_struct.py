import numpy as np
from matplotlib import pyplot as plt
import time


class Microcell:

    def __init__(self, gain=1, overvoltage=1, t_recovery=30):
        self.gain = gain # expressed as unit of overvoltage
        self.overvoltage = overvoltage
        self.t_recovery = t_recovery
        self.last_trigger_time = np.nan

    def eval_overvoltage(self, ev):
        if np.isnan(self.last_trigger_time):
            return self.overvoltage
        else:
            return self.overvoltage * (1 - np.exp(-(ev[2] - self.last_trigger_time / self.t_recovery)))

    def eval_gain(self, ev):
        return self.gain * self.eval_overvoltage(ev)

    
class SiPM: 
    ''' Class describing a SiPM'''
    def __init__(self, ncell, pde, p_ct, p_af):
        self.ncell = ncell
        self.pde = pde
        self.p_ct = p_ct
        self.p_af = p_af
        self.cellmap = np.full((int(np.sqrt(self.ncell)), int(np.sqrt(self.ncell))), Microcell())
        self.triggers_in = np.empty([0,3], float)
        self.triggers_out = np.empty([0,2], float)
        self.ct_counts = 0
        self.af_counts = 0
        self.det_counts = 0


    def detected_photons(self, all_photon):
        mask = np.random.uniform(size=len(all_photon)) > self.pde
        return all_photon[mask]

    def map_photons(self, photonList):
        dt = np.dtype([('x_coord', np.int), ('y_coord', np.int), ('time', np.float64)]) 
        x, y = np.random.randint(1, 9, size=len(photonList)), np.random.randint(1, 9, size=len(photonList))
        self.triggers_in = np.zeros(len(photonList), dtype=dt)
        self.triggers_in['x_coord'] = x
        self.triggers_in['y_coord'] = y
        self.triggers_in['time'] = photonList


    def add_crosstalk(self, ev, nearest_cells=4):

        p = 1 - ((1-self.p_ct)**(1/nearest_cells))
        n_ct = np.random.binomial(nearest_cells, p)
        step = np.random.choice(nearest_cells, n_ct, replace=False)

        for i in step:

            if i == 0 and ev[0] != 0: 
                self.triggers_in = np.vstack((self.triggers_in, np.array([ev[0]-1, ev[1], ev[2]])))
                self.ct_counts += 1
            elif i == 1 and ev[0] != (int(np.sqrt(self.ncell)) - 1): 
                self.triggers_in = np.vstack((self.triggers_in, np.array([ev[0]+1, ev[1], ev[2]])))
                self.ct_counts += 1
            elif i == 2 and ev[1] != 0:
                self.triggers_in = np.vstack((self.triggers_in, np.array([ev[0], ev[1]-1, ev[2]])))
                self.ct_counts += 1
            elif i == 3 and ev[1] != (int(np.sqrt(self.ncell)) - 1): 
                self.triggers_in = np.vstack((self.triggers_in, np.array([ev[0], ev[1]+1, ev[2]])))
                self.ct_counts += 1


    def process_photon(self, ev):
        self.det_counts += 1
        g = self.cellmap[ev[0], ev[1]].eval_gain([ev[0], ev[1], ev[2]])
        self.add_crosstalk(ev)
        self.triggers_out = np.vstack((self.triggers_out, np.array([g, ev[2]])))
        self.cellmap[ev[0], ev[1]].last_trigger_time = ev[2]



if __name__ == '__main__':
    sipm = SiPM(100, 0.2, 0.05, 0.05)
    photon_timestamps = np.arange(1, 200, 1)
    
    #print(sipm.triggers_in)
    #ev = sipm.triggers_in[0]
    #print(ev)
    i = 0
    #for i in range(len(sipm.triggers_in)):
    while i < len(sipm.triggers_in):
        sipm.process_photon(sipm.triggers_in[i])
        i += 1
    #sipm.triggers_out = sipm.triggers_out.reshape(int(len(sipm.triggers_out)/2), 2)
    print(len(photon_timestamps))
    print(len(sipm.triggers_out))
    print(sipm.ct_counts)
    



    


    