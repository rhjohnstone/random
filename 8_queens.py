import numpy as np
import itertools as it
import time

# Only considering the first 4 columns in the first row
# By symmetry, we then double the result

start = time.time()
success = 0
perms = it.permutations(range(1,8))
first_row_cols = range(4)
for perm in perms:
    for first_col in xrange(4):
        p = list(perm)
        p.insert(first_col,0)
        works = True
        board = np.zeros((8,8),dtype=int)
        for i,j in enumerate(p):
            board[i,j] = 1
        reversed_board = board[::-1,:]
        for k in xrange(-7,8):
            if (np.sum(np.diag(board,k))>1) or (np.sum(np.diag(reversed_board,k))>1):
                works = False
                break
        if works:
            #print board,"\n"
            success += 1
success *= 2 # by symmetry
time_taken = time.time()-start
    
print success
print "Time taken: {} s".format(round(time_taken,2))
