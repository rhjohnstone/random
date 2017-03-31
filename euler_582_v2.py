import math

def is_square(integer):
    root = math.sqrt(integer)
    test = int(root + 0.5)
    if test ** 2 == integer:
        return True, test
    else:
        return False, 0
        
def gcd(a,b):
    while a:
        a, b = b%a, a
    return b
    
def multi_gcd(*args):
    return reduce(gcd,args)
    
def update_a_c(a,c,P,Q,K,R,S,L):
    a, c = P*a + Q*c + K, R*a + S*c + L
    return a, c
    
def algorithm_coefficients(i):
    A = 3     # a^2
    B = 0     # ac 
    C = -1    # c^2
    D = 3*i   # a
    E = 0     # c
    F = i**2  # 1
    if (i%2==0):
        m = 2
        n = 1
        P = m
        S = m + B*n
        Q = -C*n
        K = (C*D*(P+S-2)+E*(B-B*m-2*A*C*n))/(4*A*C-B**2)
        R = A*n
        L = (D*(B-B*m-2*A*C*n)+A*E*(P+S-2))/(4*A*C-B**2) + D*n
    else:
        m = -2
        n = -1
        P = m**2 - A*C*n**2
        Q = -C*n*(2*m + B*n)
        K = -n*(E*m + C*D*n)
        R = A*n*(2*m + B*n)
        S = m**2 + 2*B*m*n + (B**2 - A*C)*n**2
        L = n*(D*m + (B*D-A*E)*n)
    return P,Q,K,R,S,L
    
def find_initial_a_c(i):
    a = 1
    while True:
        if (a>1000000):
            #print "Probably none"
            return 0,i
        c_squared = 3*a**2 + 3*i*a + i**2
        square, root = is_square(c_squared)
        if (c_squared == 122**2):
            print a,i,c_squared
            print square
        if square and (multi_gcd(a,a+i,root)==1):
            return a,root
        else:
            a += 1

    
#initial_values = [None,(7,13),(3,7),(21,39),(6,14),(35,65),(9,21)]

upper_limit = 10**3
total = 0
triples = []
for i in xrange(1,101):
    print "{} / 100".format(i)
    P,Q,K,R,S,L = algorithm_coefficients(i)
    if (i==22):
        print "P,Q,K,R,S,L =", P,Q,K,R,S,L
    #print "\n", "i = {}:".format(i), P,Q,K,R,S,L, "\n"
    #a, c = 0, i
    #a, c = initial_values[i]
    a, c = find_initial_a_c(i)
    if (a==None):
        continue
    else:
        b = a+i
        print "Initial (a,b,c) =", (a,b,c)
    while True:
        temp_gcd = multi_gcd(a,b,c)
        primitive_triple = (a/temp_gcd,b/temp_gcd,c/temp_gcd)
        if (c/temp_gcd > upper_limit):
            break
        #print (a,b,c)
        if (primitive_triple not in triples) and (a>0):
            new_i = i/temp_gcd
            max_multiples = 100/new_i
            print primitive_triple
            triples.append(primitive_triple)
            #print "(new_i,max_multiples) =",new_i,max_multiples
            max_c = c*max_multiples
            diff = max_c - upper_limit
            num_extras = max(0,diff/c+1)
            #print "num_extras =", num_extras
            num_multiples = max_multiples-num_extras
            #print "num_multiples =", num_multiples, "\n"
            total += num_multiples
        a, c = update_a_c(a,c,P,Q,K,R,S,L)
        b = a+i
print triples
print "len(triples) =", len(triples)
print total
