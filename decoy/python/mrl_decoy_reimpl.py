#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#%matplotlib inline

import os
from datetime import datetime
import numpy as np
from matplotlib import pyplot as plt
import math
import argparse
from scipy.stats import gamma
#import shutil

GAMMA_SHAPE = 19.28
GAMMA_SCALE = (1/1.61)
FILE_OUT = 'mul_2_ratio_good_py.csv'
PATH_OUT = '/tmp/' + FILE_OUT
#PATH_IN_ALT = '../data/' + FILE_IN
FILE_IN = 'gamma_distrib.csv'
PATH_IN = '/tmp/' + FILE_IN

 
def GetParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dload-disable', default=False, action='store_true', help="Disable download?")
    parser.add_argument('-o', '--one-only', default=False, action='store_true', help="Plot only one")

    return parser

class GammaPicker():
    def __init__(self, rct_offsets, shape=GAMMA_SHAPE, scale=GAMMA_SCALE):
        #define x-axis values
        self.x = np.linspace(4, 25, 100) 

        #calculate pdf of Gamma distribution for each x-value
        self.y = gamma.pdf(self.x, a=shape, scale=scale)

        #create plot of Gamma distribution
        #plt.plot(x, y)

        #display plot
        #plt.show()
        
def prepDir():
    if os.path.isdir(DIR_IN):
        shutil.rmtree(DIR_IN)
    os.makedirs(DIR_IN, exist_ok=True)


def plot_data(data, gam):
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.suptitle("Gamma distributions' PDFs")
    ax1.hist(data, bins=50)
    ax2.plot(gam.x, gam.y)
    ax1.grid()
    ax2.grid()

    ax1.set_xlabel("Monero")
    ax2.set_xlabel("Python")
    ax1.set_ylabel("Occurrences")

    plt.show()

def main():
    parser = GetParser()
    args = parser.parse_args()
    rct_outputs = [1, 2, 3]
    gam = GammaPicker(rct_outputs)
    if os.path.isfile(PATH_IN):
        PATH = PATH_IN
    else:
        PATH = PATH_IN_ALT
    data = np.loadtxt(PATH, delimiter=',')
    print(data)
    plot_data(data, gam)
    #plot_function(data)
    
if __name__ == "__main__":
    main()


