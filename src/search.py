from re import T
import numpy as np
from users import User, UserError
from beam import Beam
from typing import Union, Sequence
from plotting import Cell

def send_beam(beam: Beam, users: Union[User, Sequence[User]], cell_radius):
    ack = 0
    if isinstance(user, Sequence):
        for user in users:
            if (user.theta >= beam.start_angle) and (user.theta <= beam.end_angle) and (user.radius <= cell_radius):
                ack = ack + 1
    elif isinstance(user, User):
        if (users.theta >= beam.start_angle) and (users.theta <= beam.end_angle) and (users.radius <= cell_radius):
            ack = 1
    else:
        raise UserError(f"Can not search for objects of type {type(users)}")
    return ack

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
