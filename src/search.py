from re import T
import numpy as np
from matplotlib.axes import Axes
from statistics import mean
from users import User
from beam import Beam
from typing import Union, Sequence
from plotting import Cell

def send_beam(beam: Beam, users, cell_radius):
    ack = 0
    for user in users:
        if (user.theta >= beam.angle_one) and (user.theta <= beam.angle_two) and (user.radius <= cell_radius):
            ack = 1
    return ack

def tolerance_met(beam_list: Union[Beam, Sequence[Beam]], tolerance):
    flag = 1
    for beam in beam_list:
        if beam.span() < tolerance:
            flag = 0
    return flag

def round_robin_search(cell: Cell, users: Union[User, Sequence[User]], tolerance):
     # initial beams will be the boarders of the cell
    # Borders of the cell is np.array([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi])
    beam_list: Union[Beam, Sequence[Beam]] = []
    #create beam_list from border angles
    for i in range(0, cell.borders.size - 1):
        beam = Beam(cell.borders[i], cell.borders[i+1])
        
        # Check Beam and mark with acknowledgements
        acks = send_beam(beam, users, cell.radius)
        if acks != 0:
            beam_list.append(beam)
    
    for beam in beam_list:
        print(beam.angle_one, ":", beam.angle_two)

    
    # Divide and search beams until beam width tolerance is met
    while tolerance_met(beam_list, tolerance):
        marked_angles: Sequence[Beam] = []
        
        for beam in beam_list:
            # Divide angles into 2 angles
            lower_beam, upper_beam = beam.split()
            
            print("Next Beam")
            print(lower_beam.angle_one, ":", lower_beam.angle_two)
            print(upper_beam.angle_one, ":", upper_beam.angle_two)

            acks1 = send_beam(lower_beam, users, cell.radius)
            acks2 = send_beam(upper_beam, users, cell.radius)
            if acks1:
                marked_angles.append(lower_beam)
            if acks2:
                marked_angles.append(upper_beam)
        
        beam_list = marked_angles
        print("Next List")

    # Plot the beam where the user is found
    return beam_list
