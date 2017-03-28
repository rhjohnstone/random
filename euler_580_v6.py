# count the number of Hilbert numbers that are NOT squarefree
# because these can be directly constructed, instead of checking every Hilbert number for the squarefree property

# a Hilbert number (4k+1) squared is also a Hilbert number
# for m(4k+1) to be a Hilbert number, m must also be a Hilbert number

import time
import math
import sys

# assuming (4a+1)(4b+1)^2 <= N-1, 0<=a, 1<=b
def max_b_given_N(N):
    return int((math.sqrt(N-1)-1.)/4)
    
def num_multiples_of_4bplus1_less_than_N(b,N):
    return int(((N-1.)/(4*b+1)**2-1)/4)+1
    
def num_hilbert_numbers_less_than_N(N):
    return (N+2)/4
    
# suppose (4a+1)=(4c+1)(4d+1)^2, 0<=c, 1<=d
def max_d_given_N(N):
    return int((math.sqrt(N-1)/5-1)/4)
    
def max_c_given_d_and_N(d,N):
    return int(((N-1.)/(25*(4*d+1)**2)-1)/4)
    
def is_hilbert(n):
    if (n<1):
        return False
    elif ((n-1)%4==0):
        return True
        
def k_from_c_and_d(c,d):
    new_hilbert = (4*c+1)*(4*d+1)
    return (new_hilbert-1)/4

answers_relative_to_power_of_10 = [0,3,23,232,2324,23265,232710,2327192,23272089,232721183,2327212928,23272130893] # I think

power = 4
N = 10**power

start = time.time()

num_hilberts = num_hilbert_numbers_less_than_N(N)
print "{} Hilbert numbers less than 10^{}".format(num_hilbert_numbers_less_than_N,power)
num_non_squarefree = 0

# count all multiples, will include duplicates
# (4a+1)(4b+1)^2
b_max = max_b_given_N(N)
for b in xrange(1,b_max+1):
    num_multiples = num_multiples_of_4bplus1_less_than_N(b,N)
    num_non_squarefree += num_multiples

# (4a+1) = (4c+1)(4d+1)^2
num_repeats = 0
d_max = max_d_given_N(N)
for d in xrange(1,d_max+1):
    c_max = max_c_given_d_and_N(d,N)
    for c in xrange(c_max+1):
        n = (4*c+1)*(4*d+1)**2
        if is_hilbert(n):
            print c,d,n
            #k = k_from_c_and_d(c,d)
            num_repeats += 1
            
# (4b+1)^2 = k^2(4e+1)^2 = (k(4e+1))^2

        
answer = num_hilberts - num_non_squarefree + num_repeats
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
