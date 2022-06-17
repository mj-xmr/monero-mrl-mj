#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#%matplotlib

import numpy as np
import math
import bisect
import secrets
from scipy.stats import gamma
import decoy_consts
import mrl_decoy_plot
import mrl_decoy_plot_parallel

import time

class GammaPickerPyhon():
    def __init__(self, rct_offsets, shape=decoy_consts.GAMMA_SHAPE, scale=decoy_consts.GAMMA_SCALE):
        #gamma = std::gamma_distribution<double>(shape, scale);
        self.rct_offsets = rct_offsets
        
        self.THROW_WALLET_EXCEPTION_IF(len(rct_offsets) <= decoy_consts.CRYPTONOTE_DEFAULT_TX_SPENDABLE_AGE, "error::wallet_internal_error", "Bad offset calculation")
        
        blocks_in_a_year = int(86400 * 365 / decoy_consts.DIFFICULTY_TARGET_V2)
        #print("blocks_in_a_year", blocks_in_a_year)
        #raise IOError("B;")
        blocks_to_consider = min(len(rct_offsets), blocks_in_a_year)
        outputs_to_consider = rct_offsets[-1] - (rct_offsets[len(rct_offsets) - blocks_to_consider - 1] if blocks_to_consider < len(rct_offsets) else 0)
    
        self.begin = 0 # rct_offsets.data();
        # end = rct_offsets.data() + rct_offsets.size() - CRYPTONOTE_DEFAULT_TX_SPENDABLE_AGE;
        self.end = self.begin + len(rct_offsets) - decoy_consts.CRYPTONOTE_DEFAULT_TX_SPENDABLE_AGE
        #num_rct_outputs = *(end - 1);
        self.num_rct_outputs = rct_offsets[self.end - 1];
        self.THROW_WALLET_EXCEPTION_IF(self.num_rct_outputs == 0, "error::wallet_internal_error", "No rct outputs");
        self.average_output_time = decoy_consts.DIFFICULTY_TARGET_V2 * blocks_to_consider / float(outputs_to_consider); # // this assumes constant target over the whole rct range
        return
        print("rct_offsets.size()", len(self.rct_offsets))
        print("end - begin =", self.end - self.begin)
        print("num_rct_outputs", self.num_rct_outputs)
        print("self.average_output_time", self.average_output_time)
        print("end")

    def rand_idx(self, maxVal):
        return secrets.randbelow(maxVal)

    def lower_bound(self, iterable, val_to_find):
        i = bisect.bisect_left(iterable, val_to_find)
        if i != len(iterable):
            return i            
        #if i != len(iterable) and iterable[i] == val_to_find:
        #    return i
        return -1

    def THROW_WALLET_EXCEPTION_IF(self, cond, context, msg):
        if cond:
            raise Exception(context + ": " + msg)

    def pick_n_values_ratio(self, n):
        good = 0
        for i in range(0, n):
            val = self.pick()
            if val != decoy_consts.uint64_t_MAX:
                good += 1
        return good / n

    def pick_n_values(self, n):
        ret = []
        for i in range(0, n):
            val = self.pick()
            if val != decoy_consts.uint64_t_MAX:
                ret.append(val)
        return ret
            
        
    def pick(self):
        x = gamma.rvs(a=decoy_consts.GAMMA_SHAPE, scale=decoy_consts.GAMMA_SCALE)
        #double x = gamma(engine);
        x = math.exp(x);

        if (x > decoy_consts.DEFAULT_UNLOCK_TIME):
            x -= decoy_consts.DEFAULT_UNLOCK_TIME
        else:
            x = self.rand_idx(decoy_consts.RECENT_SPEND_WINDOW)

        output_index = int(x / self.average_output_time)
        #if output_index < 1:
        #if True:
            #print("index {} < 1. x = {}, self.average_output_time = {}".format(output_index, x, self.average_output_time))
        if (output_index >= self.num_rct_outputs):
            return decoy_consts.uint64_t_MAX; # bad pick
        #output_index = self.num_rct_outputs - output_index; # TODO: Altered
        output_index_pre = output_index;
        output_index = self.num_rct_outputs - 1 - output_index; # Original
        
        index = self.lower_bound(self.rct_offsets[self.begin:self.end], output_index)
        if index < 0:
            # TODO: This was added!
            print("output_index of {} not found, pre = {}, num_rct = {}".format(output_index, output_index_pre, self.num_rct_outputs))
            print("Begin", self.begin, ", end", self.end)
            print(self.rct_offsets[self.begin:self.end])
            pass
            #return decoy_consts.uint64_t_MAX # // bad pick
        self.THROW_WALLET_EXCEPTION_IF(index < 0, "error::wallet_internal_error", "output_index of {} not found".format(output_index))

        first_rct = 0 if index == 0 else self.rct_offsets[index - 1];
        n_rct = self.rct_offsets[index] - first_rct;
        if (n_rct == 0):
            return decoy_consts.uint64_t_MAX # // bad pick
        #MTRACE("Picking 1/" << n_rct << " in block " << index);
        return first_rct + self.rand_idx(n_rct);

    """
      const uint64_t *it = std::lower_bound(begin, end, output_index);
      THROW_WALLET_EXCEPTION_IF(it == end, error::wallet_internal_error, "output_index not found");
      uint64_t index = std::distance(begin, it);

      const uint64_t first_rct = index == 0 ? 0 : rct_offsets[index - 1];
      const uint64_t n_rct = rct_offsets[index] - first_rct;
      if (n_rct == 0)
        return std::numeric_limits<uint64_t>::max(); // bad pick
      MTRACE("Picking 1/" << n_rct << " in block " << index);
      return first_rct + crypto::rand_idx(n_rct);
    """

def gen_rct_outputs(mul):
    start = 1
    rct_outputs = list(range(start, math.floor(decoy_consts.MIN_RCT_LENGTH * mul) + start))

    return rct_outputs

def experiment(NUM_DRAWS):
    """ For comparison against C++"""
    fpath_experiment = "/tmp/test"
    fpath_experiment = '/tmp/picks_raw_py_mul_length'
    mrl_decoy_plot_parallel.picks_raw_parallel(fpath_experiment)

def minimal():
    NUM_DRAWS = 1000
    
    mul = 1000
    mul = 1 # test
   
    rct_outputs = gen_rct_outputs(mul)
    print("Mul =", mul, ", len =", len(rct_outputs), ", decoy_consts.MIN_RCT_LENGTH =", decoy_consts.MIN_RCT_LENGTH)
    print("front =", rct_outputs[0])
    print("back =", rct_outputs[-1])
    #print(rct_outputs)
    #print(len(rct_outputs))
    
    picker = GammaPickerPyhon(rct_outputs)
    
    picks = picker.pick_n_values(NUM_DRAWS)
    print("Len rct", len(rct_outputs))
    print(picks, mul)

def main():    
    start_time = time.time()

    experiment(100000)
    
    #minimal()
    #experiment(1000)

    seconds = time.time() - start_time
    hours = round(seconds / 3600, 2)
    print("hours passed:", hours)

if __name__ == "__main__":
    main()


