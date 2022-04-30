import numpy as np
from users import User, UserError
from beam import Beam, SplitBeam
from typing import Union, Sequence
from plotting import Cell

def send_beam(beam: Union[Beam, SplitBeam], users: Union[User, Sequence[User]], cell_radius):
    ack = 0
    # Only iterate over users if they are in a sequence
    if isinstance(users, Sequence):
        # TODO - Add support for SplitBeam usage
        # non_contiguous_search() only uses single user at this point
        if isinstance(beam, SplitBeam):
            for partial_beam in beam.partial_beams:
                for user in users:
                    ack = ack + get_ack(partial_beam, user, cell_radius)
        else:
            for user in users:
                ack = ack + get_ack(beam, user, cell_radius)
    else:
        raise UserError(f"Can not search for objects of type {type(users)}. Must be of type Sequence[User]")
    return ack

def get_ack(beam: Beam, user: User, cell_radius):
    ack = 0
    if (user.theta >= beam.start_angle) and (user.theta <= beam.end_angle) and (user.radius <= cell_radius):
        ack = 1
    return ack

def search_timing(beam_count, cell_radius):
    """
    Calculate the amount of time it takes to send each beam and receive the response.
    """
    c = 3e08
    time_delay = cell_radius/c
    search_time = 2*time_delay*beam_count
    return search_time

def find_beam_contiguous(beam_ack_list: Sequence[Beam], beam_count):
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

def _special_sauce(beam: Beam, ack, weird_algorithm_flag):
    if weird_algorithm_flag:
        if ack:
            # User is in the first half of the beam
            weird_algorithm_flag = False
            return Beam(start_angle=beam.start_angle, end_angle=beam.middle), weird_algorithm_flag
        else:
            weird_algorithm_flag = True
            # User is in the second half of the beam
            return Beam(start_angle=beam.middle, end_angle=beam.end_angle), weird_algorithm_flag
    else:
        if not ack:
            # User is in the first half of the beam
            weird_algorithm_flag = False
            return Beam(start_angle=beam.start_angle, end_angle=beam.middle), weird_algorithm_flag
        else:
            # User is in the second half of the beam
            weird_algorithm_flag = True
            return Beam(start_angle=beam.middle, end_angle=beam.end_angle), weird_algorithm_flag

def find_beam_non_contiguous(beam_ack_list):
    ack_bits = []
    ack_quadrant_map = [(3*np.pi/2, 2*np.pi, 4), (np.pi, 3*np.pi/2, 3), (0, np.pi/2, 1), (np.pi/2, np.pi, 2)]
    for _, ack in beam_ack_list:
        ack_bits.append(ack)
    quadrant_index = (ack_bits[0] << 1) + ack_bits[1]
    start_angle, end_angle, quadrant = ack_quadrant_map[quadrant_index]
    quadrant_beam = Beam(start_angle, end_angle)
    if quadrant == 2 or quadrant == 4:
        weird_algorithm_flag = True
    else:
        weird_algorithm_flag = False
    beam, weird_algorithm_flag = _special_sauce(quadrant_beam, ack_bits[2], weird_algorithm_flag)
    
    for ack in ack_bits[3:]:
        beam, weird_algorithm_flag = _special_sauce(beam, ack, weird_algorithm_flag)

    return beam

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

    return beam_list, search_timing(beam_count, cell.radius)

def contiguous_search(cell: Cell, users: User, beam_count):
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
    
    return find_beam_contiguous(beam_ack_list, beam_count), search_timing(beam_count, cell.radius)

def non_contiguous_search(cell: Cell, user: User, beam_count):
    """
    An algorithm to search for a single user with non-contiguous beams.
    The uncertainty region for this method is pi/(2^(beam_count-1))
    """
    if beam_count < 3:
        raise Exception("Beam count must be 3 or more.")
    beam_ack_list = []
    
    for i in range(beam_count):
        if i == 0:
            beam = Beam(0, np.pi)
            ack = send_beam(beam, user, cell.radius)
            beam_ack_list.append((beam, ack))
        elif i == 1:
            beam = Beam(np.pi/2, 3*np.pi/2)
            ack = send_beam(beam, user, cell.radius)
            beam_ack_list.append((beam, ack))
        else:
            beam_parts = 2**(i-1)  # Number of sectors in the non-contiguous beam
            partial_beams = []  # List of beams that make up the single non-contiguous beam
            for part in range(beam_parts):
                beam_shift = part*np.pi/(2**(i-2))
                beam = Beam(np.pi/(2**i) + beam_shift, 3*np.pi/(2**i) + beam_shift)
                partial_beams.append(beam)
            beam = SplitBeam(partial_beams)
            # Check Beam and mark with acknowledgements
            ack = send_beam(beam, user, cell.radius)
            beam_ack_list.append((beam, ack))
    return find_beam_non_contiguous(beam_ack_list), search_timing(beam_count, cell.radius)
