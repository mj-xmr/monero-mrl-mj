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

FILE_OUT = 'mul_2_ratio_good_py.csv'
PATH_OUT = '/tmp/' + FILE_OUT
#PATH_IN_ALT = '../data/' + FILE_IN

def GetParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dload-disable', default=False, action='store_true', help="Disable download?")
    parser.add_argument('-o', '--one-only', default=False, action='store_true', help="Plot only one")

    return parser
    
def prepDir():
    if os.path.isdir(DIR_IN):
        shutil.rmtree(DIR_IN)
    os.makedirs(DIR_IN, exist_ok=True)

def main():
    parser = GetParser()
    args = parser.parse_args()
    #if os.path.isfile(PATH_IN):
    #    PATH = PATH_IN
    #else:
    #    PATH = PATH_IN_ALT
    #data = np.loadtxt(PATH, delimiter=',')
    #print(data)
    #plot_data(data)
    #plot_function(data)
    
if __name__ == "__main__":
    main()


