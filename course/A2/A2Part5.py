import numpy as np

def genMagSpec(x):
    
    size = x.size
    freq = np.arange(0, size)
    X = np.array([])
    
    for i in freq:
        s = np.exp(1j * 2 * np.pi * i / size * freq)
        X = np.append(X, abs(sum(x * np.conjugate(s))))
        
    return X
    
genMagSpec(np.array([1,2,3,4]))
 
