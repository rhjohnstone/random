import math
import numpy as np

def primes_up_to_N(N):
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
    return x

def is_square(apositiveint):
    x = apositiveint // 2
    seen = set([x])
    while x * x != apositiveint:
        x = (x + (apositiveint // x)) // 2
        if x in seen:
            return False,0
        seen.add(x)
    return True,x

def n_root_given_k_p(k,p):
    discrim = 1+8*k*p
    square,root = is_square(discrim)
    if square:
        return (-1+root)/2
    else:
        return 0

max_prime = 10**8
primes = primes_up_to_N(max_prime)

def primes(n):
    primfac = []
    d = 2
    while d*d <= n:
        while (n % d) == 0:
            primfac.append(d)  # supposing you want multiple factors repeated
            n //= d
        d += 1
    if n > 1:
       primfac.append(n)
    return primfac
    
n = 12400
print primes((n*(n+1))/2)

"""
max_k = 10**8
max_a = 10**8
for a in xrange(1,max_a):
    prime = 47+2*a
    if prime not in primes:
        continue
    for q in xrange(1,prime):
        for k in xrange(max_k):
            discrim = 1+8*(k*prime+q)
            square,root = is_square(discrim)
            if square:
                print "n =", (-1+root)/2
"""
