#!/usr/bin/python

# Segmenting stable note regions in a signal. Quite long

import os
import sys
import numpy as np
import math
from scipy.signal import get_window
import matplotlib.pyplot as plt

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../software/models/'))
import utilFunctions as UF
import harmonicModel as HM
import stft

eps = np.finfo(float).eps

# TO calculate standard deviation
def standardDeviation(arr, length):

    size = arr.size
    
    if (not size):
        return 0

    mean = float(sum(arr)) / size

    new_arr = np.zeros(size)

    for i in range(size):
        new_arr[i] = (arr[i] - mean) ** 2

    new_mean = float(sum(new_arr)) / size

    return math.sqrt(new_mean)

def segmentStableNotesRegions(inputFile = '../../sounds/sax-phrase-short.wav', stdThsld=10, minNoteDur=0.1, 
                              winStable = 3, window='hamming', M=1024, N=2048, H=256, f0et=5.0, t=-100, 
                              minf0=310, maxf0=650):
    """
    Function to segment the stable note regions in an audio signal
    Input:
        inputFile (string): wav file including the path
        stdThsld (float): threshold for detecting stable regions in the f0 contour (in cents)
        minNoteDur (float): minimum allowed segment length (note duration)  
        winStable (integer): number of samples used for computing standard deviation
        window (string): analysis window
        M (integer): window size used for computing f0 contour
        N (integer): FFT size used for computing f0 contour
        H (integer): Hop size used for computing f0 contour
        f0et (float): error threshold used for the f0 computation
        t (float): magnitude threshold in dB used in spectral peak picking
        minf0 (float): minimum fundamental frequency in Hz
        maxf0 (float): maximum fundamental frequency in Hz
    Output:
        segments (np.ndarray): Numpy array containing starting and ending frame indexes of every segment.
    """
    fs, x = UF.wavread(inputFile)                               #reading inputFile
    w  = get_window(window, M)                                  #obtaining analysis window    
    f0 = HM.f0Detection(x, fs, w, N, H, t, minf0, maxf0, f0et)  #estimating F0

    size = f0.size

    # Step 1

    f0_cents = np.zeros(size)
    for i in range(size):
        if (f0[i] != 0):
            f0_cents[i] = 1200.0 * np.log2(float(f0[i] / 55.0))

    # Step 2    

    SD_win = np.zeros(size)

    for i in range(size):
        arr = f0_cents[i - winStable + 1: i + 1]
        SD_win[i] = standardDeviation(arr, winStable)

    # Step 3
    stableNote = np.array([])           # Append as we don't know how many stable regions

    for i in range(winStable, size):
        if (SD_win[i] < stdThsld):
            stableNote = np.append(stableNote, i)

    # Step 4
    duration = 1                        # including first
    count = 0

    start_end = []

    # Do this so we can initialise the ndarray properly

    for i in range(1, stableNote.size):
        if (stableNote[i - 1] == stableNote[i] - 1):
            duration += 1
        else: # Step 5
            if (duration * H / float(fs) >= minNoteDur):                    
                start_end.append((stableNote[i - duration], stableNote[i - 1]))
            duration = 1

    segments = np.ndarray(shape=(len(start_end), 2))

    for i in range(len(start_end)):
        segments[i] = start_end[i]

    plotSpectogramF0Segments(x, fs, w, N, H, f0, segments)  # Plot spectrogram and F0 if needed

    return segments

    # 1. convert f0 values from Hz to Cents (as described in pdf document)

    #2. create an array containing standard deviation of last winStable samples

    #3. apply threshold on standard deviation values to find indexes of the stable points in melody

    #4. create segments of continuous stable points such that consecutive stable points belong to same segment
    
    #5. apply segment filtering, i.e. remove segments with are < minNoteDur in length

    # return segments


def plotSpectogramF0Segments(x, fs, w, N, H, f0, segments):
    """
    Code for plotting the f0 contour on top of the spectrogram
    """
    # frequency range to plot
    maxplotfreq = 1000.0    
    fontSize = 16

    fig = plt.figure()
    ax = fig.add_subplot(111)

    mX, pX = stft.stftAnal(x, w, N, H)                      #using same params as used for analysis
    mX = np.transpose(mX[:,:int(N*(maxplotfreq/fs))+1])
    
    timeStamps = np.arange(mX.shape[1])*H/float(fs)                             
    binFreqs = np.arange(mX.shape[0])*fs/float(N)
    
    plt.pcolormesh(timeStamps, binFreqs, mX)
    plt.plot(timeStamps, f0, color = 'k', linewidth=5)

    for ii in range(segments.shape[0]):
        plt.plot(timeStamps[segments[ii,0]:segments[ii,1]], f0[segments[ii,0]:segments[ii,1]], color = '#A9E2F3', linewidth=1.5)        
    
    plt.autoscale(tight=True)
    plt.ylabel('Frequency (Hz)', fontsize = fontSize)
    plt.xlabel('Time (s)', fontsize = fontSize)
    plt.legend(('f0','segments'))
    
    xLim = ax.get_xlim()
    yLim = ax.get_ylim()
    ax.set_aspect((xLim[1]-xLim[0])/(2.0*(yLim[1]-yLim[0])))    
    plt.autoscale(tight=True) 
    plt.show()
    
