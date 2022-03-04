import matplotlib.pyplot as plt
from users import User, move_users
from search import upper_bound_search
from plotting import Cell, Plot
from time import perf_counter
from gif import create_gif

# Circular Cell
cell = Cell(radius=1)

# Create users
num_users = 1
user = User()
user_list = [user]

# Create plot of cell with borders and add users
plot = Plot(cell)
plot.add_users(users=user_list)

# Search for each user
beam = upper_bound_search(cell, user_list, beam_count=18)
plt.savefig('../output/up_0.png')
beams = [beam]
# Plot the beam where the user is found
plot.add_beams(beams)


# Add some brownian motion to the users
# Total time
total_time = 5.0
# Number of steps
num_steps = 50

for user in user_list:
    user.create_path(total_time, num_steps)

search_time = 0
for step in range(num_steps):
    # Remove old beams and users from plot
    plot.clear_beams()
    plot.clear_users()

    # Move each user and replot
    move_users(user_list, step)
    plot.append_user_path(user_list, num_steps=step)
    plot.add_users(users=user_list)

    # Cast beams to search for users and plot
    start = perf_counter()
    beam = upper_bound_search(cell, user_list, beam_count=18)
    stop = perf_counter()
    search_time += stop - start
    beams = [beam]
    plot.add_beams(beams)
    plt.savefig(f'../output/up_{step}.png')
    plt.pause(0.1)

print(f"Avg. search time for upper_bound_search: {search_time/num_steps}")
create_gif(f'upper_contiguous_search{num_users}')
plot.show()
