import numpy as np
import matplotlib.pyplot as plt

#####
# Bandpass weights plotter. 
# 1. Plots ell-dependent bandpass weights (see Planck 2020 IV, eq. 2) for Cross-CL:
#  a) d1s1 foregrounds + baseline pessimistic inhom. noise (solid)
#  b) d1s1 foregrounds + goal optimistic inhom. noise (dashed)
#
# 2. Plots sky-averaged bandpass weights for all three pipelines:
#  a) d1s1 foregrounds + baseline pessimistic inhom. noise (solid)
#  b) cross + auto spectra, d1s1 foregrounds + goal optimistic inhom. noise (dashed)

# Input: 
# From Cross-CL, need:
# * 100 Cross + auto spectra, d1s1 foregrounds + baseline pessimistic inhom. noise
# * 100 Cross + auto spectra, d1s1 foregrounds + goal optimistic inhom. noise
#
# From Cross-CL, map-based, NILC need:
# * 100 map-averaged bandpass weights, d1s1 foregrounds + baseline pessimistic inhom. noise
# * 100 map-averaged bandpass weights, d1s1 foregrounds + goal optimistic inhom. noise


###
# 2: Read and prepare data
# Cross-CL: ell-wise bandpass weights
w_gop = np.load('data/bandpass_weights_cross_cl_d1s1_gop.npz')
w_blpe = np.load('data/bandpass_weights_cross_cl_d1s1_blpe.npz')
leff = w_gop['leff']
bands = w_gop['bands']
weights_gop = w_gop['weights']
weights_blpe = w_blpe['weights']

# Cross-CL: map-averaged bandpass weights
w_avg_gop = np.mean(weights_gop, axis=(1))
w_avg_blpe = np.mean(weights_blpe, axis=(1))
w_file = open('data/avg_bandpass_weights_cross_cl_d1s1_gop.txt', 'w')
w_file.write('# 27GHz 39GHz 93GHz 145GHz 225GHz 280GHz\n')
for i in range(w_avg_gop.shape[0]):
    for ib in range(w_avg_gop.shape[1]):
        w_file.write(f'{w_avg_gop[i,ib]} ')
    w_file.write('\n')
w_file.close()
w_file = open('data/avg_bandpass_weights_cross_cl_d1s1_blpe.txt', 'w')
w_file.write('# 27GHz 39GHz 93GHz 145GHz 225GHz 280GHz\n')
for i in range(w_avg_blpe.shape[0]):
    for ib in range(w_avg_blpe.shape[1]):
        w_file.write(f'{w_avg_blpe[i,ib]} ')
    w_file.write('\n')
w_file.close()

# All pipelines: map-averaged bandpass weights
avg_gop_cross_cl = np.loadtxt('data/avg_bandpass_weights_cross_cl_d1s1_gop.txt', dtype='float', unpack=True)
avg_blpe_cross_cl = np.loadtxt('data/avg_bandpass_weights_cross_cl_d1s1_gop.txt', dtype='float', unpack=True)
# TODO: Replace files with true results from map-based and NILC pipeline.
avg_gop_map_based = np.loadtxt('data/avg_bandpass_weights_cross_cl_d1s1_gop.txt', dtype='float', unpack=True)
avg_blpe_map_based = np.loadtxt('data/avg_bandpass_weights_cross_cl_d1s1_gop.txt', dtype='float', unpack=True)
avg_gop_nilc = np.loadtxt('data/avg_bandpass_weights_cross_cl_d1s1_gop.txt', dtype='float', unpack=True)
avg_blpe_nilc = np.loadtxt('data/avg_bandpass_weights_cross_cl_d1s1_gop.txt', dtype='float', unpack=True)
avg_gop = [avg_gop_cross_cl, avg_gop_map_based, avg_gop_nilc]
avg_blpe = [avg_blpe_cross_cl, avg_blpe_map_based, avg_blpe_nilc]

###
# 3: Make plot
# Cross-CL: ell-wise bandpass weights
plt.figure(figsize=(6,4))
plt.axhline(0, color='k')
for ib in range(6):
    plt.plot(leff, np.mean(weights_gop[:,:,ib], axis=0), label=bands[ib]+' GHz', c=f'C{ib}', ls='-')
    plt.plot(leff, np.mean(weights_blpe[:,:,ib], axis=0), c=f'C{ib}', ls=':')
plt.legend(loc='upper right')
plt.ylabel(r'CMB weight $w_\ell$')
plt.xlabel(r'multipole $\ell$')
plt.title('Cross-CL')
plt.yscale('symlog', linthreshy=1e-3)
plt.ylim((-2,2))
plt.tight_layout()
plt.savefig('bandpass_weights_cross_cl_d1s1.pdf')
plt.clf()

# All pipelines: map-averaged bandpass weights
colors = ['r', 'g', 'b']
labels = ['CL-fiducial', 'map-based', 'NILC']
bds = [int(b) for b in bands]
for i in range(3):
    plt.errorbar([b+3*(i-1) for b in bds], np.mean(avg_gop[i], axis=1), yerr=np.std(avg_gop[i], axis=1), 
                 fmt='o', linestyle='-', color=colors[i], label=labels[i])
    plt.errorbar([b+3*(i-1) for b in bds], np.mean(avg_blpe[i], axis=1), yerr=np.std(avg_blpe[i], axis=1), 
                 fmt='x', linestyle=':', color=colors[i])
plt.axhline(0, color='k', linestyle='dashed')
plt.legend()
plt.ylabel('average CMB weight')
plt.xlabel('frequency [GHz]')
plt.yscale('symlog', linthreshy=1e-3)
plt.ylim((-2,2))
plt.title('Average over 100 sims (d1s1 FGs, blpe and gop noise)')
plt.tight_layout()
plt.savefig('map_averaged_bandpass_weights_d1s1.pdf')