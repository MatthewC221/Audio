import numpy as np
import sys

def genComplexSine(k, N):
    
    t = np.arange(0, N)
    freq = 2 * np.pi * k / N
    
    x = np.exp(1j * freq * t) 
    
    return x
