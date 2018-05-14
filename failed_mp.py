import multiprocessing as mp
import sys


def f(x):
    if x==5:
        sys.exit("x=5")
    return x**2
    

a = range(6)
pool = mp.Pool(2)
b = pool.map(f, a)
pool.close()
pool.join()

print b

