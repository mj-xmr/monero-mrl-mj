#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#%matplotlib inline

import os
from datetime import datetime
import numpy as np
from matplotlib import pyplot as plt
import argparse
from pathlib import Path
#from scipy.stats import gamma
#import shutil
import glob
#import decoy_consts
#import mrl_decoy_plot

#from scipy.stats import ks_2samp

HOME = str(Path.home()) + "/" # TODO: move this in config.json too?
 
def GetParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--interactive', default=False, action='store_true')
    #parser.add_argument('-d', '--dir', type=str, default=HOME + "/store/temp/monero/decoy/", help="Input directory")
    parser.add_argument('-d', '--dir', type=str, default="/tmp/monero/decoy", help="Input directory")

    return parser

def get_dirs(dirr):
    dirs = []
    print("iterating:", dirr)
    for entry in sorted(os.listdir(dirr)):
        path = dirr + '/' + entry
        if not os.path.isdir(path):
            continue
        if not '-' in entry:
            continue
        
        dirs.append(path)
        #dirs.append(entry)
        print(entry)
    return dirs

def get_glob(dirr, lang):
    return "{}/{}/*100000.csv".format(dirr, lang)

def process_dirs(dirs, lang):
    sum_border_pre  = 0
    sum_border_post = 0
    sum_border_pyt  = 0
    # In C++, there's a discontinuity between pre & post
    # In Python the discontinuity appears to be shifted by one
    border_pre  = 1099973
    border_post = 1099974
    border_pyt  = 1099975
    """
    value   cpp python diff
    1099973  8868   8570  298
    1099974 14336   8792 5544
    1099975 14665  14482  183
    """ 
    for dirr in dirs:
        print("Processing:", lang , dirr)
        file = glob.glob(get_glob(dirr, lang))[0]
        numbers = np.loadtxt(file)
        unique, counts = np.unique(numbers, return_counts=True)
        #plt.hist(unique, bins=50)
        #plt.show()
        dct = dict(zip(unique, counts))
        val_pre  = dct[border_pre]
        val_post = dct[border_post]
        val_pyt  = dct[border_pyt]
        #print("val_pre: ", val_pre)
        #print("val_post:", val_post)
        #print("val_pyt: ", val_pyt)

        sum_border_pre  += val_pre
        sum_border_post += val_post
        sum_border_pyt  += val_pyt

    print("================")
    print(lang)
    print("pre ", border_pre,  sum_border_pre, 0.00)
    print("post", border_post, sum_border_post, round((sum_border_post - sum_border_pre)/sum_border_pre,  2))
    print("pyt ", border_pyt,  sum_border_pyt,  round((sum_border_pyt - sum_border_post)/sum_border_post, 2))
    print("================\n")
        

def main():
    plot = True
    #plot = False
    parser = GetParser()
    args = parser.parse_args()
    dirs = get_dirs(args.dir)
    process_dirs(dirs, 'cpp')
    process_dirs(dirs, 'python')
    
    
if __name__ == "__main__":
    main()


