import time

def hilbert_numbers_up_to(n):
    k_max = (int(n)-1)/4
    hilbert_numbers = [4*k+1 for k in xrange(1,k_max+1)] # deliberately omitting 1
    return hilbert_numbers
    
def is_hilbert_squarefree(n,hilbert_numbers):
    is_squarefree = True
    #print hilbert_numbers
    for test_hilbert in hilbert_numbers:
        test_square = test_hilbert**2
        if (test_square>n):
            break
        elif (n%test_square==0):
            #print n
            #print test_hilbert
            is_squarefree = False
            break
    return is_squarefree

N = 10**7

start = time.time()
total = 1
hilbert_numbers = hilbert_numbers_up_to(N)
for hil_num in hilbert_numbers:
    total += is_hilbert_squarefree(hil_num,hilbert_numbers)
time_taken = time.time()-start
print "Total less than {}:".format(N), total
print "Time taken: {} s".format(round(time_taken,2))

"""max_n = 10
hilbert_numbers = hilbert_numbers_up_to(max_n**.5)
for n in xrange(2,max_n):
    if is_hilbert_squarefree(n,hilbert_numbers):
        print n"""
