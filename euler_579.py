from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import itertools as it

fig1 = plt.figure()
ax1 = fig1.gca(projection='3d')
ax1.set_aspect("equal")

cube_1_vertices = [(0, 0, 0), (3, 0, 0), (0, 3, 0), (0, 0, 3), (0, 3, 3), (3, 0, 3), (3, 3, 0), (3, 3, 3)]

length = 3
#draw cube
for s, e in it.combinations(np.array(cube_1_vertices), 2):
    if np.linalg.norm(np.abs(s-e)) == length:
        ax1.plot3D(*zip(s,e), color="b")

fig2 = plt.figure()
ax2 = fig2.gca(projection='3d')
ax2.set_aspect("equal")

cube_2_vertices = [(0, 2, 2), (1, 4, 4), (2, 0, 3), (2, 3, 0), (3, 2, 5), (3, 5, 2), (4, 1, 1), (5, 3, 3)]

#draw cube
for s, e in it.combinations(np.array(cube_2_vertices), 2):
    if np.linalg.norm(np.abs(s-e)) == length:
        ax2.plot3D(*zip(s,e), color="b")

plt.show()
