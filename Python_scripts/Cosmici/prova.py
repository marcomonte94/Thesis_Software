import numpy as np
import matplotlib.pyplot as plt

dt = np.dtype([('channel', np.int), ('id_board', np.int), ('id_event', np.int), ('always_0_1', np.int), ('always_0_2', np.int), ('ampl', np.float, (1024, )), ('time', np.float, (1024,))])

path = 'C:/Users/Marco/Desktop/cosmic/prova.dec'
a = np.fromfile(path, dtype=dt)
plt.plot(a[100]['time'],a[100]['ampl'])
plt.show()