import numpy as np

def compute_amplitude(time, ampl):
    baseline = ampl[:100].mean()
    a = ampl-baseline
    return min(a)

def compute_area(time, ampl):
    baseline = ampl[:100].mean()
    dt = (time[1:] - time[:-1]).mean()
    a = np.mean((ampl-baseline)*dt)
    return a

def cfd (time, ampl, th):
    baseline = ampl[:100].mean()
    a = ampl-baseline
    Vth = th*min(a)   
    time_up = np.where(a > Vth)[0]
    x, y = np.array([time[time_up[0]-1], time[time_up[0]]]), np.array([a[time_up[0]-1], a[time_up[0]]])
    popt = np.polyfit(x, y, 1)
    t_cfd = (Vth - popt[1])/popt[0]
    return t_cfd
