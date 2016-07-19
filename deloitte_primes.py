# Ross's script v2 for James's coding challenge.

# Run this from the command line by calling "python deloitte_primes.py".
# (At least on Ubuntu, not sure of the equivalent system in Windows.)
# (Try http://pythoncentral.io/execute-python-script-file-shell/ maybe.)
# Enter positive integers when prompted and press Enter.

# This version uses modulos to sum digits instead of string conversions.
# Modulo version is quicker according to my timed tests.
# However, constructing the list of primes is by far the slowest part of this script.

import time

# Define a function that sums an integer's digits by adding the last digit,
# dividing by 10 (Python automatically rounds down), and repeating.
def sum_digits(_n):
    _total = 0
    while (_n > 0):
        _total += (_n%10)
        _n /= 10
    return _total

# User-chosen values. These are inputted at the command line when prompted.
how_many_primes = int(raw_input("\nHow many primes do you want to consider?\n")) # or just set this to 2016.
target_digits_sum = int(raw_input("\nWhat would you like the primes' digits to sum to?\n")) # or just set this to 13.

# Start the timer.
start = time.time()

# Construct a list of the first N primes. There's probably a faster way to do this,
# but this method ensures it stops after the first N primes have been found.
primes = []
test = 2
while (len(primes) < how_many_primes):
    is_prime = True
    for p in primes:
        if (test%p==0):
            is_prime = False
            break
    if is_prime:
        primes.append(test)
    test += 1
    
# This first bit really takes most of the time.
print "\nTime taken to construct set of first {} primes: {} s.".format(how_many_primes,round(time.time()-start,2))

# Go through the primes in the list, and check if their digits sum to the target.
count = 0
for p in primes:
    if (sum_digits(p) == target_digits_sum):
        count += 1

# Print results and time taken (rounded to nearest decisecond).
print "\n{} of the first {} primes' digits sum to {}.\n".format(count,how_many_primes,target_digits_sum)
print "Total time taken: {} s.\n".format(round(time.time()-start,2))
