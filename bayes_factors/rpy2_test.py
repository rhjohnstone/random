import numpy as np
import numpy.random as npr

from rpy2.robjects.packages import importr
# import R's "base" package
mcmcse = importr('mcmcse')
import rpy2.robjects.numpy2ri
rpy2.robjects.numpy2ri.activate()

for p in xrange(1,4):
    num_samples = 10**p
    y = npr.randn(num_samples)
    #ry = robjects.FloatVector(y)

    something = mcmcse.mcse(y, method="obm")
    print something
    se = something[1][0]
    print se
