#!/usr/bin/python

import sys
sys.path.append('../../software/models/')
from dftModel import dftAnal, dftSynth
from scipy.signal import get_window
import matplotlib.pyplot as plt
import numpy as np
import math

def suppressFreqDFTmodel(x, fs, N):
    """
    Inputs:
        x (numpy array) = input signal of length M (odd)
        fs (float) = sampling frequency (Hz)
        N (positive integer) = FFT size
    Outputs:
        The function should return a tuple (y, yfilt)
        y (numpy array) = Output of the dftSynth() without filtering (M samples long)
        yfilt (numpy array) = Output of the dftSynth() with filtering (M samples long)
    The first few lines of the code have been written for you, do not modify it. 
    """
    M = len(x)
    w = get_window('hamming', M)
    outputScaleFactor = sum(w)
    
    # mX = mag spectrum, pX = phase spectrum
    mX, pX = dftAnal(x, w, N)
    
    # without the filter
    y = dftSynth(mX, pX, w.size) * outputScaleFactor
    
    # https://stackoverflow.com/questions/4364823/how-do-i-obtain-the-frequencies-of-each-value-in-an-fft
    fil_70 = int(math.ceil(70.0 * N / fs))
    
    mX[:fil_70 + 1] = -120
    
    yfilt = dftSynth(mX, pX, w.size) * outputScaleFactor
    
    return y, yfilt
