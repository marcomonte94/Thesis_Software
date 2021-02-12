import numpy as np
import matplotlib.pyplot as plt
from new_channelmap import channelMap

dt = np.dtype([
    ('channel',         np.int),
    ('id_board',        np.int),
    ('id_event',        np.int),
    ('always_0_1',      np.int),
    ('always_0_2',      np.int),
    ('ampl',            np.float, (1024, )),
    ('time',            np.float, (1024, ))
  ])

path = 'C:/Users/Marco/Desktop/cosmic/prova.dec'
a = np.fromfile(path, dtype=dt)
e = channelMap(a)
mask = np.logical_and(e['id_bar']==0, e['layer']==0)
print(len(e[mask]))












