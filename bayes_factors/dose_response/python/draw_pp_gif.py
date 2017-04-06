import doseresponse as dr
import numpy as np
#import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from glob import glob
import scipy.stats as st
import os

model = 2
dr.define_model(model)

drug = 'Amitriptyline'
channel = 'Cav1.2'

dir_of_chains = dr.chains_dir(model, drug, channel)
chains = glob(dir_of_chains+"*.txt")
temps = [float(c.split("_")[-2]) for c in chains]
temps.sort()

figs_dir = dr.define_figs_dir(model, drug, channel)

gif_figs = []
gif_axs = []


figs = []
axs = []
#for i in xrange(num_params):
    #figs.append(plt.figure())
    #axs.append(figs[i].add_subplot(111))

fig, ax = plt.subplots()
fig.set_tight_layout(True)


def update_hist(num, data):
    ax.cla()
    ax.hist(data[num], normed=True, color='blue', edgecolor='blue', bins=40, label="t = {}".format(round(temps[num], 3)))
    #ax.plot(prior_xs[0], prior_pdfs[0], color='red', label="Prior")
    ax.set_xlabel(dr.labels[0])
    ax.set_ylabel("Approximate marginal power posterior")
    ax.set_xlim(4, 8)
    ax.set_ylim(0, 10)
    ax.legend()

data = []
for t in temps:
    chain = np.loadtxt(dr.define_chain_file(model, drug, channel, t), usecols=[0])
    data.append(chain)

data_min = np.min(np.array(data))
data_max = np.max(np.array(data))

ax.hist(data[0], normed=True, color='blue', edgecolor='blue', bins=40, label="t = {}".format(round(temps[0], 3)))
#ax.plot(prior_xs[0], prior_pdfs[0], color='red', label="Prior")
ax.set_xlabel(dr.labels[0])
ax.set_ylabel("Approximate marginal power posterior")
ax.set_xlim(4, 8)
ax.set_ylim(0, 10)
ax.legend()

animation = FuncAnimation(fig, update_hist, len(temps), fargs=(data, ))
plt.show()


"""for i in xrange(num_params):
    axs[i].plot(prior_xs[i], prior_pdfs[i], color='red', label="Prior")
    axs[i].legend()
    axs[i].set_ylabel("Approximate power posterior")
    axs[i].set_xlabel(labels[i])
    figs[i].tight_layout()"""

#plt.close()
