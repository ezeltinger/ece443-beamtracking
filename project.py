import numpy as np
from numpy.random import rand
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from statistics import mean

def binary_search_sectors(sectors, radius, user_angle, ax):
    for i in range(0, sectors.size - 1):
        if (user_angle >= sectors[i]) and (user_angle <= sectors[i+1]):
            print(f"{sectors[i]} to {sectors[i+1]}")
            sector = mpatches.Wedge((0.,0.), radius, np.degrees(sectors[i]), np.degrees(sectors[i+1]), color=[rand(), rand(), rand()], alpha=0.5)
            ax.add_patch(sector)
            divided_sectors = np.array([sectors[i], mean([sectors[i], sectors[i+1]]), sectors[i+1]])
            break
    return divided_sectors

# Circle
r1 = 1
q1 = np.linspace(0,2*np.pi,50)
x1 = r1*np.cos(q1)
y1 = r1*np.sin(q1)

# Users
ru = rand()
qu = 2*np.pi*rand()
xu = ru*np.cos(qu)
yu = ru*np.sin(qu)

fig, ax = plt.subplots()
ax.plot(x1, y1, color='tab:blue')
ax.plot(xu, yu, marker='o')

sector_borders = np.array([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi])

for angle in sector_borders:
    if angle == 2*np.pi:
        break
    ri = 1
    qi = angle
    x = ri*np.cos(qi)
    y = ri*np.sin(qi)
    ax.plot([0, x], [0, y], color='tab:blue')

sectors = sector_borders
level = 0
while sectors[1]-sectors[0] > 0.1:
    sectors = binary_search_sectors(sectors, r1, qu, ax)
    level += 1

print(f"Searched {level} levels")

plt.show()
