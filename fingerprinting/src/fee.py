#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import traceback
import argparse
import pickle
import numpy as np
import dateutil
import datetime
import gzip
import lzma
import math
#import calendar
from copy import copy

import numpy as np
import pandas as pd

#from scipy import signal

from matplotlib import pyplot as plt
import matplotlib.dates as md
import matplotlib.colors as mcolors
from matplotlib.colors import LogNorm

WDIR='/tmp/a/fee/'
#WDIR='./'
DEFAULT_IN_DATA='tx_attribute_2021.csv'
DEFAULT_IN_DATA='xmr_report.csv'
DEFAULT_SKIP_EVERY_NTH=2000
DEFAULT_SKIP_EVERY_NTH=1000
#DEFAULT_SKIP_EVERY_NTH=5000
#DEFAULT_SKIP_EVERY_NTH=1
DEFAULT_AHEAD_POINTS=10e6
DEFAULT_YEAR_START=2019
DEFAULT_YEAR_END=datetime.datetime.now().year

DATE_MONERO_2020='2020-06-01 00:00:00'
DATE_MONERO_0_17='2020-09-15 19:59:36'
DATE_MONERO_2_3='2021-08-29 12:30:57'
DATE_MONERO_3_0='2021-11-30 17:07:33'


#from python_json_config import ConfigBuilder

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--in-data',      default=DEFAULT_IN_DATA, type=str, help="Input data (default: {})".format(DEFAULT_IN_DATA))
    parser.add_argument('-s', '--skip-every',   default=DEFAULT_SKIP_EVERY_NTH, type=int, help="Skip every N points (default: {})".format(DEFAULT_SKIP_EVERY_NTH))
    parser.add_argument('-a', '--ahead-points', default=DEFAULT_AHEAD_POINTS, type=int, help="Add N data points before 1st date (default: {})".format(DEFAULT_AHEAD_POINTS))
    parser.add_argument('-ys', '--year-start',  default=DEFAULT_YEAR_START, type=int, help="Start year for filtering (default: {})".format(DEFAULT_YEAR_START))
    parser.add_argument('-ye', '--year-end',    default=DEFAULT_YEAR_END,   type=int, help="End   year for filtering (default: {})".format(DEFAULT_YEAR_END))
    parser.add_argument('-p', '--plot',         default=False, action='store_true', help="Plot (default: OFF)")
    parser.add_argument('-f', '--full-data',    default=False, action='store_true', help="Full data (default: OFF)")
    #parser.add_argument('-r', '--battery-charge-ocr',      default=False, action='store_true', help="Initial battery charge OCR (default: OFF)")
    #parser.add_argument('-v', '--verbose',      default=TESTING, action='store_true', help="Test (default: False)")
    return parser.parse_args()

def filter_columns(file_handle, delimiter=',', skiprows=0, dtype=float):
    ret = []
    for _ in range(skiprows):
        next(file_handle)
    for i, line in enumerate(file_handle):
        line = line.decode('ascii')

        if i % 500000 == 0:
            print('line:', i, line)
        
        elements = line.rstrip().split(delimiter)
        dateStr = elements[0]
        #dat = datetime.datetime.fromisoformat('2019-01-04T16:41:24+0200')
        date = datetime.datetime.fromisoformat(dateStr).timestamp()
        #date = datetime.datetime.fromisoformat(dateStr)
        height = elements[1]
        feeStr =  elements[-1]

        ret.append((date, int(height),  int(feeStr)))
    return np.array(ret)

def filter_txt(file_handle, args, delimiter=',', skiprows=0):
    years = set()
    for year in range(args.year_start, args.year_end + 1):
        print("Adding year", year, "to filter")
        years.add(str(year))
        
    for _ in range(skiprows):
        next(file_handle)
    for i, line in enumerate(file_handle):
        lineStr = line.decode('ascii')

        if i % 500000 == 0:
            print('line:', i, lineStr)
        
        elements = lineStr.rstrip().split(delimiter)
        dateStr = elements[0]

        year = dateStr[0:4]
        
        if year not in years:
            continue
        if i % 25000 == 0:
            print(lineStr)
        yield line

def find_nearest(array,value):
    idx = np.searchsorted(array, value, side="left")
    if idx > 0 and (idx == len(array) or math.fabs(value - array[idx-1]) < math.fabs(value - array[idx])):
        return idx, array[idx-1]
    else:
        return idx, array[idx]

