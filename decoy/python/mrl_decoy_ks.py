#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#%matplotlib inline

import numpy as np
import argparse

from scipy.stats import ks_2samp

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d1', '--data1', type=str)
    parser.add_argument('-d2', '--data2', type=str)

    return parser.parse_args()


def ks(data1, data2):
    # https://en.wikipedia.org/wiki/Kolmogorov%E2%80%93Smirnov_test
    print("Performing Kolmogorov-Smirnov test")
    #print("Self-test: ", ks_2samp(data1[:, 1], data1[:, 1]))
    #print("Final-test:", ks_2samp(data1[:, 1], data2[:, 1]))
    print("Self-test: ", ks_2samp(data1, data1))
    print("Final-test:", ks_2samp(data1, data2))

def main(args):
    data1 = np.loadtxt(args.data1)
    data2 = np.loadtxt(args.data2)
    ks(data1, data2)
    
if __name__ == "__main__":
    args = get_args()
    main(args)


