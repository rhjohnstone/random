import time
    
def S(m):
    J = 1.5
    total = 1.5
    if m==1:
        return total
    for n in xrange(1,m):
        J = (0.5*J + (1./(n+1.)*(2-2**-n+2**-(n+1))))
        total += J
    return total

m = 123456789
dp = 8

start = time.time()
answer = S(m)
time_taken = time.time()-start
print "S({}) =".format(m), round(answer,dp)
print round(time_taken,2), "s"
