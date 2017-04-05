import doseresponse as dr
import argparse
import numpy as np
import sys
import numpy.random as npr
import matplotlib.pyplot as plt
import scipy.stats as st


def do_mcmc(temperature):#, theta0):
    print "Starting chain"

    #theta_cur = np.copy(theta0)
    theta_cur = np.ones(dr.num_params)
    log_target_cur = dr.log_target(responses, concs, theta_cur, num_pts, temperature, pi_bit)

    total_iterations = 20000
    thinning = 5
    num_saved = total_iterations / thinning + 1
    burn = num_saved / 4

    chain = np.zeros((num_saved, dr.num_params+1))
    chain[0, :] = np.concatenate((theta_cur, [log_target_cur]))

    loga = 0.
    acceptance = 0.

    mean_estimate = np.copy(theta_cur)
    cov_estimate = np.eye(dr.num_params)

    status_when = 5000
    adapt_when = 1000*dr.num_params

    t = 1
    s = 1
    while t <= total_iterations:
        theta_star = npr.multivariate_normal(theta_cur, np.exp(loga)*cov_estimate)
        """try:
            theta_star = npr.multivariate_normal(theta_cur, np.exp(loga)*cov_estimate)
        except Warning as e:
            print str(e)
            print "Iteration:", t
            print "temperature:", temperature
            print "theta_cur:", theta_cur
            print "loga:", loga
            print "cov_estimate:", cov_estimate
            sys.exit()"""
        log_target_star = dr.log_target(responses, concs, theta_star, num_pts, temperature, pi_bit)
        u = npr.rand()
        if np.log(u) < log_target_star - log_target_cur:
            accepted = 1
            theta_cur = theta_star
            log_target_cur = log_target_star
        else:
            accepted = 0
        acceptance = (t-1.)/t * acceptance + 1./t * accepted
        if t % thinning == 0:
            chain[t/thinning,:] = np.concatenate((theta_cur, [log_target_cur]))
        if t % status_when == 0:
            #pass
            print t/status_when, "/", total_iterations/status_when
            print "acceptance =", acceptance
        if t == adapt_when:
            mean_estimate = np.copy(theta_cur)
        if t > adapt_when:
            gamma_s = 1./(s+1.)**0.6
            temp_covariance_bit = np.array([theta_cur-mean_estimate])
            cov_estimate = (1-gamma_s) * cov_estimate + gamma_s * np.dot(np.transpose(temp_covariance_bit),temp_covariance_bit)
            mean_estimate = (1-gamma_s) * mean_estimate + gamma_s * theta_cur
            loga += gamma_s*(accepted-0.25)
            s += 1
        t += 1
    # discard burn-in before saving chain, just to save space mostly
    return chain[burn:, :]


"""parser = argparse.ArgumentParser()
requiredNamed = parser.add_argument_group('required arguments')
requiredNamed.add_argument("--data-file", type=str, help="csv file from which to read in data, in same format as provided crumb_data.csv", required=True)
parser.add_argument("-a", "--all", action='store_true', help='run hierarchical MCMC on all drugs and channels', default=False)
args = parser.parse_args()"""#

data_file = "../input/crumb_data.csv"
#run_all = False

dr.setup(data_file)
#drugs_to_run, channels_to_run = dr.list_drug_channel_options(run_all)

drug = "Amitriptyline"
channel = "Cav1.2"
num_expts, experiment_numbers, experiments = dr.load_crumb_data(drug, channel)

concs = np.array([])
responses = np.array([])
for i in xrange(num_expts):
    concs = np.concatenate((concs, experiments[i][:, 0]))
    responses = np.concatenate((responses, experiments[i][:, 1]))

num_pts = len(responses)
pi_bit = dr.compute_pi_bit_of_log_likelihood(responses)

#model = 2  #int(sys.argv[1])

n = 2
c = 5
temperatures = (np.arange(n+1.)/n)**c

num_models = 2
for model in xrange(1,num_models+1):

    dr.define_model(model)

#prior_x = np.linspace(0,2,1001)
#prior_pdf = st.logistic.pdf(prior_x, loc=dr.mu, scale=dr.s)
#prior_pdf = st.fisk.pdf(prior_x, c=dr.beta, scale=dr.alpha, loc=0)

    for temperature in temperatures:
        chain_file = dr.define_chain_file(model, drug, channel, temperature)
        chain = do_mcmc(temperature)
        np.savetxt(chain_file, chain)

"""fig = plt.figure()
ax = fig.add_subplot(111)
ax.hist(chain[:,1],color='blue',edgecolor='blue',normed=True,bins=40,label="t = {}".format(temperature))
ax.plot(prior_x,prior_pdf,color='red',label='Prior',lw=2)
ax.legend()
plt.show()"""
