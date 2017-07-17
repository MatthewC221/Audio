#!/usr/bin/python

# The only task in this program was to change M until the err is < 2Hz
# Requires some analysis

import numpy as np
from scipy.signal import get_window
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../software/models/'))
import stft
import utilFunctions as UF
import sineModel as SM
import matplotlib.pyplot as plt

def chirpTracker(inputFile='../../sounds/chirp-150-190-linear.wav'):
    """
    Input:
           inputFile (string) = wav file including the path
    Output:
           M (int) = Window length
           H (int) = hop size in samples
           tStamps (numpy array) = A Kx1 numpy array of time stamps at which the frequency components were estimated
           fTrackEst (numpy array) = A Kx2 numpy array of estimated frequency values, one row per time frame, one column per component
           fTrackTrue (numpy array) = A Kx2 numpy array of true frequency values, one row per time frame, one column per component
           K is the number of frames
    """
    # Analysis parameters: Modify values of the parameters marked XX
    M = 3100                            # Window size in samples

    ### Go through the code below and understand it, do not modify anything ###    
    H = 128                                     # Hop size in samples
    N = int(pow(2, np.ceil(np.log2(M))))        # FFT Size, power of 2 larger than M
    t = -80.0                                   # threshold
    window = 'blackman'                         # Window type
    maxnSines = 2                               # Maximum number of sinusoids at any time frame
    minSineDur = 0.0                            # minimum duration set to zero to not do tracking
    freqDevOffset = 30                          # minimum frequency deviation at 0Hz
    freqDevSlope = 0.001                        # slope increase of minimum frequency deviation
    
    fs, x = UF.wavread(inputFile)               # read input sound
    w = get_window(window, M)                   # Compute analysis window
    tStamps = genTimeStamps(x.size, M, fs, H)   # Generate the tStamps to return
    # analyze the sound with the sinusoidal model
    fTrackEst, mTrackEst, pTrackEst = SM.sineModelAnal(x, fs, w, N, H, t, maxnSines, minSineDur, freqDevOffset, freqDevSlope)
    fTrackTrue = genTrueFreqTracks(tStamps)     # Generate the true frequency tracks
    tailF = 20                                 
    # Compute mean estimation error. 20 frames at the beginning and end not used to compute error
    meanErr = np.mean(np.abs(fTrackTrue[tailF:-tailF,:] - fTrackEst[tailF:-tailF,:]),axis=0)     
    print "Mean estimation error = " + str(meanErr) + ' Hz'      # Print the error to terminal    
    # Plot the estimated and true frequency tracks
    mX, pX = stft.stftAnal(x, w, N, H)
    maxplotfreq = 1500.0
    binFreq = fs*np.arange(N*maxplotfreq/fs)/N
    plt.pcolormesh(tStamps, binFreq, np.transpose(mX[:,:N*maxplotfreq/fs+1]),cmap = 'hot_r')
    plt.plot(tStamps,fTrackTrue, 'o-', color = 'c', linewidth=3.0)
    plt.plot(tStamps,fTrackEst, color = 'y', linewidth=2.0)
    plt.legend(('True f1', 'True f2', 'Estimated f1', 'Estimated f2'))
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.autoscale(tight=True)
    plt.show()

    return M, H, tStamps, fTrackEst, fTrackTrue  # Output returned 

### Do not modify this function
def genTimeStamps(xlen, M, fs, H):
    # Generates the timeStamps as needed for output
    hM1 = int(np.floor((M+1)/2))                     
    hM2 = int(np.floor(M/2))                         
    xlen = xlen + 2*hM2
    pin = hM1
    pend = xlen - hM1                                     
    tStamps = np.arange(pin,pend,H)/float(fs)
    return tStamps

### Do not modify this function
def genTrueFreqTracks(tStamps):
    # Generates the true frequency values to compute estimation error
    # Specifically to chirp-150-190-linear.wav
    fTrack = np.zeros((len(tStamps),2))
    fTrack[:,0] = np.transpose(np.linspace(190, 190+1250, len(tStamps)))
    fTrack[:,1] = np.transpose(np.linspace(150, 150+1250, len(tStamps)))
    return fTrack

chirpTracker()
