import math
import time

def gcd(a,b):
    while a:
        a, b = b%a, a
    return b
    
def min_s(r):
    if (r>10):
        return int((-r+math.sqrt(3*r**2-200))/2.)
    else:
        return 1
        
def max_s(r):
    return int((-r+math.sqrt(3*r**2+200))/2.)

def f(N,r_max):
    #r_max = int((-1. + math.sqrt(4*N-3))/2)
    #r_max = math.sqrt(N) # for large N
    total = 0
    r = 2
    while (r<=r_max):
        s_min = min_s(r)
        s_max = max_s(r)
        for s in xrange(s_min,s_max+1):
            rr = r**2
            ss = s**2
            rs = r*s
            a = rr-ss
            b = 2*rs+ss
            a,b = min(a,b),max(a,b)
            c = rr + rs + ss
            if (gcd(a,b)==1):
                total += min(N/c,100/(b-a))
            else:
                pass
                #print a,b
        if (r%1000000==0):
            print r, total
        r += 1
    return total
    
start = time.time()
answer = f(10**100,10**50)
time_taken = time.time()-start
print answer
