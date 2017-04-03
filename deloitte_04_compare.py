import math
import time

def get_factors(x): # blog code
    a = []
    y = 1 + math.floor(x**0.5)
    for i in range(1,y):
        z = x/i
        if float(z).is_integer()==1: # left-hand side is already bool, so the "==1" isn't strictly necessary
            if i==z:
                a.append(int(i)) # i is already an int because it came from range(1,y)
            else:
                a.append(int(i)) # repeated line means we can move it outside the if statement
                a.append(int(z))
    a.sort()
    return a
    
"""
NB: if you're using/reading Python 2.7 code, "a/b" means integer division if a and b are ints,
so "3/2" will return "1" in Python 2.7, but will return "1.5" in Python 3.
I've written my code below in Python 3, just to be consistent with yours.

It's quite expensive to convert every float into an int (relative to just working with ints).
Doing everything with ints will always be quicker (I think), and more precise.
Using "//", i.e. integer division, will allow this.
Also because i came from range(1,y), it's already an int, so you're wasting a bit of time
converting it to an int.

Since you have an if statement for every value in range(1,y), might as well make check
that the number you are trying is a factor before dividing it, so that you know you're working
with ints, which is what the modulo "%" function does.
Your second if statement means that you're testing every factor for something again, but this
will only ever save one (repeated) factor, so the "success rate" of the statement is really low.
So it's probably worth not even doing the check, and just removing duplicates right at the end.
You can always do this by converting list->set->list.

In your second if statement, you append int(i) either way, so I think it's better to have that
line outside of the if statement; it's always preferable to not have repeated lines, I think.
I would just have "if (i!=z): a.append(int(z))" in this case (with a new line and indentation).

Ideally, I think variable names should be more descriptive than z,y,i, etc.
It's not much of a problem in this particular function, which is performing a quite
straightforward task, but it's generally good practice,
see https://www.python.org/dev/peps/pep-0008/.
I mean, I definitely don't adhere to all the principles, not claiming to be a perfect programmer,
but it definitely makes it easier for someone else to read and understand later on.
"""
    
def ross_factors(x):
    """Return a list of all integer factors of x (including 1 and x)."""
    factors = [1,x]
    max_factor = int(math.sqrt(x))
    for test in range(2,max_factor+1):
        if (x%test==0): # modulo function, check that test does divide x
            factors.append(test)
            factors.append(x//test) # "//" integer division, vs "/" float division
    factors = list(set(factors)) # remove possible square root duplicate
    factors.sort()
    return factors

# nice way to compare functions without copying and pasting the timing code
functions = [get_factors,ross_factors]

#n = 7405814774826
n = 806095675586097
#n = 379065191139531
for f in functions:
    print ( f )
    start = time.time()
    factors = f(n)
    time_taken = time.time()-start
    print ( factors ) # visual check that they give the same answer
    print ( round(time_taken,2),"s" )

