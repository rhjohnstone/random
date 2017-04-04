import numpy as np
import os


def chains_dir(model):
    temp_dir = "output/model_{}/chains/".format(model)
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    return temp_dir


def define_chain_file(model, temperature):
    chain_file = chains_dir(model) + 'model_{}_temp_{}_chain.txt'.format(model, temperature)
    return chain_file


def compute_pi_bit_of_log_likelihood(y):
    num_pts = len(y)
    return 0.5 * num_pts * np.log(2 * np.pi)


def log_data_likelihood(y, explan, explan_bar, params, num_pts, t, pi_bit):
    """
    Compute log likelihood of data.
    Note that pi_bit is a constant, so is not needed for MH, but when we're approximating log(p(y)), we need to include it.
    Of course, we could just add it on after, but I just left it there so I can reuse the exact same code.
    """
    # type: (object, object, object, object, object, object) -> object
    if params[-1] <= 0:
        print params
    temp_1 = 0.5 * num_pts * np.log(params[-1])
    temp_2 = np.sum((y - params[0] - params[1] * (explan - explan_bar))**2) / (2. * params[-1])
    return -t * (pi_bit + temp_1 + temp_2)


def load_pine_data():
    return np.loadtxt("pine_data.txt")


def trapezium_rule(x, y):
    return 0.5 * np.sum((x[1:]-x[:-1]) * (y[1:]+y[:-1]))