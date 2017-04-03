import numpy as np
import numpy.random as npr
import statsmodels.api as sm
from statsmodels.sandbox.regression.predstd import wls_prediction_std
import matplotlib.pyplot as plt

seed = 1
npr.seed(seed)

start = 0
end = 10
num_pts = 40
constant = 0

x = np.linspace(start,end,num_pts)
true_params = np.array([1,2,3,2.5]) # ascending powers of x
true_features = np.array([x**p for p in xrange(len(true_params))]).T

y = np.dot(true_features,true_params) + npr.randn(num_pts)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(x,y,label='Data')

highest_power_to_fit = 1
fit_features = np.array([x**p for p in xrange(highest_power_to_fit+1)]).T

model = sm.OLS(y,fit_features)
results = model.fit()
params = results.params
prstd, iv_l, iv_u = wls_prediction_std(results)

print results.summary()

fit = results.fittedvalues


ax.plot(x,fit,color='red',label='OLS fit')
ax.plot(x, iv_u, 'r--')
ax.plot(x, iv_l, 'r--')

ax.legend(loc=2)

plt.show()