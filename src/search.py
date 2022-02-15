import numpy as np
from matplotlib.axes import Axes
from statistics import mean
from users import User
from typing import Union, Sequence
from plotting import plot_beam

def round_robin_search(sectors: np.ndarray, radius, users: Union[User, Sequence[User]], tolerance, ax: Axes):
    sector_list = []
    for user in users:
        angles = sectors    # Start searching from original sector list
        found = False
        while found == False:    
            for i in range(0, angles.size - 1):
                if (user.theta >= angles[i]) and (user.theta <= angles[i+1]):
                    # Check if beam is within the width tolerance
                    if angles[i+1]-angles[i] < tolerance:
                        # Plot the beam where the user is found
                        plot_beam((angles[i], angles[i+1]), radius, ax)
                        found = True
                        sector_list.append((angles[i], angles[i+1]))
                    angles = np.array([angles[i], mean([angles[i], angles[i+1]]), angles[i+1]])  # Divide sector in half to search again
                    break
    print(sector_list)
    return sector_list
