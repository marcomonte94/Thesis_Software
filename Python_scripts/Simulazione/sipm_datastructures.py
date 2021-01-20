import numpy as np
from matplotlib import pyplot as plt
import time

class Microcell:

    def __init__(self, gain, overvoltage, tau_r, tau_df, tau_ds):
        self.gain = gain # expressed as unit of overvoltage
        self.overvoltage = overvoltage
        self.tau_r = tau_r # rise time
        self.tau_df = tau_df # fast decay time
        self.tau_ds = tau_ds # slow decay time
        self.a1 = 10
        self.a2 = 10
        self.last_trigger_time = np.nan
        self.istriggerable = True
    '''
    def eval_pde(self, ev):
        return np.random.uniform() < self.pde
    

    def eval_overvoltage(self, ev):
        if np.isnan(self.last_trigger_time):
            return self.overvoltage
        else:
            return self.overvoltage * (1 - np.exp(-(ev[2] - self.last_trigger_time / self.recovery_time)))

    '''
    def generate_signal(self, t0, t):
        return np.heaviside(t-t0, 0) * (self.a1*np.exp(-(t-t0)/self.tau_ds) + self.a2*np.exp(-(t-t0)/self.tau_df) + (self.a1 + self.a2)*np.exp(-(t-t0)/self.tau_r))


class PhotonEvent:

    def __init__(self, x, y, t):
        self.x = x
        self.y = y
        self.t = t

class SiPM:

    def __init__(self, ncell, pde, dark_count_rate, ct_probability, af_probability):
        self.ncell = ncell
        self.perside = int(np.sqrt(ncell))
        self.pde = pde
        self.dark_count_rate = dark_count_rate
        self.ct_probability = ct_probability
        self.af_probability = af_probability

    def add_darkcount(self, t0, t1):
        ''' t1 - t0 = time range of the simulation '''      
        n_mean = self.dark_count_rate * ((t1 - t0) * 1e-9)
        n_events = np.random.poisson(n_mean)
        timestamps = np.random.uniform(t0, t1, size=n_events)
        x = np.random.uniform(0, self.perside, size=len(timestamps))
        y = np.random.uniform(0, self.perside, size=len(timestamps))
        return np.stack((x, y, timestamps), axis=1)


        

if __name__ == '__main__':
    start_time = time.time()
    timestamp = np.linspace(0.5, 30, 1000)
    t = np.linspace(0, 500, 10000)
    v = np.zeros(len(t))
    m = Microcell(1, 4, 30, 5, 5, 0.5)

    for t0 in timestamp:
        v = np.vstack((v, m.generate_signal(t0, t)))

    print(v.shape)
    plt.plot(t, np.sum(v, axis=0))
    print(f"Elapses time: {time.time()-start_time}")
    plt.show()


