import numpy as np
from matplotlib import pyplot as plt
import argparse
import os

def compute_area(dt, ampl):
    return (ampl*dt).sum()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Analysis of simulation output')
    parser.add_argument('f', help='Input data')
    parser.add_argument('-l', '--side', help='Bar side (1 -> A, 2 -> B)')
    parser.add_argument('-w', '--graphs', help='Graph mode', default = '0')
    #parser.add_argument('-d', '--debug', help='Debug mode', default = '0')
    #parser.add_argument('-w', '--graphs', help='Graph mode', default = '0')
    args = parser.parse_args()


