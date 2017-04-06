import doseresponse as dr
import numpy as np
import numpy.random as npr
import matplotlib.pyplot as plt

data_file = "../input/crumb_data.csv"
dr.setup(data_file)

temperature = 1.0  # sampling from full posterior

model = 2

dr.define_model(model)
#drug = "Amiodarone"
#channel = "hERG"
drug = "Amitriptyline"
channel = "Cav1.2"
chain_file = dr.define_chain_file(model, drug, channel, temperature)

num_expts, experiment_numbers, experiments = dr.load_crumb_data(drug, channel)
figs_dir = dr.drug_channel_figs_dir(drug, channel)

concs = np.array([])
responses = np.array([])
for i in xrange(num_expts):
    concs = np.concatenate((concs, experiments[i][:, 0]))
    responses = np.concatenate((responses, experiments[i][:, 1]))

how_many_samples_to_plot = 2000

mcmc_samples = np.loadtxt(chain_file, usecols=range(dr.num_params))
saved_its = mcmc_samples.shape[0]
sample_indices = npr.randint(0, saved_its, how_many_samples_to_plot)

mcmc_samples = mcmc_samples[sample_indices]

conc_min = np.min(concs)
conc_max = np.max(concs)

fsize = 14

num_pts = 101
x_range = np.logspace(int(np.log10(conc_min))-1, int(np.log10(conc_max))+2, num_pts)

fig = plt.figure(figsize=(5,4))
ax = fig.add_subplot(111)
ax.set_xscale('log')
ax.grid()
ax.set_ylabel(r"% {} block".format(channel), fontsize=fsize)
ax.set_xlabel(r"{} concentration ($\mu$M)".format(drug), fontsize=fsize)

for i in xrange(how_many_samples_to_plot):
    if model == 1:
        pic50 = mcmc_samples[i,0]
        hill = 1
        title = "Model 1, fixed $Hill=1$, varying $pIC50$"
    elif model == 2:
        pic50, hill = mcmc_samples[i,:2]
        title = "Model 2, varying $pIC50$ and $Hill$"
    ax.plot(x_range, dr.dose_response_model(x_range, hill, dr.pic50_to_ic50(pic50)),color='black',alpha=0.01)
ax.plot(concs, responses, 'o', color='orange', ms=10, label="Expt data")
ax.set_title(title, fontsize = fsize)
ax.legend(loc=2)
fig.tight_layout()
fig.savefig(figs_dir+'{}_{}_model_{}_mcmc_samples.png'.format(drug,channel,model))
fig.savefig(figs_dir+'{}_{}_model_{}_mcmc_samples.pdf'.format(drug,channel,model))
plt.close()
