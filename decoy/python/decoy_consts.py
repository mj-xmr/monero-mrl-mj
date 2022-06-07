#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#%matplotlib inline
import os
import numpy as np
from pathlib import Path

HOME = str(Path.home()) + "/"

def get_data_path(file_name):
    DIR_TMP = '/tmp/'
    DIR_TMP_ALT = HOME + '/temp/monero/'
    optimistic = DIR_TMP + '/' + file_name
    #print("Optimistic", file_name, optimistic)
    if os.path.isfile(optimistic):
        return optimistic
    return DIR_TMP_ALT + file_name

PATH_MUL_2_RATIO_GOOD       = get_data_path('mrl_mul_2_ratio_good.csv')
PATH_MUL_2_RATIO_GOOD_PY    = get_data_path('mrl_mul_2_ratio_good_py.csv')
PATH_GAMMA_PDF              = get_data_path('mrl_gamma_distrib.csv')

PATH_MUL_2_RATIO_GOOD_PY_OUT = '/tmp/mrl_gamma_distrib_py_out'

GAMMA_SHAPE = 19.28
GAMMA_SCALE = (1/1.61)
CRYPTONOTE_DEFAULT_TX_SPENDABLE_AGE =             10
DIFFICULTY_TARGET_V2  =                          120  # // seconds
DIFFICULTY_TARGET_V1  =                          60   # // seconds - before first fork
DEFAULT_UNLOCK_TIME = (CRYPTONOTE_DEFAULT_TX_SPENDABLE_AGE * DIFFICULTY_TARGET_V2)
RECENT_SPEND_WINDOW = (15 * DIFFICULTY_TARGET_V2)
uint64_t_MAX = 18446744073709551615
MIN_RCT_LENGTH = CRYPTONOTE_DEFAULT_TX_SPENDABLE_AGE + 1



def load_data(path):
    print("Loading:", path)
    return np.loadtxt(path, delimiter=' ')
