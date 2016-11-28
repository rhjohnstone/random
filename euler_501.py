import numpy as np
import time
import sys
from bisect import bisect

def P10(n): # lucy hedgehog
    r = int(n**0.5)
    assert r*r <= n and (r+1)**2 > n
    V = [n//i for i in range(1,r+1)]
    V += list(range(V[-1]-1,0,-1))
    S={i:i-1 for i in V}
    for p in range(2,r+1):
        if S[p] > S[p-1]:  # p is prime
            sp = S[p-1]  # sum of primes smaller than p
            p2 = p*p
            for v in V:
                if v < p2: break
                S[v] -= p*(S[v//p] - sp)
    return S
    
print P10(10)
sys.exit()
    
def primesfrom2to(n):
    # http://stackoverflow.com/questions/2068372/fastest-way-to-list-all-primes-below-n-in-python/3035188#3035188
    """ Input n>=6, Returns a array of primes, 2 <= p < n """
    #sieve = np.ones(n/3 + (n%6==2), dtype=np.bool) # original
    sieve = np.array([True for _ in xrange(n/3 + (n%6==2))], dtype=np.bool) # RJ, trying to beat MemoryError
    sieve[0] = False
    for i in xrange(int(n**0.5)/3+1):
        if sieve[i]:
            k=3*i+1|1
            sieve[      ((k*k)/3)      ::2*k] = False
            sieve[(k*k+4*k-2*k*(i&1))/3::2*k] = False
    return np.r_[2,3,((3*np.nonzero(sieve)[0]+1)|1)]

def primes_up_to(n):
    numbers = np.arange(3,n+1,2)
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
    
def got_8_divisors(n,primes):
    if n in primes:
        return False
    num_prime_factors = 0
    prime_counts = {}
    while (n>1):
        none_found = True
        for p in primes:
            if (n%p==0):
                none_found = False
                try:
                    prime_counts[p] += 1
                except:
                    prime_counts[p] = 1
                num_prime_factors += 1
                if (num_prime_factors>7):
                    return False
                n /= p
                break
        if none_found:
            prime_counts[n] = 1
            num_prime_factors += 1
            if (num_prime_factors>4):
                return False
            break
    if ((num_prime_factors==4) and (len(prime_counts)==2)):
        values = prime_counts.values()
        if (values[0]==values[1]):
            return False
        else:
            return True
    elif (len(prime_counts)==3 and num_prime_factors==3):
        return True
    elif (len(prime_counts)==1 and num_prime_factors==7):
        return True
    else:
        return False
        
def num_8_divisors(max_n):
    total = 0
    primes = primesfrom2to(max_n/6)
    a_max = max_n**(1./3)
    for idx_a,a in enumerate(primes): # abc, all unique
        if (a > a_max):
            break
        else:
            for idx_b,b in enumerate(primes[idx_a+1:]):
                c_max = max_n/(a*b)
                if (c_max<=a or c_max<=b):
                    break
                else:
                    nearest_prime_to_c_max_index = bisect(primes[idx_a+1:],c_max)-1
                    index_diff = nearest_prime_to_c_max_index-idx_b
                    total += index_diff
                    #for c in primes:
                        #if (c<=b):
                            #continue
                        #else:
                            #if (a*b*c > max_n):
                                #break
                            #else:
                                #total += 1
    b_max = (max_n/2.)**(1./3)
    for b in primes: # ab^3, a,b unique
        if (b > b_max):
            break
        else:
            a_max = max_n/b**3
            if (a_max<=1):
                break
            else:
                nearest_prime_to_a_max_index = bisect(primes,a_max)-1
                #print nearest_prime_to_a_max_index
                if (nearest_prime_to_a_max_index>=0):
                    if (a_max>=b):
                        total += (nearest_prime_to_a_max_index)
                    elif (a_max<b):
                        total += (nearest_prime_to_a_max_index+1)
                else:
                    break
            
            #for a in primes:
                #if (a==b):
                    #continue
                #elif (a > (max_n/8)):
                    #break
                #else:
                    #if (a*b**3 > max_n):
                        #break
                    #else:
                        #total += 1
    for a in primes:
        if (a**7 > max_n):
            break
        else:
            total += 1
                
    return total

start = time.time()
answer = num_8_divisors(10**6)
time_taken = time.time()-start
print answer
print "Time taken: {} s = {} min".format(round(time_taken,3),round(time_taken/60.,3))
sys.exit()
   
start = time.time()
max_n = 10**12
primes = primes_up_to_root(max_n)
#print primes
total = 0
for n in xrange(1,max_n+1):
    if got_8_divisors(n,primes):
        #print n
        total += 1
time_taken = time.time()-start

print "\n",total,"\n"
print "Time taken: {} s = {} min".format(round(time_taken,2),round(time_taken/60.,2))

