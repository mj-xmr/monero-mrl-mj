#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 26.11.2021

@author: mj-xmr
"""

import os
import sys
import time
import shutil
import platform
import subprocess
import argparse
import multiprocessing as mp

NPROC=mp.cpu_count()
DIR_BUILD_BASE='build'
DIR_BIN='bin'
OFF='OFF'
ON='ON'

GENERATOR="Placeholder"

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--benchmark', default=False, action='store_true', help="benchmark (default: OFF)")
    parser.add_argument(      '--plot',      default=False, action='store_true', help="plot in Python (default: OFF)")
    parser.add_argument('-g', '--generator', default=GENERATOR, help='Generator of project files (default: "{}")'.format(GENERATOR))
    parser.add_argument('-a', '--path',      default=".",   help="Run path")
    return parser

def tests():
    print("Tests")

def main(args):
    tests()


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    main(args)
