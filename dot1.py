import numpy as np

a = np.eye(100)

T = 500000

for _ in xrange(T):
    b = np.dot(a,a)
