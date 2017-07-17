#!/usr/bin/python

# Finding frequency estimation at a time and attempts to make it accurate to 0.05Hz

import numpy as np
from scipy.signal import get_window
import math
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../software/models/'))
import dftModel as DFT
import utilFunctions as UF

# Finds next power of 2 > M
def nextPow(M):
    
    start = 1
    while (M > start):
        start = start * 2
    
    return start

def minFreqEstErr(inputFile, f):

    # analysis parameters:
    window = 'blackman'
    t = -40
    
    (fs, x) = UF.wavread(inputFile)
    
    # Get window from half of sound file
    half = int(x.size / 2)
    
    # Window size of 100 * k + 1
    M = 101
    
    # Initialise
    N = 0
    freq = 0
    err = 0.05 
    
    while (M < x.size):
        w = get_window(window, M)
        
        win_size = int(M / 2)
        
        # Taking window from halfway
        x1 = x[half-win_size : half+win_size+1]
        N = nextPow(M)
        mX, pX = DFT.dftAnal(x1, w, N)

        ploc = UF.peakDetection(mX, t)
        # iploc = interpolated peak location, ipmag = magnitude val, ipphase = phase values
        iploc, ipmag, ipphase = UF.peakInterp(mX, pX, ploc)
               
        freq = float(iploc) * float(fs) / N
        
        if (abs(f - freq) < err):
            break
        
        M += 100
    
    return (freq, M, N) 
