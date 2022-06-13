import numpy as np
import matplotlib.pyplot as plt
import healpy as hp


#####
# Cross-CL bandpass weights plotter. 
# Plots SMICA-like bandpass weights (see Planck 2020 IV, eq. 2) for each band:
#  a) cross + auto spectra, d1s1 foregrounds + baseline pessimistic inhom. noise (solid)
#  b) cross + auto spectra, d1s1 foregrounds + goal optimistic inhom. noise ()

# Input: 
# From 100 simulations, need:
# * Cross + auto spectra, d1s1 foregrounds + baseline pessimistic inhom. noise
# * Cross + auto spectra, d1s1 foregrounds + goal optimistic inhom. noise

###
# 2: Read data
w1 = np.load('data/cross_cl_weights_d1s1_gop.npz')
w2 = np.load('data/cross_cl_weights_d1s1_blpe.npz')
bands = w1['bands']
leff = w1['leff']
weights1 = w1['weights']
weights2 = w2['weights']

###
# 3: Make plot
for ib in range(6):
    plt.plot(leff, np.mean(weights1[:,:,ib], axis=0), label=bands[ib], c=f'C{ib}', ls='-')
    plt.plot(leff, np.mean(weights2[:,:,ib], axis=0), c=f'C{ib}', ls=':')
plt.legend()
plt.ylabel(r'weight $w_\ell$')
plt.xlabel(r'multipole $\ell$')
plt.title('SMICA-like weights from Cross-CL (d1s1)')
plt.yscale('log')
plt.ylim((1e-4,5))
plt.savefig('data/bandpass_weights_cross_cl.png')