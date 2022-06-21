import numpy as np
import matplotlib.pyplot as plt

#####
# Bandpass weights plotter. 
# 1: Short description
# Plots ell-dependent bandpass weights (see Planck 2020 IV, eq. 2) for Cross-CL:
#  a) d1s1 foregrounds + baseline pessimistic inhom. noise (solid)
#  b) d1s1 foregrounds + goal optimistic inhom. noise (dashed)
#
# Input: 
# From Cross-CL, need:
# * 100 Cross + auto spectra, d1s1 foregrounds + baseline pessimistic inhom. noise
# * 100 Cross + auto spectra, d1s1 foregrounds + goal optimistic inhom. noise

###
# 2: Read and prepare data
# Cross-CL: ell-wise bandpass weights
w_gop = np.load('data/bandpass_weights_cross_cl_d1s1_gop.npz')
w_blpe = np.load('data/bandpass_weights_cross_cl_d1s1_blpe.npz')
leff = w_gop['leff']
bands = w_gop['bands']
weights_gop = w_gop['weights']
weights_blpe = w_blpe['weights']

###
# 3: Make plot
plt.figure(figsize=(6,4))
plt.axhline(0, color='k')
for ib in range(6):
    plt.plot(leff, np.mean(weights_gop[:,:,ib], axis=0), label=bands[ib]+' GHz', c=f'C{ib}', ls='-')
    plt.plot(leff, np.mean(weights_blpe[:,:,ib], axis=0), c=f'C{ib}', ls=':')
plt.legend(loc='upper right')
plt.ylabel(r'CMB weight $w_\ell$')
plt.xlabel(r'multipole $\ell$')
plt.title('Cross-CL')
plt.yscale('symlog', linthresh=1e-3)
plt.ylim((-2,2))
plt.tight_layout()
plt.savefig('channel_weights_cross_cl_d1s1.pdf')
