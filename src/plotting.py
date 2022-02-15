import numpy as np
from matplotlib.axes import Axes
import matplotlib.patches as mpatches
from users import User
from typing import Union, Sequence

def plot_beam(angles: Sequence, radius, ax: Axes):
    sector = mpatches.Wedge((0.,0.), radius, 
                            np.degrees(angles[0]), 
                            np.degrees(angles[1]), 
                            color=[0, 0.5, 0],  # Make angles green
                            alpha=0.5)  # Make the wedges transparent
    ax.add_patch(sector)

def plot_users(users: Union[User, Sequence[User]], ax: Axes):
    for user in users:
        ax.plot(user.x, user.y, marker='o', c="tab:blue")
