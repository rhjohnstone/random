import time

def gcd(a,b):
    while a:
        a, b = b%a, a
    return b
    
def multi_gcd(*args):
    return reduce(gcd,args)

n = 10**3

start = time.time()
total = 0
primitive_triples = []
for c in xrange(2,n+1):
    for a in xrange(1,c):
        for b in xrange(a,a+100+1):
            if (a**2+a*b+b**2==c**2):
                total += 1
                if multi_gcd(a,b,c)==1:
                    primitive_triples.append((a,b,c))
                break
tt = time.time()-start

print total
print "There are {} primitive triples less than {}".format(len(primitive_triples),n)
print primitive_triples
print round(tt,1), "s"
