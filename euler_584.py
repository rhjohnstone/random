import numpy as np
import math
import time

import operator as op
def ncr(n, r):
    r = min(r, n-r)
    if r == 0: return 1
    numer = reduce(op.mul, xrange(n, n-r, -1))
    denom = reduce(op.mul, xrange(1, r+1))
    return numer/denom
    
def p_k_birthdays_n_people_m_days(k,n,m):
    return 1 - math.exp(-ncr(n,k)/(1.*m**2))
    
k = 3
m = 10
for n in xrange(3,11):
    print n, p_k_birthdays_n_people_m_days(k,n,m)
adf

start = time.time()

def p(n,k,m):
    """Probability of 2 people having birthdays within k days of each other, from a total of m possible birthdays, given n people"""
    assert(n>1)
    factors = range(m-n*k-(n-1),m-n*k-1+1)
    #print factors
    factorial_result = reduce(lambda x, y: x*y, factors)
    return 1. - float(factorial_result)/(m**(n-1))
    
k = 1
m = 10
for n in xrange(3,12):
    print n, 0.1*p(n-1,0,m) + 0.2*p(n-1,1,m)
