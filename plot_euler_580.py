import matplotlib.pyplot as plt

from scipy import stats
import numpy as np

x = [10**p for p in xrange(6,12)]
y = [232710,2327192,23272089,232721183,2327212928,23272130893]

slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)

print intercept, slope

fig = plt.figure()
ax = fig.add_subplot(111)
ax.grid()
ax.set_xscale('log')
ax.set_yscale('log')
ax.plot(x,y)
plt.show(block=True)
