import numpy as np
import numpy.random as npr

seed = 1
npr.seed(seed)

def sample_max_length(how_many_pieces):

    x_pts = np.concatenate(([0.],npr.rand(how_many_pieces-1),[1.]))
    x_pts.sort()

    lengths = np.diff(x_pts)
    
    return np.max(lengths)
    
how_many_samples = 1000
how_many_lengths = 3
samples = []
for _ in xrange(how_many_samples):
    samples.append(sample_max_length(how_many_lengths))

how_many_dp = 3
print "\nUsing {} samples:\n".format(how_many_samples)
print "Mean = {}\n".format(round(np.mean(samples),how_many_dp))
print "11/18 = {}\n".format(round(11./18,how_many_dp))
