import time
import math
import operator

def is_square(integer):
    root = math.sqrt(integer)
    test = int(root + 0.5)
    if test ** 2 == integer:
        return True
    else:
        return False

def gcd(a,b):
    while a:
        a, b = b%a, a
    return b
    
def multi_gcd(*args):
    return reduce(gcd,args)
    
#def max_v(N):
#    return int(math.sqrt(5*N**2-38*N+73)/2.)
    
def max_m(n,N):
    return min((N-3)/(4*n),int(math.sqrt(n**2+N-4)))
    
def max_n(N):
    return (N-3)/8
    
def flap_height(x,z):
    return math.sqrt(z**2 - (x/2.)**2)
    
def AC_diagonal_squared_times_4(x,y,h):
    return x**2 + 4*(y+h)**2
    
def z_range(x,y):
    z_min = x/2 + 1
    z_max = int(math.sqrt(x**2+4*(y-1)**2)/2.)
    return z_min, z_max
    

N = 10**3
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
print primitive_pythag_triples


total = 0
how_often = 20
num_triples = len(primitive_pythag_triples)
status_when = num_triples/how_often

for j,triple in enumerate(primitive_pythag_triples):
    if (j%status_when==0) and (j>0):
        print j/status_when, "/", how_often
    #print triple
    for i in xrange(2):
        primitive_x,primitive_y = triple[i],triple[1-i]
        x,y = primitive_x,primitive_y
        
        z_min, z_max = z_range(x,y)
        for top_triple in primitive_pythag_triples:
            original_2z = 2*top_triple[-1]
            a = 0
            while True:
                a += 1
                temp_2z = a*original_2z
                if (temp_2z < 2*z_min):
                    continue
                elif (2*z_min <= temp_2z <= 2*z_max):
                    #print top_triple
                    if (x in top_triple):
                        perim = x + 2*y + temp_2z
                        if (perim<=N):
                            total += perim
                            print (x, y, temp_2z)
                else:
                    break
time_taken = time.time()-start    

print "\n{}: {}".format(N,total)
print round(time_taken,1), "s\n"
