from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
import time


def f(y, t, k1, k2, k3, k4):
    C, O, IO = y
    IC = 1 - C - O - IO
    dCdt = -(k1+k3)*C + k2*O + k4*IC
    dOdt = -(k2+k3)*O + k1*C + k4*IO
    dIOdt = -(k2+k4)*IO + k3*O + k1*IC
    return [dCdt, dOdt, dIOdt]


def jac(y, t, k1, k2, k3, k4):
    ddCdtdy = [-(k1+k3+k4), k2-k4, -k4]
    ddOdtdy = [k1, -(k2+k3), k4]
    ddIOdtdy = [-k1, k3-k1, -(k2+k4+k1)]
    return [ddCdtdy, ddOdtdy, ddIOdtdy]


def compute_ks(V, P1, P2, P3, P4, P5, P6, P7, P8):
    k1 = P1 * np.exp(P2*V)
    k2 = P3 * np.exp(-P4*V)
    k3 = P5 * np.exp(P6*V)
    k4 = P7 * np.exp(-P8*V)
    return k1, k2, k3, k4


num_pts = 1001
solve_start = 0
solve_end = 5
t_trace = np.linspace(solve_start, solve_end, num_pts)

step_start = 2
step_end = 3

step_indices = np.where((step_start <= t_trace) & (t_trace <= step_end))

V_trace = 0.*np.ones(num_pts)
V_trace[step_indices] = 10.
#plt.plot(V_trace)
#plt.show()

y0 = [1., 0., 0.]
solved_traces = np.zeros((num_pts, len(y0)))
solved_traces[0,:] = y0

P1, P2, P3, P4, P5, P6, P7, P8 = 1, 1, 1, 1, 1, 1, 1, 1

start = time.time()
for step in xrange(num_pts-1):
    t = t_trace[step:step+2]
    k1, k2, k3, k4 = compute_ks(V_trace[step], P1, P2, P3, P4, P5, P6, P7, P8)
    sol = odeint(f, y0, t, args=(k1, k2, k3, k4), Dfun=jac)  # not sure if Dfun speeds up or slows down
    solved_traces[step, :] = sol[1]
    y0 = sol[1]
time_taken = time.time()-start
#print solved_traces

print "Time taken: {} s".format(round(time_taken,1))

fig = plt.figure()
ax = fig.add_subplot(111)
ax.grid()
ax.plot(t_trace, solved_traces)
plt.show()