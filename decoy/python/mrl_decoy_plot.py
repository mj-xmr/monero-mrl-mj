#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#%matplotlib inline

import os
from datetime import datetime
import numpy as np
from matplotlib import pyplot as plt
import math
import argparse
#import shutil
import decoy_consts

def GetParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dload-disable', default=False, action='store_true', help="Disable download?")
    parser.add_argument('-o', '--one-only', default=False, action='store_true', help="Plot only one")

    return parser

def plot_data(data):
    fig, (ax1, ax2) = plt.subplots(1, 2)
    #fig.suptitle('Horizontally stacked subplots')
    ax1.scatter(data[:,0], data[:, 1])
    ax2.scatter(data[:,0], data[:, 1])
    
    ax1.set_xlabel("Multiple of the RCT's minimal lenght")
    ax2.set_xlabel("Multiple of the RCT's minimal lenght (log scale)")
    ax1.set_ylabel("Probability of a good pick")
    ax2.set_xscale('log')
    ax1.grid()
    ax2.grid()
    plt.show()

def plot_function(data):
    # This might approximate the gathered data
    def f(x):
        return (-1/x) + 1

    x = data[:,0]
    y = f(x)
    plt.plot(x, y)
    plt.grid()
    plt.show()

def main():
    parser = GetParser()
    args = parser.parse_args()
    data = np.loadtxt(decoy_consts.PATH_MUL_2_RATIO_GOOD, delimiter=',')
    #print(data)
    plot_data(data)
    #plot_function(data)
    
if __name__ == "__main__":
    main()


