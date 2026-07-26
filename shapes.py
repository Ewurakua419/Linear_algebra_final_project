import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from typing import cast
cube = np.array([
    [0, 0, 0],
    [1, 0, 0],
    [1, 1, 0],
    [0, 1, 0],
    [0, 0, 1],
    [1, 0, 1],
    [1, 1, 1],
    [0, 1, 1]
])

pyramid = np.array([
    [0, 0, 0],
    [2, 0, 0],
    [2, 2, 0],
    [0, 2, 0],
    [1, 1, 2]   # Apex
])

house = np.array([
    # Base 
    [0,0,0],
    [2,0,0],
    [2,2,0],
    [0,2,0],
    [0,0,2],
    [2,0,2],
    [2,2,2],
    [0,2,2],

    # Roof 
    [1,0,3],
    [1,2,3]
])

robot = np.array([
    # Head
    [1,1,5],
    [2,1,5],
    [2,2,5],
    [1,2,5],
    [1,1,6],
    [2,1,6],
    [2,2,6],
    [1,2,6],

    # Body
    [0.5,0.5,2],
    [2.5,0.5,2],
    [2.5,2.5,2],
    [0.5,2.5,2],
    [0.5,0.5,5],
    [2.5,0.5,5],
    [2.5,2.5,5],
    [0.5,2.5,5],

    # Arms
    [-0.5,1.5,4],
    [3.5,1.5,4],

    # Hands
    [-1.0,1.5,3],
    [4.0,1.5,3],

    # Legs
    [1.0,1.0,0],
    [1.0,1.0,2],
    [2.0,1.0,0],
    [2.0,1.0,2]
])

airplane = np.array([
    # Nose
    [5,0,0],

    # Fuselage
    [0,0,0],
    [1,0,0],
    [2,0,0],
    [3,0,0],
    [4,0,0],

    # Wings
    [2,-3,0],
    [2,3,0],
    [3,-2,0],
    [3,2,0],

    # Tail
    [0,-1,0],
    [0,1,0],

    # Vertical stabilizer
    [0,0,1.5],

    # Horizontal stabilizers
    [0,-2,0],
    [0,2,0]
])
edges = [
    (0,1), (1,2), (2,3), (3,0),   # Bottom square
    (4,5), (5,6), (6,7), (7,4),   # Top square
    (0,4), (1,5), (2,6), (3,7)    # Vertical edges
]
'''fig = plt.figure(figsize=(12,12))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(cube[:,0],cube[:,1],cube[:,2])
for start, end in edges:
    ax.plot(
        [cube[start,0], cube[end,0]],
        [cube[start,1], cube[end,1]],
        [cube[start,2], cube[end,2]],
        linewidth=2
    )'''
R = np.array([#along yz plane
    [-1, 0,0],
    [0,1,0],[0,0,1]
])
#oreflect = R @ cube

'''ax.scatter(cube[:,0],cube[:,1],cube[:,2])
for start, end in edges:
    ax.plot(
        [oreflect[start,0], oreflect[end,0]],
        [oreflect[start,1], oreflect[end,1]],
        [oreflect[start,2], oreflect[end,2]],
        linewidth=7
    )'''
cube= np.ones((3,3,3),dtype='bool')
fig = plt.figure()
ax = cast(Axes3D, fig.add_subplot(111, projection="3d"))
# use add_subplot to ensure a 3D Axes3D instance (has voxels)
#ax = plt.axes(projection='3d')
ax.set_facecolor("Cyan")
ax.voxels(cube, facecolor="#E02050", edgecolors='k')
ax.axis('off')

plt.show();