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
        print(self.y)


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

"""
class GammaPickerPyhon():
    def __init__(self, rct_offsets, shape=decoy_consts.GAMMA_SHAPE, scale=decoy_consts.GAMMA_SCALE):
        gamma = std::gamma_distribution<double>(shape, scale);
        THROW_WALLET_EXCEPTION_IF(rct_offsets.size() <= CRYPTONOTE_DEFAULT_TX_SPENDABLE_AGE, error::wallet_internal_error, "Bad offset calculation");
        const size_t blocks_in_a_year = 86400 * 365 / DIFFICULTY_TARGET_V2;
        const size_t blocks_to_consider = std::min<size_t>(rct_offsets.size(), blocks_in_a_year);
        const size_t outputs_to_consider = rct_offsets.back() - (blocks_to_consider < rct_offsets.size() ? rct_offsets[rct_offsets.size() - blocks_to_consider - 1] : 0);
        begin = rct_offsets.data();
        end = rct_offsets.data() + rct_offsets.size() - CRYPTONOTE_DEFAULT_TX_SPENDABLE_AGE;
        num_rct_outputs = *(end - 1);
        THROW_WALLET_EXCEPTION_IF(num_rct_outputs == 0, error::wallet_internal_error, "No rct outputs");
        awaitoutput_time = DIFFICULTY_TARGET_V2 * blocks_to_consider / static_cast<double>(outputs_to_consider); // this assumes constant target over the whole rct range

    def pick()
    {
      double x = gamma(engine);
      x = exp(x);

      if (x > DEFAULT_UNLOCK_TIME) 
      {
        // We are trying to select an output from the chain that appeared 'x' seconds before the
        // current chain tip, where 'x' is selected from the gamma distribution recommended in Miller et al.
        // (https://arxiv.org/pdf/1704.04299/).
        // Our method is to get the average time delta between outputs in the recent past, estimate the number of
        // outputs 'n' that would have appeared between 'chain_tip - x' and 'chain_tip', select the real output at
        // 'current_num_outputs - n', then randomly select an output from the block where that output appears.
        // Source code to paper: https://github.com/maltemoeser/moneropaper
        //
        // Due to the 'default spendable age' mechanic in Monero, 'current_num_outputs' only contains
        // currently *unlocked* outputs, which means the earliest output that can be selected is not at the chain tip!
        // Therefore, we must offset 'x' so it matches up with the timing of the outputs being considered. We do
        // this by saying if 'x` equals the expected age of the first unlocked output (compared to the current
        // chain tip - i.e. DEFAULT_UNLOCK_TIME), then select the first unlocked output.
        x -= DEFAULT_UNLOCK_TIME;
      }
      else 
      {
        // If the spent time suggested by the gamma is less than the unlock time, that means the gamma is suggesting an output
        // that is no longer feasible to be spent (possible since the gamma was constructed when consensus rules did not enforce the
        // lock time). The assumption made in this code is that an output expected spent quicker than the unlock time would likely
        // be spent within RECENT_SPEND_WINDOW after allowed. So it returns an output that falls between 0 and the RECENT_SPEND_WINDOW.
        // The RECENT_SPEND_WINDOW was determined with empirical analysis of observed data.
        x = crypto::rand_idx(static_cast<uint64_t>(RECENT_SPEND_WINDOW));
      }

      uint64_t output_index = x / average_output_time;
      if (output_index >= num_rct_outputs)
        return std::numeric_limits<uint64_t>::max(); // bad pick
      output_index = num_rct_outputs - 1 - output_index;

      const uint64_t *it = std::lower_bound(begin, end, output_index);
      THROW_WALLET_EXCEPTION_IF(it == end, error::wallet_internal_error, "output_index not found");
      uint64_t index = std::distance(begin, it);

      const uint64_t first_rct = index == 0 ? 0 : rct_offsets[index - 1];
      const uint64_t n_rct = rct_offsets[index] - first_rct;
      if (n_rct == 0)
        return std::numeric_limits<uint64_t>::max(); // bad pick
      MTRACE("Picking 1/" << n_rct << " in block " << index);
      return first_rct + crypto::rand_idx(n_rct);
    };
"""

class GammaPickerMonero():
    def __init__(self, rct_offsets):
        pass # TODO: This will only read the data file

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

def main():
    parser = GetParser()
    args = parser.parse_args()
    rct_outputs = [1, 2, 3]
    gamPDFPy = GammaPDFPython()
    gamRVSMo = GammaRVSMonero()
    gamRVSPy = GammaRVSPython()
    
    plot_data(gamRVSMo, gamRVSPy, gamPDFPy)
    #plot_function(data)
    
if __name__ == "__main__":
    main()


