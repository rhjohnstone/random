import numpy as np
#import sys
import time

#N = int(sys.argv[1])
N = 10**7
print "Constructing list of primes less than or equal to {}".format(N)

start = time.time()
x = np.arange(3,N+1,2)
lenx = len(x)
for i in xrange(int(np.sqrt(N))-1):
    a = x[i]
    if (a==0):
        continue
    else:
        x[np.arange(a/2-1+a,lenx,a)] = 0

x = x[np.where(x>0)]
x = np.insert(x,0,2)
print x[:10]
print x[-10:]
print "Constructed list of first {} primes".format(len(x))
print "Time taken: {} s".format(np.round(time.time()-start,1))
