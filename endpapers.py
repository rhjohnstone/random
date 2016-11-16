import numpy as np
import vigenere as vg

front_txt = '01_front_cover.txt'
back_txt = '02_back_cover.txt'

matrix_shape = (26,12)

front = np.zeros(matrix_shape,dtype=str)
back = np.zeros(matrix_shape,dtype=str)

front_str = ""
with open(front_txt,'r') as infile:
    for i,line in enumerate(infile):
        front_str += line[:-1]
        
back_str = ""
with open(back_txt,'r') as infile:
    for i,line in enumerate(infile):
        back_str += line[:-1]
        
#print front_str
#print back_str

v = vg.Vigenere()
key_maybe = "zachary quinto"
for i in xrange(len(key_maybe)):
    print v.decode(front_str,key_maybe),"\n"
    key_maybe = key_maybe[1:]+key_maybe[0]
