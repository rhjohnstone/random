import seaborn as sns
sns.set_style("whitegrid")
import matplotlib.pyplot as plt
import numpy as np
import numpy.random as npr
import pandas as pd

gridshape = (5,4)

fig = plt.figure()

colours = ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c','#fdbf6f','#ff7f00','#cab2d6','#6a3d9a'] # from brewer

# big axis at top
# you could refine this to get any (rational) size axis you want, I think
ax1 = plt.subplot2grid(gridshape, (0, 1), rowspan=2, colspan=2)

axes = {}
for i in xrange(10):
    col = i%4
    row = i/4+2
    #print row,col
    if (col==0) and (row==2):
        axes[(row,col)] = plt.subplot2grid(gridshape, (row, col))
    elif (row==2):
        axes[(row,col)] = plt.subplot2grid(gridshape, (row, col),sharey=axes[(row,0)])
    elif (col==0):
        axes[(row,col)] = plt.subplot2grid(gridshape, (row, col),sharex=axes[(2,col)])
    else:
        axes[(row,col)] = plt.subplot2grid(gridshape, (row, col),sharex=axes[(2,col)],sharey=axes[(row,0)])
        
    if (col>0):
        plt.setp(axes[(row,col)].get_yticklabels(), visible=False)
    if (0<=col<=1) and (row<4):
        plt.setp(axes[(row,col)].get_xticklabels(), visible=False)
    if (2<=col<=3) and (row<3):
        plt.setp(axes[(row,col)].get_xticklabels(), visible=False)
        
    axes[(row,col)].plot(npr.randn(col+5),color=colours[i])
   
   

df = pd.DataFrame(columns=["axis","value","other"])
df["axis"] = range(10)+range(10)
df["value"] = np.concatenate((npr.randn(10),npr.randn(10)+1))
df["other"] = ["P1"]*10+["P2"]*10

print df

sns.swarmplot(y=df["value"],ax=ax1,hue=df["axis"],palette=colours,x=df["other"])

ax1.set_ylabel("")
ax1.set_xlabel("")
ax1.legend_.remove()

#fig.tight_layout()#pad=0.4, w_pad=0.5, h_pad=1.0)
plt.show(block=True)