def get_nearest_index_of_date(data, date_str, date_format="%Y-%m-%d %H:%M:%S"):
    ts = time.mktime(datetime.datetime.strptime(date_str, date_format).timetuple())
    idx_nearest, _ = find_nearest(data[:, 0], ts)
    return idx_nearest

def dates_descr_2_ts_descr(data, dates_descr):
    ret = []
    for ele in dates_descr:
        date_str = ele[0]
        idx_nearest = get_nearest_index_of_date(data, date_str)
        date = data[idx_nearest, 0]
        height = data[idx_nearest, 1]

        #print(ele[1])
        #print("Nearest:", idx_nearest, date, height, ele[1])

        ret.append((date, height, ele[1]))

    return ret;

def get_dates_desct():
    dates_descr = []

    #dates_descr.append((DATE_MONERO_2020,      DATE_MONERO_2020.split()[0]))
    #dates_descr.append((DATE_MONERO_0_17,      'monero-core: Oxygen Orion v0.17.0.0'))
    dates_descr.append((DATE_MONERO_2_3,       'monero-core: Oxygen Orion 2.3'))
    dates_descr.append((DATE_MONERO_3_0,       'monero-core: Oxygen Orion 3.0'))
    dates_descr.append(('2022-02-28 02:55:41', 'mm-core-cpp-c: Update fee calc to use CLSAG'))
    #dates_descr.append(('2022-02-28 02:58:43', 'mm-core-cpp-c: Re-use the same set of outs'))
    dates_descr.append(('2022-04-07 11:43:45', 'mm-app-js: v1.2.6'))
    dates_descr.append(('2022-07-14 12:14:14', 'mm-core-cpp-c: Merge PR #35 j-berman/clsag-fees'))
    dates_descr.append(('2022-07-15 11:43:15', 'monero-core: v0.18.0.0'))
    dates_descr.append(('2022-07-18 12:52:50', 'mm-core-cpp-c: Merge PR #36 j-berman/tie-outs-to-mix-outs'))
    dates_descr.append(('2022-07-30 20:15:21', 'mm-core-cpp-c: Update monero-core-custom to 0.18.0.0'))
    dates_descr.append(('2022-07-31 11:31:19', 'mm-core-cpp-c: eabedb9 PR #38 from ndorf/master'))
    dates_descr.append(('2022-08-09 22:34:23', 'monero-core: v0.18.1.0 Fluorine Fermi'))
    dates_descr.append(('2022-08-10 17:09:19', 'mm-app-js: v1.3.0 Merge dev into master'))

    return dates_descr

def get_data(args):
    start = datetime.datetime.now()
    PATH_DATA = WDIR + args.in_data + '.pkl'
    PATH_DATA_FILTERED = WDIR + args.in_data + '-filtered.tar.gz'
    os.makedirs(WDIR, exist_ok=True)

    status, data = try_pickle(PATH_DATA)
    if status:
        end = datetime.datetime.now()
        print("Unpickled in:", datetime.datetime.now() - start)
    else:
        PATH_SRC = args.in_data + '.tar.gz'
        
        # Filter rows
        if not os.path.isfile(PATH_DATA_FILTERED):
            print('Loading', PATH_SRC)
            with gzip.open(PATH_SRC, 'rb') as f:
                dataStr = filter_txt(f, args, skiprows=1)
                print('Dumping filtered rows to', PATH_DATA_FILTERED)
                with gzip.open(PATH_DATA_FILTERED, 'wb') as fout:
                    for x in dataStr:
                        fout.write(x)

        #data = np.loadtxt(args.in_data, skiprows=1, delimiter=',')
        #with gzip.open(args.in_data, 'rb') as f:
        #    data = iter_loadtxt(f, skiprows=10000000, dtype=int)
        

        with gzip.open(PATH_DATA_FILTERED, 'rb') as f:
            print("Reading", PATH_DATA_FILTERED)
            data = filter_columns(f)
        print('Pickling to', PATH_DATA)
        with open(PATH_DATA, 'wb') as fout:
            pickle.dump(data, fout, protocol=pickle.HIGHEST_PROTOCOL)
   
    return data

