import numpy as np
from matplotlib.axes import Axes
from statistics import mean
from users import User
from typing import Union, Sequence
from plotting import plot_beam

def search_sector(start_angle, end_angle, users):
    ack = 0
    for user in users:
        if (user.theta >= start_angle) and (user.theta <= end_angle):
            ack = ack + 1
    return ack

def round_robin_search(sectors: np.ndarray, radius, users: Union[User, Sequence[User]], tolerance, ax: Axes):
    sector_list = []
    marked_angles = []
    # Search through sectors once and mark sectors with acknowledgements
    for i in range(0, sectors.size - 1):
        acks = search_sector(sectors[i], sectors[i+1], users)
        if acks != 0:
            marked_angles.append((sectors[i], sectors[i+1], acks))
    sector_list = marked_angles

    # Divide and search sectors until sector width tolerance is met
    while sector_list[0][1] - sector_list[0][0] > tolerance:
        marked_angles = []
        for start_angle, end_angle, acks in sector_list:
            # Divide angles into 2 angles
            mid_angle = mean([start_angle, end_angle])
            acks1 = search_sector(start_angle, mid_angle, users)
            acks2 = search_sector(mid_angle, end_angle, users)
            if acks1:
                marked_angles.append((start_angle, mid_angle, acks1))
            if acks2:
                marked_angles.append((mid_angle, end_angle, acks2))
        sector_list = marked_angles

    for start_angle, end_angle, _ in sector_list:
        # Plot the beam where the user is found
        plot_beam((start_angle, end_angle), radius, ax)
    print(sector_list)
    return sector_list
