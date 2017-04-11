import doseresponse as dr
import matplotlib.pyplot as plt

model = 2
dr.define_model(model)


for i in xrange(dr.num_params):
    fig = plt.figure(figsize=(5, 4))
    ax = fig.add_subplot(111)
    ax.plot(dr.prior_xs[i], dr.prior_pdfs[i])
    ax.grid()
    ax.set_ylabel('Prior pdf')
    ax.set_xlabel(dr.labels[i])
    fig.tight_layout()
plt.show()
