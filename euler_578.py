import numpy as np
import collections
import time

def primes_up_to_root(n):
    numbers = np.arange(3,int(np.sqrt(n))+1,2)
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
    
def factorise(n,primes):
    factors = []
    while (n>1):
        for p in primes:
            if (n%p==0):
                factors.append(p)
                n /= p
                break
    return factors
    
start = time.time()
num_increasing = 0
max_n = 10**2
primes = primes_up_to_root(max_n**2)
for n in xrange(18,max_n+1): # 18 is the smallest that is increasing
    if n in primes:
        continue
    factors = factorise(n,primes)
    count = sorted(collections.Counter(factors).items())
    for i in xrange(len(count)-1):
        if (count[i+1][1] > count[i][1]):
            num_increasing += 1
            is_dpp = False
            break
answer = max_n - num_increasing
time_taken = time.time()-start
        
print answer
print time_taken
