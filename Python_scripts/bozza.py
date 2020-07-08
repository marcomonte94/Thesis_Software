import time
import numpy as np
import sys
from matplotlib import pyplot as plt
from readTrc import Trc

def shift(xs, n):
    if n >= 0:
        return np.concatenate((np.full(n, 0), xs[:-n]))
    else:
        return np.concatenate((xs[-n:], np.full(-n, 0)))

trc = Trc()

wf_path = 'C1--prova--00000.trc'
time, ampl, d = trc.open(wf_path)

zeri = np.zeros(5)
left_time = np.linspace(time[0]-6*1e-10, time[0]-1e-10, 5)
right_time = np.linspace(time[len(time)-1]+1e-10, time[len(time)-1]+6*1e-10, 5)


timeDLDED = np.concatenate((time[5:], right_time))
print(len(timeDLDED))
#amplDLDED = np.concatenate((ampl[:-5], zeri))
amplDLDED = shift(ampl, 5)



plt.figure()
plt.plot(time, ampl, label='Wavefor')
plt.plot(timeDLDED, amplDLDED, label='DLED Waveform')
plt.legend(loc='best')


plt.figure()
plt.plot(time, amplDLDED-ampl)

plt.xlabel('Time (s)')
plt.ylabel('Amplitude (V)')

plt.show()