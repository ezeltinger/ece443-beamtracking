import numpy as np
from numpy.random import rand
import matplotlib.pyplot as plt

class User:

    def __init__(self, radius=None, theta=None):
        self.radius = radius if radius is not None else rand()
        self.theta = theta if theta is not None else 2*np.pi*rand()
        self.x = self.radius*np.cos(self.theta)
        self.y = self.radius*np.sin(self.theta)

    