def main(args):
    start = datetime.datetime.now()
    data = get_data(args)
    print('got', int(len(data)/1000), 'thousand rows.')#, 'Shape =', data.shape)

    dates_descr = get_dates_desct()
    height_descr = dates_descr_2_ts_descr(data, dates_descr)
    dates_start = dates_descr[0][0]

    idx_nearest_monero_fee_update = get_nearest_index_of_date(data, dates_start)
    ts_fee_upgrade_monero = data[idx_nearest_monero_fee_update, 0]
    print("Nearest:", idx_nearest_monero_fee_update, datetime.datetime.fromtimestamp(ts_fee_upgrade_monero))

    if not args.full_data:
        rang = int(args.ahead_points)
        idx_start = idx_nearest_monero_fee_update - rang
        if idx_start < 0:
            idx_start = 0
        #data = data[idx_nearest_monero_fee_update - rang : idx_nearest_monero_fee_update + rang]
        data = data[idx_start : ]
        print("Pre:  ", len(data))
        data = data[::args.skip_every] # Every nth
        print("Post: ", len(data))

    print("Start:", datetime.datetime.fromtimestamp(data[0, 0]))
    print("End:  ", datetime.datetime.fromtimestamp(data[-1, 0]))
        
    data = data[data[:, 2] < 94730652324144]
    data = data[data[:, 2] > 0]
    values = data[:, 2]
    #values = np.log(values)
    xxx = data[:, 0]

    rows_list = []
    ts_prev = 0
    for i, ts in enumerate(data[:, 0]):
        if ts != ts_prev:
            #date = datetime.datetime.fromtimestamp(int(ts))
            ts_prev = ts
        #print(i, date, ts)
        

        fee = data[i, 2]
        height = data[i, 1]
        val = np.log(fee)
        rows_list.append({'timestamp': height, 'fee': val})
            
    dframe = pd.DataFrame(rows_list)

    print("Processed in:", datetime.datetime.now() - start)
    #
    #print(max(values))
    #if args.plot:
    if True:
        #plt.bar(xxx, values)
        #plot_xy(xxx, np.log(values), height_descr)
        plot_color(dframe, height_descr)
        #plot_box(boxplot_x, boxplot_data, height_descr)
        #
        #plot_isth(dframe)
        #plot_seaborn(dframe)
        print("Plotted in:", datetime.datetime.now() - start)
        #plt.savefig('fig.png')
        plt.show()
    #dump(xxx, values)

def plot_isth(dframe):
    import pandas as pd
    import isthmuslib as isli

#dframe = pd.DataFrame(data=data[1:,1:],    # values
     #         index=data[1:,0],    # 1st column as index
      #        columns=data[0,1:])  # 1st row as the column names
    #dframe = pd.DataFrame(data=np_arr[0:,0:])  # 1st row as the column names


    print(dframe.head)
    #dframe.set_axis(['timestamp', "height", "fee"], axis=1, inplace=True)
    #dframe.index.names = ['timestamp']
    print(dframe.head)
    
    tsr = isli.VectorSequence().from_dataframe(dframe, inplace=False,
    basis_col_name='timestamp', name_root='Experiment gamma')

    #tsr = isli.VectorSequence().from_dataframe(dframe, inplace=False)
    
    #tsr.hist('fee', bins=50)
    tsr.plot(x='timestamp', y='fee')
    #tsr.surface('timestamp', 'fee', 'fee')
    plt.show()

def dump(xxx, vals):
    DUMP = WDIR + "/FEES.csv.gz"
    #with open(DUMP, mode='w') as fout:
    with gzip.open(DUMP, mode='wb') as fout:
        for x, v in zip(xxx, vals):
            fout.write("{},{}\n".format(int(x), int(v)).encode('ascii'))

def add_timeline_get_legend(height_descr, x_index_fun):
    legend = []
    for i, ele in enumerate(height_descr):
        vert_x = x_index_fun(ele)
        descr = ele[2]
        tab_col = mcolors.TABLEAU_COLORS
        #tab_col = mcolors.CSS4_COLORS
        keys = list(tab_col.keys())
        key = keys[i % len(keys)]
        plt.axvline(x=vert_x, color=tab_col[key])
        legend.append(descr)
    return legend

def plot_color(dframe, height_descr):
    ts = dframe['timestamp']
    fees = dframe['fee']

    cmap = copy(plt.cm.plasma)
    cmap.set_bad(cmap(0))

    h, xedges, yedges = np.histogram2d(ts, fees, bins=[100, 70])

    fig, ax = plt.subplots()
    pcm = ax.pcolormesh(xedges, yedges, h.T, cmap=cmap,
                             norm=LogNorm(vmax=h.max()),
                        rasterized=True)
    fig.colorbar(pcm, ax=ax, label="# points", pad=0)
    legend_timeline = add_timeline_get_legend(height_descr, lambda ele: ele[1])
    plt.legend(legend_timeline)
    ax.set_title("Transaction fees' timeline & occurence")
    plt.ylabel('log(fee)') 
    plt.xlabel('height')

