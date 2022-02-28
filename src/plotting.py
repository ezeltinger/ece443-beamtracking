from venv import create
import numpy as np
from matplotlib.axes import Axes
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from users import User
from beam import Beam
from typing import Union, Sequence

# Circular Cell
class Cell:
    def __init__(self, radius = 1): # Defined by radius
        self.radius = radius
        self.q = np.linspace(0,2*np.pi,50)
        self.x = radius*np.cos(self.q)
        self.y = radius*np.sin(self.q)
        self.borders = np.array([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi])

# Plot Cell, Users, and Beams
class Plot:
    def __init__(self, cell: Cell): # Requires a Cell
        self.cell = cell
        self.fig, self.ax = plt.subplots()
        self.ax.plot(cell.x, cell.y, color='tab:blue')
        for angle in cell.borders:
            if angle == 2*np.pi:
                break
            ri = 1
            qi = angle
            x = ri*np.cos(qi)
            y = ri*np.sin(qi)
            self.ax.plot([0, x], [0, y], color='tab:blue')

        self.points = [] # Member defines users on plot

    def add_beam(self, beam: Beam): # To plot a single Beam
        wedge = mpatches.Wedge((0.,0.), beam.length,
                                    np.degrees(beam.angle_one),
                                    np.degrees(beam.angle_two),
                                    color = beam.color, # color of beam
                                    alpha = 0.5) # Make the wedges transparent
        self.ax.add_patch(wedge)

    def clear_beams(self):
        [p.remove() for p in reversed(self.ax.patches)]

    def add_beams(self, beams: Union[Beam, Sequence[Beam]]): # To plot multiple beams
        for beam in beams:
            self.add_beam(beam)

    def add_users(self, users: Union[User, Sequence[User]]): # To plot multiple users
        self.points = []
        for user in users:
            self.points.extend(
                self.ax.plot(user.x, user.y, marker='o', color='tab:blue')
            )

    def append_user_path(self, users: Union[User, Sequence[User]], num_steps=None):
        if num_steps is not None:
            num_steps = num_steps + 1
        for user in users:
            self.ax.plot(user.path[0, 0:num_steps], user.path[1, 0:num_steps])

    def clear_users(self):
        for point in self.points:
            point.remove()
            

    def show(self):
        plt.show()
