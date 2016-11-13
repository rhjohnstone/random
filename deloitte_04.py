import numpy as np

def primes_up_to_root(n):
    numbers = np.arange(3,int(np.sqrt(n))+1,2)
    length = len(numbers)
    for i in xrange(length):
        a = numbers[i]
        if (not a):
            continue
        else:
            numbers[np.arange(a/2-1+a,length,a)] = 0
    numbers = numbers[np.where(numbers)]
    numbers = np.insert(numbers,0,2)
    return numbers
    
def factorise(n,primes):
    factors = []
    while (n>1):
        for p in primes:
            if (n%p==0):
                factors.append(p)
                n /= p
                break
    return factors
    
first_number_to_factorise = 379065191139531
next_numbers_to_factorise = [35432488, 806095675586097, 7405814774826, 379065191139531]

max_number_to_factorise = max([first_number_to_factorise]+next_numbers_to_factorise)

primes = primes_up_to_root(max_number_to_factorise)

factors = factorise(first_number_to_factorise,primes)

print first_number_to_factorise
print factors, "\n"

target_factors = []

for n in next_numbers_to_factorise:
    factors = factorise(n,primes)
    target_factors.append(factors)
    print n
    print factors, "\n"
    

