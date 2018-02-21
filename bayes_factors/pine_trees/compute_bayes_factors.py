import pine_trees_setup as pt
import numpy as np
from glob import glob
import itertools as it

num_models = 2
model_pairs = it.combinations(range(1, num_models+1), r=2)
expectations = {}

num_params = 3
data = pt.load_pine_data()
y = data[:, 0]
num_pts = len(y)
for m in xrange(1, num_models+1):
    explan = data[:, m]
    explan_bar = np.mean(explan)
    pi_bit = pt.compute_pi_bit_of_log_likelihood(y)
    chain_dir = pt.chains_dir(m)
    chains = np.array(glob(chain_dir+"*_chain.txt"))
    temps = np.array([float(c.split("_")[-2]) for c in chains])
    ordered_indices = np.argsort(temps)
    temps = temps[ordered_indices]
    chains = chains[ordered_indices]
    num_temps = len(temps)
    log_p_ys = np.zeros(num_temps)
    for i in xrange(num_temps):
        chain = np.loadtxt(chains[i], usecols=range(num_params))
        num_its = chain.shape[0]
        total = 0.
        for it in xrange(num_its):
            total += pt.log_data_likelihood(y, explan, explan_bar, chain[it, :], num_pts, 1, pi_bit)
        log_p_ys[i] = total / num_its
    expectations[m] = pt.trapezium_rule(temps, log_p_ys)

for pair in model_pairs:
    i, j = pair
    Bij = np.exp(expectations[i]-expectations[j])
    print "B_{}{} = {}".format(i, j, Bij)
    print "B_{}{} = {}".format(j, i, 1./Bij)
