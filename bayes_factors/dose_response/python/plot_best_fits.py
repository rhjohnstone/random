import doseresponse as dr
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import cma
import itertools as it
import os


def sum_of_square_diffs(params, model):
    if model == 1:
        pic50 = params[0]
        hill = 1
    elif model == 2:
        pic50, hill = params
    predicted = dr.dose_response_model(concs,hill,dr.pic50_to_ic50(pic50))
    return np.sum((responses-predicted)**2)


model = 2
dr.define_model(model)

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

def do_plot(drug_channel):

    drug, channel = drug_channel
    num_expts, experiment_numbers, experiments = dr.load_crumb_data(drug, channel)
    figs_dir = dr.drug_channel_figs_dir(drug, channel)

    concs = np.array([])
    responses = np.array([])
    for i in xrange(num_expts):
        concs = np.concatenate((concs, experiments[i][:, 0]))
        responses = np.concatenate((responses, experiments[i][:, 1]))

    x0 = np.ones(2)
    sigma0 = 0.1
    opts = cma.CMAOptions()
    es = cma.CMAEvolutionStrategy(x0, sigma0, opts)
    while not es.stop():
        X = es.ask()
        f_vals = [sum_of_square_diffs(x, model) for x in X]
        es.tell(X, f_vals)
        es.disp()
    res = es.result()
    pic50, hill = res[0]
    if model == 1:
        hill = 1

    conc_min = np.min(concs)
    conc_max = np.max(concs)

    num_pts = 201
    x_range = np.logspace(int(np.log10(conc_min))-1, int(np.log10(conc_max))+2, num_pts)
    predicted = dr.dose_response_model(x_range, hill, dr.pic50_to_ic50(pic50))

    fsize = 14

    fig = plt.figure(figsize=(5,4))
    ax = fig.add_subplot(111)
    ax.grid()
    ax.set_xscale('log')
    ax.set_ylabel(r"% {} block".format(channel),fontsize=fsize)
    ax.set_xlabel(r"{} concentration ($\mu$M)".format(drug),fontsize=fsize)
    ax.plot(x_range, predicted, color='blue', lw=2, label="Best fit")
    ax.plot(concs, responses, 'o', color='orange', ms=10, label="Expt data")
    ax.legend(loc=2)
    ax.set_title("Model {}, pIC50 = {}, Hill = {}".format(model, round(pic50,3), round(hill,3)),fontsize=fsize)
    fig.tight_layout()
    fig.savefig(figs_dir+"{}_{}_model_{}_best_fit.png".format(drug,channel,model))
    fig.savefig(all_figs_dir+"{}_{}_model_{}_best_fit.png".format(drug,channel,model))
    #fig.savefig(figs_dir+"{}_{}_model_{}_best_fit.pdf".format(drug,channel,model))
    plt.close()

for drug_channel in it.product(drugs_to_run, channels_to_run):
    try:
        do_plot(drug_channel)
    except:
        print "can't do", drug_channel
