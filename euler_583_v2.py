import time
import math

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
    

N = 10**4
start = time.time()
primitive_pythag_triples = []
n_max = max_n(N)
for n in xrange(1,n_max+1,2):
    m_max = max_m(n,N)
    for m in xrange(n+1,m_max+1,2):
        if (gcd(m,n)!=1):
            continue
        primitive_pythag_triples.append((m**2-n**2, 2*m*n))
for n in xrange(2,n_max+1,2):
    m_max = max_m(n,N)
    for m in xrange(n+1,m_max+1,2):
        if (gcd(m,n)!=1):
            continue
        primitive_pythag_triples.append((m**2-n**2, 2*m*n))
        
#print primitive_pythag_triples

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
        while (x<=N-4) and (y<=(N-3)/2):
            for z in xrange(x/2+1,int(math.sqrt(4*(y-1)**2+x**2)/2)+1):
                h = flap_height(x,z)
                if (h>=y):
                    break
                else:
                    u_squared_times_4 = AC_diagonal_squared_times_4(x,y,h)
                    if is_square(u_squared_times_4):
                        perim = x + 2*y + 2*z
                        if (perim<=N):
                            #print (x,y,z),h
                            total += perim 
            x += primitive_x
            y += primitive_y
time_taken = time.time()-start    

print "\n{}: {}".format(N,total)
print round(time_taken,1), "s\n"
