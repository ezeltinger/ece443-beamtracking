import numpy as np
from numpy.random import rand
import matplotlib.patches as mpatches
from statistics import mean

class Beam:
    def __init__(self, angle_one, angle_two, length=1, color=[rand(), rand(), rand()]):
        self.angle_one = angle_one
        self.angle_two = angle_two
        self.length = length
        self.color = color
    def span(self):
        span_value = self.angle_two - self.angle_one
        return span_value
    def middle(self):
        average = (self.angle_two + self.angle_one)/2
        return average
    def split(self):
        middle = self.middle()
        upper_beam = Beam(middle, self.angle_two)
        lower_beam = Beam(self.angle_one, middle)
        return lower_beam, upper_beam
    def setAngles(self, angle_one, angle_two):
        self.angle_one = angle_one
        self.angle_two = angle_two
