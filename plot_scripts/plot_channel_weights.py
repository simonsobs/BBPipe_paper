import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

#####
# 1: Quick description
# Make three vertically stacked subplots with shared x-axis = 
# band central frequency and showing in the three panels:
# * SMICA bandpass weights for Cross-CL, plotting all 27 ell-bins 
#   (d1s1 + blpe)
# * NILC bandpass weights, plotting all 5 windows (d1s1 + blpe)
# * map-averaged map-based weights (d1s1 + blpe)

####
# 2: Read data
# SMICA
w_smica_gop = np.load('data/bandpass_weights_cross_cl_d1s1_gop.npz')
w_smica_blpe = np.load('data/bandpass_weights_cross_cl_d1s1_blpe.npz')
leff_smica = w_smica_gop['leff']
bands = w_smica_gop['bands']
weights_smica_gop = w_smica_gop['weights'] # shape (100,27,6)
weights_smica_blpe = w_smica_blpe['weights'] # shape (100,27,6)

# NILC
# shape (100,5,6)
weights_nilc_gop = np.load('data/weights_per_channel_nilc_inhg_goal-op_d1s1.npy')
weights_nilc_blpe = np.load('data/weights_per_channel_nilc_inhg_baseline-pe_d1s1.npy')

# map-based
avg = np.loadtxt('data/channel_weights.txt', usecols=(4,5,6,7,8,9), dtype='float', unpack=True).T
weights_map_based_gop = avg[4] # shape (1,6)
weights_map_based_blpe = avg[5] # shape (1,6)

###
# 3: Make plot.
fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, sharex=True, figsize=(5,9))
bds = [int(b) for b in bands]
ax1.set_ylabel('SMICA weights')
ax2.set_ylabel('NILC weights')
ax3.set_ylabel('map-based weights')

for ax in [ax1, ax2, ax3]:
    ax.axhline(0, color='k', linestyle='dashed')
    ax.set_yscale('symlog', linthresh=1e-3)
    ax.set_ylim((-2,2))
    ax.set_xticks([27,39,93,145,225,280], minor=False)
    ax.xaxis.grid(True, which='major')
    ax.yaxis.grid()
    if ax==ax3:
        ax.set_xlabel('frequency [GHz]')

# SMICA
col = plt.cm.Reds(np.linspace(0.2,1,len(leff_smica)))
for il,l in enumerate(leff_smica):
    ax1.plot([b for b in bds], np.mean(weights_smica_blpe[:,il,:], axis=0), 
             c=col[il], ls='-', marker='')
    ax1.plot([b for b in bds], np.mean(weights_smica_gop[:,il,:], axis=0), 
             c=col[il], ls='--', marker='')
line_ell0 = Line2D([0], [0], label=r'$\ell_{\rm eff}=%.i$' % leff_smica[0], 
                   color=col[0])
line_ell8 = Line2D([0], [0], label=r'$\ell_{\rm eff}=%.i$' % leff_smica[8], 
                   color=col[8])
line_ell18 = Line2D([0], [0], label=r'$\ell_{\rm eff}=%.i$' % leff_smica[18], 
                    color=col[18])
line_ell26 = Line2D([0], [0], label=r'$\ell_{\rm eff}=%.i$' % leff_smica[26], 
                    color=col[26])
handles, labels = ax1.get_legend_handles_labels()
handles.extend([line_ell0, line_ell8, line_ell18, line_ell26])
ax1.legend(handles=handles, loc='lower center')

# NILC
col = plt.cm.Blues(np.linspace(0.4,1,5))
for w in range(1,6):
    ax2.plot([b for b in bds], np.mean(weights_nilc_blpe[:,w-1,:], axis=0), 
             c=col[w-1], ls='-', marker='', label=f'window {w}')
    ax2.plot([b for b in bds], np.mean(weights_nilc_gop[:,w-1,:], axis=0), 
             c=col[w-1], ls='--', marker='')
    ax2.legend(loc='lower center')

# map-based
ax3.plot([b for b in bds], weights_map_based_blpe, c='green', ls='-', marker='')
ax3.plot([b for b in bds], weights_map_based_gop, c='green', ls='--', marker='')
plt.tight_layout()
plt.savefig('channel_weights.pdf')