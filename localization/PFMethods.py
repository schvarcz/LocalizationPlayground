
import logging
import math


class PFLocalization():
    """ Performs the robot localization using the PF approach """
    def __init__(self, landmarks, numParticles, initialPose=(0,0,0)):
        self.poses = [initialPose]
        self.landmarks = landmarks
        self.__lastData__ = None

        self.numParticles = numParticles
        #Should create in random positions!! It is localization, not SLAM
        self.particles = [initialPose] * self.numParticles

    def localize(self, data):
        if self.__lastData__ == None:
            self.__lastData__ = data
        dt = data.time-self.__lastData__.time

        self.__propagate__(data.omega, data.v, dt)
        self.__weighting__()
        self.__resample__()

        self.__lastData__ = data

    def __propagate__(self, omega, v, dt):
        for idx in range(self.numParticles):
            particle = self.particles[idx]

            #Must add some noise here
            self.particles[idx] = [
                particle[0]+v*math.cos(particle[2]),
                particle[1]+v*math.cos(particle[2]),
                particle[2]+omega]

    def __weighting__(self):
        pass

    def __resample__(self):
        pass
