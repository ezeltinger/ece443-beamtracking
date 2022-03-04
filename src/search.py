from re import T
import numpy as np
from users import User, UserError
from beam import Beam
from typing import Union, Sequence
from plotting import Cell

def send_beam(beam: Beam, users: Union[User, Sequence[User]], cell_radius):
    ack = 0
    if isinstance(users, Sequence):
        for user in users:
            if (user.theta >= beam.start_angle) and (user.theta <= beam.end_angle) and (user.radius <= cell_radius):
                ack = ack + 1
    elif isinstance(users, User):
        if (users.theta >= beam.start_angle) and (users.theta <= beam.end_angle) and (users.radius <= cell_radius):
            ack = 1
    else:
        raise UserError(f"Can not search for objects of type {type(users)}")
    return ack

def find_beam(beam_ack_list: Sequence[Beam], beam_count):
    # Check for acks
    if [beam_ack for beam_ack in beam_ack_list if beam_ack[1] == 1]:
        # start with the case where all beams return an ack
        start_angle = beam_ack_list[-1][0].start_angle
        end_angle = beam_ack_list[0][0].end_angle
        # We can't change ack state until we've tried more than one beam
        last_ack = beam_ack_list[0][1]
        for beam, ack in beam_ack_list:
            if ack == last_ack:
                last_ack == ack
                last_beam = beam
            else:
                if last_ack == 1:
                    start_angle = last_beam.start_angle
                    end_angle = beam.start_angle
                    break
                else:
                    start_angle = last_beam.end_angle
                    end_angle = beam.end_angle
                    break
        return Beam(start_angle, end_angle)
    else: # There are no acks
        return Beam(2*np.pi - np.pi/beam_count, 2*np.pi)

def exhaustive_search(cell: Cell, users: Union[User, Sequence[User]], beam_count):
    """
    An algorithm to exhaustively search the cell for users.
    Uncertainty region is always 2pi/beam_count
    """
    beam_width = 2*np.pi/beam_count
    beam_list = []
    
    # create beam_list from beam_count
    for b in range(beam_count):
        beam = Beam(b*beam_width, (b+1)*beam_width)
        # Check Beam and mark with acknowledgements
        acks = send_beam(beam, users, cell.radius)
        if acks != 0:
            beam_list.append(beam)

    return beam_list

def upper_bound_search(cell: Cell, users: User, beam_count):
    """
    An algorithm to search for a single user with contiguous beams.
    The uncertainty region for this method is pi/beam_count.
    This models the upper bound of possible uncertainty regions for contiguous beams.
    """
    beam_ack_list = []
    for i in range(beam_count):
        beam = Beam(i*np.pi/beam_count, np.pi + i*np.pi/beam_count)
        # Check Beam and mark with acknowledgements
        ack = send_beam(beam, users, cell.radius)
        beam_ack_list.append((beam, ack))
    
    return find_beam(beam_ack_list, beam_count)
