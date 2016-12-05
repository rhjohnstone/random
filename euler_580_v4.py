# count the number of Hilbert numbers that are NOT squarefree
# because these can be directly constructed, instead of checking every Hilbert number for the squarefree property

# a Hilbert number (4k+1) squared is also a Hilbert number
# for m(4k+1) to be a Hilbert number, m must also be a Hilbert number

import time

power = 7
N = 10**power

start = time.time()

num_hilbert_numbers_less_than_N = (N+2)/4

max_possible_hilbert_number = int(N**.5)
max_k = (max_possible_hilbert_number-1)/4

used_square_factors = [] # to avoid counting Hilbert numbers with multiple square factors
num_non_squarefree_hilbert_numbers = 0
for k in xrange(1,max_k+1):
    test = 4*k+1
    test_square = test**2
    multiple_of_test_square = test_square
    while (multiple_of_test_square<N):
        not_yet_used = True
        for factor in used_square_factors:
            if (multiple_of_test_square%factor==0):
                not_yet_used = False
                break
        if not_yet_used:
            num_non_squarefree_hilbert_numbers += 1
        multiple_of_test_square += 4*test_square
    used_square_factors.append(test_square)
answer = num_hilbert_numbers_less_than_N-num_non_squarefree_hilbert_numbers
tt = time.time()-start

print "\nTotal less than 10^{}:".format(power), answer
print "Time taken: {} s\n".format(round(tt,2))

"""
Total less than 10^1: 3
Time taken: 1.4e-05 s


Total less than 10^2: 23
Time taken: 2.6e-05 s


Total less than 10^3: 232
Time taken: 2.9e-05 s


Total less than 10^4: 2324
Time taken: 0.0001 s


Total less than 10^5: 23265
Time taken: 0.000788 s


Total less than 10^6: 232710
Time taken: 0.007783 s


Total less than 10^7: 2327192
Time taken: 0.08449 s


Total less than 10^8: 23272089
Time taken: 0.894421 s


Total less than 10^9: 232721183
Time taken: 8.79501 s


Total less than 10^10: 2327212928
Time taken: 89.999935 s


Total less than 10^11: 23272130893
Time taken: 1007.300136 s
"""
