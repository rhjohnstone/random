import doseresponse as dr
#import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import cma
import itertools as it
import os

hill_lower = 0
pic50_lower = -3

def sum_of_square_diffs(params, model):
    if model == 1:
        pic50 = params[0]
        hill = 1
    elif model == 2:
        pic50, hill = params
    if hill <= hill_lower or pic50 <= pic50_lower:
        return 1e9
    else:
        predicted = dr.dose_response_model(concs, hill, dr.pic50_to_ic50(pic50))
        return np.sum((responses-predicted)**2)




data_file = "../input/crumb_data.csv"
run_all = True

dr.setup(data_file)
drugs_to_run, channels_to_run = dr.list_drug_channel_options(run_all)

all_figs_dir = "../output/all_best_fits/"
if not os.path.exists(all_figs_dir):
    os.makedirs(all_figs_dir)

#drug = "Amitriptyline"
#channel = "Cav1.2"
#drug = "Amiodarone"
#channel = "hERG"

num_models = 2


def do_plot(drug_channel):
    global concs, responses

    fig = plt.figure(figsize=(10, 4))
    axes = {}
    axes[1] = fig.add_subplot(121)
    axes[2] = fig.add_subplot(122)#, sharey=axes[1])

    fsize = 14

    for model in xrange(1, num_models+1):

        dr.define_model(model)

        drug, channel = drug_channel
        num_expts, experiment_numbers, experiments = dr.load_crumb_data(drug, channel)
        figs_dir = dr.drug_channel_figs_dir(drug, channel)

        concs = np.array([])
        responses = np.array([])
        for i in xrange(num_expts):
            concs = np.concatenate((concs, experiments[i][:, 0]))
            responses = np.concatenate((responses, experiments[i][:, 1]))

        if model == 1:
            x0 = np.ones(2)
            sigma0 = 0.1
        elif model == 2:
            x0 = np.copy([pic50, hill])
            sigma0 = 0.01
        #x0[0] = 6.9

        opts = cma.CMAOptions()
        es = cma.CMAEvolutionStrategy(x0, sigma0, opts)
        while not es.stop():
            X = es.ask()
            f_vals = [sum_of_square_diffs(x, model) for x in X]
            es.tell(X, f_vals)
            es.disp()
        res = es.result()
        ss = res[1]
        pic50, hill = res[0]
        if model == 1:
            hill = 1

        conc_min = np.min(concs)
        conc_max = np.max(concs)

        num_pts = 501
        x_range = np.logspace(int(np.log10(conc_min))-1, int(np.log10(conc_max))+2, num_pts)
        predicted = dr.dose_response_model(x_range, hill, dr.pic50_to_ic50(pic50))



        #fig = plt.figure(figsize=(5,4))
        #ax = fig.add_subplot(111)
        axes[model].grid()
        axes[model].set_xscale('log')
        axes[model].set_ylim(0,100)
        if model == 1:
            axes[model].set_ylabel(r"% {} block".format(channel),fontsize=fsize)
        axes[model].set_xlabel(r"{} concentration ($\mu$M)".format(drug),fontsize=fsize)
        axes[model].plot(x_range, predicted, color='blue', lw=2, label="Best fit")
        axes[model].plot(concs, responses, 'o', color='orange', ms=10, label="Expt data")
        axes[model].legend(loc=2)
        axes[model].set_title("$M_{}, pIC50 = {}, Hill = {}, SS = {}$".format(model, round(pic50,2), round(hill,2), round(ss,2)),fontsize=fsize)
    axes[2].set_yticklabels([])
    fig.tight_layout()
    #fig.savefig(figs_dir+"{}_{}_model_{}_best_fit.png".format(drug,channel,model))
    fig.savefig(all_figs_dir+"{}_{}_best_fits.png".format(drug, channel))
    #fig.savefig(figs_dir+"{}_{}_model_{}_best_fit.pdf".format(drug,channel,model))
    plt.close()

for drug_channel in it.product(drugs_to_run, channels_to_run):
    try:
        do_plot(drug_channel)
    except:
        print "can't do", drug_channel

#do_plot(("Amiodarone", "Cav1.2"))
