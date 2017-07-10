#!/usr/bin/python

import numpy as np
import scipy.fftpack as sci
import math

def optimalZeropad(x, fs, f):
    """
    Inputs:
        x (numpy array) = input signal of length M
        fs (float) = sampling frequency in Hz
        f (float) = frequency of the sinusoid in Hz
    Output:
        The function should return
        mX (numpy array) = The positive half of the DFT spectrum of the N point DFT after zero-padding 
                        x appropriately (zero-padding length to be computed). mX is (N/2)+1 samples long
    """
    ## Your code here
    
    samples_per_sin = float(fs) / f
    
    periods = float(x.size) / samples_per_sin
    
    diff = (math.ceil(periods) - periods) * samples_per_sin
    
    for i in range(int(diff)):
        x = np.append(x, 0)
    
    DFT = sci.fft(x)
    
    size = x.size / 2 + 1
    
    mX = np.array([])
    for i in DFT[:size]:
        mX = np.append(mX, 20 * math.log(abs(i), 10))
    
    return mX

