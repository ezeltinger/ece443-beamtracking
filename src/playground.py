"""
This file is for making demos, debugging an algorithm, or any other nonsense.
Use wisely and keep the good stuff.
"""
import matplotlib.pyplot as plt
from users import User, move_users
from search import contiguous_search, exhaustive_search
from plotting import Cell, Plot
from time import perf_counter
from gif import create_gif
from beam import Beam, SplitBeam
import numpy as np
import time

# Circular Cell
cell = Cell(radius=1)

# Create users
num_users = 1
user = User(radius=0.5, theta=2*np.pi/3)
user_list = [user]

# Create plot of cell with borders and add users
plot = Plot(cell)
plot.add_users(users=user_list)

def upper_cont_demo():
    beam_count = 4
    for i in range(beam_count):
        plot.clear_beams()
        beam = Beam(i*np.pi/beam_count, np.pi + i*np.pi/beam_count)
        plot.add_beam(beam)
        for k in range(10):
            plt.savefig(f'../output/up_{i}_{k}.png')
        plt.pause(0.1)

    # Search for each user
    plot.clear_beams()
    beam = contiguous_search(cell, user_list, beam_count=beam_count)
    plot.add_beam(beam)
    for k in range(10):
        plt.savefig(f'../output/up_{i+1}_{k}.png')
    plt.pause(0.1)
    create_gif('upper_cont_demo')

def exh_search_demo():
    beam_count = 8
    beam_width = 2*np.pi/beam_count
    for i in range(beam_count):
        plot.clear_beams()
        beam = Beam(i*beam_width, (i+1)*beam_width)
        plot.add_beam(beam)
        for k in range(10):
            plt.savefig(f'../output/ex_{i}_{k}.png')
        plt.pause(0.1)

    # Search for each user
    plot.clear_beams()
    beam = exhaustive_search(cell, user_list, beam_count=beam_count)[0]
    plot.add_beam(beam)
    for k in range(10):
        plt.savefig(f'../output/up_{i+1}_{k}.png')
    create_gif('exh_search_demo')

def show_split_beam(beam_number):
    i = beam_number
    sectors = 32
    for count in range(sectors):
            ri = 1
            qi = count*2*np.pi/sectors
            x = ri*np.cos(qi)
            y = ri*np.sin(qi)
            plot.ax.plot([0, x], [0, y], color='tab:blue')
    beam_parts = 2**(i-1)  # Number of sectors in the non-contiguous beam
    partial_beams = []  # List of beams that make up the single non-contiguous beam
    for part in range(beam_parts):
        beam_shift = part*np.pi/(2**(i-2))
        beam = Beam(np.pi/(2**i) + beam_shift, 3*np.pi/(2**i) + beam_shift)
        partial_beams.append(beam)
    beam = SplitBeam(partial_beams)
    plot.add_beams([beam])

if __name__ == "__main__":
    # exh_search_demo()
    # upper_cont_demo()
    show_split_beam(beam_number=3)
    plot.show()
