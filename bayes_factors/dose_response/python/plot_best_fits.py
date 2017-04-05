import doseresponse as dr
#import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import cma

def sum_of_square_diffs(params):
    predicted = dr.dose_response_model(concs,params[1],dr.pic50_to_ic50(params[0]))
    return np.sum((responses-predicted)**2)

data_file = "../input/crumb_data.csv"
dr.setup(data_file)

drug = "Amitriptyline"
channel = "Cav1.2"
num_expts, experiment_numbers, experiments = dr.load_crumb_data(drug, channel)

concs = np.array([])
responses = np.array([])
for i in xrange(num_expts):
    concs = np.concatenate((concs, experiments[i][:, 0]))
    responses = np.concatenate((responses, experiments[i][:, 1]))

num_params = 2
x0 = np.ones(num_params)
sigma0 = 0.1
opts = cma.CMAOptions()
es = cma.CMAEvolutionStrategy(x0, sigma0, opts)
while not es.stop():
    X = es.ask()
    f_vals = [sum_of_square_diffs(x) for x in X]
    es.tell(X, f_vals)
    es.disp()
res = es.result()
pic50, hill = res[0]

conc_min = np.min(concs)
conc_max = np.max(concs)

num_pts = 1001
x_range = np.logspace(int(np.log10(conc_min))-1, int(np.log10(conc_max))+1, num_pts)
predicted = dr.dose_response_model(x_range, hill, dr.pic50_to_ic50(pic50))

fig = plt.figure()
ax = fig.add_subplot(111)
ax.grid()
ax.set_xscale('log')
ax.set_ylabel(r"% {} block".format(channel))
ax.set_xlabel(r"{} concentration ($\mu$M)".format(drug))
ax.plot(x_range, predicted, color='blue', lw=2, label="Best fit")
ax.plot(concs, responses, 'o', color='orange', ms=10, label="Expt data")
ax.legend(loc=2)
ax.set_title("pIC50 = {}, Hill = {}".format(round(pic50,3), round(hill,3)))
fig.tight_layout()
plt.show(block=True)
