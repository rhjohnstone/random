import doseresponse as dr
import matplotlib.pyplot as plt

model = 2
dr.define_model(model)

plt.plot(dr.prior_xs[0], dr.prior_pdfs[0])
plt.show()