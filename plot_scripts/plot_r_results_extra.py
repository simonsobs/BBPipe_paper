import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

#####
# 1: Quick description
# Error bars plot of r results for extra cases (r=0.01, AL=1), (r=0, AL=0.5), (r=0.01, AL=0.5)

###
# 2: Read data
# Important: data needs to be formatted like in the example "r_results_cl_fiducial.txt"
_, _, _, _, _, mean_r_cl_fiducial, mean_std_r_cl_fiducial = np.loadtxt("data/r_results_cl_extra.txt", dtype='str', unpack=True)
_, _, _, _, _, mean_r_map_based, mean_std_r_map_based = np.loadtxt("data/r_results_map_based_extra.txt", dtype='str', unpack=True)
_, _, _, _, _, mean_r_cl_moments, mean_std_r_cl_moments = np.loadtxt("data/r_results_moments_extra.txt", dtype='str', unpack=True)
# TODO: Replace the results files with the other pipeline results
_, _, _, _, _, mean_r_nilc, mean_std_r_nilc = np.loadtxt("data/r_results_moments_extra.txt", dtype='str', unpack=True)

mean_r_cl_fiducial = mean_r_cl_fiducial.astype('float')
mean_std_r_cl_fiducial = mean_std_r_cl_fiducial.astype('float')
mean_r_map_based = mean_r_map_based.astype('float')
mean_std_r_map_based = mean_std_r_map_based.astype('float')
mean_r_nilc = mean_r_nilc.astype('float')
mean_std_r_nilc = mean_std_r_nilc.astype('float')
mean_r_cl_moments = mean_r_cl_moments.astype('float')
mean_std_r_cl_moments = mean_std_r_cl_moments.astype('float')

###
# 3: Make plot. This is the part that the designated plotter will tweak.
plt.figure(figsize=(6,4))
plt.axhline(0, color='k')
plt.axhline(0.01, color='k', linestyle='dashed')
case_labels = [r"$(r=0,$"+'\n'+r"$A_{\rm{lens}}=1)$",
               r"$(r=0,$"+'\n'+r"$A_{\rm{lens}}=0.5)$",
               r"$(r=0.01,$"+'\n'+r"$A_{\rm{lens}}=1)$",
               r"$(r=0.01,$"+'\n'+r"$A_{\rm{lens}}=0.5)$"]

# 0: (r=0,AL=1), 1: (r=0,AL=.5), 2: (r=.01,AL=1), 3: (r=.01,AL=.5)
for case in range(4):
    idx = case
    plt.errorbar(case-0.225, mean_r_cl_fiducial[idx], yerr=mean_std_r_cl_fiducial[idx], fmt='r.')
    plt.errorbar(case-0.075, mean_r_map_based[idx], yerr=mean_std_r_map_based[idx], fmt='g.')
    plt.errorbar(case+0.075, mean_r_nilc[idx], yerr=mean_std_r_nilc[idx], fmt='b.')
    plt.errorbar(case+0.225, mean_r_cl_moments[idx], yerr=mean_std_r_cl_moments[idx], fmt='y.')

plt.xticks([0,1,2,3], case_labels, rotation=45, ha="center")
line_cl_fiducial = Line2D([0], [0], label='CL-fiducial', color='r')
line_map_based = Line2D([0], [0], label='map-based', color='g')
line_nilc = Line2D([0], [0], label='NILC', color='b')
line_cl_moments = Line2D([0], [0], label='CL-moments', color='y')

handles, labels = plt.gca().get_legend_handles_labels()
handles.extend([line_cl_fiducial, line_map_based, line_nilc, line_cl_moments])
plt.ylabel(r'$r$')
plt.legend(handles=handles, loc='upper left')
plt.savefig('r_extra.pdf', bbox_inches='tight')

###
# 4: Make LaTeX table to paste into paper draft 
print(" ")
print(" ")
stout = "\\begin{table*}\n\centering\n\\begin{tabular}{|l|c|c|c|c|}\n"
stout += "\hline\n"
stout += "\multicolumn{5}{|c|}{$10^3\\times(r\pm\sigma(r))$}\\\\\n"
stout += "\hline\n"
stout += "Input CMB & Pipeline A & $+$ moments & Pipeline B & Pipeline C\\\\\n"
stout += "\hline\n"
for case in range(4):
    idx = case
    st = case_labels[idx] + " & "
    st += " $%.1lf \pm %.1lf$ & " % (mean_r_cl_fiducial[idx]*1E3, mean_std_r_cl_fiducial[idx]*1E3)
    st += " $%.1lf \pm %.1lf$ & " % (mean_r_cl_moments[idx]*1E3, mean_std_r_cl_moments[idx]*1E3)
    st += " $%.1lf \pm %.1lf$ & " % (mean_r_map_based[idx]*1E3, mean_std_r_map_based[idx]*1E3)
    st += " $%.1lf \pm %.1lf$ \\\\\n " % (mean_r_nilc[idx]*1E3, mean_std_r_nilc[idx]*1E3)
    stout += st
stout += "\hline\n"
stout += "\\end{tabular}\n"
stout += "\caption{\lipsum[5]}\label{tab:r_fiducial_results}\n"
stout += "\end{table*}\n"
print(stout)
print(" ")
print(" ")
