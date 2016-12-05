import numpy as np
import numpy.random as npr
import matplotlib.pyplot as plt
from matplotlib import ticker

seed = 1
npr.seed(seed)

x = np.linspace(55478, 55486, 100)*1e-10
y = npr.rand(100) - 0.5
y = np.cumsum(y)
y -= y.min()
y *= 1e-8

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(x,y)

scale_pow = 8
def my_formatter_fun(x, p):
    return "%.2f" % (x * (10 ** scale_pow))
ax.get_xaxis().set_major_formatter(ticker.FuncFormatter(my_formatter_fun))
ax.set_xlabel('my label ' + '$10^{{{0:d}}}$'.format(scale_pow))

plt.show(block=True)
