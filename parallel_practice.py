import multiprocessing as mp
import time
import numpy as np


def f(n):
    """Any function you want, add more operations / increase computation time to see parallel benefits"""
    return np.sqrt(np.abs(np.sin(n))) + np.cos(n)


def sum_f_in_sequence(n):
    """Compute each f(i) in series and add as you go along"""
    total = 0.
    for i in xrange(1,n+1):
        total += f(i)
    return total


def do_f_in_parallel_then_sum(n):
    """Compute the f(i)s in parallel and then sum"""
    num_processors = mp.cpu_count()-1  # never use all CPUs - too resource-heavy
    pool = mp.Pool(num_processors)  # start the processes
    squares = pool.map(f, xrange(1,n+1))  # the actual call to solve f in parallel
    pool.close()  # not entirely sure what these two lines do, but good practice
    pool.join()  # not entirely sure what these two lines do, but good practice
    return sum(squares)
    
    
def do_all_in_numpy(n):
    """Can do a vectorised version in numpy"""
    return np.sum(f(np.arange(1,n+1)))
    

if __name__ == '__main__':  # good practice to prevent some kind of recursive problems, but not entirely sure what

    functions_to_time = [sum_f_in_sequence, do_f_in_parallel_then_sum, do_all_in_numpy]
    function_names = ["sum_f_in_sequence", "do_f_in_parallel_then_sum", "do_all_in_numpy"]

    N = 5000000

    print "\n"
    for i in xrange(len(functions_to_time)):
        current_f = functions_to_time[i]
        print function_names[i]
        try:
            start = time.time()
            temp_sum = current_f(N)
            temp_tt = time.time()-start
            print "sum =", temp_sum
            print "time taken: {} s\n".format(round(temp_tt,1))
        except:
            print "Failed for some reason\n"

