import time
import numpy as np

s = time.time()

a = np.arange(200)
b = np.ones(200)
n = 5000000


for _ in xrange(n):
    c = np.dot(a,b)
    
tt = time.time()-s
print round(tt,2)
