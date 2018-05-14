import time
import math
import bisect
start=time.time()

def prime_end(n):
    q=math.ceil(n**.5)
    return bisect.bisect_right(primes,q)
    
def prime(n):
    sieve = [True] * (n/2)
    for i in xrange(3,int(n**0.5)+1,2):
        if sieve[i/2]:
            sieve[i*i/2::i] = [False] * ((n-i*i-1)/(2*i)+1)
    return [2]+[2*i+1 for i in xrange(1,n/2) if sieve[i]]

def addition(sett,primesA,N):
    tott=0
    for p in primesA:
        end=(sett[1]//p)*p
        if sett[0]%p==0:
            begin=sett[0]
        else:
            begin=sett[0]+p-sett[0]%p
        #print begin, end
        tott+=(begin+end)*(end/p-begin/p+1)/2
    if primesA[0]*primesA[1]<=N:
        tott-=primesA[0]*primesA[1]*2
    return tott

N=99996666333300000
#N=1000
tott=0
primes=prime(int((N+1)**.5)+100)
zz=prime_end(N)
primes=primes[0:zz+1]
print "Time 1 is ",time.time()-start

answer=0
for p in xrange(0,len(primes)-1):
    sett=(primes[p]**2+1,primes[p+1]**2-1)
    if sett[1]>N:
        sett=(sett[0],N)
        
    primesA=(primes[p],primes[p+1])
    subtot=addition(sett,primesA,N)
    answer+=subtot
print p,primes[p], primes[p+1],sett,primesA,subtot,answer
print "Time 2 is ",time.time()-start


