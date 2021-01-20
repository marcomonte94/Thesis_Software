import numpy as np
from matplotlib import pyplot as plt

class SiPM: 
    ''' Class describing a SiPM'''
    def __init__(self, ncell, pde, p_ct, p_af):
        '''Arguments'''
        self.ncell = ncell           # number of total cells
        self.pde = pde               # photon detection efficency
        self.p_ct = p_ct             # cross-talk probability
        self.p_af = p_af             # after-pulse probability
        self.tau_af = 100            # after-pulse time (ns)
        self.overvoltage = 8         # V overvoltage
        self.recovery_time = 40      # cell recovey time
        self.triggers=np.array([])   # list of all trigger events (empty at starting)
        self.matrix = np.zeros(shape=(int(np.sqrt(self.ncell)), int(np.sqrt(self.ncell))))
        self.time_map = np.full((int(np.sqrt(self.ncell)), int(np.sqrt(self.ncell))), np.nan)
        self.ct_counts = 0
        self.af_counts = 0


    def eval_pde(self, ev):

        return np.random.uniform() < self.pde

    def eval_overvoltage(self, ev):

        if np.isnan(self.time_map[ev[0], ev[1]]):
            return self.overvoltage
        else:
            return self.overvoltage * (1 - np.exp(-(ev[2] - self.time_map[ev[0], ev[1]]) / self.recovery_time))
    

    def eval_crosstalk(self, ev, nncell=4):

        p = 1 - ((1-self.p_ct)**(1/nncell))
        n_ct = np.random.binomial(nncell, p)
        step = np.random.choice(nncell, n_ct, replace=False)

        for i in step:

            if i == 0 and self.matrix[ev[0]+1, ev[1]] == 0: # Nord
                self.triggers = np.vstack((self.triggers, ([ev[0]+1, ev[1], ev[2]])))
                self.matrix[ev[0]+1, ev[1]] = 1
                self.ct_counts += 1

            elif i == 1 and self.matrix[ev[0]-1, ev[1]] == 0: # Sud
                self.triggers = np.vstack((self.triggers, ([ev[0]-1, ev[1], ev[2]])))
                self.matrix[ev[0]-1, ev[1]] = 1
                self.ct_counts += 1

            elif i == 2 and self.matrix[ev[0], ev[1]-1] == 0: # Ovest
                self.triggers = np.vstack((self.triggers, ([ev[0], ev[1]-1, ev[2]])))
                self.matrix[ev[0], ev[1]-1] = 1
                self.ct_counts += 1

            elif i == 3 and self.matrix[ev[0], ev[1]+1] == 0: # Est
                self.triggers = np.vstack((self.triggers, ([ev[0], ev[1]+1, ev[2]])))
                self.matrix[ev[0], ev[1]+1] = 1
                self.ct_counts += 1


    def eval_afterpulse(self, ev):

        r = np.random.uniform()

        if r < self.p_af:
            taf = np.random.exponential(self.tau_af)
            self.triggers = np.vstack((self.triggers, ([ev[0], ev[1], ev[2]+taf])))
            self.af_counts += 1



if __name__ == '__main__':
    my_sipm = SiPM(10000, 0.5, 0.8, 0.2)
    plt.figure()
    plt.imshow(my_sipm.matrix)

    ev = np.array([50, 50, 0])
    my_sipm.matrix[ev[0], ev[1]] = 1
    my_sipm.triggers = ev
    my_sipm.eval_crosstalk(ev)
    print(my_sipm.triggers)
    print(np.where(my_sipm.matrix>0))
    print(my_sipm.ct_counts)

    plt.figure()
    plt.imshow(my_sipm.matrix)

    plt.show()


