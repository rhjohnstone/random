import time
import sys
start=time.time()

#N=60000000
N = 20

def sieve(n):
    nums = [[] for x in range(n)]
    prime = 2
    while prime < n:
        power = prime
        while power < n:
            multiple = power
            if multiple==2:
                pass
            else:
                while multiple < n:
                    nums[multiple].append(prime)
                    multiple += power
            power *= prime
        k = prime + 1
        if k >= n:    # no primes left!!!
            return nums
        while len(nums[k]) > 0:
            k += 1
            if k >= n:    # no primes left!!!
                return nums
        prime = k
    return nums

factors=sieve(N+2)
factors[0]=[0]
factors[1]=[1]
print factors
print "len(factors) =", len(factors)
print "Size of factors:", sys.getsizeof(factors)
ghjg
print "Time 1 is ",time.time()-start

for a in xrange(1,len(factors)-1):
    factors[a]+=factors[a+1]
factors.pop()    
#print factors
for i in xrange(0,len(factors)):
    j=factors[i]
    j=list(set(j))
    q=1
    for k in j:
        q*=(factors[i].count(k)+1)
    factors[i]=q
factors[0]=0
#print factors
print len(factors)
print "Time 2 is ",time.time()-start

print "Time 3 is ",time.time()-start

count=0
for a in xrange(1,len(factors)-2):
    if factors[a] not in [2,3]:
        for b in xrange(a+1,len(factors)-1):
            if factors[b]!=2:
                if factors[a]>factors[b]:
                    z=factors[b]
                    for i in xrange(2,z,2):
                        count+=factors[b+1::].count(i)
                        count=count%10**18

print count            
print "Time 4 is ",time.time()-start        
    
