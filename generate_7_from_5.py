# Given the ability to uniformly sample integers between 1 and 5, uniformly sample an integer between 1 and 7

import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import numpy.random as npr
import itertools as it


def sample_two_5s():
    a, b = npr.randint(1, 6, 2)
    return 10*a + b
    

all_possible_combos = [10*a+b for a,b in it.product(range(1,6), repeat=2)][:21]


def sample_1_7():
    while True:
        two_digit_5_sample = sample_two_5s()
        if two_digit_5_sample in all_possible_combos:
            break
    return all_possible_combos.index(two_digit_5_sample)/3 + 1


T = 1000000
samples = np.zeros(T)
for t in xrange(T):
    samples[t] = sample_1_7()

d = np.diff(np.unique(samples)).min()
left_of_first_bin = samples.min() - float(d)/2
right_of_last_bin = samples.max() + float(d)/2
plt.hist(samples, np.arange(left_of_first_bin, right_of_last_bin + d, d))
plt.show()


