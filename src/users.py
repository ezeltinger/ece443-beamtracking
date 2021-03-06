import numpy as np
from numpy.random import rand
import matplotlib.pyplot as plt
from brownian import brownian
from typing import Union, Sequence

class UserError(Exception):
    pass


def cart2pol(x, y):
    """Converts cartesian coordinates to polar coordinates"""
    rho = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)
    # arctan2 returns values on [-pi, pi], we want values on [0, 2pi]
    if theta < 0:
        theta = 2*np.pi + theta
    return(rho, theta)

def pol2cart(rho, theta):
    """Converts polar coordinates to cartesian coordinates"""
    x = rho * np.cos(theta)
    y = rho * np.sin(theta)
    return(x, y)

class User:
    """Class for tracking user position
    """
    idGenerator = (x for x in range(0x01, 0xFF))

    def __init__(self, radius=None, theta=None, path_color = [rand(), rand(), rand()]):
        self.radius = radius if radius is not None else np.sqrt(rand())
        self.theta = theta if theta is not None else 2*np.pi*rand()
        self.x, self.y = pol2cart(self.radius, self.theta)
        self.path = None
        self.path_color = path_color
        self.id = User.idGenerator.__next__()

    def create_path(self, time, steps, delta=0.25):
        dt = time/steps
        self.path = np.empty((2, steps+1))
        self.path[0, 0] = self.x
        self.path[1, 0] = self.y
        brownian(self.path[:,0], steps, dt, delta, out=self.path[:,1:])

    def move(self, step):
        if self.path is None:
            raise UserError("Need to create path before moving along path.")
        elif step>self.path.shape[1]:
            print(f"Length of path: {self.path.shape}")
            raise UserError("Can't go to step that is farther than path is defined.")
        else:
            self.x = self.path[0, step]
            self.y = self.path[1, step]
            self.radius, self.theta = cart2pol(self.x, self.y)


def move_users(users: Union[User, Sequence[User]], step):
    for user in users:
        user.move(step)
        
