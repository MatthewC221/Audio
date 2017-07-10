# -*- coding: utf-8 -*-

import numpy as np
import scipy.fftpack as sci
import math
from fractions import gcd

# P7OyJRruZdMdMSkz

def minimizeEnergySpreadDFT(x, fs, f1, f2):
    """
    Inputs:
        x (numpy array) = input signal 
        fs (float) = sampling frequency in Hz
        f1 (float) = frequency of the first sinusoid component in Hz
        f2 (float) = frequency of the second sinusoid component in Hz
    Output:
        The function should return 
        mX (numpy array) = The positive half of the DFT spectrum (in dB) of the M sample segment of x. 
                           mX is (M/2)+1 samples long (M is to be computed)
    """
    GCD = gcd(f1, f2)
    M = fs / GCD
    
    Mx_size = int(M / 2) + 1
    
    DFT = sci.fft(x[:int(M)])

    Mx = np.array([])
    for i in DFT[0:Mx_size]:
        Mx = np.append(Mx, 20 * math.log(abs(i), 10))

    return Mx
    
    
    
    
    
    
