#!/usr/bin/python

from scipy.io.wavfile import read
import matplotlib.pyplot as plt
import sys

if (len(sys.argv) != 2):
    print ("Usage ./plotter.py <.wav file>")
else:

# read audio samples
    input_data = read(sys.argv[1])
    audio = input_data[1]
    # plot the first 1024 samples
    plt.plot(audio[0:1024])
    # label the axes
    plt.ylabel("Amplitude")
    plt.xlabel("Time")
    # set the title  
    plt.title(sys.argv[1] + " Wav")
    # display the plot
    plt.show()
