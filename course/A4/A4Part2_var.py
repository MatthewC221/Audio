#!/usr/bin/python

# A4Part2.py VARIATION

import os
import sys
import numpy as np
import math
from scipy.signal import get_window
import matplotlib.pyplot as plt

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../software/models/'))
import stft
import utilFunctions as UF
eps = np.finfo(float).eps
        
# Inverse of E(db) = 10log10(E), we have E(db)
# Therefore, 10 ^ (E(db) / 10)
def energy_computation(mX):

    energy = np.sum(10 ** (mX / 10))
    return energy
    
def computeSNR(inputFile, window, M, N, H):
    """
    Input:
            inputFile (string): wav file name including the path 
            window (string): analysis window type (choice of rectangular, triangular, hanning, hamming, 
                    blackman, blackmanharris)
            M (integer): analysis window length (odd positive integer)
            N (integer): fft size (power of two, > M)
            H (integer): hop size for the stft computation
    Output:
            The function should return a python tuple of both the SNR values (SNR1, SNR2)
            SNR1 and SNR2 are floats.
    """
    
    # Calculate the SNR after synthesis and analysis STFT
    
    w = get_window(window, M)
    
    # SNR (signal to noise ratio) = 10log10(Energy of signal / Energy of noise)
    
    (fs, x) = UF.wavread(inputFile)
    
    # Do analysis and synthesis
    mX, pX = stft.stftAnal(x, w, N, H)    
    y = stft.stftSynth(mX, pX, M, H)

    # Resizing y so we can calculate energy of noise
    resized_y = y[:x.size]
    
    # Calculating the noise of part 1 and 2
    noise1 = x - resized_y
    noise2 = x[w.size:-w.size] - resized_y[w.size:-w.size]
    
    # Analyse both noises
    mNoise1, pNoise1 = stft.stftAnal(noise1, w, N, H)
    mNoise2, pNoise2 = stft.stftAnal(noise2, w, N, H)
    
    energyInput = energy_computation(mX)
    energyNoise1 = energy_computation(mNoise1)
    energyNoise2 = energy_computation(mNoise2)    
    
    SNR1 = 10 * np.log10(energyInput / energyNoise1)
    SNR2 = 10 * np.log10(energyInput / energyNoise2)

    return SNR1, SNR2
    
    
    
    
    
