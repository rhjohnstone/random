import numpy as np

npdot = np.dot

a = np.eye(100)

T = 500000

for _ in xrange(T):
    b = npdot(a,a)
