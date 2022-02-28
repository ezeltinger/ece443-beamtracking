import numpy as np
from numpy.random import rand
import matplotlib.pyplot as plt
from users import User, move_users
from search import round_robin_search
from plotting import Cell, Plot

# Circular Cell
cell = Cell(1) # Radius 1

#Create users
num_users = 2
user_list = []
for _ in range(num_users):
    user_list.append(User())

# Create plot of cell with borders and add users
plot = Plot(cell)
plot.add_users(users=user_list)

# Search for each user
beams = round_robin_search(cell, user_list, tolerance=0.1)
# Plot the beam where the user is found
plot.add_beams(beams)


# Add some brownian motion to the users
# Total time
total_time = 5.0
# Number of steps
num_steps = 200

for user in user_list:
    user.create_path(total_time, num_steps)

for step in range(num_steps):
    # Remove old beams and users from plot
    plot.clear_beams()
    plot.clear_users()

    # Move each user and replot
    move_users(user_list, step)
    plot.append_user_path(user_list, num_steps=step)
    plot.add_users(users=user_list)

    # Cast beams to search for users and plot
    beams = round_robin_search(cell, user_list, tolerance=0.1)
    plot.add_beams(beams)
    plt.pause(0.1)


plot.show()
