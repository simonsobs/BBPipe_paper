import numpy as np
import matplotlib.pyplot as plt

#### 
# 1: Quick description
# Comparison plot between homogeneous and inhomogeneous noise

###
# 2: Read data
# Important: data needs to be formatted like in the example "r_results_cl_fiducial.txt"
_, _, _, mean_r_cl_fiducial, mean_std_r_cl_fiducial = np.loadtxt("data/r_results_cl_fiducial.txt", dtype='str', skiprows=1, unpack=True)
_, _, _, mean_r_map_based, mean_std_r_map_based = np.loadtxt("data/r_results_map_based_fiducial.txt", dtype='str', skiprows=1, unpack=True)
_, _, _, mean_r_nilc, mean_std_r_nilc = np.loadtxt("data/r_results_NILC_fiducial.txt", dtype='str', skiprows=1, unpack=True)
_, _, _, mean_r_cl_moments, mean_std_r_cl_moments = np.loadtxt("data/r_results_moments_fiducial.txt", dtype='str', unpack=True)

mean_r_cl_fiducial = mean_r_cl_fiducial.astype('float')
mean_std_r_cl_fiducial = mean_std_r_cl_fiducial.astype('float')
mean_r_map_based = mean_r_map_based.astype('float')
mean_std_r_map_based = mean_std_r_map_based.astype('float')
mean_r_nilc = mean_r_nilc.astype('float')
mean_std_r_nilc = mean_std_r_nilc.astype('float')
mean_r_cl_moments = mean_r_cl_moments.astype('float')
mean_std_r_cl_moments = mean_std_r_cl_moments.astype('float')

###
# 3: Make plot.
fig, ax1 = plt.subplots(figsize=(6,4))
ax2 = ax1.twinx()

ax1.set_ylabel(r'$r$')
ax2.set_ylabel(r'relative increase $\sigma(r)$')
ax1.axhline(0, color='k', linestyle='dashed')
ax1.set_ylim((-.0045,.0045))
ax2.set_ylim((-.45,.45))

markers = ['o', 'x']

for noi in [2]:                # 0: gop, 1: gpe, 2: blop, 3: blpe; for now blop only
    for fgs in [1]:            # 0: gauss, 1: d0s0, 2: d1s1, 3: dmsm; for now d0s0 only
        idx_inhom = 4*noi + fgs
        idx_hom = 16 + 4*noi + fgs
        ratios = [mean_std_r_cl_fiducial[idx_inhom]/mean_std_r_cl_fiducial[idx_hom]-1,
                  mean_std_r_cl_moments[idx_inhom]/mean_std_r_cl_moments[idx_hom]-1,
                  mean_std_r_nilc[idx_inhom]/mean_std_r_nilc[idx_hom]-1,
                  mean_std_r_map_based[idx_inhom]/mean_std_r_map_based[idx_hom]-1]
        ax2.plot([-3,-1,1,3], ratios, ls='-', marker='o', c='k')
        for inh in [0,1]:                # 0: inhom, 1: hom
            m = markers[inh]
            idx = 16*inh + 4*noi + fgs
            ax1.errorbar(-3+.5*(inh-.5), mean_r_cl_fiducial[idx], 
                         yerr=mean_std_r_cl_fiducial[idx], fmt=f'r{m}')
            ax1.errorbar(-1+.5*(inh-.5), mean_r_cl_moments[idx], 
                         yerr=mean_std_r_cl_moments[idx], fmt=f'y{m}')
            ax1.errorbar(1+.5*(inh-.5), mean_r_nilc[idx], 
                         yerr=mean_std_r_nilc[idx], fmt=f'b{m}')
            ax1.errorbar(3+.5*(inh-.5), mean_r_map_based[idx], 
                         yerr=mean_std_r_map_based[idx], fmt=f'g{m}')

ax1.set_xticks([-3, -1, 1, 3])
ax1.set_xticklabels(['Pipeline A', r'$+$ moments', 'Pipeline B', 'Pipeline C'])
plt.tight_layout()
plt.savefig('hom_vs_inhom.pdf')

###
# 4: Make LaTeX table to paste into paper draft
print(" ")
print(" ")
stout = "\\begin{table*}\n\centering\n\\begin{tabular}{|l|c|c|c|c|}\n"
stout += "\hline\n"
stout += "\multicolumn{5}{|c|}{$10^3\\times(r\pm\sigma(r))$}\\\\\n"
stout += "\hline\n"
stout += "Noise & Pipeline A & $+$ moments & Pipeline B & Pipeline C\\\\\n"
stout += "\hline\n"
for noi in [2]:                # 0: gop, 1: gpe, 2: blop, 3: blpe; for now blop only
    for fgs in [1]:            # 0: gauss, 1: d0s0, 2: d1s1, 3: dmsm; for now d0s0 only
        first = ['d0s0 inhom.', 'd0s0 hom.']
        for inh in [0,1]:      # 0: inhom, 1: hom
            idx = 16*inh + 4*noi + fgs
            st = first[inh] + " & "
            st += " $%.1lf \pm %.1lf$ & " % (mean_r_cl_fiducial[idx]*1E3, mean_std_r_cl_fiducial[idx]*1E3)
            st += " $%.1lf \pm %.1lf$ & " % (mean_r_cl_moments[idx]*1E3, mean_std_r_cl_moments[idx]*1E3)
            st += " $%.1lf \pm %.1lf$ & " % (mean_r_nilc[idx]*1E3, mean_std_r_nilc[idx]*1E3)
            st += " $%.1lf \pm %.1lf$ \\\\\n " % (mean_r_map_based[idx]*1E3, mean_std_r_map_based[idx]*1E3)      
            stout += st
        idx_inhom = 4*noi + fgs
        idx_hom = 16 + 4*noi + fgs
        ratios = [mean_std_r_cl_fiducial[idx_inhom]/mean_std_r_cl_fiducial[idx_hom]-1,
                  mean_std_r_cl_moments[idx_inhom]/mean_std_r_cl_moments[idx_hom]-1,
                  mean_std_r_map_based[idx_inhom]/mean_std_r_map_based[idx_hom]-1,
                  mean_std_r_nilc[idx_inhom]/mean_std_r_nilc[idx_hom]-1]
        stout += "\hline\n"
        st = r"rel. increase $\sigma(r)$" + " & "
        st += " $%.2lf$ & " % (ratios[0])
        st += " $%.2lf$ & " % (ratios[1])
        st += " $%.2lf$ & " % (ratios[2])
        st += " $%.2lf$ \\\\\n " % (ratios[3])            
        stout += st
            
stout += "\hline\n"
stout += "\\end{tabular}\n"
stout += "\caption{\lipsum[5]}\label{tab:r_fiducial_results}\n"
stout += "\end{table*}\n"
print(stout)
print(" ")
print(" ")