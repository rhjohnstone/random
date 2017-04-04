import numpy as np
#import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
from glob import glob
import scipy.stats as st
import os


def chains_dir(model):
    return "output_chains/model_{}/".format(model)


def chain_file(model, temperature):
    main_dir = chains_dir(model)
    return main_dir + 'model_{}_temp_{}_chain.txt'.format(model, temperature)


def define_figs_dir(model):
    temp_dir = "output/model_{}/figs/".format(model)
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    return temp_dir


num_params = 3

model = 1

if model == 1:
    file_names = ["alpha", "beta", "sigma_sq"]
    labels = [r"$\alpha$", r"$\beta$", r"$\sigma^2$", "log-target"]
elif model == 2:
    file_names = ["gamma$", "delta$", "tau_sq"]
    labels = [r"$\gamma$", r"$\delta$", r"$\tau^2$", "log-target"]
else:
    sys.exit("Illegal model number\n")

dir_of_chains = chains_dir(model)
chains = glob(dir_of_chains+"*.txt")
temps = [float(c.split("_")[5]) for c in chains]
temps.sort()

params_mean = np.array([3000, 185]) # same for both models
params_vars = np.array([10**6, 10**4]) # independent, so not bothering with covariance matrix

a = 3.
b = 1./(2*300**2)

prior_xs = [np.linspace(-2000, 7000, 1001), np.linspace(-200, 600, 1001), np.linspace(190, 700000, 10001)]
prior_pdfs = [st.norm.pdf(prior_xs[0], params_mean[0], np.sqrt(params_vars[0])),
              st.norm.pdf(prior_xs[1], params_mean[1], np.sqrt(params_vars[1])),
              st.invgamma.pdf(prior_xs[2], a=a, scale=1./b)]

figs_dir = define_figs_dir(model)

figs = []
axs = []
for i in xrange(num_params):
    figs.append(plt.figure())
    axs.append(figs[i].add_subplot(111))

for t in temps:
    chain = np.loadtxt(chain_file(model, t), usecols=range(num_params))
    for i in xrange(num_params):
        axs[i].hist(chain[:, i], normed=True, edgecolor=None, bins=40, alpha=0.3, label="t = {}".format(round(t, 3)))
for i in xrange(num_params):
    axs[i].plot(prior_xs[i], prior_pdfs[i], color='red', label="Prior")
    axs[i].legend()
    axs[i].set_ylabel("Approximate power posterior")
    axs[i].set_xlabel(labels[i])
    figs[i].tight_layout()
    figs[i].savefig(figs_dir+"power_posterior_"+file_names[i]+".png")

plt.close()
