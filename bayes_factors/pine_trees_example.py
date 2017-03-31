import numpy as np
import numpy.random as npr
import matplotlib.pyplot as plt
import sys
import scipy.stats as st
import multiprocessing as mp
from time import time

from rpy2.robjects.packages import importr
# import R's "base" package
mcmcse = importr('mcmcse')
import rpy2.robjects.numpy2ri
rpy2.robjects.numpy2ri.activate()

start = time()

model = int(sys.argv[1])

seed = model
npr.seed(seed)


def log_data_likelihood(y, explan, explan_bar, params, num_pts, t, pi_bit):
    """
    compute log likelihood of data 
    """
    # type: (object, object, object, object, object, object) -> object
    if params[-1] <= 0:
        print params
    temp_1 = 0.5 * num_pts * np.log(params[-1])
    temp_2 = np.sum((y - params[0] - params[1] * (explan - explan_bar))**2) / (2. * params[-1])
    return -t * (pi_bit + temp_1 + temp_2)


def log_invgamma_prior(x, a, b):
    if x <= 0:
        return -np.inf
    else:
        return -1./(b*x) - (a+1.)*np.log(x)


def log_normal_prior(x, x_means, x_vars):
    return -np.sum((x-x_means)**2/(2*x_vars))


def log_target(params, y, explan, explan_bar, num_pts, a, b, params_means, params_vars, t):
    if params[-1] <= 0:
        return -np.inf
    else:
        return (log_data_likelihood(y, explan, explan_bar, params, num_pts, t, pi_bit)
                + log_normal_prior(params[:2], params_means, params_vars)
                + log_invgamma_prior(params[-1], a, b))


# (yi, xi, zi)
pine_data = np.array([[3040, 29.2, 25.4],
                      [2470, 24.7, 22.2],
                      [3610, 32.3, 32.2],
                      [3480, 31.3, 31.0],
                      [3810, 31.5, 30.9],
                      [2330, 24.5, 23.9],
                      [1800, 19.9, 19.2],
                      [3110, 27.3, 27.2],
                      [3160, 27.1, 26.3],
                      [2310, 24.0, 23.9],
                      [4360, 33.8, 33.2],
                      [1880, 21.5, 21.0],
                      [3670, 32.2, 29.0],
                      [1740, 22.5, 22.0],
                      [2250, 27.5, 23.8],
                      [2650, 25.6, 25.3],
                      [4970, 34.5, 34.2],
                      [2620, 26.2, 25.7],
                      [2900, 26.7, 26.4],
                      [1670, 21.1, 20.0],
                      [2540, 24.1, 23.9],
                      [3840, 30.7, 30.7],
                      [3800, 32.7, 32.6],
                      [4600, 32.6, 32.5],
                      [1900, 22.1, 20.8],
                      [2530, 25.3, 23.1],
                      [2920, 30.8, 29.8],
                      [4990, 38.9, 38.1],
                      [1670, 22.1, 21.3],
                      [3310, 29.2, 28.5],
                      [3450, 30.1, 29.2],
                      [3600, 31.4, 31.4],
                      [2850, 26.7, 25.9],
                      [1590, 22.1, 21.4],
                      [3770, 30.3, 29.8],
                      [3850, 32.0, 30.6],
                      [2480, 23.2, 22.6],
                      [3570, 30.3, 30.3],
                      [2620, 29.9, 23.8],
                      [1890, 20.8, 18.4],
                      [3030, 33.2, 29.4],
                      [3030, 28.2, 28.2]])

y = pine_data[:,0]

num_pts = len(y)
pi_bit = 0.5*num_pts*np.log(2*np.pi)

params_mean = np.array([3000, 185]) # same for both models
params_vars = np.array([10**6, 10**4]) # independent, so not bothering with covariance matrix
num_params = 3

a = 3
b = 1./(2*300**2)

#model = 2

if model == 1:
    explan = pine_data[:,1]
    labels = [r"$\alpha$", r"$\beta$", r"$\sigma^2$", "log-target"]
elif model == 2:
    explan = pine_data[:,2]
    labels = [r"$\gamma$", r"$\delta$", r"$\tau^2$", "log-target"]
else:
    sys.exit("Illegal model number\n")
explan_bar = np.mean(explan)


def approximate_log_likelihood(chain):
    end = chain.shape[0]
    burn = end/4
    log_likelihood_samples = np.zeros(end-burn)
    total = 0.
    for it in xrange(burn,end):
        log_likelihood_samples[it-burn] = log_data_likelihood(y, explan, explan_bar, chain[it, :num_params], num_pts, 1, pi_bit)
    log_likelihood_mcse = mcmcse.mcse(log_likelihood_samples, method="obm")
    se = log_likelihood_mcse[1][0]
    #print "se =", se
    return np.sum(log_likelihood_samples)/(end-burn), se


