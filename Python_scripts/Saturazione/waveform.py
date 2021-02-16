import numpy as np
import os
import argparse
import matplotlib.pyplot as plt
from readTrc import Trc


filepath = 'C:/Users/Marco/Desktop/Saturazione/foot/6'
allMyData = list(os.listdir(filepath))
print(allMyData[0])
trc = Trc()
time, ampl, _ = trc.open(f'{filepath}/{allMyData[0]}')
ampl = -ampl
baseline = ampl[:150].mean()

f = 0.3
a = np.where((ampl-baseline)>f*max(ampl-baseline))



plt.figure()
plt.plot(time, ampl-baseline)
plt.plot(time, (ampl-baseline)[a[0]])

plt.plot(time, np.zeros(len(time))+f*max(ampl-baseline))
plt.show()