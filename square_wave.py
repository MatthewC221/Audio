#!/usr/bin/python

from scipy import signal
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 1000, endpoint=True)

plt.plot(x, signal.square(2 * np.pi * 15 * x))
plt.title("Square wave, 15 Hz sampled at 1000 Hz / sec")

plt.xlabel('Time (mSec)')
plt.ylabel('Amp')

plt.ylim(-2, 2)
plt.show()