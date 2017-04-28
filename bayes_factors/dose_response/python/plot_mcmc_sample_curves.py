import doseresponse as dr
import numpy as np
import numpy.random as npr
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import itertools as it
import multiprocessing as mp


all_figs_dir = "../output/all_mcmc_samples/"
if not os.path.exists(all_figs_dir):
    os.makedirs(all_figs_dir)


data_file = "../input/crumb_data.csv"
run_all = True
dr.setup(data_file)
drugs_to_run, channels_to_run = dr.list_drug_channel_options(run_all)

temperature = 1.0  # sampling from full posterior


def plot_mcmc_samples(drug_channel):
    drug, channel = drug_channel

    fig = plt.figure(figsize=(5, 10))
    axes = {}
    axes[1] = fig.add_subplot(211)
    axes[2] = fig.add_subplot(212)

    #drug = "Amiodarone"
    #channel = "hERG"
    # drug = "Lopinavir"
    # channel = "Kir2.1"

    num_models = 2
    for model in xrange(1, num_models+1):

        dr.define_model(model)

        chain_file = dr.define_chain_file(model, drug, channel, temperature)

        num_expts, experiment_numbers, experiments = dr.load_crumb_data(drug, channel)
        figs_dir = dr.drug_channel_figs_dir(drug, channel)

        concs = np.array([])
        responses = np.array([])
        for i in xrange(num_expts):
            concs = np.concatenate((concs, experiments[i][:, 0]))
            responses = np.concatenate((responses, experiments[i][:, 1]))

        how_many_samples_to_plot = 1200

        mcmc_samples = np.loadtxt(chain_file, usecols=range(dr.num_params))
        saved_its = mcmc_samples.shape[0]
        sample_indices = npr.randint(0, saved_its, how_many_samples_to_plot)

        mcmc_samples = mcmc_samples[sample_indices]

        conc_min = np.min(concs)
        conc_max = np.max(concs)

        fsize = 14

        num_pts = 101
        x_range = np.logspace(int(np.log10(conc_min))-1, int(np.log10(conc_max))+2, num_pts)


        axes[model].set_xscale('log')
        axes[model].grid()
        axes[model].set_ylabel(r"% {} block".format(channel), fontsize=fsize)
        axes[model].set_xlabel(r"{} concentration ($\mu$M)".format(drug), fontsize=fsize)
        axes[model].set_ylim(0,100)

        for i in xrange(how_many_samples_to_plot):
            if model == 1:
                pic50 = mcmc_samples[i,0]
                hill = 1
                title = "$M_1$, fixed $Hill=1$, varying $pIC50$"
            elif model == 2:
                pic50, hill = mcmc_samples[i,:2]
                title = "$M_2$, varying $pIC50$ and $Hill$"
            axes[model].plot(x_range, dr.dose_response_model(x_range, hill, dr.pic50_to_ic50(pic50)),color='black',alpha=0.01)
        axes[model].plot(concs, responses, 'o', color='orange', ms=10, label="Expt data")
        axes[model].set_title(title, fontsize = fsize)
        axes[model].legend(loc=2)
    #axes[2].set_yticklabels([])
    fig.tight_layout()
    fig.savefig(all_figs_dir+'{}_{}_mcmc_samples.png'.format(drug, channel))
    fig.savefig(figs_dir+'{}_{}_mcmc_samples.pdf'.format(drug,channel,model))
    plt.close()
    return None


def try_and_plot(drug_channel):
    try:
        return plot_mcmc_samples(drug_channel)
    except:
        print "Can't plot for", drug_channel
        return None

drugs_channels = [('Amiodarone', 'hERG'), ('Amitriptyline', 'Cav1.2')]
#drugs_channels = it.product(drugs_to_run, channels_to_run)

"""for drug_channel in drugs_channels:
    try:
        plot_mcmc_samples(drug_channel)
    except:
        print "can't plot mcmc samples for", drug_channel"""

num_processes = 2
pool = mp.Pool(num_processes)
results = pool.map(try_and_plot, drugs_channels)
pool.close()
pool.join()

