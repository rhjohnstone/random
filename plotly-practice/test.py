import plotly
import plotly.graph_objs as go


def dose_response_model(conc, ic50, hill):
    return 100. * (1. - 1./(1. + (conc/ic50)**hill))

# Create random data with numpy
import numpy as np

N = 100
ic50 = 1.
hill = 1.
x = np.logspace(-3, 3, N)
y = dose_response_model(x, ic50, hill)

# Create a trace
trace = go.Scatter(
    x = x,
    y = y
)
layout = go.Layout(
    xaxis=dict(
        type='log',
        autorange=True
    )
)

data = [trace]

fig = go.Figure(data=data, layout=layout)

plotly.offline.plot(fig)


