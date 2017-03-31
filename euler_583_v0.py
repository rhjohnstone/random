import time

def max_e(q):
    return (q-1)/2
    
def b_bounds(e,q):
    b_min = int(1 + 0.5*q - q**2/(8.*e)) + 1
    b_max = 2*e + 1 - q/2
    return b_min, b_max
    

    
N = 10**2
status = N/10

start = time.time()
total = 0
for q in xrange(1,N+1):
    if (q%status==0):
        print (q/status), "/", N/status
        print "Time so far:", time.time()-start, "s"
    for b in xrange(2,q):
        for e in xrange(b,(q-1)/2+1):
            x = q - 2*e
            y = b - 1
            z = 1 + e - b
            if (x>0 and y>0 and z>0):
                if (4*y**2 + x**2 - 4*z**2>0):
                    total += q
                    print (x,y,z),q
                else:
                    break
time_taken = time.time() - start
print "{}: {}".format(N,total)
print round(time_taken,1), "s"
