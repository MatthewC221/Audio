#!/usr/bin/python

# UNvoCyAMGDE85uDU

import numpy as np
from scipy.signal import get_window
from scipy.fftpack import fft, fftshift
import math
import matplotlib.pyplot as plt
eps = np.finfo(float).eps

def extractMainLobe(window, M):
    """
    Input:
            window (string): Window type to be used (Either rectangular ('boxcar'), 'hamming' or '
                blackmanharris')
            M (integer): length of the window to be used
    Output:
            The function should return a numpy array containing the main lobe of the magnitude 
            spectrum of the window in decibels (dB).
    """    
    w = get_window(window, M)         # get the window 
    
    N = 8 * M
    half_N = int(N / 2) 
        
    # Creating fftbuffer of 8 * M
    fftbuffer = np.zeros(N)
    
    # Left and right of window
    left = int(M / 2)
    right = M - left

    # Copying values from the window
    fftbuffer[:right] = w[left:]
    fftbuffer[N-left:] = w[:left]
           
    x = fft(fftbuffer)
    absX = abs(x)
    mX = 20 * np.log10 (absX)
    
    # Appending last half of mX with first half of mX (symmetrical)
    mX = np.append(mX[half_N:], mX[:half_N])
    
    # Find where the increase starts
    saved = 0
    for i in range(half_N):
        tmp = half_N + i
        if (mX[tmp] < mX[tmp + 1]):
            saved = i
            break    

    return mX[(half_N - saved):(half_N + saved + 1)]
    
    
    
    
    
    
    
    
    
    
    
    
    
    
