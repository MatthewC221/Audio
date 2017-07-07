import numpy as np

def IDFT(X):

    size = X.size
    freq = np.arange(0, size)
    x = np.array([])
    
    for i in freq:
        s = np.exp(1j * 2 * np.pi * i / size * freq)
        x = np.append(x, sum(X * s) * 1.0 / size)
    
    print x
    return x
    
IDFT(np.array([1,2,3,4]))
    
    
    
    
    
    
    
    
    
