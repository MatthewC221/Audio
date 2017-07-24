import os
import sys
import numpy as np
import math
from scipy.signal import get_window
import matplotlib.pyplot as plt

# This one took a while, computing inharmonicity 

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../software/models/'))
import utilFunctions as UF
import harmonicModel as HM
import stft

eps = np.finfo(float).eps

def estimateInharmonicity(inputFile = '../../sounds/piano.wav', t1=0.1, t2=0.5, window='hamming', 
                            M=2048, N=2048, H=128, f0et=5.0, t=-90, minf0=130, maxf0=180, nH = 10):
    """
    Function to estimate the extent of inharmonicity present in a sound
    Input:
        inputFile (string): wav file including the path
        t1 (float): start time of the segment considered for computing inharmonicity
        t2 (float): end time of the segment considered for computing inharmonicity
        window (string): analysis window
        M (integer): window size used for computing f0 contour
        N (integer): FFT size used for computing f0 contour
        H (integer): Hop size used for computing f0 contour
        f0et (float): error threshold used for the f0 computation
        t (float): magnitude threshold in dB used in spectral peak picking
        minf0 (float): minimum fundamental frequency in Hz
        maxf0 (float): maximum fundamental frequency in Hz
        nH (integer): number of integers considered for computing inharmonicity
    Output:
        meanInharm (float or np.float): mean inharmonicity over all the frames between the time interval 
                                        t1 and t2. 
    """
    # 0. Read the audio file and obtain an analysis window
    
    fs, x = UF.wavread(inputFile)

    w = get_window(window, M)

    # 1. Use harmonic model to compute the harmonic frequencies and magnitudes
    xhfreq, xhmag, xhphase = HM.harmonicModelAnal(x, fs, w, N, H, t, nH, minf0, maxf0, f0et, harmDevSlope=0.01, minSineDur=0.0)

    # 2. Extract the time segment in which you need to compute the inharmonicity. 
    
    interval_start = int(math.ceil(t1 * fs / float(H)))
    interval_end = int(math.ceil(t2 * fs / float(H)))

    # 3. Compute the mean inharmonicity of the segment

    # Refer to the pdf for the formulas used

    f0 = HM.f0Detection(x, fs, w, N, H, t, minf0, maxf0, f0et)

    f0_slice = f0[interval_start:interval_end]
    sliced = xhfreq[interval_start:interval_end]
    inharmon = np.zeros(sliced.size)

    for index, arr in enumerate(sliced):
        tmp_sum = 0

        for j in range(1, arr.size):
            val = j + 1
            tmp_sum += np.abs(arr[j] - val * f0_slice[index]) / float(val)

        inharmon[index] = tmp_sum * (1 / float(nH))

    mean_inharmon = sum(inharmon) / (interval_end - interval_start + 1)

    return mean_inharmon