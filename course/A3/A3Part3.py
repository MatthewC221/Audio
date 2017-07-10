#!/usr/bin/python

import numpy as np
import scipy.fftpack as sci
import math

def testRealEven(x):

    size = x.size
    
    half = x.size / 2
    size = x.size - 1
    
    i = 0
    flag = True
    
    while (half > i):
        if (x[i] != x[size - i]):
            flag = False
            break
            
        i += 1
    
    for i in range(size):
        if (x[i] != abs(x[i])):
            flag = False
    
    dftbuffer = np.array([])
    
    for i in range(half, x.size):
        dftbuffer = np.append(dftbuffer, x[i])
    
    for i in range(0, half):
        dftbuffer = np.append(dftbuffer, x[i]) 
        
    X = sci.fft(dftbuffer)

    return (flag), dftbuffer, X
    
    
    
    
