import doseresponse as dr
import numpy as np
from glob import glob
import itertools as it

num_models = 2
model_pairs = it.combinations(range(1, num_models+1), r=2)
expectations = {}

data_file = "../input/crumb_data.csv"
#run_all = True

dr.setup(data_file)
#drugs_to_run, channels_to_run = dr.list_drug_channel_options(run_all)

drug = "Amiodarone"
channel = "hERG"
num_expts, experiment_numbers, experiments = dr.load_crumb_data(drug, channel)

concs = np.array([])
responses = np.array([])
for i in xrange(num_expts):
    concs = np.concatenate((concs, experiments[i][:, 0]))
    responses = np.concatenate((responses, experiments[i][:, 1]))

pi_bit = dr.compute_pi_bit_of_log_likelihood(responses)
num_pts = len(responses)
for m in xrange(1, num_models+1):
    dr.define_model(m)
    chain_dir = dr.chains_dir(m)
    chains = np.array(glob(chain_dir+"*_chain.txt"))
    temps = np.array([float(c.split("_")[-2]) for c in chains])
    ordered_indices = np.argsort(temps)
    temps = temps[ordered_indices]
    chains = chains[ordered_indices]
    num_temps = len(temps)
    log_p_ys = np.zeros(num_temps)
    for i in xrange(num_temps):
        chain = np.loadtxt(chains[i], usecols=range(dr.num_params))
        num_its = chain.shape[0]
        total = 0.
        for it in xrange(num_its):
            temperature = 1  # approximating full likelihood
            total += dr.log_data_likelihood(responses, concs, chain[it, :], num_pts, temperature, pi_bit)
        log_p_ys[i] = total / num_its
    expectations[m] = dr.trapezium_rule(temps, log_p_ys)

for pair in model_pairs:
    i, j = pair
    Bij = np.exp(expectations[i]-expectations[j])
    print "B_{}{} = {}".format(i, j, Bij)
    print "B_{}{} = {}".format(j, i, 1./Bij)
