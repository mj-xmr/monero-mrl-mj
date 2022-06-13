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
from scipy.stats import ks_2samp
import mrl_decoy_reimpl

#import shutil
import decoy_consts

def GetParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dload-disable', default=False, action='store_true', help="Disable download?")
    parser.add_argument('-o', '--one-only', default=False, action='store_true', help="Plot only one")

    return parser

class GammaRVSPython():
    "Random variates"
    def __init__(self, shape=decoy_consts.GAMMA_SHAPE, scale=decoy_consts.GAMMA_SCALE):
        num_samples = 5000
        self.y = []
        for i in range(0, num_samples):
            self.y.append(gamma.rvs(a=shape, scale=scale))
        #print(self.y)


class GammaPDFPython():
    def __init__(self, shape=decoy_consts.GAMMA_SHAPE, scale=decoy_consts.GAMMA_SCALE):
        #define x-axis values
        self.x = np.linspace(4, 25, 100) 

        #calculate pdf of Gamma distribution for each x-value
        self.y = gamma.pdf(self.x, a=shape, scale=scale)

class GammaRVSMonero():
    def __init__(self):
        self.data = decoy_consts.load_data(decoy_consts.PATH_GAMMA_PDF)
        print(self.data)

def plot_cpp_distrib(data, title=""):
#    data = data[:-20]
    fig, (ax1, ax2) = plt.subplots(1, 2)
    if len(title):
        fig.suptitle(title)
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

class GammaPickerMonero():
    def __init__(self, rct_offsets):
        pass # TODO: This will only read the data file

def plot_picks(values):
    plt.plot(values)

    plt.show()

def picks(NUM_DRAWS=100, output_file=''):
    offsets_ratios = []

    mul = 1e5
    #mul = 1e3 # For testing
    while True:
        if mul <= 1: # TODO: Should be <= 1, but it crashes so far
            pass
            break
        num_hits = 0;
        start = 1 # At start == 0 there's a corner case to test
        rct_outputs = list(range(start, int(decoy_consts.MIN_RCT_LENGTH * mul) + start))
        #print(rct_outputs)
        #print(len(rct_outputs))
        picker = GammaPickerPyhon(rct_outputs)
        ratio_good_picks = picker.pick_n_values_ratio(NUM_DRAWS)
        print(ratio_good_picks, len(rct_outputs))
        offsets_ratios.append((mul, ratio_good_picks))
        mul *= 0.85

    npa = np.array(offsets_ratios)
    if output_file:
        np.savetxt(output_file, npa, header='# multiplier_of_the_minimal_vector_length,ratio_good_picks')

    return npa

def picks_raw(NUM_DRAWS=100, output_file=''):
    offsets_ratios = []

    mul = 1e5
    #mul = 1e3 # For testing
    while True:
        if mul <= 1: # TODO: Should be <= 1, but it crashes so far
            pass
            break
        start = 1 # At start == 0 there's a corner case to test
        rct_outputs = list(range(start, int(decoy_consts.MIN_RCT_LENGTH * mul) + start))
        #print(rct_outputs)
        #print(len(rct_outputs))
        picker = mrl_decoy_reimpl.GammaPickerPyhon(rct_outputs)
        picks = picker.pick_n_values(NUM_DRAWS)
        print(len(rct_outputs))
        
        if output_file:
            fname = output_file + "_{}.csv".format(math.floor(round(mul)))
            np.savetxt(fname, picks)
            print("Saved to", fname)

        mul *= 0.85

    #npa = np.array(offsets_ratios)

    #return npa

def plot_data(gamRVSMo, gamRVSPy, gamPDFPy):
    fig, (ax1, ax2) = plt.subplots(1, 2)
    bins = 50
    fig.suptitle("Gamma distributions' PDFs")
    ax1.hist(gamRVSMo.data, bins=bins)
    ax2.hist(gamRVSPy.y,    bins=bins)
    #ax2.plot(gamPDFPy.x, gamPDFPy.y)
    ax1.grid()
    ax2.grid()

    ax1.set_xlabel("Monero")
    ax2.set_xlabel("Python")
    ax1.set_ylabel("Occurrences")

    plt.show()

def plot_picker_py(ratios):
    plot_cpp_distrib(ratios, "Python reimpl. gamma picker")

def ks(data1, data2):
    # https://en.wikipedia.org/wiki/Kolmogorov%E2%80%93Smirnov_test
    print("Performing Kolmogorov-Smirnov test")
    print("Self-test: ", ks_2samp(data1[:, 1], data1[:, 1]))
    print("Final-test:", ks_2samp(data1[:, 1], data2[:, 1]))


def simple_run():
    parser = GetParser()
    args = parser.parse_args()
    data = decoy_consts.load_data(decoy_consts.PATH_MUL_2_RATIO_GOOD)
    #print(data)
    plot_cpp_distrib(data, "Monero C++ gamma picker")
    #plot_function(data)

def full_run():
    plot = True
    #plot = False
    parser = GetParser()
    args = parser.parse_args()
    
    fpath_template = '/tmp/picks_raw_py_mul_length'
    #picks_raw(100, fpath_template)
    picks_raw(10000, fpath_template)
    

    return
    #max_element = 20
    #data1 = data1[:-max_element]
    #data2 = data2[:-max_element]
    
    data_cpp = decoy_consts.load_data(decoy_consts.PATH_MUL_2_RATIO_GOOD)
    if plot:
        plot_cpp_distrib(data_cpp, "Monero C++ gamma picker")

    start = 1 # At start == 0 there's a corner case to test
    rct_outputs = list(range(start, (decoy_consts.CRYPTONOTE_DEFAULT_TX_SPENDABLE_AGE + 1) * 1000 + start))

    if os.path.isfile(decoy_consts.PATH_MUL_2_RATIO_GOOD_PY):
        print("Loading", decoy_consts.PATH_MUL_2_RATIO_GOOD_PY)
        ratios = np.loadtxt(decoy_consts.PATH_MUL_2_RATIO_GOOD_PY)
    else:
        print("Generating", decoy_consts.PATH_MUL_2_RATIO_GOOD_PY)
        ratios = picks()
        np.savetxt(decoy_consts.PATH_MUL_2_RATIO_GOOD_PY, ratios)
    print("K-S test on the aggregates")
    ks(data_cpp, ratios)
    if plot:
        plot_picker_py(ratios)

    
    #return
    gamPDFPy = GammaPDFPython()
    gamRVSMo = GammaRVSMonero()
    gamRVSPy = GammaRVSPython()

    if plot:
        plot_data(gamRVSMo, gamRVSPy, gamPDFPy)
    ##plot_function(data)

    

    MAX_NUM = 20
    NUM_DRAWS = 100000
    for i in range(0, MAX_NUM):
        #print("Writing {} or {}".format(i, MAX_NUM))
        pass
        #ratios_new = picks(NUM_DRAWS, decoy_consts.PATH_MUL_2_RATIO_GOOD_PY_OUT + "_{}.csv".format(i))
        #ks(data_cpp, ratios_new)

def main():
    #simple_run()
    full_run()
    
if __name__ == "__main__":
    main()


