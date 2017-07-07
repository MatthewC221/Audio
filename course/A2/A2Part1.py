import numpy as np
import sys

def genSine(A, f, phi, fs, t):

    t = np.arange(0, t, 1.0/fs)
    x = A * np.cos (2 * np.pi * f * t + phi)
    
    return x 
        






