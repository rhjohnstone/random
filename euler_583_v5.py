import math
import time
import operator

def gcd(a,b):
    while a:
        a, b = b%a, a
    return b
    
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
    
def max_m(n,N):
    return min((N-3)/(4*n),int(math.sqrt(n**2+N-4)))
    
def max_n(N):
    return (N-3)/8
    
def flap_height(x,z):
    return math.sqrt(z**2 - (x/2.)**2)
    
def AC_diagonal_squared_times_4(x,y,h):
    return x**2 + 4*(y+h)**2
    
def z_bounds(x,y):
    z_min = x/2 + 1
    z_max = int(math.ceil(math.sqrt(x**2+4*y**2)/2.))-1
    return z_min, z_max
       

N = 10**4
start = time.time()
primitive_pythag_triples = []
n_max = max_n(N)
for n in xrange(1,n_max+1,2):
    m_max = max_m(n,N)
    for m in xrange(n+1,m_max+1,2):
        if (gcd(m,n)!=1):
            continue
        mm, nn = m**2, n**2
        primitive_pythag_triples.append((mm-nn, 2*m*n, mm+nn))
for n in xrange(2,n_max+1,2):
    m_max = max_m(n,N)
    for m in xrange(n+1,m_max+1,2):
        if (gcd(m,n)!=1):
            continue
        mm, nn = m**2, n**2
        primitive_pythag_triples.append((mm-nn, 2*m*n, mm+nn))
        
primitive_pythag_triples.sort(key=operator.itemgetter(2))
first_time = time.time()-start
print "{} primitive triples".format(len(primitive_pythag_triples))
print "Time taken to make and sort primitive Pythagorean triples list: {} s".format(round(first_time,1))
#print primitive_pythag_triples

# Heron triangles
herons = []
m_max = N
for trip in primitive_pythag_triples:
    for i in xrange(2):
        x, y = trip[i], trip[1-i]
        z_min, z_max = z_bounds(x,y)
        for m in xrange(2,m_max+1):
            if (x%(2*m)==0):
                z = 2*m**3 - x/2
                if (z < z_min):
                    continue
                elif (z_min <= z <= z_max) and ((x,z) not in herons):
                    herons.append((x,z))
                else:
                    break
time_taken = time.time()-start
#print herons
print round(time_taken,1), "s"
