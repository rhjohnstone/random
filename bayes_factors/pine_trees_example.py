import numpy as np
import numpy.random as npr
import matplotlib.pyplot as plt
import scipy.special as sp
import sys


def log_data_likelihood(y, explan, explan_bar, params, num_pts):
    temp_1 = 0.5 * num_pts * np.log(params[-1])
    temp_2 = np.sum((y - params[0] - params[1] * (explan - explan_bar))**2) / (2. * params[-1])
    return - temp_1 - temp_2


def log_invgamma_prior(x, a, b):
    return -(1./(b*x) + sp.gammaln(a) + a*np.log(b) + (a+1.)*np.log(x))


def log_target(params, y, explan, explan_bar, num_pts, a, b):
    return log_data_likelihood(y, explan, explan_bar, params, num_pts) + log_invgamma_prior(params[-1], a, b)


# (yi, xi, zi)
pine_data = np.array([[3040, 29.9, 25.4],
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

model = 1

if model == 1:
    explan = pine_data[:,1]
elif model == 2:
    explan = pine_data[:,2]
else:
    sys.exit("Illegal model number\n")

y = pine_data[:,0]
explan_bar = np.mean(explan)
num_pts = len(y)

params_mean = np.array([3000, 185]) # same for both models
params_cov = np.diag([10**6, 10**4]) # same for both models
num_params = 3

a = 3
b = 1./(2*300**2)

theta_cur = np.array([3000, 185, 1./(b*(a+1))])
log_target_cur = log_target(theta_cur, y, explan, explan_bar, num_pts, a, b)

total_iterations = 1000
thinning = 10
num_saved = total_iterations / thinning + 1

chain = np.zeros((num_saved, num_params+1))
chain[0,:] = np.concatenate((theta_cur,[log_target_cur]))

proposal_cov = 0.1*np.diag(theta_cur)

t = 1
while t <= total_iterations:
    theta_star = npr.multivariate_normal(theta_cur,proposal_cov)
    log_target_star = log_target(theta_star, y, explan, explan_bar, num_pts, a, b)
    u = npr.rand()
    if np.log(u) < log_target_star - log_target_cur:
        theta_cur = theta_star
        log_target_cur = log_target_star
    if t%thinning == 0:
        chain[t/thinning,:] = np.concatenate((theta_cur,[log_target_cur]))

print chain
