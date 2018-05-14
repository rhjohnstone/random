import time
import numpy as np

s = time.time()

a = np.arange(200)
b = np.ones(200)
n = 5000000

dot = np.dot
for _ in xrange(n):
    c = dot(a,b)
    
tt = time.time()-s
print round(tt,2)
