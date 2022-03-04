import matplotlib.pyplot as plt
from users import User, move_users
from search import exhaustive_search
from plotting import Cell, Plot
from time import perf_counter
from gif import create_gif

# Circular Cell
cell = Cell(radius=1)

# Create users
num_users = 1
user_list = []
for _ in range(num_users):
    user_list.append(User())

# Create plot of cell with borders and add users
plot = Plot(cell)
plot.add_users(users=user_list)

# Search for each user
beams = exhaustive_search(cell, user_list, beam_count=36)
# Plot the beam where the user is found
plot.add_beams(beams)
plt.savefig('../output/exh_0.png')


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
    beams = exhaustive_search(cell, user_list, beam_count=36)
    stop = perf_counter()
    search_time += stop - start
    plot.add_beams(beams)
    plt.pause(0.1)
    plt.savefig(f'../output/exh_{step+1}.png')

print(f"Avg. search time for exhaustive search: {search_time/num_steps}")
create_gif(f'exhaustive_search{num_users}')
plot.show()
