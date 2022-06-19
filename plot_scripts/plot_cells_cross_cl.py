import numpy as np
import matplotlib.pyplot as plt

#####
# Cross-CL pipeline plotter. 
# Plots:
#  a) residuals CL_data - CL_FG_model(MAP params) for both models
#  b) best-fit CMB model (containing r_MAP and A_lens_MAP) for both models
#  c) lensing template 

# Input: 
# From 100 simulations containing goal optimistic noise + dmsm foregrounds, need:
# * CAMB templates 'lens_nobb' (A_lens=1, r=0) and 'lens_r1' (A_lens=1, r=1)
# * Coadded BB D_ells from 100 simulations (np array, shape (nsims=100,nbpws=27,nbands=6,nbands=6))
# * Coadded BB D_ells error bars (np array, shape (nbpws=27,nbands=6,nbands=6))
# * CL-fiducial MAP parameters (txt, 100+1 rows, 9+1 columns)
# * CL-moments MAP parameters (txt, 100+1 rows, 13+1 columns)
# * CL-fiducial predicted D_ells from 100 simulations (np array, shape (nsims=100,nbpws=27,nbands=6,nbands=6))
# * CL-moments predicted D_ells from 100 simulations (np array, shape (nsims=100,nbpws=27,nbands=6,nbands=6))

def get_triangle_axes():
    nbins=6
    fig, axes = plt.subplots(nbins, nbins,
                             figsize=(15, 10),
                             constrained_layout=True,
                             sharex=True)
    for b1 in range(nbins) :
        for b2 in range(nbins) :
            if b2<b1 :
                axes[b2,b1].axis('off')
    return axes

####
# 2: Read data
camb_lens_nobb_path = 'data/camb_lens_nobb_nico.dat' 
camb_lens_r1_path = 'data/camb_lens_r1_nico.dat'
dells_path = 'data/dells_coadded.npz'
dells_model_fid_path = 'data/dells_coadded_model_cl_fiducial.npz'
params_fid_path = 'data/params_cl_fiducial.txt'
# TODO: Replace files with true moments results. 
dells_model_mom_path = 'data/dells_coadded_model_cl_moments.npz'
params_mom_path = 'data/params_cl_moments.txt'                   

# templates
cmb_ls = np.loadtxt(camb_lens_r1_path)[:,0]
mask = (cmb_ls <= 300) & (cmb_ls > 30)
ls = cmb_ls[mask]
dl2cl = 2*np.pi/ls/(ls+1)
cmb_r1 = np.loadtxt(camb_lens_r1_path)[:,3][mask]
cmb_tens = (np.loadtxt(camb_lens_r1_path)[:,3] - np.loadtxt(camb_lens_nobb_path)[:,3])[mask]
cmb_lens = np.loadtxt(camb_lens_nobb_path)[:,3][mask]

# parameters
with open(params_fid_path) as fid:
    fid_names = np.array(fid.readline().strip().split()[1:])
fid_params = np.loadtxt(params_fid_path)[:,1:]
r_fid = fid_params[:,np.where(fid_names=='r_tensor')].flatten()
AL_fid = fid_params[:,np.where(fid_names=='A_lens')].flatten()
with open(params_mom_path) as mom:
    mom_names = np.array(mom.readline().strip().split()[1:])
mom_params = np.loadtxt(params_mom_path)[:,1:]
r_mom = mom_params[:,np.where(mom_names=='r_tensor')].flatten()
AL_mom = mom_params[:,np.where(mom_names=='A_lens')].flatten()

# Factor 0.5 below is just for demonstration. 
# TODO: remove once real moments data are included!
cmb_dls_fid = r_fid[:,None]*cmb_tens[None,:] + AL_fid[:,None]*cmb_lens[None,:]
cmb_dls_mom = 0.5*r_mom[:,None]*cmb_tens[None,:] + AL_mom[:,None]*cmb_lens[None,:]
print('r:', np.mean(r_fid), '(fid)', np.mean(r_mom), '(mom)\n AL:', np.mean(AL_fid), '(fid)', np.mean(AL_mom), '(mom)')

# data
ells = np.load(dells_path)['l']
dell2cell = 2*np.pi/ells/(ells+1)
cmb_dls_fid_ells = []
cmb_dls_mom_ells = []
for il,l in enumerate(ls):
    if l in list(ells.astype('int')):
        cmb_dls_fid_ells.append(cmb_dls_fid[:,il])
        cmb_dls_mom_ells.append(cmb_dls_mom[:,il])    
cmb_dls_fid_ells = np.asarray(cmb_dls_fid_ells).T
cmb_dls_mom_ells = np.asarray(cmb_dls_mom_ells).T

dells_err = np.load(dells_path)['el']/np.sqrt(len(r_fid))
dells_mom = np.load(dells_model_mom_path)['dl']
residual_dells_fid = np.mean(np.load(dells_path)['dl'] - np.load(dells_model_fid_path)['dl'] + cmb_dls_fid_ells[:,:,None,None], axis=0)
residual_dells_mom = np.mean(np.load(dells_path)['dl'] - np.load(dells_model_mom_path)['dl'] + cmb_dls_mom_ells[:,:,None,None], axis=0)

