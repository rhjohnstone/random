import string
import matplotlib.pyplot as plt
import collections

alphabet = string.ascii_lowercase

freqs = "e t a o i n s r h l d c u m f p g w y b v k x j q z".split()

seq = [1,2,3,4,5,6,7,3,8,4,9,10,8,9,11,3,4,1,2,3,4,12,13,14,3,15,8,4,13,16,4,6,4,17,13,13,18,4,6,15,3,4,15,3,16,3,15,15,3,11,4,1,13,4,6,8,4,3,10,11,5,6,5,3,15,8,4,3,14,3,10,4,1,2,3,4,13,10,3,8,4,6,1,4,1,2,3,4,16,15,13,10,1]
counter=collections.Counter(seq)

print seq, "\n"

how_many = 3
trip_count = {}
for i in xrange(len(seq)-how_many):
    try:
        trip_count[tuple(seq[i:i+how_many])] += 1
    except:
        trip_count[tuple(seq[i:i+how_many])] = 1
        
for i in xrange(2,len(seq)-7):
    if (seq[i]==seq[i+4]):
        print seq[i-2:i+5]
        
for i in trip_count:
    if (trip_count[i]>1):
        print i, trip_count[i]
        
print trip_count

keys_counts = counter.most_common()
print keys_counts

minn = 1
maxx = max(seq)

possible_doubles = ["b","c","d","e","f","g","l","m","n","o","p","r","s","t","u","v","z"]

"""
fig = plt.figure()
ax = fig.add_subplot(111)
ax.grid()
ax.hist(seq,bins=range(minn,maxx+2))
plt.show(block=True)
"""

new_letters = {}

#for i in xrange(5):
    #new_letters[keys_counts[i][0]] = freqs[i] 11, 3, 4, 1, 2, 3, 4
    

new_letters[1] = "t"
new_letters[2] = "h"
new_letters[3] = "e"
new_letters[4] = "."
new_letters[13] = "o"
new_letters[16] = "f"
new_letters[6] = "a"
new_letters[8] = "s"
new_letters[11] = "d"
new_letters[10] = "n"
new_letters[9] = "i"
new_letters[5] = "p"
new_letters[7] = "g"
new_letters[17] = "b"
new_letters[18] = "k"
new_letters[12] = "c"
new_letters[14] = "v"
new_letters[15] = "r"
    
new_str = ""
for i in xrange(len(seq)):
    try:
        new_str += new_letters[seq[i]]
    except:
        new_str += str(seq[i])
    new_str += " "
    
print "\n", new_str, "\n"

print ' '.join(''.join(new_str.split()).split('.'))









