#!/usr/bin/python

import sys
import numpy as np
import matplotlib.pylab as plt

# Generating sine, cosine waves in numpy

lower_bound = -np.pi * 4
upper_bound = lower_bound * -1

arr = np.linspace(lower_bound, upper_bound, 801)
plt.plot(arr, np.sin(arr))
plt.xlabel('Angle (rad)')
plt.ylabel('Amplitude')
plt.axis('tight')

plt.plot(arr, np.cos(arr))
plt.show()