####
# 3: Make plot (D_ells).
axes = get_triangle_axes()
ylims = [[1e-4, 100],[1e-4, 100],[1e-4, 1e-1],[1e-4, 1e-1],[1e-4, 1],[1e-4, 1]]
for i1 in range(6):
    for i2 in range(i1,6):
        ax = axes[i2, i1]
        ax.plot(ls, cmb_lens, 'k-')
        
        # CL-fiducial
        ax.errorbar(ells, residual_dells_fid[:,i1,i2], yerr=dells_err[:,i1,i2], fmt='b.', elinewidth=.5)
        high_fid = np.where(residual_dells_fid[:,i1,i2] > ylims[i1][1])
        low_fid = np.where(residual_dells_fid[:,i1,i2] < ylims[i1][0])
        ax.scatter(ells[high_fid], np.full(len(ells[high_fid]), ylims[i1][1]), c='b', marker='^', s=30)
        ax.scatter(ells[low_fid], np.full(len(ells[low_fid]), ylims[i1][0]), c='b', marker='v', s=30)
        ax.plot(ls, np.mean(cmb_dls_fid, axis=0), 'b--')
        
        # CL-moments
        # Factor 0.9 below is just for demonstration. 
        # TODO: remove once real moments data are included!
        ax.errorbar(ells, 0.9*residual_dells_mom[:,i1,i2], yerr=dells_err[:,i1,i2], fmt='r.', elinewidth=.5)
        high_mom = np.where(residual_dells_mom[:,i1,i2] > ylims[i1][1])
        low_mom = np.where(residual_dells_mom[:,i1,i2] < ylims[i1][0])
        ax.scatter(ells[high_mom], np.full(len(ells[high_mom]), ylims[i1][1]), c='r', marker='^', s=20)
        ax.scatter(ells[low_mom], np.full(len(ells[low_mom]), ylims[i1][0]), c='r', marker='v', s=20)
        ax.plot(ls, np.mean(cmb_dls_mom, axis=0), 'r--')
        
        ax.set_ylim(ylims[i1])
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_xticks([30,100,200])
        ax.set_xticklabels([30,100,200])
        props = dict(facecolor='white', alpha=0.5, edgecolor='white')
        ax.text(0.04, 0.78, f'$({i1+1},{i2+1})$',
                transform=ax.transAxes, fontsize=12, bbox=props)
        if i2 == 5:
            ax.set_xlabel(r'$\ell$', fontsize=14)
        if i1 == 0:
            ax.set_ylabel(r'$D_\ell\;[\mu\rm{K}^2]$', fontsize=14)
        if (i1==1) or (i1==3) or (i1==5):
            ax.set_yticklabels([])
plt.savefig('plot_dells_cross_cl.pdf')

####
# 4: Make plot (C_ells).
axes = get_triangle_axes()
ylims = [[-5e-5, 5e-5],[-5e-5, 5e-5],[1e-6, 4e-6],[1e-6, 4e-6],[-5e-5, 5e-5],[-5e-5, 5e-5]]
for i1 in range(6):
    for i2 in range(i1,6):
        ax = axes[i2, i1]
        ax.plot(ls, dl2cl*cmb_lens, 'k-')
        
        # CL-fiducial
        ax.errorbar(ells, dell2cell*residual_dells_fid[:,i1,i2], yerr=dell2cell*dells_err[:,i1,i2], fmt='b.', elinewidth=.5)
        high_fid = np.where(dell2cell*residual_dells_fid[:,i1,i2] > ylims[i1][1])
        low_fid = np.where(dell2cell*residual_dells_fid[:,i1,i2] < ylims[i1][0])
        ax.scatter(ells[high_fid], np.full(len(ells[high_fid]), ylims[i1][1]), c='b', marker='^', s=30)
        ax.scatter(ells[low_fid], np.full(len(ells[low_fid]), ylims[i1][0]), c='b', marker='v', s=30)
        ax.plot(ls, dl2cl*np.mean(cmb_dls_fid, axis=0), 'b--')
        
        # CL-moments
        # Factor 0.9 below is just for demonstration. 
        # TODO: remove once real moments data are included!
        ax.errorbar(ells, 0.9*dell2cell*residual_dells_mom[:,i1,i2], yerr=dell2cell*dells_err[:,i1,i2], fmt='r.', elinewidth=.5)
        high_mom = np.where(dell2cell*residual_dells_mom[:,i1,i2] > ylims[i1][1])
        low_mom = np.where(dell2cell*residual_dells_mom[:,i1,i2] < ylims[i1][0])
        ax.scatter(ells[high_mom], np.full(len(ells[high_mom]), ylims[i1][1]), c='r', marker='^', s=20)
        ax.scatter(ells[low_mom], np.full(len(ells[low_mom]), ylims[i1][0]), c='r', marker='v', s=20)
        ax.plot(ls, dl2cl*np.mean(cmb_dls_mom, axis=0), 'r--')
        
        ax.set_ylim(ylims[i1])
        ax.set_xticks([50,150,250])
        ax.set_xticklabels([50,150,250])
        props = dict(facecolor='white', alpha=0.5, edgecolor='white')
        ax.text(0.04, 0.78, f'$({i1+1},{i2+1})$',
                transform=ax.transAxes, fontsize=12, bbox=props)
        if i2 == 5:
            ax.set_xlabel(r'$\ell$', fontsize=14)
        if i1 == 0:
            ax.set_ylabel(r'$C_\ell\;[\mu\rm{K}^2]$', fontsize=14)
        if (i1==1) or (i1==3) or (i1==5):
            ax.set_yticklabels([])
plt.savefig('plot_cells_cross_cl.pdf')
