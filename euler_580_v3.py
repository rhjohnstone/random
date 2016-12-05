import time
#import numpy as np

def is_hilbert(n):
    if ((n-1)%4==0):
        return True
    else:
        return False

N = 10**3


start = time.time()

num_hilbert_numbers_less_than_N = (N+2)/4

print num_hilbert_numbers_less_than_N

max_possible_hilbert_number = int(N**.5)
max_k = (max_possible_hilbert_number-1)/4

non_squarefree_hilbert_numbers = []
for k in xrange(1,max_k+1):
    test = 4*k+1
    test_square = test**2
    multiple_of_test_square = test_square
    while (multiple_of_test_square<N):
        non_squarefree_hilbert_numbers.append(multiple_of_test_square)
        multiple_of_test_square += 4*test_square
        
#print non_squarefree_hilbert_numbers
        
num_non_squarefree_hilberts = len(set(non_squarefree_hilbert_numbers))
answer = num_hilbert_numbers_less_than_N-num_non_squarefree_hilberts#-1

tt = time.time()-start

print "Total less than {}:".format(N), answer
print "Time taken: {} s".format(round(tt,6))
