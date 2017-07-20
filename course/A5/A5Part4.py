#!/usr/bin/python


# The task here was just to complete selectFlatPhasePeak which was just to see if the region was flat by comparing it's standard deviation to the thres

import numpy as np
from scipy.signal import get_window
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../software/models/'))
import utilFunctions as UF
import sineModel as SM
import stft
import matplotlib.pyplot as plt
import math

## Complete this function
def selectFlatPhasePeak(pX, p, phaseDevThres):
    """
    Function to select a peak index based on phase flatness measure. 
    Input: 
            pX (numpy array) = The phase spectrum of the frame
            p (positive integer) = The index of peak in the magnitude spectrum
            phaseDevThres (float) = The threshold value to measure flatness of phase
    Output: 
            selectFlag (Boolean) = True, if the peak at index p is a mainlobe, False otherwise
    """
    surround = pX[p-2:p+3]
    
    mean = float(sum(surround)) / 5
    
    #  Compute squared differences
    for i in range(len(surround)):
        surround[i] = (float(surround[i]) - mean) ** 2
    
    SD = math.sqrt(float(sum(surround)) / 5)
    
    return SD < phaseDevThres
        
### Go through the code below and understand it, but do not modify anything ###
def sineModelAnalEnhanced(inputFile= '../../sounds/sines-440-602-transient.wav'):
    """
    Input:
           inputFile (string): wav file including the path
    Output:
           tStamps: A Kx1 numpy array of time stamps at which the frequency components were estimated
           tfreq: A Kx2 numpy array of frequency values, one column per component
    """
    phaseDevThres = 1e-2                                   # Allowed deviation in phase
    M = 2047                                               # window size
    N = 4096                                               # FFT size 
    t = -80                                                # threshold in negative dB
    H = 128                                                # hop-size
    window='blackman'                                      # window type
    fs, x = UF.wavread(inputFile)                          # Read input file
    w = get_window(window, M)                              # Get the window
    hM1 = int(np.floor((w.size+1)/2))                      # half analysis window size by rounding
    hM2 = int(np.floor(w.size/2))                          # half analysis window size by floor
    x = np.append(np.zeros(hM2),x)                         # add zeros at beginning to center first window at sample 0
    x = np.append(x,np.zeros(hM2))                         # add zeros at the end to analyze last sample
    pin = hM1                                              # initialize sound pointer in middle of analysis window       
    pend = x.size - hM1                                    # last sample to start a frame
    tStamps = np.arange(pin,pend,H)/float(fs)              # Generate time stamps
    w = w / sum(w)                                         # normalize analysis window
    tfreq = np.array([])
    while pin<pend:                                        # while input sound pointer is within sound            
        x1 = x[pin-hM1:pin+hM2]                            # select frame
        mX, pX = SM.DFT.dftAnal(x1, w, N)                  # compute dft
        ploc = UF.peakDetection(mX, t)                     # detect locations of peaks
        ###### CODE DIFFERENT FROM sineModelAnal() #########
        # Phase based mainlobe tracking
        plocSelMask = np.zeros(len(ploc))                  
        for pindex, p in enumerate(ploc):
            if p > 2 and p < (len(pX) - 2):                    # Peaks at either end of the spectrum are not processed
                if selectFlatPhasePeak(pX, p, phaseDevThres):  # Select the peak if the phase spectrum around the peak is flat
                    plocSelMask[pindex] = 1        
            else:
                plocSelMask[pindex] = 1                        
        plocSel = ploc[plocSelMask.nonzero()[0]]               # Select the ones chosen
        if len(plocSel) != 2:                                  # Ignoring frames that don't return two selected peaks
            ipfreq = [0.0, 0.0]
        else:
            iploc, ipmag, ipphase = UF.peakInterp(mX, pX, plocSel) # Only selected peaks to refine peak values by interpolation
            ipfreq = fs*iploc/float(N)                             # convert peak locations to Hertz
        ###### CODE DIFFERENT FROM sineModelAnal() #########
        if pin == hM1:                                        # if first frame initialize output frequency track
            tfreq = ipfreq 
        else:                                                 # rest of frames append values to frequency track
            tfreq = np.vstack((tfreq, ipfreq))
        pin += H
    # Plot the estimated frequency tracks
    mX, pX = stft.stftAnal(x, w, N, H)
    maxplotfreq = 1500.0
    binFreq = fs*np.arange(N*maxplotfreq/fs)/N
    numFrames = int(mX[:,0].size)
    frmTime = H*np.arange(numFrames)/float(fs) 
    plt.pcolormesh(frmTime, binFreq, np.transpose(mX[:,:N*maxplotfreq/fs+1]), cmap='hot_r')
    plt.plot(tStamps,tfreq[:,0], color = 'y', linewidth=2.0)
    plt.plot(tStamps,tfreq[:,1], color = 'c', linewidth=2.0)
    plt.legend(('Estimated f1', 'Estimated f2'))
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.autoscale(tight=True)
    return tStamps, tfreq