def plot_xy(x, y, height_descr):
    dates=[datetime.datetime.fromtimestamp(ts) for ts in x]
    plt.xticks( rotation=25 )
    plt.subplots_adjust(bottom=0.2)
    ax=plt.gca()
    xfmt = md.DateFormatter('%Y-%m-%d')
    ax.xaxis.set_major_formatter(xfmt)
    plt.plot(dates,y, color='black')
    legend = ['tx fee']
    legend_timeline = add_timeline_get_legend(height_descr, lambda ele: datetime.datetime.fromtimestamp(ele[0]))
    legend.extend(legend_timeline)
    plt.title("Transaction fees' timeline")
    plt.legend(legend)
    plt.ylabel('log(fee)')    
    plt.xlabel('Date')
    
    #plt.show()

def plot_box(x, y, height_descr):
    plt.boxplot(y)
    #plt.boxplot(y, positions=list(x))
    legend = ['tx fee']       
    plt.title("Transaction fees' timeline")
    plt.legend(legend)
    #plt.legend(legend)
    plt.ylabel('log(fee)')    
    plt.xlabel('Date')
    plt.grid()

def plot_seaborn(dframe):
    import seaborn as sns
    import pandas as pd

    #dframe = pd.DataFrame(data=data)  # 1st row as the column names
    #dframe.dropna(inplace=True)
    #print(dframe.head)
    
    #dframe.set_axis(["fee"], axis=1, inplace=True)
    print(dframe.head)
        
    plt.figure(figsize=(12, 8))
    sns.violinplot(x='timestamp', y='fee', data=dframe, color='yellow', inner='stick')
    #sns.violinplot(x='price', y='color', data=dframe, color='yellow', inner='stick')
    #add_cosmetics()
    

def plot_ts(values, timestamps): 
    plt.xticks( rotation=25 )
    plt.subplots_adjust(bottom=0.2)
    ax=plt.gca()
    xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
    ax.xaxis.set_major_formatter(xfmt)
    
    #dates=[datetime.datetime.fromtimestamp(ts) for ts in timestamps]
    dates = timestamps
    
    plt.plot(dates,values)
    plt.legend(['tx_fee'])
    
    plt.show()

def try_pickle(PATH_DATA):
    candidates = []
    candidates.append((PATH_DATA, open))
    candidates.append((PATH_DATA + ".gz",  gzip.open))
    candidates.append((PATH_DATA + ".xz", lzma.open))

    for pat, file_opener in candidates:
        print("Trying:", pat)
        if os.path.isfile(pat):
            print("Unpickling:", pat)
            with file_opener(pat, 'rb') as fin:
                return True, pickle.load(fin)
    return False, None

if __name__ == "__main__":
    args = get_args()
    main(args)

# How to load 
##def iter_loadtxt(file_handle, delimiter=',', skiprows=0, dtype=float):
##    def iter_func():
##        for _ in range(skiprows):
##            next(file_handle)
##        for i, line in enumerate(file_handle):
##            line = line.decode('ascii')
##
##            if i % 50000 == 0:
##                print('line:', i, line)
##            
##            elements = line.rstrip().split(delimiter)
##            
##            dateStr = elements[0]
##            feeStr =  elements[-1]
##            yield dtype(feeStr)
##            #for item in elements:
##            #    yield dtype(item)
##        iter_loadtxt.rowlength = len(line) # ?
##
##    data = np.fromiter(iter_func(), dtype=dtype)
##    #data = data.reshape((-1, iter_loadtxt.rowlength))
##    return data
##
# https://stackoverflow.com/a/8964779
##def generate_text_file(length=1e6, ncols=20):
##    data = np.random.random((length, ncols))
##    np.savetxt('large_text_file.csv', data, delimiter=',')
##
##def iter_loadtxt(filename, delimiter=',', skiprows=0, dtype=float):
##    def iter_func():
##        with open(filename, 'r') as infile:
##            for _ in range(skiprows):
##                next(infile)
##            for line in infile:
##                line = line.rstrip().split(delimiter)
##                for item in line:
##                    yield dtype(item)
##        iter_loadtxt.rowlength = len(line)
##
##    data = np.fromiter(iter_func(), dtype=dtype)
##    data = data.reshape((-1, iter_loadtxt.rowlength))
##    return data
##
###generate_text_file()
##data = iter_loadtxt('large_text_file.csv')
