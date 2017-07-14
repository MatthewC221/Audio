#!/usr/bin/python3

import os
import sys
import numpy as np
from scipy.signal import get_window
import matplotlib.pyplot as plt

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../software/models/'))
import stft
import utilFunctions as UF

eps = np.finfo(float).eps

def energy_computation(mX):
    energy = 10 * np.log10(np.sum((10 ** (mX / 10)), axis=1))
    return energy

def computeEngEnv(inputFile, window, M, N, H):

    w = get_window(window, M)
    
    (fs, x) = UF.wavread(inputFile)

    mX, pX = stft.stftAnal(x, w, N, H)
    
    size = int(N / 2) - 1
    freq = np.zeros(size)
    count = 0
    
    for val in range(size):
        freq[val] = val * float(fs) / N
        
    # Low frequency: freq > 0 and freq < 3000 (np.where can only do one cond)
    high_freq = np.where((freq > 3000) & (freq < 10000))
    
    engEnv = np.array([])
    
    LFL = []    # Low frequency list
    
    # https://stackoverflow.com/questions/21887138/iterate-over-the-output-of-np-where
    low_freq = zip(*np.where((freq > 0) & (freq < 3000)))
    high_freq = zip(*np.where((freq > 3000) & (freq < 10000)))
    # Can do this or calculate k * fs / N
   
    # Need to convert because of tuples, finds bounds
    UB_low = max(low_freq)[0]
    LB_high = min(high_freq)[0]
    UB_high = max(high_freq)[0]
    
    # Get FFT size / 2 + 1
    resize = int (N / 2) + 1
    new_size = int (mX.size / resize)
    
    low = np.zeros(shape=(new_size, UB_low))
    high = np.zeros(shape=(new_size, UB_high-LB_high+1))
   
    for i in range(new_size):
        low[i] = mX[i][1:LB_high]
        high[i] = mX[i][LB_high:UB_high+1]
    
    # Compute energy (energy conversions using log and sum ** 2)
    low_energy = energy_computation(low)
    high_energy = energy_computation(high)    
    
    # Change to right structure
    engEnvs = np.append([low_energy], [high_energy], axis=0)
    engEnvs = np.transpose(engEnvs)
    
    return engEnvs
    
    
    
