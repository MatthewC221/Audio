# Audio processing (my uni project will be uploaded here in the future)
## My implementations of VERY BASIC audio processing

I don't have any extremely meaningful projects in mind so for now they will all go under one repo. Special thanks to Andrew Owen for the mini-project suggestions.

## General folder

Wav_reader, volume_decrease and volume_limit are all very similar

- wav_reader.c = takes in a .wav file and outputs the same one to same.wav
- wav.h = header file for wav headers and data
- volume_decrease.c = takes in .wav file, decreases the volume by a percentage into new.wav. I got stuck for a bit on this one because the sample code I looked at used short int, but I needed to use uint8_t.

- FIR.c = FIR filter, [0.25, 0.5, 0.25]
- Complex_FIR.c = more complex FIR filter (in the works)
- plotter.py = plots .wav files for visual analysis (requires scipy and matplotlib, use pip for install)

- DFT.c = will turn into a FFT / DFT lib in the future hopefully.

## Under course is material from the coursera course on Audio DSP: https://www.coursera.org/learn/audio-signal-processing/

- Weekly assignments

Triangle_filters.py:
![Triangle filters, fs=44100, FFT_size=1024, min_freq=300, max_freq=22050](/triangle_filters.png?raw=true "Triangle filters, fs=44100, FFT_size=1024, min_freq=300, max_freq=22050")
