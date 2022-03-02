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

def find_overlap(ack_beams: Sequence[Beam], non_ack_beams: Sequence[Beam], beam_count):
    if ack_beams:
        # find the end angle of the first ack beam
        end_angle = ack_beams[0].end_angle
        # find the start angle of the last ack beam
        start_angle = ack_beams[-1].start_angle
        if non_ack_beams:
            if non_ack_beams[-1].end_angle >= end_angle:
                end_angle = non_ack_beams[-1].start_angle
            else:
                start_angle = non_ack_beams[-1].end_angle
        return Beam(start_angle, end_angle)
    else:
        return Beam(2*np.pi - np.pi/beam_count, 2*np.pi)

def exhaustive_search(cell: Cell, users: Union[User, Sequence[User]], beam_count):
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
    ack_beams = []
    non_ack_beams = []
    for i in range(beam_count):
        beam = Beam(i*np.pi/beam_count, np.pi + i*np.pi/beam_count)
        # Check Beam and mark with acknowledgements
        ack = send_beam(beam, users, cell.radius)
        if ack:
            ack_beams.append(beam)
        else:
            non_ack_beams.append(beam)
    
    return find_overlap(ack_beams, non_ack_beams, beam_count)
