#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#%matplotlib inline
import os
import numpy as np
from pathlib import Path

HOME = str(Path.home()) + "/"

GAMMA_SHAPE = 19.28
GAMMA_SCALE = (1/1.61)

def get_data_path(file_name):
    DIR_TMP = '/tmp/'
    DIR_TMP_ALT = HOME + '/temp/monero/'
    optimistic = DIR_TMP + '/' + file_name
    if os.path.isfile(optimistic):
        return optimistic
    return DIR_TMP_ALT + file_name
    
PATH_MUL_2_RATIO_GOOD = get_data_path('mrl_mul_2_ratio_good.csv')
PATH_GAMMA_PDF = get_data_path('mrl_gamma_distrib.csv')

def load_data(path):
    print("Loading:", path)
    return np.loadtxt(path, delimiter=',')
