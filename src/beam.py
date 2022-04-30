from typing import Sequence
import numpy as np
from numpy import linspace, sinc, arange
import matplotlib.pyplot as plt
from users import User
from scipy.integrate import quad


class Beam:
    def __init__(self, start_angle, end_angle, length=1, color=[0, 0.5, 0]):
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

class SplitBeam:
    def __init__(self, beam_list: Sequence[Beam]):
        self.partial_beams = beam_list

class SignalSender:
    def __init__(self):
        self.W = 20e06
        self.fc = 1.9e09
        self.t = linspace(0, 8/self.W, 1000000)
        self.beam_bits = [1, 1, 1, 1, 1, 1, 1, 1]
        self.num_bits = 8
        self.a = 10 
        self.B = 2
        self.c = 3e08
        self.snr = 10000
        # self.PL = a + 10*B*log10(d); % Path Loss
        # h = abs(normrnd(0, sqrt(10^(-0.1*PL)))); % Fading coefficient

    def unit_step(self, t):
        return 1*(t>=0)

    def bitmask(self, x):
        return 1 << x

    def mod_bits(self, t, bits):
        g = t * 0
        for i in range(len(bits)):
            g = g + (2*bits[i]-1)*sinc(self.W*(t-i/self.W)) # input signal
        return g

    def demod_bits(self, t, y, td):
        return y*np.cos(2*np.pi*self.fc*(t-td))

    def beam_signal(self):
        return self.mod_bits(self.t, self.beam_bits)

    def ack_signal(self, t, user: User):
        user_id_bits = [user.id & self.bitmask(i) for i in range(8)]
        print(user.id)
        ack_bits = []
        for bit in user_id_bits:
            print(f"bit = {bit}")
            ack_bits.append(int(bit))
        ack_bits = ack_bits.append(1)
        print(ack_bits)
        return self.mod_bits(t, ack_bits)

    def receive_ack(self, user: User):
        received_ack_bits = []
        td = user.radius/self.c
        path_loss = self.a + 10*self.B*np.log10(user.radius)  # Path Loss
        h = abs(np.random.normal(0, np.sqrt(10**(-0.1*path_loss))))  # Fading coefficient
        noise = np.random.normal(0, np.sqrt((h**2) / self.snr), len(self.t))  # Noise
        print(noise)
        Y = h*self.ack_signal(self.t-td, user)*np.cos(2*np.pi*self.fc*(self.t-td)) + noise
        # func = @(t) Y(t).*cos(2*pi*fc.*(t-td));
        for i in range(self.num_bits):
            demodulate_1 = quad(self.demod_bits, (i-1)/self.W + 1/(2*self.W) + td, i/self.W + 1/(2*self.W) + td, args=(Y, td))
            received_ack_bits.append(self.unit_step(demodulate_1))
        print(received_ack_bits)
        return received_ack_bits
        #     br(i) = u(demodulate_1);

if __name__ == "__main__":
    sig = SignalSender()
    user = User(radius=0.5, theta=np.pi/4)
    # fig, ax = plt.subplots()
    # g = sig.mod_bits(3.5/sig.W, sig.beam_bits)
    # print(g)
    ack_bits = sig.receive_ack(user)
    print(ack_bits)
    # ax.plot(2/sig.W, g, color='tab:blue')
    # plt.show()
