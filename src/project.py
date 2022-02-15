import numpy as np
from numpy.random import rand
import matplotlib.pyplot as plt
from users import User
from search import round_robin_search
from plotting import plot_users

# Circle
r1 = 1
q1 = np.linspace(0,2*np.pi,50)
x1 = r1*np.cos(q1)
y1 = r1*np.sin(q1)

num_users = 10
user_list = []
for _ in range(num_users):
    user_list.append(User())

# Plot Cell and Users
fig, ax = plt.subplots()
ax.plot(x1, y1, color='tab:blue')
plot_users(users=user_list, ax=ax)

# ax.plot(xu, yu, marker='o')

# Create and plot starting sectors
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
sectors = round_robin_search(sectors, r1, user_list, tolerance=0.1, ax=ax)

plt.show()
