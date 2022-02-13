import numpy as np
from matplotlib.axes import Axes
import matplotlib.patches as mpatches
from statistics import mean
from users import User
from typing import Union, Sequence

def round_robin_search(sectors: np.ndarray, radius, users: Union[User, Sequence[User]], tolerance, ax: Axes):
    sector_list = []
    for user in users:
        angles = sectors    # Start searching from original sector list
        found = False
        while found == False:    
            for i in range(0, angles.size - 1):
                if (user.theta >= angles[i]) and (user.theta <= angles[i+1]):
                    # Check if beam is within the width tolerance
                    if angles[1]-angles[0] < tolerance:
                        # Plot a wedge for the beam where the user is found
                        sector = mpatches.Wedge((0.,0.), radius, 
                                                np.degrees(angles[i]), 
                                                np.degrees(angles[i+1]), 
                                                color=[0, 0.5, 0],  # Make angles green
                                                alpha=0.5)  # Make the wedges transparent
                        ax.add_patch(sector)
                        found = True
                        sector_list.append((angles[i], angles[i+1]))
                    angles = np.array([angles[i], mean([angles[i], angles[i+1]]), angles[i+1]])  # Divide sector in half to search again
                    break
    print(sector_list)
    return sector_list

def plot_users(users: Union[User, Sequence[User]], ax: Axes):
    for user in users:
        ax.plot(user.x, user.y, marker='o', c="tab:blue")
