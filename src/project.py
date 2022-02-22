import numpy as np
from numpy.random import rand
import matplotlib.pyplot as plt
from users import User, move_users
from search import round_robin_search
from plotting import plot_users, plot_user_path

# Circular Cell
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

# Create and plot starting beams
starting_beam_borders = np.array([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi])

for angle in starting_beam_borders:
    if angle == 2*np.pi:
        break
    ri = 1
    qi = angle
    x = ri*np.cos(qi)
    y = ri*np.sin(qi)
    ax.plot([0, x], [0, y], color='tab:blue')

beams, beam_plots = round_robin_search(starting_beam_borders, r1, user_list, tolerance=0.1, ax=ax)

# Add some brownian motion to the users
# Total time
total_time = 5.0
# Number of steps
num_steps = 20

for user in user_list:
    user.create_path(total_time, num_steps)

for step in range(num_steps):
    for beam_plot in beam_plots:
        beam_plot.remove()
    move_users(user_list, step)
    plot_user_path(user_list, ax, num_steps=step)
    beams, beam_plots = round_robin_search(starting_beam_borders, r1, user_list, tolerance=0.1, ax=ax)
    plt.pause(2)

plot_users(users=user_list, ax=ax)

plt.show()
