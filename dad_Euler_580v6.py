#2327192
import time
start=time.time()

def H(n): #Hilbert numbers under n
    return (n+2)/4

def HH(n,mult):
    return int((n-1)/mult-1.0)/4+1
    

N=10**7
NN=int(N**.5)+1
ends=int(NN/3)
sett=[(4*k+1) for k in xrange(0,ends+1)]
sett=[x for x in sett if x<=NN]
settA=[k*k for k in sett if k!=1] #gets squares of Hilbert numbers
print sett[0:10]
print sett[-10::]
print settA[0:10]
print settA[-10::]

for i in xrange(0,len(settA)-1):
    if settA[i]==0:
        continue
    for j in xrange(i+1, len(settA)): #eliminates multiples of squares
        if settA[j]%settA[i]==0:
            settA[j]=0
print "BBB",settA[0:10]
print "ccc",settA[-10::]
settA=[p for p in settA if p!=0]
#print "RRR",len(settA)
print settA[0:10]
print "Time 1 ",time.time()-start
countq,countr=0,0
for s in xrange(0,len(settA)): #
    q=HH(N,settA[s])
    #r=H(N/settA[s]**2)
    countq+=q   
    #countr+=r
    #print settA[s],q,countq
print "Time 2 ",time.time()-start
mult=1
for x in xrange(0,len(settA)): #calculates "end" or inclusion/exclusion
        mult*=settA[x]
        if mult>N:
            end=x
            break
#print end,settA[0:20]
print "Time 3 ",time.time()-start

def combinations(s, K):  #gives all combinations of sett "s" with length "K"
    """
    On entry: s sequence of items; K size of the combinations       
    Returns: list of all possible K-combinations without replacement of
    s.
    """
    N = len(s)
    assert K<=N, 'Error K must be less or igual than N'
    S = [[] for i in range(K+1) ]
    for n in range(1,N+1):
        newS = [[] for i in range(K+1) ]
        for k in range(max(1, n-(N-K)), min(K+1, n+1)):
            newS[k].extend(S[k])
            if len(S[k-1])==0:
                newS[k].append([s[n-1]])
            else:
                newS[k].extend( [el+[s[n-1]] for el in S[k-1]] )
        S = newS

    return S[K]
countA,countB=0,0
for vv in xrange(2,end+1): #Uses aboe combiinations to calculate inclusion/exclusion
    combs=combinations(settA, vv)  
    #print "RREW",combs
    for ww in xrange(0,len(combs)):
        mult=1
        for xx in xrange(0,len(combs[ww])):
            mult*=combs[ww][xx]
        #print mult
        if mult>N:
            break
        else:
            elim=HH(N,mult)
            #print "DDD",combs[ww],mult,N/mult,elim
            if len(combs[ww])%2==0:
                countA+=elim
            else:
                countB-=elim
        print "DDD",combs[ww],elim,countA,countB
 
print "Time 3 ",time.time()-start   
print "Time 4 ",time.time()-start            



print "v2",H(N),countq,countA,countB,H(N)-countq+countA-countB
print time.time()-start
print 2327192 #just a note of the corrct answer
