# This version will count the factors while doing the factorisation, instead of after

import numpy as np
import time

def primes_up_to_half(n):
    numbers = np.arange(3,n/2+1,2)
    length = len(numbers)
    for i in xrange(length):
        a = numbers[i]
        if (not a):
            continue
        else:
            numbers[np.arange(a/2-1+a,length,a)] = 0
    numbers = numbers[np.where(numbers)]
    numbers = np.insert(numbers,0,2)
    return numbers
    
def is_increasing(n,primes):
    if n in primes:
        return False
    p_count_old = 44 # no count can get higher than this for the question
    for p in primes:
        p_count_cur = 0
        while (n%p==0):
            n /= p
            p_count_cur += 1
            if (p_count_cur > p_count_old):
                return True
        if (p_count_cur>0):
            p_count_old = p_count_cur
        if (n==1):
            return False

start = time.time()
num_increasing = 0
max_n = 2*10**4
primes = primes_up_to_half(2*max_n)
for n in xrange(1,max_n+1):
    if is_increasing(n,primes):
        num_increasing += 1
num_decreasing = max_n - num_increasing
time_taken = time.time()-start
        
print num_decreasing
print time_taken


