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

bar1, bar2 = 11, 14
l1, l2 = 0, 1

n_id = 500
#e =k [k['id_event'] == n_id]

print(e['id_bar'])
print(e['layer'])
print(e['side'])

print(len(e))
sullaBarra1 = e['id_bar'] == bar1
sulFront = e['layer'] == 0
sullaBarra2 = e['id_bar'] == bar2
sulRear = e['layer'] == 1

mask1 = np.logical_and(sullaBarra1, sulFront)
mask2 = np.logical_and(sullaBarra2, sulRear)

e0 = e[mask1]
e1 = e[mask2]

print((e0['id_event']))
print(e1['id_event'])


ee = np.intersect1d(e0['id_event'], e1['id_event'])

for i in ee:
    print(f'OOOOOOh {i}')
    k = e0[e0['id_event']==i]
    kd, ks = k[k['side']==1], k[k['side']==0]
    plt.plot(kd['ampl'][0])
    plt.plot(ks['ampl'][0])
    plt.plot(kd['clk'][0])
    plt.show()











