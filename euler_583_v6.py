import math
import time
import operator
import random

def gcd(a,b):
    while a:
        a, b = b%a, a
    return b

def unique_prime_factors(n):
    factors=[]
    d=2
    while(d*d<=n):
        while(n>1):            
            while n%d==0:
                factors.append(d)
                n=n/d
            d+=1
    return sorted(set(factors))
    
def multi_gcd(*args):
    return reduce(gcd,args)
    
def is_square(integer):
    try:
        root = math.sqrt(integer)
    except:
        return False, 0
    test = int(root + 0.5)
    if test ** 2 == integer:
        return True, int(root)
    else:
        return False, 0
    
    
def max_n(N):
    return (N-3)/8
    
def flap_height(x,z):
    return math.sqrt(z**2 - (x/2.)**2)
    
def AC_diagonal_squared_times_4(x,y,h):
    return x**2 + 4*(y+h)**2
    
def z_bounds(x,y):
    z_min = int(math.ceil(math.sqrt(4+x**2)/2.))
    z_max = int(math.sqrt(4*(y-1)**2+x**2)/2)
    return z_min, z_max
    
def pythag_max_x_or_y(N):
    return max(N-4,(N-3)/2)
    
def max_m(N):
    return int(math.sqrt((1.+math.sqrt(2))*(N-4.)/2.))
    
def heron_m_max(N):
    return int(((5*N**2-32*N+52)/16.)**(1./6))
       

N = 10**2
m_max = max_m(N)

start = time.time()
primitive_pythag_triples = []
for m in xrange(1,m_max+1,2):
    for n in xrange(2,m,2):
        if (gcd(m,n)!=1):
            continue
        mm, nn = m**2, n**2
        x, y, u = mm-nn, 2*m*n, mm+nn
        if (x+y>N-3):
            continue
        else:
            primitive_pythag_triples.append((x,y,u))
for m in xrange(2,m_max+1,2):
    for n in xrange(1,m,2):
        if (gcd(m,n)!=1):
            continue
        mm, nn = m**2, n**2
        x, y, u = mm-nn, 2*m*n, mm+nn
        if (x+y>N-3):
            continue
        else:
            primitive_pythag_triples.append((x,y,u))
        
primitive_pythag_triples.sort(key=operator.itemgetter(2))
first_time = time.time()-start
#print primitive_pythag_triples
print "{} primitive triples".format(len(primitive_pythag_triples))
print "Time taken to make and sort primitive Pythagorean triples list: {} s".format(round(first_time,1))


# Heron triangles
herons = []
m_max = heron_m_max(N)
print m_max
quit = False
for m in xrange(1,m_max+1):
    for n in xrange(1,m+1):
        k_min = int(math.ceil(m*math.sqrt(n/(2.*m+n))))
        k_max = int(math.ceil(math.sqrt(m*n)))-1
        for k in xrange(k_min,k_max+1):
            a = n*(m**2+k**2)
            b = m*(n**2+k**2)
            c = (m+n)*(m*n-k**2)
            print a, (m,n,k)
            if (a,b,c) not in herons:
                herons.append((a,b,c))
    

time_taken = time.time()-start
print herons
print round(time_taken,1), "s"






