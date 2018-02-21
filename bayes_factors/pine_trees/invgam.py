import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import invgamma

a = 3
b = 1./(2*300**2)

scale = b

x = np.linspace(1,5,10001)
y = invgamma.pdf(x,a=a,scale=scale)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(x,y)
plt.show()
