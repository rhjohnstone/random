import numpy as np
import vigenere as vg
import matplotlib.pyplot as plt
import collections

front_txt = '01_front_cover.txt'
back_txt = '02_back_cover.txt'

matrix_shape = (26,12)

front = np.zeros(matrix_shape,dtype=str)
back = np.zeros(matrix_shape,dtype=str)


front_str = ""
with open(front_txt,'r') as infile:
    for i,line in enumerate(infile):
        front_str += line[:-1]
        front[i,:] = [x for x in line[:-1]]
        
back_str = ""
with open(back_txt,'r') as infile:
    for i,line in enumerate(infile):
        back_str += line[:-1]
        back[i,:] = [x for x in line[:-1]]
        
print front_str
front_count = collections.Counter(front_str)
print front_count

freqs = "e t a o i n s r h l d c u m f p g w y b v k x j q z".split()

new_letters = {}

new_str = ""
for i in front_str:
    if (i==" "):
        new_str += "E"
    elif (i=="S"):
        new_str += "T"
    elif (i=="T"):
        new_str += "A"
    elif (i=="V"):
        new_str += "O"
    elif (i=="J"):
        new_str += "I"
    elif (i=="U"):
        new_str += "N"
    elif (i=="F"):
        new_str += "S"
    else:
        new_str += "."
    
print "\n", new_str, "\n"
        
"""print front
print back

front_bool = np.zeros(matrix_shape,dtype=int)
front_bool[np.where(front!=" ")] = 1
print front_bool

back_bool = np.zeros(matrix_shape,dtype=int)
back_bool[np.where(back!=" ")] = 1
print back_bool


plt.matshow(np.hstack((front_bool,back_bool)),cmap=plt.cm.gray)
plt.show(block=True)"""

#v = vg.Vigenere()
#key_maybe = "zachary quinto"
#for i in xrange(len(key_maybe)):
#    print v.decode(front_str,key_maybe),"\n"
#    key_maybe = key_maybe[1:]+key_maybe[0]
