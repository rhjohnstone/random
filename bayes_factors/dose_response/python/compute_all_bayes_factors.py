import doseresponse as dr
import numpy as np
import itertools as it

data_file = "../input/crumb_data.csv"
run_all = True

dr.setup(data_file)
drugs_to_run, channels_to_run = dr.list_drug_channel_options(run_all)

output_dir = "../output/bayes_factors/"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
bf_file = output_dir + "bayes_factors.txt"
with open(bf_file, "w") as outfile:
    outfile.write("# Bayes factors\n")
    outfile.write("# M1. fixed Hill = 1, varying pIC50\n")
    outfile.write("# M2. varying pIC50 and Hill\n\n")

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
    B_12 = 1./B_21

    return B_21, B_12

for drug_channel in it.product(drugs_to_run, channels_to_run):
    try:
        print "\n"
        print drug_channel
        B_21, B_12 = compute_log_pys(drug_channel)
        with open(bf_file, "a") as outfile:
            outfile.write("{}\n".format(drug_channel))
            outfile.write("B_21 = {}\n".format(B_21))
            outfile.write("B_12 = {}\n\n".format(B_12))
        print "\n"
    except:
        print "no log_pys for", drug_channel
        continue

"""drug_channel = ('Amiodarone', 'hERG')
compute_log_pys(drug_channel)"""
