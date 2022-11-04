#!/bin/bash

# Runs Monero daemon in a loop.
# The daemon may be killed with killall monerod, after which it's safe to copy the blockchain elsewhere for analysis.
# The function process_iteration from monerod-internal.sh handles this operation.
#
# Author: mj-xmr


while true; do
        source monerod-internal.sh # Reload any changes
        run_daemon # awaiting to be killed
        # let the process close all the file handles
        echo "Processing the output"
        sleep 1
        source monerod-internal.sh # Reload any changes
        process_iteration
        echo "Restarting the cycle"
done

