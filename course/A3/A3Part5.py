#!/usr/bin/python

import numpy as np
import sys
sys.path.append('../../software/models/')
from scipy.fftpack import fft
import matplotlib.pyplot as plt
from scipy.signal import get_window
from dftModel import dftAnal

def zpFFTsizeExpt(x, fs):
    """
    Inputs:
        x (numpy array) = input signal (2*M = 512 samples long)
        fs (float) = sampling frequency in Hz
    Output:
        The function should return a tuple (mX1_80, mX2_80, mX3_80)
        mX1_80 (numpy array): The first 80 samples of the magnitude spectrum output of dftAnal for Case-1
        mX2_80 (numpy array): The first 80 samples of the magnitude spectrum output of dftAnal for Case-2
        mX3_80 (numpy array): The first 80 samples of the magnitude spectrum output of dftAnal for Case-3
        
    The first few lines of the code to generate xseg and the windows have been written for you, 
    please use it and do not modify it. 
    """
    
    M = len(x)/2
    xseg = x[:M]
    w1 = get_window('hamming',M)
    w2 = get_window('hamming',2*M)
    ## Your code here 
    
    mX1, pX1 = dftAnal(xseg, w1, M)
    mX2, pX2 = dftAnal(x, w2, 2 * M)
    mX3, pX3 = dftAnal(xseg, w1, 2 * M)
    
    plt.plot(mX1[:80], label="Case 1: xseg, w1, size=256", color="green")
    plt.plot(mX2[:80], label="Case 2: x   , w2, size=512", color="red")
    plt.plot(mX3[:80], label="Case 3: xseg, w1, size=512", color="blue")
    plt.xlabel('Samples')
    plt.ylabel('Magnitude (Hz)')
    plt.show()
    
    return (mX1[:80], mX2[:80], mX3[:80])
