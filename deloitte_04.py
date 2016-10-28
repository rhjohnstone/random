import numpy as np
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
    
def factorise(n):
    primes = primes_up_to_root(n)
    factors = []
    while (n>1):
        for p in primes:
            if (n%p==0):
                factors.append(p)
                n /= p
                break
    return factors
    
number_to_factorise = 379065191139531

start = time.time()
factors = factorise(number_to_factorise)
time_taken = time.time()-start

print number_to_factorise
print factors
print "Time taken: {} s\n".format(round(time_taken,2))

targets = [35432488, 806095675586097, 7405814774826, 379065191139531]
target_factors = []

for n in targets:
    factors = factorise(n)
    target_factors.append(factors)
    print n
    print factors, "\n"
    

