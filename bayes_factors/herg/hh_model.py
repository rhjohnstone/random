from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
import cma
import scipy.io as sio


def model_1(y, t, k1, k2, k3, k4):
    C, O, IO = y
    IC = 1 - C - O - IO
    dCdt = -(k1+k3)*C + k2*O + k4*IC
    dOdt = -(k2+k3)*O + k1*C + k4*IO
    dIOdt = -(k2+k4)*IO + k3*O + k1*IC
    return [dCdt, dOdt, dIOdt]


def jac_1(y, t, k1, k2, k3, k4):
    ddCdtdy = [-(k1+k3+k4), k2-k4, -k4]
    ddOdtdy = [k1, -(k2+k3), k4]
    ddIOdtdy = [-k1, k3-k1, -(k2+k4+k1)]
    return [ddCdtdy, ddOdtdy, ddIOdtdy]


def model_2(y, t, k1, k2, k3, k4):
    C, O = y
    dCdt = -k1*C + k2*O
    dOdt = -(k2+k3+k4)*O + (k1-k4)*C + k4
    return [dCdt, dOdt]


def jac_2(y, t, k1, k2, k3, k4):
    C, O = y
    ddCdtdy = [-k1, k2]
    ddOdtdy = [-(k2+k3+k4), k1-k4]
    return [ddCdtdy, ddOdtdy]


def compute_ks(V, P1, P2, P3, P4, P5, P6, P7, P8):
    k1 = P1 * np.exp(P2*V)
    k2 = P3 * np.exp(-P4*V)
    k3 = P5 * np.exp(P6*V)
    k4 = P7 * np.exp(-P8*V)
    return k1, k2, k3, k4


def sum_of_square_diffs(x, model):
    if np.any(x <= 0):
        return 1e9
    else:
        temp_O_soln = solve_model_for_O(model, x)
        temp_current = G_Kr * temp_O_soln * (V_trace-E_K)
        return np.sum((temp_current-expt_current)**2)


def solve_model_for_O(model, params):
    P1, P2, P3, P4, P5, P6, P7, P8 = params
    if model == 1:
        y0 = np.array([1., 0., 0.])
        model_f = model_1
        jac_f = jac_1
    elif model == 2:
        y0 = np.array([1., 0.])
        model_f = model_2
        jac_f = jac_2
    model_soln = np.zeros((num_pts, len(y0)))
    model_soln[0, :] = np.copy(y0)
    for step in xrange(num_pts - 1):
        t = t_trace[step:step + 2]
        k1, k2, k3, k4 = compute_ks(V_trace[step], P1, P2, P3, P4, P5, P6, P7, P8)
        step_sol = odeint(model_f, y0, t, args=(k1, k2, k3, k4),
                             Dfun=jac_f)  # not sure if Dfun speeds up or slows down
        model_soln[step + 1, :] = step_sol[1]
        y0 = step_sol[1]
    return model_soln[:, 1]


expt_mat = sio.loadmat('sine_wave_16713110_dofetilide_subtracted_leak_subtracted.mat')
expt_current = expt_mat['T'][:, 0]

num_pts = len(expt_current)
solve_start = 0.
solve_end = 8000.
t_trace = np.linspace(solve_start, solve_end, num_pts)
V_trace = 1.*np.ones(num_pts)

step_durs = [250, 50, 200, 1000, 500, 1000, 3500, 500, 1000]
step_Vs = [-80, -120, -80, 40, -120, -80, 0, -120, -80]

step_start = 0
step_end = 0
for i in xrange(len(step_durs)):
    step_end += step_durs[i]
    indices = np.where((t_trace > step_start) & (t_trace <= step_end))
    V_trace[indices] *= step_Vs[i]
    step_start = step_end
V_trace[0] = step_Vs[0]


A1 = 54
A2 = 26
A3 = 10
w1 = 0.007/(2*np.pi)
w2 = 0.037/(2*np.pi)
w3 = 0.19/(2*np.pi)

t_offset = 2500.
sine_V = (-30. +
           A1*np.sin(2*np.pi*w1*(t_trace-t_offset)) +
           A2*np.sin(2*np.pi*w2*(t_trace-t_offset)) +
           A3*np.sin(2*np.pi*w3*(t_trace-t_offset)))

V_trace[np.where(V_trace == 0)] = sine_V[np.where(V_trace == 0)]

G_Kr = 0.1524

R = 8314.
K_i = 130.
k_o = 4.
T = 294.6
F = 96485.33289

E_K = ((R*T)/F)*np.log(k_o/K_i)

print "E_K =", E_K

"""fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(t_trace, V_trace)
ax.set_xlabel("Time (ms)")
ax.set_ylabel("Voltage (mV)")
plt.show()"""

P1, P2, P3, P4, P5, P6, P7, P8 = 2.26e-4, 0.0699, 3.45e-5, 0.05462, 0.0873, 8.92e-3, 5.15e-3, 0.03158

model = 1
O = solve_model_for_O(model, (P1, P2, P3, P4, P5, P6, P7, P8))

O_2 = solve_model_for_O(2, (P1, P2, P3, P4, P5, P6, P7, P8))

I_Kr = G_Kr * O * (V_trace-E_K)

I_Kr_2 = G_Kr * O_2 * (V_trace-E_K)

#plt.plot(t_trace,O)
#plt.show()

fig = plt.figure()
ax = fig.add_subplot(312)
ax.grid()
#for i in xrange(3):
    #ax.plot(t_trace, solved_traces[:, i], label=labels[i])
ax.plot(t_trace/1000., I_Kr, label=r"$M_1, I_{Kr}$")
ax.legend(loc=4)

ax3 = fig.add_subplot(313)
ax3.grid()
ax3.plot(t_trace/1000., I_Kr_2, label=r"$M_2, I_{Kr}$")
ax3.legend(loc=4)

ax2 = fig.add_subplot(311)
ax2.plot(t_trace/1000., V_trace)
ax2.grid()
ax3.set_xlabel("Time (s)")
ax2.set_xticklabels([])
ax.set_xticklabels([])
ax.set_ylabel('Current (nA)')
ax3.set_ylabel('Current (nA)')
ax2.set_ylabel('Voltage (mV)')
ax.plot(t_trace/1000., expt_current, color='red', label='Expt')
ax3.plot(t_trace/1000., expt_current, color='red', label='Expt')
fig.tight_layout()
plt.show(block=True)


"""data_fig = plt.figure()
data_ax = data_fig.add_subplot(111)

data_ax.plot(t_trace, expt_current)
data_fig.tight_layout()

plt.show(block=True)"""


model = 1
x0 = np.array([P1, P2, P3, P4, P5, P6, P7, P8])
sigma0 = 0.01
opts = cma.CMAOptions()
es = cma.CMAEvolutionStrategy(x0, sigma0, opts)
while not es.stop():
    X = es.ask()
    f_vals = [sum_of_square_diffs(x, model) for x in X]
    es.tell(X, f_vals)
    es.disp()
res = es.result()

best_fit_params = res[0]
best_fit = solve_model_for_O(model, best_fit_params)
I_Kr = G_Kr * best_fit * (V_trace-E_K)
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(t_trace/1000., I_Kr, color='blue', label='Best fit')
ax.plot(t_trace/1000., expt_current, color='red', label='Expt')
fig.tight_layout()
plt.show(block=True)
