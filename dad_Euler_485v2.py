import time
start=time.time()

def sieve(n):
    nums = [[] for x in range(n)]
    prime = 2
    while prime < n:
        power = prime
        while power < n:
            multiple = power
            while multiple < n:
                nums[multiple].append(prime)
                multiple += power
            power *= prime
        k = prime + 1
        if k >= n:    # no primes left!!!
            return nums
        while len(nums[k]) > 0:
            k += 1
            if k >= 10**4:    # no primes left!!!
                return nums
        prime = k
    return nums

N=10**8
k=10**5
factors=sieve(N+1)
#print factors
print "Time 1 is ",time.time()-start

for i in xrange(0,len(factors)):
    j=factors[i]
    j=list(set(j))
    q=1
    for k in j:
        q*=(factors[i].count(k)+1)
    factors[i]=q
factors[0]=0
#print factors
print "Time 2 is ",time.time()-start  
count=0
k=10
for i in xrange(1,N-k+2):
    z=max(factors[i:i+k])
    count+=z
    #if i>980:
        #print i, factors[i:i+k],z,count
print count
print "Time 3 is ",time.time()-start        
    
