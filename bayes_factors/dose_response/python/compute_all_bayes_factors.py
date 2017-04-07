import doseresponse as dr
import numpy as np
import itertools as it

data_file = "../input/crumb_data.csv"
run_all = True

dr.setup(data_file)
drugs_to_run, channels_to_run = dr.list_drug_channel_options(run_all)

def compute_log_pys(drug_channel):
    global responses, concs, num_pts, pi_bit

    #print drug_channel

    drug, channel = drug_channel

    num_expts, experiment_numbers, experiments = dr.load_crumb_data(drug, channel)

    concs = np.array([])
    responses = np.array([])
    for i in xrange(num_expts):
        concs = np.concatenate((concs, experiments[i][:, 0]))
        responses = np.concatenate((responses, experiments[i][:, 1]))

    num_models = 2
    quads = {}

    for model in xrange(1, num_models+1):
        log_py_file = dr.define_log_py_file(model, drug, channel)

        temps_and_log_pys = np.loadtxt(log_py_file)
        temps = temps_and_log_pys[:,0]
        log_pys = temps_and_log_pys[:,1]
        quadrature = dr.trapezium_rule(temps, log_pys)
        quads[model] = quadrature

    B_21 = np.exp(quads[2]-quads[1])
    print "B_21 =", B_21
    print "B_12 =", 1./B_21

    return None

for drug_channel in it.product(drugs_to_run, channels_to_run):
    try:
        compute_log_pys(drug_channel)
    except:
        continue
        #print "no log_pys for", drug_channel