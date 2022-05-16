import numpy as np
import matplotlib.pyplot as plt

#####
# 1: include a quick description of what this script generates
#
# Simple BB power spectrum plot to serve as an example 


####
# 2: Read data
l, _, _, dlbb, _ = np.loadtxt("data/camb_example.dat", unpack=True)


###
# 3: Make plot. This is the part that the designated plotter will tweak.
# The simpler the better.
plt.figure()
plt.plot(l, dlbb, 'k-', label='BB')
plt.xlabel(r'$\ell$', fontsize=15)
plt.ylabel(r'$D_\ell$', fontsize=15)
plt.loglog()
plt.legend(loc='upper left')
plt.savefig('example.pdf', bbox_inches='tight')
plt.show()

