import os
import pandas as pd
import numpy as np

alpha = 1.
beta = 5.
mu = 6.
s = 0.15
sigma_lower = 0.
sigma_upper = 1000.


def chains_dir(model, drug, channel):
    temp_dir = "../output/{}/{}/model_{}/chains/".format(drug, channel, model)
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    return temp_dir


def define_chain_file(model, drug, channel, temperature):
    chain_file = chains_dir(model, drug, channel) + '{}_{}_model_{}_temp_{}_chain.txt'.format(drug, channel, model, temperature)
    return chain_file


def define_figs_dir(model, drug, channel):
    temp_dir = "../output/{}/{}/model_{}/figs/".format(drug, channel, model)
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    return temp_dir


def compute_pi_bit_of_log_likelihood(y):
    num_pts = len(y)
    return 0.5 * num_pts * np.log(2 * np.pi)


def dose_response_model(dose, hill, ic50):
    return 100. * (1. - 1. / (1. + (1. * dose / ic50) ** hill))


def pic50_to_ic50(pic50):  # IC50 in uM
    return 10 ** (6 - pic50)


def ic50_to_pic50(ic50):  # IC50 in uM
    return 6 - np.log10(ic50)


def log_data_likelihood_model_1(y, concs, params, num_pts, t, pi_bit):
    """
    Compute log likelihood of data.
    Note that pi_bit is a constant, so is not needed for MH, but when we're approximating log(p(y)), we need to include it.
    Of course, we could just add it on after, but I just left it there so I can reuse the exact same code.
    """
    pic50, sigma_sq = params
    predicted_responses = dose_response_model(concs, 1, pic50_to_ic50(pic50))
    #if sigma_sq <= 0:
    #    print params
    temp_1 = 0.5 * num_pts * np.log(sigma_sq)
    temp_2 = np.sum((y-predicted_responses)**2/(2.*sigma_sq))
    return -t * (pi_bit + temp_1 + temp_2)


def log_data_likelihood_model_2(y, concs, params, num_pts, t, pi_bit):
    """
    Compute log likelihood of data.
    Note that pi_bit is a constant, so is not needed for MH, but when we're approximating log(p(y)), we need to include it.
    Of course, we could just add it on after, but I just left it there so I can reuse the exact same code.
    """
    pic50, hill, sigma_sq = params
    predicted_responses = dose_response_model(concs, hill, pic50_to_ic50(pic50))
    #if sigma_sq <= 0:
    #    print params
    temp_1 = 0.5 * num_pts * np.log(sigma_sq)
    temp_2 = np.sum((y-predicted_responses)**2/(2.*sigma_sq))
    return -t * (pi_bit + temp_1 + temp_2)


def setup(given_file):
    global file_name, dir_name, df, drugs, channels
    file_name = given_file
    dir_name = given_file.split('/')[-1][:-4]
    df = pd.read_csv(file_name, names=['Drug', 'Channel', 'Experiment', 'Concentration', 'Inhibition'], skiprows=1)
    drugs = df.Drug.unique()
    channels = df.Channel.unique()


def list_drug_channel_options(args_all):
    if not args_all:
        print "\nDrugs:\n"
        for i in range(len(drugs)):
            print "{}. {}".format(i+1,drugs[i])
        drug_indices = [x-1 for x in map(int,raw_input("\nSelect drug numbers: ").split())]
        assert(0 <= len(drug_indices) <= len(drugs))
        drugs_to_run = [drugs[drug_index] for drug_index in drug_indices]
        print "\nChannels:\n"
        for i in range(len(channels)):
            print "{}. {}".format(i+1,channels[i])
        channel_indices = [x-1 for x in map(int,raw_input("\nSelect channel numbers: ").split())]
        assert(0 <= len(channel_indices) <= len(channels))
        channels_to_run = [channels[channel_index] for channel_index in channel_indices]
    else:
        drugs_to_run = drugs
        channels_to_run = channels
    return drugs_to_run, channels_to_run


def load_crumb_data(drug,channel):
    experiment_numbers = np.array(df[(df['Drug'] == drug) & (df['Channel'] == channel)].Experiment.unique())
    num_expts = max(experiment_numbers)
    experiments = []
    for expt in experiment_numbers:
        experiments.append(np.array(df[(df['Drug'] == drug) & (df['Channel'] == channel) & (df['Experiment'] == expt)][['Concentration','Inhibition']]))
    experiment_numbers -= 1
    return num_expts, experiment_numbers, experiments
    
    
def define_model(model):
    """Choose whether to fix Hill = 1 (#1) or allow Hill to vary (#2)"""
    global log_data_likelihood, log_priors, num_params, file_names, labels
    if model == 1:
        num_params = 2
        log_data_likelihood = log_data_likelihood_model_1
        log_priors = log_priors_model_1
        file_names = ["pic50", "sigma_sq"]
        labels = [r"$PIC_{50}$", r"$\sigma^2$"]
    elif model == 2:
        num_params = 3
        log_data_likelihood = log_data_likelihood_model_2
        log_priors = log_priors_model_2
        file_names = ["pic50", "hill", "sigma_sq"]
        labels = [r"$PIC_{50}$", r"$Hill", r"$\sigma^2$"]
    #theta0 = np.ones(num_params-1)


def log_hill_log_logistic_likelihood(x):
    return (beta-1.)*np.log(x) - 2.*np.log(1.+(x/alpha)**beta)


def log_pic50_logistic_likelihood(x):
    return -x/s - 2.*np.log(1 + np.exp((mu-x)/s))


def log_priors_model_1(params):
    pic50, sigma_sq = params
    if sigma_sq <= sigma_lower or sigma_sq > sigma_upper:
        return -np.inf
    else:
        return log_pic50_logistic_likelihood(pic50)


def log_priors_model_2(params):
    pic50, hill, sigma_sq = params
    if sigma_sq <= sigma_lower or sigma_sq > sigma_upper:
        return -np.inf
    else:
        return log_hill_log_logistic_likelihood(hill) + log_pic50_logistic_likelihood(pic50)


def log_target(y, concs, params, num_pts, t, pi_bit):
    return log_data_likelihood(y, concs, params, num_pts, t, pi_bit) + log_priors(params)


def trapezium_rule(x, y):
    return 0.5 * np.sum((x[1:]-x[:-1]) * (y[1:]+y[:-1]))
