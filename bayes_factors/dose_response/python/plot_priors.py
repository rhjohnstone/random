import doseresponse as dr
import matplotlib.pyplot as plt
import os

model = 2
dr.define_model(model)
fsize = 14
priors_fig_dir = '../output/priors/'
if not os.path.exists(priors_fig_dir):
    os.makedirs(priors_fig_dir)

for i in xrange(dr.num_params):
    fig = plt.figure(figsize=(5, 4))
    ax = fig.add_subplot(111)
    ax.plot(dr.prior_xs[i], dr.prior_pdfs[i], lw=2)
    xlower, xupper = dr.prior_xs[i][[0,-1]]
    ax.set_xlim(xlower, xupper)
    ax.grid()
    if i==0:
        ax.set_xticks(range(int(xlower), int(xupper)+1, 3))
    ax.set_ylabel('Prior pdf', size=fsize)
    ax.set_xlabel(dr.labels[i], size=fsize)
    fig.tight_layout()
    fig.savefig(priors_fig_dir+'{}_prior.pdf'.format(dr.labels[i]))
    plt.close()
