import time

start = time.time()
    
P = 3
Q = 4
K = -3
R = 2
S = 3
L = -2

max_N = 10**12

b, N = 15, 21
while N <= max_N:
    N,b = P*N + Q*b + K, R*N + S*b + L
time_taken = time.time()-start
print b
print "Time taken: {} s".format(round(time_taken,5))
