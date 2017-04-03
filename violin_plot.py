# There does exist pandas.read_table which might be 

import seaborn as sns
import numpy as np
import numpy.random as npr
import matplotlib.pyplot as plt
import pandas as pd

seed = 1
npr.seed(seed)

num_samples = 100
num_data_sets = 30
data = np.array([i+npr.randn(num_samples) for i in xrange(num_data_sets)])
print data

labels = []
for i in xrange(num_data_sets):
    labels += ["Drug {}".format(i+1)]*num_samples
print labels

df = pd.DataFrame(columns=["Drug","APD90 (ms)"])
print df

df["Drug"] = labels
df["APD90 (ms)"] = data.flatten()
print df

fig = plt.figure()
ax = sns.violinplot(y="APD90 (ms)",x="Drug",data=df)
ax.set_xlabel('')
labels = ax.get_xticklabels()
plt.setp(labels, rotation=60)

fig2 = plt.figure()
ax2 = sns.violinplot(x="APD90 (ms)",y="Drug",data=df)
ax2.set_ylabel('')


plt.show()
