import numpy as np
from matplotlib.axes import Axes
from statistics import mean
from users import User
from typing import Union, Sequence
from plotting import plot_beams

def send_beam(start_angle, end_angle, users, cell_radius):
    ack = 0
    for user in users:
        if (user.theta >= start_angle) and (user.theta <= end_angle) and (user.radius <= cell_radius):
            ack = ack + 1
    return ack

def round_robin_search(beams: np.ndarray, cell_radius, users: Union[User, Sequence[User]], tolerance, ax: Axes):
    beam_list = []
    marked_angles = []
    # Search through beams once and mark beams with acknowledgements
    for i in range(0, beams.size - 1):
        acks = send_beam(beams[i], beams[i+1], users, cell_radius)
        if acks != 0:
            marked_angles.append((beams[i], beams[i+1], acks))
    beam_list = marked_angles

    # Divide and search beams until beam width tolerance is met
    while beam_list[0][1] - beam_list[0][0] > tolerance:
        marked_angles = []
        for start_angle, end_angle, acks in beam_list:
            # Divide angles into 2 angles
            mid_angle = mean([start_angle, end_angle])
            acks1 = send_beam(start_angle, mid_angle, users, cell_radius)
            acks2 = send_beam(mid_angle, end_angle, users, cell_radius)
            if acks1:
                marked_angles.append((start_angle, mid_angle, acks1))
            if acks2:
                marked_angles.append((mid_angle, end_angle, acks2))
        beam_list = marked_angles

    # Plot the beam where the user is found
    beam_plots = plot_beams(beam_list, cell_radius, ax)
    print(beam_list)
    return beam_list, beam_plots