def do_mcmc(temperature):#, theta0):

    #print "Starting a chain"

    #theta_cur = np.copy(theta0)
    theta_cur = 100*np.ones(num_params)
    log_target_cur = log_target(theta_cur, y, explan, explan_bar, num_pts, a, b, params_mean, params_vars, temperature)

    total_iterations = 200000
    thinning = 5
    num_saved = total_iterations / thinning + 1
    burn = num_saved / 4

    chain = np.zeros((num_saved, num_params+1))
    chain[0,:] = np.concatenate((theta_cur,[log_target_cur]))

    proposal_cov = np.eye(num_params)
    loga = 0.
    acceptance = 0.

    cov_estimate = np.copy(proposal_cov)

    status_when = 1000
    adapt_when = 100*num_params

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
        log_target_star = log_target(theta_star, y, explan, explan_bar, num_pts, a, b, params_mean, params_vars, temperature)
        u = npr.rand()
        if np.log(u) < log_target_star - log_target_cur:
            accepted = 1
            theta_cur = theta_star
            log_target_cur = log_target_star
        else:
            accepted = 0
        acceptance = (t-1.)/t * acceptance + 1./t * accepted
        if t%thinning == 0:
            chain[t/thinning,:] = np.concatenate((theta_cur,[log_target_cur]))
        if t%status_when == 0:
            pass
            #print t/status_when, "/", total_iterations/status_when
            #print "acceptance =", acceptance
        if t==adapt_when:
            mean_estimate = np.copy(theta_cur)
        if t>adapt_when:
            gamma_s = 1./(s+1.)**0.6
            temp_covariance_bit = np.array([theta_cur-mean_estimate])
            cov_estimate = (1-gamma_s) * cov_estimate + gamma_s * np.dot(np.transpose(temp_covariance_bit),temp_covariance_bit)
            mean_estimate = (1-gamma_s) * mean_estimate + gamma_s * theta_cur
            loga += gamma_s*(accepted-0.25)
            s += 1
        t += 1
    return chain

"""marginal_figs = {}
marginal_axes = {}
for k in xrange(num_params):
    marginal_figs[k] = plt.figure()
    marginal_axes[k] = marginal_figs[k].add_subplot(111)"""


n = 30
c = 5
temperatures = (np.arange(n+1.)/n)**c


def log_approxn(temperature):
    chain_file = 'model_{}_chain_n_{}_c_{}_temp_{}.txt'.format(model, n, c, temperature)
    chain = do_mcmc(temperature)
    np.savetxt(chain_file,chain)
    end = chain.shape[0]
    burn = end/4
    #for j in xrange(num_params):
    #    marginal_axes[j].hist(chain[burn:,j],normed=True,alpha=0.3)
    approx_log_likelihood, se = approximate_log_likelihood(chain)
    return approx_log_likelihood, se





def log_model_likelihood():



    #theta0 = 10*np.ones(num_params)
    """log_approxns = np.zeros(n+1)

    for i in xrange(n+1):
        #temperatures[i] = ((1.*i)/n)**c
        chain = do_mcmc(temperatures[i])#,theta0)
        end = chain.shape[0]
        burn = end/4
        #theta0 = np.mean(chain[burn:,:num_params], axis=0)
        log_approxns[i] = approximate_log_likelihood(chain)"""

    num_cores = 1
    #pool = mp.Pool(num_cores)
    #log_approxns = np.array(pool.map_async(log_approxn,temperatures).get(9999))
    if num_cores==1:
        log_approxns = np.zeros(n+1)
        ses = np.zeros(n+1)
        for i in xrange(n+1):
            la, se = log_approxn(temperatures[i])
            log_approxns[i] = la
            ses[i] = se
    elif num_cores>1:
        pool = mp.Pool(num_cores)
        log_approxns_and_ses = np.array(pool.map_async(log_approxn,temperatures).get(9999))
        log_approxns = log_approxns_and_ses[:,0]
        ses = log_approxns_and_ses[:,1]

    print "ses:", ses
    print log_approxns
    total_se = 0.5 * np.sqrt((temperatures[1]-temperatures[0])**2 * ses[0]**2 +
                             np.sum((temperatures[2:]-temperatures[:-2])**2 * ses[1:-1]**2) +
                             (temperatures[-1]-temperatures[-2])**2 * ses[-1]**2)


    #print log_approxns

    integral_approxn = 0.5*np.sum((temperatures[1:]-temperatures[:-1])*(log_approxns[1:]+log_approxns[:-1]))
    return integral_approxn, total_se


integral_approxn, total_se = log_model_likelihood()
print "\nlog(B{}) is approx".format(model), integral_approxn, "\n"

print "n:", n
print "total_se:", total_se

"""temperature = 1
chain = do_mcmc(temperature, 10*np.ones(num_params))"""

priors = True
prior_xs = [np.linspace(-2000,7000,1001),np.linspace(-200,600,1001),np.linspace(190,700000,10001)]
prior_pdfs = [st.norm.pdf(prior_xs[0],params_mean[0],np.sqrt(params_vars[0])),
              st.norm.pdf(prior_xs[1],params_mean[1],np.sqrt(params_vars[1])),
              st.invgamma.pdf(prior_xs[2],a=a,scale=1./b)]


"""for i in xrange(num_params):
    if i<3:
        marginal_axes[i].set_xlabel(labels[i])
    else:
        marginal_axes[i].set_ylabel(labels[i])
    if priors and i<3:
        marginal_axes[i].plot(prior_xs[i], prior_pdfs[i], label='Prior', color='red')
    #ax.legend()"""

#fig = plt.figure()
#ax = fig.add_subplot(111)
#ax.plot(chain[burn:,-1])


time_taken = time()-start
print "Time taken: {} s".format(time_taken)

#plt.show()

