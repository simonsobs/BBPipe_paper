import numpy as np
import matplotlib.pyplot as plt

#####
# Channel weights plotter. 
# Plots sky-averaged channel weights for all three pipelines:
#  a) d1s1 foregrounds + baseline pessimistic inhom. noise (solid)
#  b) cross + auto spectra, d1s1 foregrounds + goal optimistic inhom. noise (dashed)

###
# 1. Load data
# TODO: Replace NaNs with results from NILC pipeline.
avg = np.loadtxt('data/channel_weights.txt', usecols=(4,5,6,7,8,9), dtype='float', unpack=True).T

###
# 2. Make plot
plt.figure(figsize=(6,4))
bands = ['27', '39', '93', '145', '225', '280']
colors = ['r', 'b', 'g']
labels = [['A goal + opt.', 'baseline + pess.'], 
          ['B goal + opt.', 'baseline + pess.'],
          ['C goal + opt.', 'baseline + pess.']]
lines = ['-', ':']
markers = ['o', 'x']
bds = [int(b) for b in bands]
plt.axhline(0, color='k', linestyle='dashed')
for pip in range(3): # 0: cross-cl, 1: nilc, 2: map-based
    for noise in range(2): # 0: gop, 1: blpe
        idx = 2*pip + noise
        l = lines[noise]
        c = colors[pip]
        lab = labels[pip][noise]
        m = markers[noise]
        plt.plot([b for b in bds], avg[idx], c=c, ls=l, marker=m, label=lab)
plt.yscale('symlog', linthresh=1.e-3)
plt.ylim((-2,2))
plt.xlabel('frequency [GHz]')
plt.ylabel('CMB weight')
plt.title('Average over 100 sims (d1s1 foregrounds)')
plt.legend()
plt.tight_layout()
plt.savefig('map_averaged_channel_weights_d1s1.pdf')