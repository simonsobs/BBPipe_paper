import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

#####
# 1: Quick description
# Error bars plot of r results with the Cross-CL pipeline
####

# 2: Read data
# Important: data needs to be formatted like in the example "r_results_cl_fiducial.txt"
_, _, _, mean_r_cl_fiducial, mean_std_r_cl_fiducial = np.loadtxt("data/r_results_cl_fiducial.txt", dtype='str', skiprows=1, unpack=True)
# TODO: Replace the results files with the other pipeline results
_, _, _, mean_r_map_based, mean_std_r_map_based = np.loadtxt("data/r_results_cl_fiducial.txt", dtype='str', skiprows=1, unpack=True)
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

# 3: Make plot. This is the part that the designated plotter will tweak.
plt.figure(figsize=(6,4))
plt.axhline(0, color='k')
markers = ['o', 's', 'v', 'x']

for inh in range(1):                # 0: inhom, 1: hom; for now inhom only
    for noi in [0, 3]:                # 0: gop, 1: gpe, 2: blop, 3: blpe; for now gop and blpe only
        m = markers[noi]
        for fgs in range(4):           # gauss, d0s0, d1s1, dmsm
            idx = 16*inh + 4*noi + fgs
            plt.errorbar(fgs + noi*0.02, mean_r_cl_fiducial[idx], yerr=mean_std_r_cl_fiducial[idx], fmt=f'r{m}')
            plt.errorbar(fgs+0.2+noi*0.02, mean_r_map_based[idx], yerr=mean_std_r_map_based[idx], fmt=f'g{m}')
            plt.errorbar(fgs+0.4+noi*0.02, mean_r_nilc[idx], yerr=mean_std_r_nilc[idx], fmt=f'b{m}')
            plt.errorbar(fgs+0.6+noi*0.02, mean_r_cl_moments[idx], yerr=mean_std_r_cl_moments[idx], fmt=f'y{m}')
plt.xticks([0.33,1.33,2.33,3.33], ['Gaussian', 'd0s0', 'd1s1', 'dmsm'])

line_cl_fiducial = Line2D([0], [0], label='CL-fiducial', color='r')
line_map_based = Line2D([0], [0], label='map-based', color='g')
line_nilc = Line2D([0], [0], label='NILC', color='b')
line_cl_moments = Line2D([0], [0], label='CL-moments', color='y')

fgnames = ['Gaussian', 'd0s0', 'd1s1', 'dmsm']
nlev = ['Goal rms,', 'Goal rms,', 'Baseline rms,', 'Baseline rms,']
oof = ['optimistic $1/f$', 'pessimistic $1/f$',
       'optimistic $1/f$', 'pessimistic $1/f$']
print(" ")
print(" ")
stout = "\\begin{table*}\n\centering\n\\begin{tabular}{|l|l|c|c|c|c|}\n"
stout += "\hline\n"
stout += "\multicolumn{6}{|c|}{$10^3\\times(r\pm\sigma(r))$}\\\\\n"
stout += "\hline\n"
stout += "Noise & FG model & Pipeline A & $+$ moments & Pipeline B & Pipeline C\\\\\n"
for inh in range(1):
    for noi in range(4):
        stout += "\hline\n"
        for fgs in range(4):
            if fgs in [0, 3]:
                first = ' & '
            elif fgs == 1:
                first = nlev[noi] + " & "
            elif fgs == 2:
                first = oof[noi] + " & "
            idx = 16*inh+4*noi+fgs
            st = first + fgnames[fgs] + " & "
            st += " $%.2lf \pm %.2lf$ & " % (mean_r_cl_fiducial[idx]*1E3, mean_std_r_cl_fiducial[idx]*1E3)
            st += " $%.2lf \pm %.2lf$ & " % (mean_r_cl_moments[idx]*1E3, mean_std_r_cl_moments[idx]*1E3)
            st += " $%.2lf \pm %.2lf$ & " % (mean_r_map_based[idx]*1E3, mean_std_r_map_based[idx]*1E3)
            st += " $%.2lf \pm %.2lf$ \\\\\n " % (mean_r_nilc[idx]*1E3, mean_std_r_nilc[idx]*1E3)
            stout += st
stout += "\hline\n"
stout += "\\end{tabular}\n"
stout += "\caption{\lipsum[5]}\label{tab:r_fiducial_results}\n"
stout += "\end{table*}\n"
print(stout)
print(" ")
print(" ")

handles, labels = plt.gca().get_legend_handles_labels()
handles.extend([line_cl_fiducial, line_map_based, line_nilc, line_cl_moments])
plt.ylabel(r'$r$')
plt.legend(handles=handles, loc='lower right')
plt.savefig('r_fiducial.pdf', bbox_inches='tight')
plt.show()
