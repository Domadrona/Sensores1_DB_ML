# -*- coding: utf-8 -*-
"""
Created on 2020

@author: Julio Cuadros
"""
import numpy as np
from scipy import stats
import scipy.io as sio

mat = sio.loadmat('signal.mat')
# number of signals in .mat file
n = mat['signal'].shape[0]
# get the signals
signals = mat['signal'][:,0]

def Features(signal):
    mu = np.mean(signal)                            # Mean                  
    variance  = np.var(signal)                      # variance
    skw = stats.skew(signal)                        # skewness
    kurt = stats.kurtosis(signal, fisher=False)     # Kurtosis
    rms = np.sqrt(np.mean(signal ** 2))             # Root mean square
    
    tfeatures = np.array([mu,variance,skw,kurt,rms])

    
    return  tfeatures

# pre-allocate memory without initializing it
features_mat = np.empty((n,5))
for i, signal in enumerate(signals):
    features_mat[i,:] = Features(signal)
print('Time features were extracted successfully')

features_mat = np.column_stack((features_mat,np.ones((n,),dtype=int)))
features_mat[25:50,5] = 0
print('Enter Filename: ')
Filename = input()
np.save(Filename, features_mat) 
db=np.load('Features.npy')