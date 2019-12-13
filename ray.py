import numpy as np

# class for light rays
class Rays():
    '''Vectorized creation of light rays

    Attributes:
        points -- array of origins for rays, shape = (3,nray)
        directions -- array of origins for rays, shape = (3,nray)
    '''
    def __init__(self, points, directions):
        self.points = points
        self.directions = directions/np.sqrt(np.sum(directions**2., axis=0))

    def get_points(self):
        return self.points

    def get_directions(self):
        return self.directions

    def get_nray(self):
        return self.points.shape[1]


