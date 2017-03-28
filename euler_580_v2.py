import time
#import numpy as np


N = 10**2

start = time.time()
k_max = (N-1)/4
#hilberts = 4*np.arange(1,k_max+1)+1
hilberts = [4*k+1 for k in xrange(1,k_max+1)]

max_to_check = int(N**.5)
for i,n in enumerate(hilberts):
    if (n>max_to_check):
        break
    n_squared = n**2
    for m in hilberts[i:]:
        if (m%n_squared==0):
            hilberts.remove(m)
answer = len(hilberts)

tt = time.time()-start

print "Total less than {}:".format(N), answer
print "Time taken: {} s".format(round(tt,2))
