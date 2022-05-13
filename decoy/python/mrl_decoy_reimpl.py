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
import decoy_consts
 
def GetParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dload-disable', default=False, action='store_true', help="Disable download?")
    parser.add_argument('-o', '--one-only', default=False, action='store_true', help="Plot only one")

    return parser

class GammaPDFPython():
    def __init__(self, shape=decoy_consts.GAMMA_SHAPE, scale=decoy_consts.GAMMA_SCALE):
        #define x-axis values
        self.x = np.linspace(4, 25, 100) 

        #calculate pdf of Gamma distribution for each x-value
        self.y = gamma.pdf(self.x, a=shape, scale=scale)

class GammaPDFMonero():
    def __init__(self):
        self.data = decoy_consts.load_data(decoy_consts.PATH_GAMMA_PDF)
        print(self.data)

class GammaPickerPyhon():
    def __init__(self, rct_offsets, shape=decoy_consts.GAMMA_SHAPE, scale=decoy_consts.GAMMA_SCALE):
        pass # TODO: This is meant to be the reimplementation

class GammaPickerMonero():
    def __init__(self, rct_offsets):
        pass # TODO: This will only read the data file

def plot_data(gamPDFMo, gamPDFPy):
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.suptitle("Gamma distributions' PDFs")
    ax1.hist(gamPDFMo.data, bins=50)
    ax2.plot(gamPDFPy.x, gamPDFPy.y)
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
    gamPDFPy = GammaPDFPython()
    gamPDFMo = GammaPDFMonero()
    plot_data(gamPDFMo, gamPDFPy)
    #plot_function(data)
    
if __name__ == "__main__":
    main()


