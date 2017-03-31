import time

def sieve(n):
    nums = [[] for x in xrange(n)]
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
            if k >= n:    # no primes left!!!
                return nums
        prime = k
    return nums

start = time.time()
N=10**5
NN=int((N**.5)/2.0)
sett=sieve(N)
#print sett

for i in xrange(0,len(sett)):
    Q=list(set(sett[i]))
    Q.sort()
    A=[]
    for q in Q:
        A.append((q,sett[i].count(q)))
    sett[i]=A
#print sett
tott=0
for i in xrange(0,len(sett)):
    if len(sett[i])<2:
        continue
    #print i,j,sett[i], len(sett[i])
    for j in xrange(0,len(sett[i])-1):
        #print i,j,
        if sett[i][j][1]<sett[i][j+1][1]:
            tott+=1
            #print i,j,sett[i],tott
            break
time_taken = time.time()-start
print tott,N-tott,round(time_taken,2)


    
                


    
