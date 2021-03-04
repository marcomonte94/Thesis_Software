import numpy as np
from matplotlib import pyplot as plt
import time
import argparse
from sipm_struct import Microcell, SiPM, run_simulation, dt_evt

x = np.random.randint(0, 57600, size=1000)