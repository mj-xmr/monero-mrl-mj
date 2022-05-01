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

FILE_IN = 'mul_2_ratio_good.csv'
PATH_IN = '/tmp/' + FILE_IN
PATH_IN_ALT = '../data/' + FILE_IN

def GetParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dload-disable', default=False, action='store_true', help="Disable download?")
    parser.add_argument('-o', '--one-only', default=False, action='store_true', help="Plot only one")

    return parser
    
def prepDir():
    if os.path.isdir(DIR_IN):
        shutil.rmtree(DIR_IN)
    os.makedirs(DIR_IN, exist_ok=True)
    
def writeTimestamp():
    with open(PATH_TIMESTAMP, 'w') as fout:
        fout.write(datetime.now().replace(microsecond=0).isoformat().replace('T', '  '))

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
    if os.path.isfile(PATH_IN):
        PATH = PATH_IN
    else:
        PATH = PATH_IN_ALT
    data = np.loadtxt(PATH, delimiter=',')
    #print(data)
    plot_data(data)
    #plot_function(data)
    
if __name__ == "__main__":
    main()


