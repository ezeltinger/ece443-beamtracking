import numpy as np
from matplotlib.axes import Axes
import matplotlib.patches as mpatches
from users import User
from typing import Union, Sequence

def plot_beam(angles: Sequence, radius, ax: Axes):
    beam = mpatches.Wedge((0.,0.), radius, 
                            np.degrees(angles[0]), 
                            np.degrees(angles[1]), 
                            color=[0, 0.5, 0],  # Make angles green
                            alpha=0.5)  # Make the wedges transparent
    ax.add_patch(beam)
    return beam

def plot_beams(beam_list, cell_radius, ax):
    beam_plots = []
    for start_angle, end_angle, _ in beam_list:
        beam = plot_beam((start_angle, end_angle), cell_radius, ax)
        beam_plots.append(beam)
    return beam_plots

def plot_users(users: Union[User, Sequence[User]], ax: Axes):
    user_plots = []
    for user in users:
        user_plot = ax.plot(user.x, user.y, marker='o', c="tab:blue")
        user_plots.append(user_plot)
    return user_plots

def plot_user_path(users: Union[User, Sequence[User]], ax: Axes, num_steps=None):
    if num_steps is not None:
        num_steps = num_steps + 1
    path_plots = []
    for user in users:
        path_plot = ax.plot(user.path[0, 0:num_steps], user.path[1, 0:num_steps])
        path_plots.append(path_plot)
        # ax.plot(user.path[0,0], user.path[1,0], 'go')
        # ax.plot(user.path[0,num_steps], user.path[1,num_steps], 'ro')
    return path_plots
