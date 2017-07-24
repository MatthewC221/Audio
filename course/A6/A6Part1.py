#!/usr/bin/python

import os
import sys
import numpy as np
import math
from scipy.signal import get_window
import matplotlib.pyplot as plt

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../software/models/'))
import utilFunctions as UF
import harmonicModel as HM
import sineModel as SM
import stft

eps = np.finfo(float).eps

def estimateF0(inputFile = '../../sounds/cello-double-2.wav'):
    """
    Function to estimate fundamental frequency (f0) in an audio signal. This function also plots the 
    f0 contour on the spectrogram and synthesize the f0 contour.
    Input:
        inputFile (string): wav file including the path
    Output:
        f0 (numpy array): array of the estimated fundamental frequency (f0) values
    """

    ### Change these analysis parameter values marked as XX
    window = 'blackman'
    M = 4401
    N = 8192
    f0et = 8
    t = -90.0
    minf0 = 130
    maxf0 = 200

    ### Do not modify the code below 
    H = 256                                                     #fix hop size
      
    fs, x = UF.wavread(inputFile)                               #reading inputFile
    w  = get_window(window, M)                                  #obtaining analysis window    
    
    ### Method 1
    f0 = HM.f0Detection(x, fs, w, N, H, t, minf0, maxf0, f0et)  #estimating F0
    startFrame = np.floor(0.5*fs/H)    
    endFrame = np.ceil(4.0*fs/H)
    f0[:startFrame] = 0
    f0[endFrame:] = 0
    y = UF.sinewaveSynth(f0, 0.8, H, fs)
    UF.wavwrite(y, fs, 'synthF0Contour.wav')

    ## Code for plotting the f0 contour on top of the spectrogram
    # frequency range to plot
    maxplotfreq = 500.0    
    fontSize = 16
    plot = 1

    fig = plt.figure()
    ax = fig.add_subplot(111)

    mX, pX = stft.stftAnal(x, w, N, H)                      #using same params as used for analysis
    mX = np.transpose(mX[:,:int(N*(maxplotfreq/fs))+1])
    
    timeStamps = np.arange(mX.shape[1])*H/float(fs)                             
    binFreqs = np.arange(mX.shape[0])*fs/float(N)
    
    plt.pcolormesh(timeStamps, binFreqs, mX)
    plt.plot(timeStamps, f0, color = 'k', linewidth=1.5)
    plt.plot([0.5, 0.5], [0, maxplotfreq], color = 'b', linewidth=1.5)
    plt.plot([4.0, 4.0], [0, maxplotfreq], color = 'b', linewidth=1.5)
    
    
    plt.autoscale(tight=True)
    plt.ylabel('Frequency (Hz)', fontsize = fontSize)
    plt.xlabel('Time (s)', fontsize = fontSize)
    plt.legend(('f0',))
    
    xLim = ax.get_xlim()
    yLim = ax.get_ylim()
    ax.set_aspect((xLim[1]-xLim[0])/(2.0*(yLim[1]-yLim[0])))    

    if plot == 1: #save the plot too!
        plt.autoscale(tight=True) 
        plt.show()
    else:
        fig.tight_layout()
        fig.savefig('f0_over_Spectrogram.png', dpi=150, bbox_inches='tight')

    return f0

estimateF0()