# count the number of Hilbert numbers that are NOT squarefree
# because these can be directly constructed, instead of checking every Hilbert number for the squarefree property

# a Hilbert number (4k+1) squared is also a Hilbert number
# for m(4k+1) to be a Hilbert number, m must also be a Hilbert number

import time
import math
import sys

def reduce_b(b):
    pseudo_factors = []
    c_max = int((math.sqrt(0.25+b)-0.5)/2)
    for c in xrange(1,c_max+1):
        if ((b-c)%(4*c+1)==0):
            d = (b-c)/(4*c+1)
            pseudo_factors += [c,d]
    return pseudo_factors
    
def fully_reduce_b(b):
    all_factors = reduce_b(b)
    for i in all_factors:
        temp_factors = reduce_b(i)
        all_factors += temp_factors
    #print b, all_factors
    return all_factors
    
#b = 28

#print fully_reduce_b(b)

#sys.exit()

answers_relative_to_power_of_10 = [0,3,23,232,2324,23265,232710,2327192,23272089,232721183,2327212928,23272130893]

power = 7
N = 10**power

start = time.time()

num_hilbert_numbers_less_than_N = (N+2)/4
print "{} Hilbert numbers less than 10^{}".format(num_hilbert_numbers_less_than_N,power)
num_non_squarefree = 0
b_max = int((math.sqrt(N)-1.)/4)
print "b_max =", b_max
for b in xrange(1,b_max+1):
    num_multiples = int((N/(4.*b+1.)**2-1.)/4.)+1
    num_unique_factors_of_b = len(set(fully_reduce_b(b)))
    #print "b, count:", b, num_unique_factors_of_b
    num_non_squarefree += (1-num_unique_factors_of_b)*num_multiples # removing multiply counted squares (not taken scalar multiples into account)
    #num_non_squarefree += num_multiples
answer = num_hilbert_numbers_less_than_N - num_non_squarefree
tt = time.time()-start

print "\nTotal less than 10^{}:".format(power), answer
print "Time taken: {} s\n".format(round(tt,2))

try:
    correct_answer = answers_relative_to_power_of_10[power]
    undershoot = correct_answer - answer
    print "For 10^{}, answer is".format(power), undershoot, "below what it should be\n"
    if (undershoot>0):
        print "Therefore counting too few squarefree numbers"
        print "i.e. counting too many non-squarefree numbers"
        print "This must be because some non-squarefree numbers are being counted multiple times"
except:
    print "Don't know the correct answer for 10^{}".format(power)

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
