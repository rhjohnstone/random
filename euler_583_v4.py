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
    
def z_bounds(x,y):
    z_min = x/2 + 1
    z_max = int(math.ceil(math.sqrt(x**2+4*y**2)/2.))-1
    return z_min, z_max
    
def max_x(N):
    return int(math.ceil((N-2.)/2.))-1
    
def max_y(N):
    return (N-3)/2
    

N = 2*10**4
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
        x_max, y_max = max_x(N), max_y(N)
        while (x<=x_max) and (y<=y_max):
            z_min, z_max = z_bounds(x,y)
            for top_triangle in primitive_pythag_triples:
                original_z = top_triangle[2]
                if (original_z > z_max):
                    break
                scaled_z = 2*original_z
                while (scaled_z < 2*z_min):
                    scaled_z += 2*original_z
                while (2*z_min <= scaled_z <= 2*z_max):
                    scale = scaled_z / original_z
                    if (scale*top_triangle[0]==x) or (scale*top_triangle[1]==x):
                        z = (scale/2)*top_triangle[2]
                        v_squared = y**2 + z**2 + y*math.sqrt(4*z**2-x**2)
                        if is_square(v_squared):
                            perim = x + 2*y + 2*z
                            if (perim <= N):
                                total += perim
                            #print (x,y,z),(scale*top_triangle[0],scale*top_triangle[1],scale*top_triangle[2])
                    scaled_z += 2*original_z
                
            # find all triples with x and 2z in it, such that z satisfies bounds
            x += primitive_x
            y += primitive_y
        

time_taken = time.time()-start    

print "\n{}: {}".format(N,total)
print round(time_taken,1), "s\n"
