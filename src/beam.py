from numpy.random import rand

class Beam:
    def __init__(self, start_angle, end_angle, length=1, color=[rand(), rand(), rand()]):
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.length = length
        self.color = color
    
    @property
    def span(self):
        return self.end_angle - self.start_angle
    
    @property
    def middle(self):
        return (self.end_angle + self.start_angle)/2
    
    def split(self):
        upper_beam = Beam(self.middle, self.end_angle)
        lower_beam = Beam(self.start_angle, self.middle)
        return lower_beam, upper_beam
    
    def setAngles(self, start_angle, end_angle):
        self.start_angle = start_angle
        self.end_angle = end_angle
